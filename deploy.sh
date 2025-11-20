#!/usr/bin/env bash
set -euxo pipefail

# Р СџРЎС“РЎвЂљРЎРЉ Р С” Р С—РЎР‚Р С‘Р В»Р С•Р В¶Р ВµР Р…Р С‘РЎР‹ (Р СР С•Р В¶Р Р…Р С• Р С—Р ВµРЎР‚Р ВµР С•Р С—РЎР‚Р ВµР Т‘Р ВµР В»Р С‘РЎвЂљРЎРЉ РЎвЂЎР ВµРЎР‚Р ВµР В· env APP_DIR)
APP_DIR="${APP_DIR:-/srv/psytest}"
BRANCH="${BRANCH:-main}"
VENV_DIR="${APP_DIR}/venv"
SERVICE="${SERVICE:-psytest.service}"

# Р С’Р Т‘РЎР‚Р ВµРЎРѓ РЎР‚Р ВµР С—Р С•Р В·Р С‘РЎвЂљР С•РЎР‚Р С‘РЎРЏ Р Т‘Р В»РЎРЏ Р С”Р В»Р С•Р Р…Р С‘РЎР‚Р С•Р Р†Р В°Р Р…Р С‘РЎРЏ. Р С›РЎРѓРЎвЂљР В°Р Р†РЎРЉРЎвЂљР Вµ SSH-РЎвЂћР С•РЎР‚Р СР В°РЎвЂљ Р С‘Р В»Р С‘ Р В·Р В°Р СР ВµР Р…Р С‘РЎвЂљР Вµ Р Р…Р В° HTTPS
REPO_SSH="git@github.com:SergeyK3/psytest.git"
# REPO_SSH="https://github.com/SergeyK3/psytest.git"

# Р вЂўРЎРѓР В»Р С‘ Р Р† РЎвЂ Р ВµР В»Р ВµР Р†Р С•Р в„– Р Т‘Р С‘РЎР‚Р ВµР С”РЎвЂљР С•РЎР‚Р С‘Р С‘ РЎС“Р В¶Р Вµ Р ВµРЎРѓРЎвЂљРЎРЉ .git РІР‚вЂќ Р С•Р В±Р Р…Р С•Р Р†Р В»РЎРЏР ВµР С, Р С‘Р Р…Р В°РЎвЂЎР Вµ Р С”Р В»Р С•Р Р…Р С‘РЎР‚РЎС“Р ВµР С / Р С‘Р Р…Р С‘РЎвЂ Р С‘Р В°Р В»Р С‘Р В·Р С‘РЎР‚РЎС“Р ВµР С
if [ -d "${APP_DIR}/.git" ]; then
  echo "Updating existing repo in ${APP_DIR}"
  git -C "${APP_DIR}" fetch --all --prune
  git -C "${APP_DIR}" reset --hard "origin/${BRANCH}"
else
  echo "Target dir ${APP_DIR} doesn't contain .git"
  mkdir -p "${APP_DIR}"

  # Р вЂўРЎРѓР В»Р С‘ Р С”Р В°РЎвЂљР В°Р В»Р С•Р С– Р С—РЎС“РЎРѓРЎвЂљ РІР‚вЂќ Р СР С•Р В¶Р Р…Р С• Р В±Р ВµР В·Р С•Р С—Р В°РЎРѓР Р…Р С• Р С”Р В»Р С•Р Р…Р С‘РЎР‚Р С•Р Р†Р В°РЎвЂљРЎРЉ
  if [ -z "$(ls -A "${APP_DIR}")" ]; then
    echo "Directory is empty РІР‚вЂќ cloning repo into ${APP_DIR}"
    git clone --depth=1 --branch "${BRANCH}" "${REPO_SSH}" "${APP_DIR}"
  else
    # Р С™Р В°РЎвЂљР В°Р В»Р С•Р С– РЎРѓРЎС“РЎвЂ°Р ВµРЎРѓРЎвЂљР Р†РЎС“Р ВµРЎвЂљ Р С‘ Р Р…Р Вµ Р С—РЎС“РЎРѓРЎвЂљР С•Р в„–, Р Р…Р С• Р Р…Р Вµ РЎРѓР С•Р Т‘Р ВµРЎР‚Р В¶Р С‘РЎвЂљ .git РІР‚вЂќ Р С‘Р Р…Р С‘РЎвЂ Р С‘Р В°Р В»Р С‘Р В·Р С‘РЎР‚РЎС“Р ВµР С Р С‘ Р С—Р С•Р Т‘РЎвЂљРЎРЏР Р…Р ВµР С
    echo "Directory exists and is not empty РІР‚вЂќ initializing git and fetching from origin"
    git -C "${APP_DIR}" init
    # Р Р€Р Т‘Р В°Р В»РЎРЏР ВµР С Р Р†Р С•Р В·Р СР С•Р В¶Р Р…РЎвЂ№Р в„– origin, РЎвЂЎРЎвЂљР С•Р В±РЎвЂ№ Р Р…Р Вµ Р В±РЎвЂ№Р В»Р С• Р С”Р С•Р Р…РЎвЂћР В»Р С‘Р С”РЎвЂљР В°
    git -C "${APP_DIR}" remote remove origin 2>/dev/null || true
    git -C "${APP_DIR}" remote add origin "${REPO_SSH}"
    # Р СџР С•Р В»РЎС“РЎвЂЎР В°Р ВµР С Р Р…РЎС“Р В¶Р Р…РЎС“РЎР‹ Р Р†Р ВµРЎвЂљР С”РЎС“ (Р С–Р В»РЎС“Р В±Р С‘Р Р…Р В° 1) Р С‘ РЎРѓР В±РЎР‚Р В°РЎРѓРЎвЂ№Р Р†Р В°Р ВµР С РЎРѓР С•Р Т‘Р ВµРЎР‚Р В¶Р С‘Р СР С•Р Вµ Р С”Р В°РЎвЂљР В°Р В»Р С•Р С–Р В° Р Р† РЎРѓР С•РЎРѓРЎвЂљР С•РЎРЏР Р…Р С‘Р Вµ origin/BRANCH
    git -C "${APP_DIR}" fetch --depth=1 origin "${BRANCH}"
    git -C "${APP_DIR}" reset --hard "FETCH_HEAD"
  fi
