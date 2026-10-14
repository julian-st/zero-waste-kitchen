# =====================================================================
# infra/ollama-pull.sh — one command to get the open-weight models
# =====================================================================
# #!/usr/bin/env bash
# set -euo pipefail
#
# MODELS=(
#   "qwen2.5:14b-instruct-q5_K_M"   # planner (fits 8 GB VRAM)
#   "qwen2.5vl:7b"                  # receipt / fridge-photo vision
# )
# for m in "${MODELS[@]}"; do
#   docker compose exec ollama ollama pull "$m"
# done
# echo "Run: docker compose up --build  ->  http://localhost:5173"
