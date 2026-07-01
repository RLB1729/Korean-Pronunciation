"""Tests for the CLI entry point."""

import sys
import subprocess
import json


def test_cli_plain():
    cmd = [sys.executable, "-m", "korean_pronunciation.main", "선의"]
    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    assert result.returncode == 0
    lines = result.stdout.strip().splitlines()
    prons = [line.split(" (")[0] for line in lines]
    assert "서늬" in prons
    assert "서니" in prons
    assert len(lines) == 2


def test_cli_json():
    cmd = [sys.executable, "-m", "korean_pronunciation.main", "선의", "--json"]
    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    assert result.returncode == 0
    data = json.loads(result.stdout.strip())
    prons = [item["pronunciation"] for item in data]
    assert "서늬" in prons
    assert "서니" in prons
    assert len(data) == 2
