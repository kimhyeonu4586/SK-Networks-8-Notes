from fastapi import APIRouter, File, UploadFile, HTTPException, status
from fastapi.responses import JSONResponse
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.transforms as transforms
import torchvision.datasets as datasets
from torch.utils.data import DataLoader
from io import BytesIO
from PIL import Image
import os

# FastAPI 라우터 생성
dcganRouter = APIRouter()

# 하이퍼파라미터 설정
latent_dim = 100
epochs = 10
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Generator 정의
class Generator(nn.Module):
    def __init__(self):
        super(Generator, self).__init__()
        self.model = nn.Sequential(
            nn.ConvTranspose2d(latent_dim, 512, 4, 1, 0, bias=False),
            nn.BatchNorm2d(512),
            nn.ReLU(True),

            nn.ConvTranspose2d(512, 256, 4, 2, 1, bias=False),
            nn.BatchNorm2d(256),
            nn.ReLU(True),

            nn.ConvTranspose2d(256, 128, 4, 2, 1, bias=False),
            nn.BatchNorm2d(128),
            nn.ReLU(True),

            nn.ConvTranspose2d(128, 3, 4, 2, 1, bias=False),  # RGB 채널로 수정
            nn.Tanh()
        )

    def forward(self, x):
        return self.model(x)

# Discriminator 정의
class Discriminator(nn.Module):
    def __init__(self):
        super(Discriminator, self).__init__()
        self.model = nn.Sequential(
            nn.Conv2d(3, 64, kernel_size=4, stride=2, padding=1),
            nn.LeakyReLU(0.2),
            nn.Conv2d(64, 128, kernel_size=4, stride=2, padding=1),
            nn.LeakyReLU(0.2),
            nn.Conv2d(128, 256, kernel_size=4, stride=2, padding=1),
            nn.LeakyReLU(0.2),
            nn.Conv2d(256, 1, kernel_size=4, stride=1, padding=0),
            nn.AdaptiveAvgPool2d((1, 1)),  # 🔥 추가
            nn.Sigmoid()
        )

    def forward(self, x):
        output = self.model(x)
        # print(f"Discriminator output shape: {output.shape}")  # 출력 크기 확인
        return output.view(x.size(0), -1)  # (batch_size, 1)로 강제 변환

# 모델 초기화
G = Generator().to(device)
D = Discriminator().to(device)

# 학습 API
@dcganRouter.post("/dcgan/train")
async def train_dcgan(batch_size: int = 128):
    print(f"[INFO] Training DCGAN with batch size {batch_size} on {device}")

    transform = transforms.Compose([
        transforms.Resize((64, 64)),  # 64x64로 크기 조정
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),  # RGB 이미지를 [-1, 1] 범위로 정규화
    ])

    # CIFAR-10 데이터셋
    dataset = datasets.CIFAR10(root="./data", train=True, download=True, transform=transform)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

    criterion = nn.BCELoss()
    optimizer_G = optim.Adam(G.parameters(), lr=0.0002, betas=(0.5, 0.999))
    optimizer_D = optim.Adam(D.parameters(), lr=0.0002, betas=(0.5, 0.999))

    for epoch in range(epochs):
        for i, (real_imgs, _) in enumerate(dataloader):
            real_imgs = real_imgs.to(device)
            batch_size = real_imgs.size(0)

            real_labels = torch.ones(batch_size, 1).to(device)
            fake_labels = torch.zeros(batch_size, 1).to(device)

            optimizer_D.zero_grad()

            real_output = D(real_imgs)
            # print(f"real_output shape: {real_output.shape}, real_labels shape: {real_labels.shape}")  # 디버깅 출력
            real_loss = criterion(real_output, real_labels)  # 여기서 에러 발생 가능성 있음

            z = torch.randn(batch_size, latent_dim, 1, 1).to(device)
            fake_imgs = G(z).detach()
            fake_output = D(fake_imgs)
            fake_loss = criterion(fake_output, fake_labels)

            d_loss = real_loss + fake_loss
            d_loss.backward()
            optimizer_D.step()

            # Generator 학습
            optimizer_G.zero_grad()
            fake_output = D(G(z))
            g_loss = criterion(fake_output, real_labels)
            g_loss.backward()
            optimizer_G.step()

            if i % 100 == 0:
                print(f"Epoch [{epoch + 1}/{epochs}] | Step [{i}/{len(dataloader)}] | "
                      f"D Loss: {d_loss.item():.4f} | G Loss: {g_loss.item():.4f}")

    os.makedirs("models", exist_ok=True)
    torch.save(G.state_dict(), "models/dcgan_generator.pth")
    print("[INFO] Training completed! Model saved at models/dcgan_generator.pth")
    return {"message": "✅ DCGAN 학습 완료! 모델 저장됨."}


# 이미지 생성 API
@dcganRouter.post("/dcgan/generate")
async def generate_image():
    if not os.path.exists("models/dcgan_generator.pth"):
        raise HTTPException(status_code=404, detail="Model not found. Please train the model first.")

    print("[INFO] Loading trained generator model...")
    G.load_state_dict(torch.load("models/dcgan_generator.pth", map_location=device), strict=False)
    G.eval()

    z = torch.randn(1, latent_dim, 1, 1).to(device)
    with torch.no_grad():
        generated_image = G(z).cpu().squeeze(0).permute(1, 2, 0)

    transform_to_pil = transforms.ToPILImage()
    generated_pil_image = transform_to_pil(generated_image)

    img_bytes = BytesIO()
    generated_pil_image.save(img_bytes, format="PNG")
    img_bytes.seek(0)

    print("[INFO] Image generation successful!")
    return JSONResponse(content={"message": "Image generated successfully"}, status_code=status.HTTP_200_OK,
                        media_type="image/png",
                        headers={"Content-Disposition": "attachment; filename=generated_image.png",
                                 "Content-Type": "image/png"})
