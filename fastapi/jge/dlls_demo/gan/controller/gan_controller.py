import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.transforms as transforms
import torchvision.datasets as datasets
from torch.utils.data import DataLoader
from fastapi import APIRouter, Response
from io import BytesIO
from PIL import Image
import os

ganRouter = APIRouter()

# 하이퍼파라미터 설정
batch_size = 128
latent_dim = 100
epochs = 10
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Generator 정의
class Generator(nn.Module):
    def __init__(self):
        super(Generator, self).__init__()
        self.model = nn.Sequential(
            nn.Linear(latent_dim, 256),
            nn.ReLU(),
            nn.Linear(256, 512),
            nn.ReLU(),
            nn.Linear(512, 1024),
            nn.ReLU(),
            nn.Linear(1024, 28 * 28),
            nn.Tanh()
        )

    def forward(self, x):
        return self.model(x).view(-1, 1, 28, 28)

# Discriminator 정의
class Discriminator(nn.Module):
    def __init__(self):
        super(Discriminator, self).__init__()
        self.model = nn.Sequential(
            nn.Linear(28 * 28, 1024),
            nn.LeakyReLU(0.2),
            nn.Linear(1024, 512),
            nn.LeakyReLU(0.2),
            nn.Linear(512, 256),
            nn.LeakyReLU(0.2),
            nn.Linear(256, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.model(x.view(-1, 28 * 28))

# ✅ 모델 초기화
G = Generator().to(device)
D = Discriminator().to(device)

# 학습 API
@ganRouter.post("/gan/train")
def train_gan():
    # MNIST 데이터 로드
    transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5,), (0.5,))])
    dataset = datasets.MNIST(root="./data", train=True, download=True, transform=transform)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

    # 손실 함수 및 옵티마이저 설정
    criterion = nn.BCELoss()
    optimizer_G = optim.Adam(G.parameters(), lr=0.0002)
    optimizer_D = optim.Adam(D.parameters(), lr=0.0002)

    # 학습 실행
    for epoch in range(epochs):
        for real_imgs, _ in dataloader:
            real_imgs = real_imgs.to(device)

            # 진짜/가짜 라벨
            real_labels = torch.ones(real_imgs.size(0), 1).to(device)
            fake_labels = torch.zeros(real_imgs.size(0), 1).to(device)

            # Discriminator 학습
            optimizer_D.zero_grad()
            real_loss = criterion(D(real_imgs), real_labels)

            z = torch.randn(real_imgs.size(0), latent_dim).to(device)
            fake_imgs = G(z).detach()
            fake_loss = criterion(D(fake_imgs), fake_labels)

            d_loss = real_loss + fake_loss
            d_loss.backward()
            optimizer_D.step()

            # Generator 학습
            optimizer_G.zero_grad()
            fake_imgs = G(z)
            g_loss = criterion(D(fake_imgs), real_labels)
            g_loss.backward()
            optimizer_G.step()

        print(f"Epoch [{epoch+1}/{epochs}] | D Loss: {d_loss.item():.4f} | G Loss: {g_loss.item():.4f}")

    # 모델 저장
    os.makedirs("models", exist_ok=True)
    torch.save(G.state_dict(), "models/generator.pth")

    return {"message": "✅ GAN 학습 완료! 모델 저장됨."}

# ✅ 숫자 생성 API
@ganRouter.get("/gan/generate")
def generate_image():
    # 모델 불러오기
    if not os.path.exists("models/generator.pth"):
        return {"error": "❌ 먼저 /gan/train 을 호출해 모델을 학습하세요."}

    G.load_state_dict(torch.load("models/generator.pth", map_location=device))
    G.eval()

    # 숫자 생성
    z = torch.randn(1, 100).to(device)
    with torch.no_grad():
        generated_image = G(z).cpu().squeeze(0).squeeze(0)

    # 이미지 변환
    transform = transforms.ToPILImage()
    img = transform(generated_image)

    # 이미지 바이트로 변환
    img_bytes = BytesIO()
    img.save(img_bytes, format="PNG")
    img_bytes.seek(0)

    return Response(content=img_bytes.getvalue(), media_type="image/png")
