import importlib
import subprocess
import sys
from pathlib import Path


LESSON4_PATH = Path(__file__).with_name("lesson4.py")


def test_filter_by_name(monkeypatch):
	monkeypatch.setattr(sys, "argv", [str(LESSON4_PATH), "--name", "Bob"])
	lesson4 = importlib.import_module("lesson4")

	assert lesson4.filter_by_name(lesson4.test_scores, "Bob") == {
		"Name": "Bob",
		"Math": [82, 62, 92],
		"Eng": [52, 82, 92],
	}


def test_lesson4_cli_prints_selected_scores():
	result = subprocess.run(
		[sys.executable, str(LESSON4_PATH), "--name", "Ann"],
		capture_output=True,
		text=True,
		check=False,
	)

	assert result.returncode == 0
	assert "Math scores:  [70, 80, 90]" in result.stdout
	assert "English scores:  [20, 80, 70]" in result.stdout
	assert "Name is in position 0" in result.stdout
