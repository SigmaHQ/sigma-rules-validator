import importlib.util
import os
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent

spec = importlib.util.spec_from_file_location("validate", REPO_ROOT / "validate.py")
validate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validate)


@pytest.fixture
def clean_env(monkeypatch):
    for var in (
        "GITHUB_WORKSPACE",
        "GITHUB_ACTION_PATH",
        "SIGMA_RULES_PATH",
        "SIGMA_SCHEMA_FILE",
        "SIGMA_SCHEMA_URL",
    ):
        monkeypatch.delenv(var, raising=False)


def test_generate_all_files_yields_yml(tmp_path):
    (tmp_path / "a.yml").write_text("x")
    (tmp_path / "b.txt").write_text("x")
    sub = tmp_path / "sub"
    sub.mkdir()
    (sub / "c.yml").write_text("x")

    found = sorted(p.name for p in validate.generate_all_files(tmp_path))
    assert found == ["a.yml", "c.yml"]


def test_get_rules_returns_absolute_paths(tmp_path):
    (tmp_path / "rule.yml").write_text("x")
    rules = validate.get_rules([tmp_path])
    assert len(rules) == 1
    assert Path(rules[0]).is_absolute()
    assert rules[0].endswith("rule.yml")


def test_get_rules_exits_when_empty(tmp_path, monkeypatch):
    def _raise(code):
        raise SystemExit(code)

    monkeypatch.setattr(validate.os, "_exit", _raise)
    with pytest.raises(SystemExit), pytest.warns(UserWarning, match="No rules found"):
        validate.get_rules([tmp_path])


def test_get_envs_defaults(clean_env, monkeypatch, tmp_path):
    monkeypatch.setenv("GITHUB_WORKSPACE", str(tmp_path))
    envs = validate.get_envs()
    assert envs["GITHUB_WORKSPACE"] == Path(str(tmp_path))
    assert envs["SIGMA_RULES_PATH"] == [Path(str(tmp_path))]
    assert envs["SIGMA_SCHEMA_FILE"] is None
    assert "sigma-specification" in envs["SIGMA_SCHEMA_URL"]


def test_get_envs_splits_multiline_paths(clean_env, monkeypatch, tmp_path):
    monkeypatch.setenv("GITHUB_WORKSPACE", str(tmp_path))
    monkeypatch.setenv("SIGMA_RULES_PATH", "rules\ncustom-rules\n")
    envs = validate.get_envs()
    names = [p.name for p in envs["SIGMA_RULES_PATH"]]
    assert names == ["rules", "custom-rules"]


class _FakeResponse:
    def __init__(self, status_code: int, content: bytes = b""):
        self.status_code = status_code
        self.content = content


def _envs(workspace: Path, action_path: Path, schema_file=None) -> dict:
    return {
        "GITHUB_WORKSPACE": workspace,
        "GITHUB_ACTION_PATH": action_path,
        "SIGMA_RULES_PATH": [workspace],
        "SIGMA_SCHEMA_FILE": schema_file,
        "SIGMA_SCHEMA_URL": "https://example.invalid/schema.json",
    }


def test_download_schema_file_uses_explicit_existing(tmp_path, monkeypatch):
    workspace = tmp_path / "ws"
    action_path = tmp_path / "action"
    workspace.mkdir()
    action_path.mkdir()
    schema = workspace / "my-schema.json"
    schema.write_text("{}")

    called = {"hit": False}

    def _no_http(*a, **kw):
        called["hit"] = True
        raise AssertionError("requests.get must not be called")

    monkeypatch.setattr(validate.requests, "get", _no_http)
    envs = _envs(workspace, action_path, schema_file=str(schema))
    result = validate.download_schema_file(envs)
    assert result == schema.absolute()
    assert called["hit"] is False


def test_download_schema_file_warns_when_explicit_missing(tmp_path, monkeypatch):
    workspace = tmp_path / "ws"
    action_path = tmp_path / "action"
    workspace.mkdir()
    action_path.mkdir()

    monkeypatch.setattr(
        validate.requests, "get", lambda url: _FakeResponse(200, b'{"ok": true}')
    )
    envs = _envs(workspace, action_path, schema_file="missing-schema.json")

    with pytest.warns(UserWarning, match="not found, falling back"):
        result = validate.download_schema_file(envs)

    expected = (action_path / "sigma-schema.json").absolute()
    assert result == expected
    assert expected.read_bytes() == b'{"ok": true}'


def test_download_schema_file_downloads_when_unset(tmp_path, monkeypatch):
    workspace = tmp_path / "ws"
    action_path = tmp_path / "action"
    workspace.mkdir()
    action_path.mkdir()

    decoy = workspace / "sigma-schema.json"
    decoy.write_text("DECOY")

    monkeypatch.setattr(
        validate.requests, "get", lambda url: _FakeResponse(200, b"FRESH")
    )
    envs = _envs(workspace, action_path, schema_file=None)
    result = validate.download_schema_file(envs)

    expected = (action_path / "sigma-schema.json").absolute()
    assert result == expected
    assert expected.read_bytes() == b"FRESH"
    assert decoy.read_text() == "DECOY"


def test_download_schema_file_exits_on_http_failure(tmp_path, monkeypatch):
    workspace = tmp_path / "ws"
    action_path = tmp_path / "action"
    workspace.mkdir()
    action_path.mkdir()

    monkeypatch.setattr(validate.requests, "get", lambda url: _FakeResponse(500))

    def _raise(code):
        raise SystemExit(code)

    monkeypatch.setattr(validate.os, "_exit", _raise)
    envs = _envs(workspace, action_path, schema_file=None)
    with pytest.raises(SystemExit), pytest.warns(UserWarning, match="Failed to download"):
        validate.download_schema_file(envs)
