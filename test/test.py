import subprocess
import sys
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from currency_translator import convert_currency, get_rates

def test_abraham():
    rates = get_rates()
    result = convert_currency(50, "USD", "USD", rates)
    assert result == 50

def test_best_abigail():
    rates = get_rates()
    result = convert_currency(1, "USD", "EUR", rates)
    assert result == 0.861