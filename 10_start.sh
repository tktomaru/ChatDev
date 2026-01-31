#!/bin/bash

# ChatDev サーバーとフロントエンドを起動するスクリプト

# 色付き出力
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  ChatDev 起動スクリプト${NC}"
echo -e "${BLUE}========================================${NC}"

# スクリプトのディレクトリに移動
cd "$(dirname "$0")"

# バックエンドサーバーを起動
echo -e "${GREEN}[1/2] バックエンドサーバーを起動中...${NC}"
echo "      URL: http://localhost:6400"
uv run python server_main.py --port 6400 --reload &
BACKEND_PID=$!

# サーバーが起動するまで少し待つ
sleep 2

# フロントエンドを起動
echo -e "${GREEN}[2/2] フロントエンドを起動中...${NC}"
cd frontend
VITE_API_BASE_URL=http://localhost:6400 npm run dev &
FRONTEND_PID=$!

cd ..

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}起動完了！${NC}"
echo "  バックエンド PID: $BACKEND_PID"
echo "  フロントエンド PID: $FRONTEND_PID"
echo ""
echo "終了するには Ctrl+C を押してください"
echo -e "${BLUE}========================================${NC}"

# 終了シグナルをキャッチして両プロセスを停止
cleanup() {
    echo ""
    echo -e "${BLUE}シャットダウン中...${NC}"
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo -e "${GREEN}終了しました${NC}"
    exit 0
}

trap cleanup SIGINT SIGTERM

# 両プロセスが終了するまで待機
wait
