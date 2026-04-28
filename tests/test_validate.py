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
