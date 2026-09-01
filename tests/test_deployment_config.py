from pathlib import Path


def test_systemd_unit_targets_ps_kz_and_protected_state():
    unit_path = Path("psychtest-bot.service")
    unit_bytes = unit_path.read_bytes()
    unit = unit_bytes.decode("utf-8")

    required = (
        "User=psychtest",
        "Group=psychtest",
        "WorkingDirectory=/opt/projects/psytest",
        "EnvironmentFile=/etc/psytest/psytest.env",
        "ExecStart=/opt/projects/psytest/.venv/bin/python3",
        "Environment=MPLBACKEND=Agg",
        "ReadWritePaths=/var/lib/psytest/work",
        "ReadWritePaths=/var/lib/psytest/pending-reports",
        "ReadWritePaths=/var/lib/psytest/matplotlib",
        "ReadWritePaths=/var/lib/psytest/locks",
        "ProtectSystem=strict",
        "NoNewPrivileges=true",
        "UMask=0077",
    )
    for setting in required:
        assert setting in unit
    assert unit.count("EnvironmentFile=") == 1
    assert "ReadWritePaths=/opt/projects" not in unit
    assert not unit_bytes.startswith(b"\xef\xbb\xbf")
    assert b"\r" not in unit_bytes


def test_deploy_is_manual_fast_forward_and_non_destructive():
    deploy = Path("deploy.sh").read_text(encoding="utf-8")
    workflow = Path(".github/workflows/deploy.yml").read_text(encoding="utf-8")

    assert "merge --ff-only" in deploy
    assert "status --porcelain" in deploy
    assert "reset --hard" not in deploy
    assert "psychtest-bot.service" in deploy
    assert "requirements.lock" in deploy
    assert "push:" not in workflow
    assert "workflow_dispatch:" in workflow


def test_credentials_are_configuration_not_repository_dependencies():
    requirements = Path("requirements.txt").read_text(encoding="utf-8")
    lock = Path("requirements.lock").read_text(encoding="utf-8")
    ignore = Path(".gitignore").read_text(encoding="utf-8")
    env_example = Path(".env.example").read_text(encoding="utf-8")
    prepare = Path("deploy/prepare-ps-kz.sh").read_text(encoding="utf-8")
    runbook = Path("PS_KZ_DEPLOYMENT.md").read_text(encoding="utf-8")

    assert "-e git+" not in requirements
    assert "openai==" in requirements
    assert "openai==" in lock
    assert all(
        "==" in line and "git+" not in line and "@" not in line
        for line in lock.splitlines()
        if line and not line.startswith("#")
    )
    assert "*-credentials.json" in ignore
    assert "GOOGLE_APPLICATION_CREDENTIALS=" in env_example
    assert "GOOGLE_DRIVE_FOLDER_ID=" in env_example
    assert "PENDING_REPORTS_DIR=" in env_example
    assert "REPORT_WORK_DIR=" in env_example
    assert "GOOGLE_DRIVE_LOCK_PATH=" in env_example
    assert "chmod 0600 /etc/psytest/google-drive-credentials.json" in prepare
    assert "getent passwd psychtest" in prepare
    assert "id -gn psychtest" in prepare
    assert "groupadd --system psychtest" in prepare
    assert "--gid psychtest" in prepare
    assert "--no-create-home" in prepare
    assert "--home-dir /nonexistent" in prepare
    assert "--shell /usr/sbin/nologin" in prepare
    assert prepare.index("groupadd --system psychtest") < prepare.index("useradd \\")
    assert "expected 'psychtest'" in prepare
    assert "usermod" not in prepare
    assert "/opt/projects/psytest" not in prepare
    assert "reset --hard" not in prepare
    assert "systemctl start" not in prepare
    assert "systemctl restart" not in prepare
    assert "git clone --no-checkout" in runbook
    assert "checkout --detach" in runbook
    assert "requirements.lock" in runbook
