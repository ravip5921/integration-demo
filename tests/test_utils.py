import pytest
from integrations.utils import is_odd, is_even

def test_is_odd_positive_odd():
    assert is_odd(1) is True
    assert is_odd(3) is True
    assert is_odd(101) is True

def test_is_odd_positive_even():
    assert is_odd(2) is False
    assert is_odd(4) is False
    assert is_odd(100) is False

def test_is_odd_negative_odd():
    assert is_odd(-1) is True
    assert is_odd(-3) is True
    assert is_odd(-101) is True

def test_is_odd_negative_even():
    assert is_odd(-2) is False
    assert is_odd(-4) is False
    assert is_odd(-100) is False

def test_is_odd_zero():
    assert is_odd(0) is False

@pytest.mark.parametrize("n, expected", [
    (2, True),
    (1, False),
    (-2, True),
    (-1, False),
    (0, True),
    (42, True),
    (43, False),
    (-42, True),
    (-43, False),
])
def test_is_even(n, expected):
    assert is_even(n) is expected