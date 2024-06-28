#!/bin/bash
# これから命令するよって宣言

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FULL_PATH=$(realpath "$SCRIPT_DIR/../src/main.py")

echo "SCRIPT_DIR: $SCRIPT_DIR"
echo "FULL_PATH: $FULL_PATH"

if command -v python3 &>/dev/null; then
    echo "pythonはインストールされてます。"
else
    echo "pythonがInstallされてないので実行できません。"
    exit 1
fi

MAIN_PY_PATH="$FULL_PATH"

# main.pyの実行
# /..は親要素に戻る
if [ -f "$MAIN_PY_PATH" ]; then
    python3 "$MAIN_PY_PATH"
else
    echo "main.pyが見つまりません"
    exit 1
fi