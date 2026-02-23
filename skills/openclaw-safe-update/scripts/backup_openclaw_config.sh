#!/usr/bin/env bash
set -euo pipefail

SRC="${1:-$HOME/.openclaw-dev/openclaw.json}"
OUT_DIR="${2:-$HOME/.openclaw-dev/backups}"

mkdir -p "$OUT_DIR"
TS="$(date +%Y%m%d-%H%M%S)"
OUT="$OUT_DIR/openclaw.json.$TS.bak"

cp "$SRC" "$OUT"
echo "$OUT"
