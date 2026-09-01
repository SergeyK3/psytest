# PS.kz manual deployment runbook

Automatic deployment is intentionally disabled. External services must only be
contacted during an approved cutover or retry window.

## One-time preparation

1. Copy only the reviewed `deploy/prepare-ps-kz.sh` to a temporary operator
   location and run it as root. It creates the service user plus `/etc/psytest`
   and `/var/lib/psytest`; it deliberately does not create or modify
   `/opt/projects` or `/opt/projects/psytest`.
2. Confirm `/opt/projects/psytest` does not exist, then clone without using a
   Beget working tree or server snapshot:

   ```bash
   test ! -e /opt/projects/psytest
   git clone --no-checkout <REPOSITORY_URL> /opt/projects/psytest
   REVIEWED_COMMIT=<FULL_REVIEWED_COMMIT_SHA>
   git -C /opt/projects/psytest checkout --detach "$REVIEWED_COMMIT"
   ```

3. As root, create the isolated environment and install the reviewed lock:

   ```bash
   python3.12 -m venv /opt/projects/psytest/.venv
   /opt/projects/psytest/.venv/bin/python -m pip install --upgrade pip
   /opt/projects/psytest/.venv/bin/python -m pip install \
     -r /opt/projects/psytest/requirements.lock
   chown -R root:psychtest /opt/projects/psytest
   chmod -R go-w /opt/projects/psytest
   install -o root -g root -m 0644 /opt/projects/psytest/psychtest-bot.service \
     /etc/systemd/system/psychtest-bot.service
   systemctl daemon-reload
   ```

4. Keep `/etc/psytest` owned by `root:psychtest` with mode `0750`. Populate
   `/etc/psytest/psytest.env`; owner `psychtest:psychtest`, mode `0600`.
5. Place service-account credentials at
   `/etc/psytest/google-drive-credentials.json`; owner `psychtest:psychtest`,
   mode `0600`. Never place the JSON in the repository. Re-running the prepare
   script only reapplies ownership/mode and never reads or replaces this file.

Required variable names are `BOT_TOKEN`, `GOOGLE_APPLICATION_CREDENTIALS`,
`GOOGLE_DRIVE_FOLDER_ID`, `GOOGLE_DRIVE_LOCK_PATH`, `PENDING_REPORTS_DIR`, and
`REPORT_WORK_DIR`. `OPENAI_API_KEY` is optional; static interpretations are used
when it is absent. Use the production paths from `.env.example`.

## Offline validation

```bash
BOT_TOKEN=offline-placeholder OPENAI_API_KEY= \
PYTHONDONTWRITEBYTECODE=1 PYTEST_ADDOPTS='-p no:cacheprovider' \
MPLCONFIGDIR=/tmp/psytest-matplotlib .venv/bin/python -m pytest tests -q

.venv/bin/python retry_pending_reports.py
```

The retry command is a dry-run unless `--execute` is supplied.
Dry-run never claims, renames, recovers, or uploads pending files.

## Google Drive preparation

1. Create or select a parent folder in a shared drive or another location where
   the service account can create files.
2. Grant the service-account identity content-manager/editor access.
3. Put only that parent folder identifier in `GOOGLE_DRIVE_FOLDER_ID`.
4. Verify reports appear under `YYYY/MM-Month` and are visible to operators.

## Cutover

1. Confirm the PS.kz pending queue is empty and offline tests pass.
2. Stop `psychtest-bot.service` on Beget. Never run two polling instances with
   the same bot token.
3. Start `psychtest-bot.service` on PS.kz.
4. Verify status, journal, memory, Telegram delivery, Drive placement, and queue.

## Pending retry

Offline inspection:

```bash
sudo -u psychtest /opt/projects/psytest/.venv/bin/python \
  /opt/projects/psytest/retry_pending_reports.py
```

Approved retry with Google Drive:

```bash
sudo -u psychtest /opt/projects/psytest/.venv/bin/python \
  /opt/projects/psytest/retry_pending_reports.py --execute
```

Successful retries delete their pending PDF; failed retries retain it.
Each execute run atomically claims files, and stale processing claims are
recovered after one hour. Upload-confirmed local cleanup markers can be removed
without Drive access:

```bash
sudo -u psychtest /opt/projects/psytest/.venv/bin/python \
  /opt/projects/psytest/retry_pending_reports.py --cleanup-uploaded
```

## Rollback

1. Stop the PS.kz service and preserve `/var/lib/psytest/pending-reports`.
2. Restart Beget only after confirming the PS.kz process is stopped.
3. For code rollback on PS.kz, use a clean reviewed prior checkout and reinstall
   dependencies. Do not use `git reset --hard`.
