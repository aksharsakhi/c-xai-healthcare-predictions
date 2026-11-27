#!/usr/bin/env bash
set -e
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$DIR/.." && pwd)"
cd "$ROOT"
echo "=================================================================="
echo "  C-XAI Live Clinical Auditing Dashboard (ICMLDE 2026 · Paper 857)"
echo "  URL: http://127.0.0.1:8570"
echo "=================================================================="
PYTHONPATH="$ROOT:$ROOT/src" python3 -m uvicorn dashboard.app:app --host 127.0.0.1 --port 8570
