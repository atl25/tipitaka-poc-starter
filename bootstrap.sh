#!/usr/bin/env bash
# bootstrap.sh — one-click helpers for Weaviate + ETL pipeline
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Detect docker compose v2 vs v1
if command -v docker >/dev/null 2>&1 && docker compose version >/dev/null 2>&1; then
  COMPOSE="docker compose"
elif command -v docker-compose >/dev/null 2>&1; then
  COMPOSE="docker-compose"
else
  echo "❌ docker compose not found. Install Docker Desktop or docker-compose." >&2
  exit 1
fi

WEAVIATE_HOST_PORT="${WEAVIATE_HOST_PORT:-8080}"
WEAVIATE_GRPC_HOST_PORT="${WEAVIATE_GRPC_HOST_PORT:-50051}"

usage() {
  cat <<EOF
Usage: ./bootstrap.sh {setup|up|build|load|logs|down|ps}

  setup  : up → build → load (one-click)
  up     : start Weaviate (and deps) in background
  build  : build ETL image
  load   : run ETL pipeline (schema + CSV + vectors + sanity search)
  logs   : follow logs (weaviate + etl)
  down   : stop and remove containers/volumes (CAREFUL)
  ps     : show running containers for this project

Env (optional):
  WEAVIATE_HOST_PORT       (default: 8080)
  WEAVIATE_GRPC_HOST_PORT  (default: 50051)
EOF
}

port_in_use() {
  local port="$1"
  # works on Git Bash/WSL/Linux/macOS
  if command -v lsof >/dev/null 2>&1; then
    lsof -iTCP -sTCP:LISTEN -P | grep -q ":${port} "
  elif command -v netstat >/dev/null 2>&1; then
    netstat -ano 2>/dev/null | grep -q ":${port} "
  else
    return 1
  fi
}

check_ports() {
  for p in "$WEAVIATE_HOST_PORT" "$WEAVIATE_GRPC_HOST_PORT"; do
    if port_in_use "$p"; then
      echo "⚠️  Port ${p} looks in use on host. If compose fails, edit docker-compose.yml to map a free port (e.g. 8081/50052)."
    fi
  done
}

cmd_up() {
  check_ports
  echo "🚀 Starting services (weaviate)…"
  # Build weaviate image if needed; do not start ETL yet
  (cd "$PROJECT_ROOT" && $COMPOSE up -d --remove-orphans weaviate)
  echo "✅ Weaviate should be coming up."
  echo "   Try: http://localhost:${WEAVIATE_HOST_PORT}/v1/graphql"
}

cmd_build() {
  echo "🔧 Building ETL image…"
  (cd "$PROJECT_ROOT" && $COMPOSE build etl)
  echo "✅ ETL image built."
}

cmd_load() {
  echo "📦 Running ETL pipeline (schema + CSV + vectors + sanity)…"
  # Use the image's default CMD (pipeline.py). If you prefer explicit python, uncomment the second line.
  (cd "$PROJECT_ROOT" && $COMPOSE run --rm etl)
  # (cd "$PROJECT_ROOT" && $COMPOSE run --rm etl python etl/app/pipeline.py)
  echo "✅ Data load finished."
}

cmd_logs() {
  echo "🪵 Tailing logs (Ctrl+C to stop)…"
  (cd "$PROJECT_ROOT" && $COMPOSE logs -f weaviate etl || true)
}

cmd_down() {
  echo "🧹 Stopping & removing containers (and volumes)…"
  (cd "$PROJECT_ROOT" && $COMPOSE down -v)
  echo "✅ Done."
}

cmd_ps() {
  (cd "$PROJECT_ROOT" && $COMPOSE ps)
}

cmd_setup() {
  cmd_up
  cmd_build
  cmd_load
  echo "🎉 Setup complete. Open GraphQL: http://localhost:${WEAVIATE_HOST_PORT}/v1/graphql"
}

main() {
  local action="${1:-}"
  case "$action" in
    setup) cmd_setup ;;
    up)    cmd_up ;;
    build) cmd_build ;;
    load)  cmd_load ;;
    logs)  cmd_logs ;;
    down)  cmd_down ;;
    ps)    cmd_ps ;;
    ""|-h|--help|help) usage ;;
    *) echo "Unknown command: $action"; usage; exit 1 ;;
  esac
}

main "$@"
