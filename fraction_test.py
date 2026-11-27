"""Pytest tests for the Fraction class. Run with: pytest -v"""
import pytest
from fraction import Fraction

def test_init_simplifies() -> None:
    """Fractions are stored in simplest form."""
    f = Fraction(2, 4)
    assert (f.numerator, f.denominator) == (1, 2)
    assert Fraction(-6, 8) == Fraction(-3, 4)

@pytest.mark.parametrize("denominator", [0, -1])
def test_denominator_must_be_positive(denominator: int) -> None:
    """Zero or negative denominators are rejected."""
    with pytest.raises(ValueError):
        Fraction(1, denominator)

@pytest.mark.parametrize("num, den",
                         [(1.5, 2), (1, 2.0), ("1", 2), (True, 2)])
def test_integers_required(num: object, den: object) -> None:
    """Non-integer parts are rejected."""
    with pytest.raises(TypeError):
        Fraction(num, den)

def test_equality() -> None:
    """Equal values are equal, different values are not."""
    assert Fraction(1, 2) == Fraction(2, 4)
    assert Fraction(1, 2) != Fraction(1, 3)
    assert Fraction(1, 2) != "1/2"

def test_ordering() -> None:
    """<, <=, > and >= give the right answers."""
    small, big = Fraction(1, 3), Fraction(1, 2)
    assert small < big
    assert small <= big
    assert big > small
    assert big >= small
    assert small <= Fraction(2, 6)
    assert small >= Fraction(2, 6)
    assert not big < small
    assert Fraction(-1, 2) < Fraction(1, 3)

def test_ordering_with_other_type() -> None:
    """Comparing with a non-Fraction raises TypeError."""
    with pytest.raises(TypeError):
        Fraction(1, 2) < "x"

def test_add_and_subtract() -> None:
    """Addition and subtraction."""
    assert Fraction(1, 2) + Fraction(1, 3) == Fraction(5, 6)
    assert Fraction(1, 2) - Fraction(1, 3) == Fraction(1, 6)

def test_multiply_and_divide() -> None:
    """Multiplication and division, including negative and zero."""
    assert Fraction(2, 3) * Fraction(3, 4) == Fraction(1, 2)
    assert Fraction(1, 2) / Fraction(1, 4) == Fraction(2, 1)
    assert Fraction(1, 2) / Fraction(-1, 4) == Fraction(-2, 1)
    with pytest.raises(ZeroDivisionError):
        Fraction(1, 2) / Fraction(0, 5)

def test_neg_abs_float() -> None:
    """Negation, absolute value and conversion to float."""
    assert -Fraction(1, 2) == Fraction(-1, 2)
    assert abs(Fraction(-1, 2)) == Fraction(1, 2)
    assert float(Fraction(1, 4)) == 0.25

def test_str_repr_hash() -> None:
    """Text output and hashing."""
    assert str(Fraction(3, 6)) == "1/2"
    assert str(Fraction(4, 2)) == "2"
    assert repr(Fraction(3, 6)) == "Fraction(1, 2)"
    assert hash(Fraction(1, 2)) == hash(Fraction(2, 4))
