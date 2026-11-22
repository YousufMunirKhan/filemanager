"""A fresh copy of the project (git clone, maybe with a badly copied backend/.env) must start cleanly."""
import os
import subprocess
import sys
from pathlib import Path

from app import create_app
from app.config import TestConfig
from app.startup import report_rows
from settings_files import load_settings, merged_settings

BACKEND_DIR = Path(__file__).resolve().parent.parent
SETTINGS = ("EMAIL_DEMO_MODE", "SMTP_HOST", "AI_PROVIDER", "OPENAI_API_KEY", "TWO_FACTOR_ENABLED")
NEW_USER = {"name": "New Student", "email": "student@example.com", "password": "Passw0rd!"}


def fresh_config(**env) -> dict:
    """Read Config in a new Python process with none of our settings in the environment except `env`."""
    clean = {name: value for name, value in os.environ.items() if name not in SETTINGS}
    clean.update(env)
    code = "from app.config import Config as C; print(C.EMAIL_DEMO_MODE, C.AI_PROVIDER)"
    out = subprocess.run([sys.executable, "-c", code], cwd=BACKEND_DIR, env=clean,
                         capture_output=True, text=True, check=True)
    demo, provider = out.stdout.split()
    return {"EMAIL_DEMO_MODE": demo == "True", "AI_PROVIDER": provider}


def test_fresh_copy_never_shows_codes_on_screen_and_uses_the_local_ai():
    assert fresh_config() == {"EMAIL_DEMO_MODE": False, "AI_PROVIDER": "local"}


def test_an_openai_key_alone_switches_gpt_on():
    assert fresh_config(OPENAI_API_KEY="sk-test")["AI_PROVIDER"] == "openai"
    assert fresh_config(OPENAI_API_KEY="sk-test", AI_PROVIDER="")["AI_PROVIDER"] == "openai"
    assert fresh_config(OPENAI_API_KEY="sk-test", AI_PROVIDER="local")["AI_PROVIDER"] == "local"


def test_demo_mode_still_works_when_switched_on(client):
    client.application.config.update(TWO_FACTOR_ENABLED=True, SMTP_HOST="", EMAIL_DEMO_MODE=True)

    res = client.post("/api/auth/register", json=NEW_USER)
    assert res.status_code == 202
    res = client.post("/api/auth/register/verify", json={"email": NEW_USER["email"], "code": res.get_json()["demo_code"]})
    assert res.status_code == 201

    res = client.post("/api/auth/login", json={"email": NEW_USER["email"], "password": NEW_USER["password"]})
    assert res.status_code == 202
    res = client.post("/api/auth/login/verify", json={"email": NEW_USER["email"], "code": res.get_json()["demo_code"]})
    assert res.status_code == 200 and res.get_json()["access_token"]


def test_database_problem_gives_a_clear_message_not_something_went_wrong(tmp_path):
    broken_db = f"sqlite:///{(tmp_path / 'no-such-folder' / 'app.db').as_posix()}"
    app = create_app(TestConfig, LOCAL_STORAGE_DIR=str(tmp_path / "uploads"), SQLALCHEMY_DATABASE_URI=broken_db)
    client = app.test_client()
    for res in (client.post("/api/auth/register", json=NEW_USER),
                client.post("/api/auth/login", json={"email": NEW_USER["email"], "password": NEW_USER["password"]})):
        assert res.status_code == 503
        assert res.get_json()["error"]["code"] == "DATABASE_UNAVAILABLE"
        assert "MySQL" in res.get_json()["error"]["message"]

    rows = dict(report_rows(app, []))
    assert "NOT WORKING" in rows["Database"] and "start MySQL" in rows["Database"]


def test_startup_report_says_what_is_set_up(app, monkeypatch):
    from app.services import extraction

    monkeypatch.setattr(extraction, "tesseract_available", lambda: False)
    rows = dict(report_rows(app, []))
    assert "none found" in rows["Settings file"]
    assert rows["Database"].endswith("- ready")
    assert "add OPENAI_API_KEY" in rows["AI analysis"]
    assert "not available" in rows["Reading scans"]

    app.config.update(TWO_FACTOR_ENABLED=True, SMTP_HOST="", EMAIL_DEMO_MODE=True)
    assert dict(report_rows(app, []))["Sign-in codes"].startswith("DEMO MODE")
    app.config.update(EMAIL_DEMO_MODE=False)
    assert dict(report_rows(app, []))["Sign-in codes"].startswith("NOT SET UP")
    app.config.update(SMTP_HOST="smtp.example.com", SMTP_PORT=465)
    assert dict(report_rows(app, []))["Sign-in codes"] == "emailed through smtp.example.com:465"


