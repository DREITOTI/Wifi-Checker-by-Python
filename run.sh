#!/bin/zsh
cd "$(dirname "$0")" || exit 1
export TK_SILENCE_DEPRECATION=1
./.venv/bin/python main.py
