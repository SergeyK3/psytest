#!/usr/bin/env bash
set -euxo pipefail

# РџСѓС‚СЊ Рє РїСЂРёР»РѕР¶РµРЅРёСЋ (РјРѕР¶РЅРѕ РїРµСЂРµРѕРїСЂРµРґРµР»РёС‚СЊ С‡РµСЂРµР· env APP_DIR)
APP_DIR="${APP_DIR:-/srv/psytest}"
BRANCH="${BRANCH:-main}"
VENV_DIR="${APP_DIR}/venv"
SERVICE="${SERVICE:-psytest.service}"

# РђРґСЂРµСЃ СЂРµРїРѕР·РёС‚РѕСЂРёСЏ РґР»СЏ РєР»РѕРЅРёСЂРѕРІР°РЅРёСЏ. РћСЃС‚Р°РІСЊС‚Рµ SSH-С„РѕСЂРјР°С‚ РёР»Рё Р·Р°РјРµРЅРёС‚Рµ РЅР° HTTPS
REPO_SSH="git@github.com:SergeyK3/psytest.git"
# REPO_SSH="https://github.com/SergeyK3/psytest.git"

# Р•СЃР»Рё РІ С†РµР»РµРІРѕР№ РґРёСЂРµРєС‚РѕСЂРёРё СѓР¶Рµ РµСЃС‚СЊ .git вЂ” РѕР±РЅРѕРІР»СЏРµРј, РёРЅР°С‡Рµ РєР»РѕРЅРёСЂСѓРµРј / РёРЅРёС†РёР°Р»РёР·РёСЂСѓРµРј
if [ -d "${APP_DIR}/.git" ]; then
  echo "Updating existing repo in ${APP_DIR}"
  git -C "${APP_DIR}" fetch --all --prune
  git -C "${APP_DIR}" reset --hard "origin/${BRANCH}"
else
  echo "Target dir ${APP_DIR} doesn't contain .git"
  mkdir -p "${APP_DIR}"

  # Р•СЃР»Рё РєР°С‚Р°Р»РѕРі РїСѓСЃС‚ вЂ” РјРѕР¶РЅРѕ Р±РµР·РѕРїР°СЃРЅРѕ РєР»РѕРЅРёСЂРѕРІР°С‚СЊ
  if [ -z "$(ls -A "${APP_DIR}")" ]; then
    echo "Directory is empty вЂ” cloning repo into ${APP_DIR}"
    git clone --depth=1 --branch "${BRANCH}" "${REPO_SSH}" "${APP_DIR}"
  else
    # РљР°С‚Р°Р»РѕРі СЃСѓС‰РµСЃС‚РІСѓРµС‚ Рё РЅРµ РїСѓСЃС‚РѕР№, РЅРѕ РЅРµ СЃРѕРґРµСЂР¶РёС‚ .git вЂ” РёРЅРёС†РёР°Р»РёР·РёСЂСѓРµРј Рё РїРѕРґС‚СЏРЅРµРј
    echo "Directory exists and is not empty вЂ” initializing git and fetching from origin"
    git -C "${APP_DIR}" init
    # РЈРґР°Р»СЏРµРј РІРѕР·РјРѕР¶РЅС‹Р№ origin, С‡С‚РѕР±С‹ РЅРµ Р±С‹Р»Рѕ РєРѕРЅС„Р»РёРєС‚Р°
    git -C "${APP_DIR}" remote remove origin 2>/dev/null || true
    git -C "${APP_DIR}" remote add origin "${REPO_SSH}"
    # РџРѕР»СѓС‡Р°РµРј РЅСѓР¶РЅСѓСЋ РІРµС‚РєСѓ (РіР»СѓР±РёРЅР° 1) Рё СЃР±СЂР°СЃС‹РІР°РµРј СЃРѕРґРµСЂР¶РёРјРѕРµ РєР°С‚Р°Р»РѕРіР° РІ СЃРѕСЃС‚РѕСЏРЅРёРµ origin/BRANCH
    git -C "${APP_DIR}" fetch --depth=1 origin "${BRANCH}"
    git -C "${APP_DIR}" reset --hard "FETCH_HEAD"
  fi
fi

# РџРµСЂРµС…РѕРґРёРј РІ РґРёСЂРµРєС‚РѕСЂРёСЋ РїСЂРёР»РѕР¶РµРЅРёСЏ
cd "$APP_DIR" || { echo "Directory $APP_DIR not found"; exit 1; }

echo "Deploy: branch=${BRANCH}, app_dir=${APP_DIR}"

# РћР±РЅРѕРІР»СЏРµРј РєРѕРґ (РЅР° РІСЃСЏРєРёР№ СЃР»СѓС‡Р°Р№)
git fetch --all --prune
git checkout "$BRANCH"
git pull --ff-only origin "$BRANCH"

# Р’РёСЂС‚СѓР°Р»СЊРЅРѕРµ РѕРєСЂСѓР¶РµРЅРёРµ Рё Р·Р°РІРёСЃРёРјРѕСЃС‚Рё (РµСЃР»Рё РµСЃС‚СЊ requirements.txt)
if [ -f requirements.txt ]; then
  if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
  fi
  # shellcheck disable=SC1090
  source "$VENV_DIR/bin/activate"
  pip install --upgrade pip
  pip install -r requirements.txt
fi

# Django-СЃРїРµС†РёС„РёС‡РЅС‹Рµ С€Р°РіРё (РµСЃР»Рё РµСЃС‚СЊ manage.py)
if [ -f manage.py ]; then
  source "$VENV_DIR/bin/activate" || true
  python manage.py migrate --noinput || true
  python manage.py collectstatic --noinput || true
fi

# РџРµСЂРµР·Р°РїСѓСЃРєР°РµРј systemd-СЃРµСЂРІРёСЃ, РµСЃР»Рё Р·Р°РґР°РЅ
if command -v systemctl >/dev/null 2>&1 && systemctl list-units --type=service --all | grep -q "$SERVICE"; then
  sudo systemctl daemon-reload || true
  sudo systemctl restart "$SERVICE" || true
  echo "Service $SERVICE restarted"
fi

echo "Deploy finished."
