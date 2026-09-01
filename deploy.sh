#!/usr/bin/env bash
set -euo pipefail

# Manual PS.kz update. Refuses dirty trees and uses fast-forward only.
APP_DIR="${APP_DIR:-/opt/projects/psytest}"
BRANCH="${BRANCH:-main}"
SERVICE="${SERVICE:-psychtest-bot.service}"
VENV_DIR="${APP_DIR}/.venv"

if [[ ! -d "${APP_DIR}/.git" ]]; then
  echo "ERROR: ${APP_DIR} is not an existing Git checkout" >&2
  exit 1
fi
if [[ -n "$(git -C "${APP_DIR}" status --porcelain)" ]]; then
  echo "ERROR: refusing to deploy over a dirty working tree" >&2
  exit 1
fi

git -C "${APP_DIR}" fetch origin "${BRANCH}"
git -C "${APP_DIR}" switch "${BRANCH}"
git -C "${APP_DIR}" merge --ff-only "origin/${BRANCH}"

if [[ ! -x "${VENV_DIR}/bin/python3" ]]; then
  python3 -m venv "${VENV_DIR}"
fi
"${VENV_DIR}/bin/python3" -m pip install --upgrade pip
"${VENV_DIR}/bin/python3" -m pip install -r "${APP_DIR}/requirements.lock"

cd "${APP_DIR}"
BOT_TOKEN=offline-placeholder OPENAI_API_KEY= \
PYTHONDONTWRITEBYTECODE=1 PYTEST_ADDOPTS="-p no:cacheprovider" \
MPLCONFIGDIR=/tmp/psytest-matplotlib \
"${VENV_DIR}/bin/python3" -m pytest tests -q

sudo install -o root -g root -m 0644 \
  "${APP_DIR}/psychtest-bot.service" \
  "/etc/systemd/system/psychtest-bot.service"
sudo systemctl daemon-reload
sudo systemctl restart "${SERVICE}"
sudo systemctl is-active --quiet "${SERVICE}"
echo "Deployment completed and ${SERVICE} is active."