# ---------------------------------------------------------------- settings copied to another laptop
def test_settings_pasted_above_the_empty_template_lines_still_count(tmp_path):
    env = tmp_path / ".env"
    env.write_text("\n".join(["SMTP_HOST=smtp.example.com", "SMTP_PASSWORD='p|a:s~s#1'", "",
                              "# template below", "SMTP_HOST=", "SMTP_PASSWORD=", "SMTP_PORT=465"]),
                   encoding="utf-8")
    assert merged_settings([env]) == {"SMTP_HOST": "smtp.example.com", "SMTP_PASSWORD": "p|a:s~s#1",
                                      "SMTP_PORT": "465"}


def test_typed_values_beat_template_values_above_or_below(tmp_path):
    template = {"SMTP_PORT": "587", "SMTP_USE_TLS": "true", "SMTP_HOST": ""}
    pasted = ["SMTP_HOST=smtp.example.com", "SMTP_PORT=465", "SMTP_USE_TLS=false"]
    template_lines = ["SMTP_HOST=", "SMTP_PORT=587", "SMTP_USE_TLS=true"]
    for lines in (pasted + template_lines, template_lines + pasted):
        env = tmp_path / ".env"
        env.write_text("\n".join(lines), encoding="utf-8")
        assert merged_settings([env], template) == {"SMTP_HOST": "smtp.example.com", "SMTP_PORT": "465",
                                                    "SMTP_USE_TLS": "false"}


def test_template_value_already_loaded_by_flask_is_replaced(tmp_path, monkeypatch):
    template, env = tmp_path / ".env.example", tmp_path / ".env"
    template.write_text("SMTP_PORT=587\n", encoding="utf-8")
    env.write_text("SMTP_PORT=465\nSMTP_PORT=587\n", encoding="utf-8")
    monkeypatch.setenv("SMTP_PORT", "587")  # `flask run` loaded the last line
    load_settings([env], template)
    assert os.environ["SMTP_PORT"] == "465"


def test_filled_values_from_a_second_env_file_are_used(tmp_path):
    backend_env, project_env = tmp_path / "backend.env", tmp_path / "project.env"
    backend_env.write_text("SMTP_HOST=\nOPENAI_API_KEY=sk-backend\n", encoding="utf-8")
    project_env.write_text("SMTP_HOST=smtp.example.com\nOPENAI_API_KEY=sk-project\n", encoding="utf-8")
    assert merged_settings([backend_env, project_env]) == {"SMTP_HOST": "smtp.example.com",
                                                          "OPENAI_API_KEY": "sk-backend"}


def test_empty_value_already_loaded_by_flask_is_filled_in(tmp_path, monkeypatch):
    env = tmp_path / ".env"
    env.write_text("SMTP_HOST=smtp.example.com\nSMTP_HOST=\nSMTP_PORT=465\n", encoding="utf-8")
    monkeypatch.setenv("SMTP_HOST", "")      # what `flask run` loads by itself (the last line wins there)
    monkeypatch.setenv("SMTP_PORT", "587")   # a real environment variable is kept
    assert load_settings([env, tmp_path / "missing.env"]) == [env]
    assert os.environ["SMTP_HOST"] == "smtp.example.com" and os.environ["SMTP_PORT"] == "587"


def test_change_email_moves_the_demo_account_to_a_real_inbox(app, client):
    client.post("/api/auth/register", json={**NEW_USER, "email": "demo@fileai.test"})
    runner = app.test_cli_runner()
    result = runner.invoke(args=["change-email", "demo@fileai.test", "Student@Gmail.com"])
    assert result.exit_code == 0, result.output
    res = client.post("/api/auth/login", json={"email": "student@gmail.com", "password": NEW_USER["password"]})
    assert res.status_code == 200
    assert runner.invoke(args=["change-email", "demo@fileai.test", "x@example.com"]).exit_code != 0  # gone
    client.post("/api/auth/register", json={**NEW_USER, "email": "taken@example.com"})
    result = runner.invoke(args=["change-email", "student@gmail.com", "taken@example.com"])
    assert result.exit_code != 0 and "already has an account" in result.output
