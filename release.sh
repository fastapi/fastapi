#!/bin/bash

set -e

# === 配置 ===
USER=fewinter               # 你的 Docker Hub 用户名
BACKEND_DIR=./backend
FRONTEND_DIR=./frontend
BACKEND_IMAGE=$USER/fastapi-backend
FRONTEND_IMAGE=$USER/fastapi-frontend
TAG=${1:-latest}           # 默认 tag 是 latest，传参可覆盖

# === 构建并推送 ===
echo "▶ Building and pushing backend..."
docker buildx build --platform linux/amd64 -t $BACKEND_IMAGE:$TAG $BACKEND_DIR --push

echo "▶ Building and pushing frontend..."
docker buildx build --platform linux/amd64 -t $FRONTEND_IMAGE:$TAG $FRONTEND_DIR --push

echo "✅ Release completed: $TAG"
