#!/usr/bin/env bash
set -euo pipefail

if [[ "${EUID}" -ne 0 ]]; then
  echo "ERROR: run this one-time preparation script as root" >&2
  exit 1
fi
if ! id psychtest >/dev/null 2>&1; then
  useradd --system --home-dir /nonexistent --shell /usr/sbin/nologin psychtest
fi

install -d -o root -g psychtest -m 0750 /var/lib/psytest
install -d -o psychtest -g psychtest -m 0700 /var/lib/psytest/pending-reports
install -d -o psychtest -g psychtest -m 0700 /var/lib/psytest/matplotlib
install -d -o psychtest -g psychtest -m 0700 /var/lib/psytest/work
install -d -o psychtest -g psychtest -m 0700 /var/lib/psytest/locks
install -d -o root -g psychtest -m 0750 /etc/psytest

if [[ ! -e /etc/psytest/psytest.env ]]; then
  install -o psychtest -g psychtest -m 0600 /dev/null /etc/psytest/psytest.env
fi
chown psychtest:psychtest /etc/psytest/psytest.env
chmod 0600 /etc/psytest/psytest.env

if [[ -e /etc/psytest/google-drive-credentials.json ]]; then
  chown psychtest:psychtest /etc/psytest/google-drive-credentials.json
  chmod 0600 /etc/psytest/google-drive-credentials.json
fi
echo "Host directories are ready. Populate protected config manually."
