#!/bin/bash

set -e

# === 配置 ===
USER=fewinter
BACKEND_DIR=./backend
FRONTEND_DIR=./frontend
BACKEND_IMAGE=$USER/fastapi-backend
FRONTEND_IMAGE=$USER/fastapi-frontend

# === 解析参数 ===
TAG=latest
TARGET=all

if [[ $# -eq 1 ]]; then
    if [[ "$1" == "all" || "$1" == "backend" || "$1" == "frontend" ]]; then
        TARGET="$1"
    else
        TAG="$1"
    fi
elif [[ $# -eq 2 ]]; then
    TAG="$1"
    TARGET="$2"
fi

# === 检查目标 ===
if [[ "$TARGET" != "backend" && "$TARGET" != "frontend" && "$TARGET" != "all" ]]; then
    echo "❌ 无效的目标: $TARGET"
    echo "用法: $0 [tag] [backend|frontend|all]"
    exit 1
fi

# === 构建并推送 ===
if [[ "$TARGET" == "backend" || "$TARGET" == "all" ]]; then
    echo "▶ Building and pushing backend..."
    docker buildx build --platform linux/amd64 -t $BACKEND_IMAGE:$TAG $BACKEND_DIR --push
fi

if [[ "$TARGET" == "frontend" || "$TARGET" == "all" ]]; then
    echo "▶ Building and pushing frontend..."
    docker buildx build --platform linux/amd64 -t $FRONTEND_IMAGE:$TAG $FRONTEND_DIR --push
fi

echo "✅ Release completed: tag=$TAG target=$TARGET"