fi

# Р СџР ВµРЎР‚Р ВµРЎвЂ¦Р С•Р Т‘Р С‘Р С Р Р† Р Т‘Р С‘РЎР‚Р ВµР С”РЎвЂљР С•РЎР‚Р С‘РЎР‹ Р С—РЎР‚Р С‘Р В»Р С•Р В¶Р ВµР Р…Р С‘РЎРЏ
cd "$APP_DIR" || { echo "Directory $APP_DIR not found"; exit 1; }

echo "Deploy: branch=${BRANCH}, app_dir=${APP_DIR}"

# Р С›Р В±Р Р…Р С•Р Р†Р В»РЎРЏР ВµР С Р С”Р С•Р Т‘ (Р Р…Р В° Р Р†РЎРѓРЎРЏР С”Р С‘Р в„– РЎРѓР В»РЎС“РЎвЂЎР В°Р в„–)
git fetch --all --prune
git checkout "$BRANCH"
git pull --ff-only origin "$BRANCH"

# Р вЂ™Р С‘РЎР‚РЎвЂљРЎС“Р В°Р В»РЎРЉР Р…Р С•Р Вµ Р С•Р С”РЎР‚РЎС“Р В¶Р ВµР Р…Р С‘Р Вµ Р С‘ Р В·Р В°Р Р†Р С‘РЎРѓР С‘Р СР С•РЎРѓРЎвЂљР С‘ (Р ВµРЎРѓР В»Р С‘ Р ВµРЎРѓРЎвЂљРЎРЉ requirements.txt)
if [ -f requirements.txt ]; then
  if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
  fi
  # shellcheck disable=SC1090
  source "$VENV_DIR/bin/activate"
  pip install --upgrade pip
  pip install -r requirements.txt
fi

# Django-РЎРѓР С—Р ВµРЎвЂ Р С‘РЎвЂћР С‘РЎвЂЎР Р…РЎвЂ№Р Вµ РЎв‚¬Р В°Р С–Р С‘ (Р ВµРЎРѓР В»Р С‘ Р ВµРЎРѓРЎвЂљРЎРЉ manage.py)
if [ -f manage.py ]; then
  source "$VENV_DIR/bin/activate" || true
  python manage.py migrate --noinput || true
  python manage.py collectstatic --noinput || true
fi

# Р СџР ВµРЎР‚Р ВµР В·Р В°Р С—РЎС“РЎРѓР С”Р В°Р ВµР С systemd-РЎРѓР ВµРЎР‚Р Р†Р С‘РЎРѓ, Р ВµРЎРѓР В»Р С‘ Р В·Р В°Р Т‘Р В°Р Р…
if command -v systemctl >/dev/null 2>&1 && systemctl list-units --type=service --all | grep -q "$SERVICE"; then
  sudo systemctl daemon-reload || true
  sudo systemctl restart "$SERVICE" || true
  echo "Service $SERVICE restarted"
fi

echo "Deploy finished."

