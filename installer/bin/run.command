#!/bin/bash
# これから命令するよって宣言

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if command -v python3 &>/dev/null; then
    echo "pythonはインストールされてます。"
else
    echo "pythonがInstallされてないので実行できません。"
    exit 1
fi

# main.pyの実行
# /..は親要素に戻る
if [ -f "$SCRIPT_DIR/../src/main.py" ]; then
    python3 "$SCRIPT_DIR/../src/main.py"
else
    echo "main.pyが見つまりません"
    exit 1
fi