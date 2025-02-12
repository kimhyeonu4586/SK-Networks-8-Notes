# 빌드
FROM node:18-alpine AS builder

# 작업 디렉토리 설정
WORKDIR /app

# package.json과 package-lock.json 복사
COPY package*.json

# 필요한 패키지 설치
RUN npm install

# 소스 코드 복사
COPY . .

# Nuxt의 Production 모드로 빌드
RUN npm run build

# 실행
FROM node:18-alpine

# 작업 디렉토리 설정
WORKDIR /app

# 빌드된 결과만 복사
COPY --from=builder /app ./

# 포트 설정 (Nuxt 기본 포트 3000)
EXPOSE 3000

# Docker Container가 실행 될 때 실행 할 명령어 (Production 모드)
CMD ["npm", "run", "start"]