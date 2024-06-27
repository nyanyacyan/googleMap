#!/bin/bash
#! これから命令するよ！って宣言

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if command -v python3 &>/dev/null; then
    echo "Pythonはインストールされてます"
else
    echo "Pythonがインストールされてないため実行ができません。"
    exit 1
fi

# requirements.txtのインストール
if [ -f "$SCRIPT_DIR/requirements.txt" ]; then
    python3 -m pip install -r "$SCRIPT_DIR/requirements.txt"
    echo "必要なライブラリなどのInstallが完了しました。"
else
    echo "必要なものをインストールできませんでした。"
    exit 1
fi
