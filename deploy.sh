#!/usr/bin/env bash
set -euo pipefail

# Путь к приложению (можно переопределить через env APP_DIR)
APP_DIR="${APP_DIR:-/srv/psytest}"
BRANCH="${BRANCH:-main}"
VENV_DIR="${APP_DIR}/venv"
SERVICE="${SERVICE:-psytest.service}"

cd "$APP_DIR" || { echo "Directory $APP_DIR not found"; exit 1; }

echo "Deploy: branch=${BRANCH}, app_dir=${APP_DIR}"

# Обновляем код
git fetch --all --prune
git checkout "$BRANCH"
git pull --ff-only origin "$BRANCH"

# Виртуальное окружение и зависимости (если есть requirements.txt)
if [ -f requirements.txt ]; then
  if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
  fi
  # shellcheck disable=SC1090
  source "$VENV_DIR/bin/activate"
  pip install --upgrade pip
  pip install -r requirements.txt
fi

# Django-специфичные шаги (если есть manage.py)
if [ -f manage.py ]; then
  source "$VENV_DIR/bin/activate" || true
  python manage.py migrate --noinput || true
  python manage.py collectstatic --noinput || true
fi

# Перезапускаем systemd-сервис, если задан
if command -v systemctl >/dev/null 2>&1 && systemctl list-units --type=service --all | grep -q "$SERVICE"; then
  sudo systemctl daemon-reload || true
  sudo systemctl restart "$SERVICE" || true
  echo "Service $SERVICE restarted"
fi

echo "Deploy finished."