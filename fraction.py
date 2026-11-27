"""Fraction class with automatic simplification."""
from math import gcd
class Fraction:
    """A fraction such as 3/4, stored in its simplest form."""

    def __init__(self, numerator: int, denominator: int = 1) -> None:
        """Create a fraction.
        Both parts must be integers and the denominator must be > 0.
        The fraction is simplified, so Fraction(2, 4) becomes 1/2.
        """
        # bool is a subclass of int in Python, so exclude it explicitly.
        for part in (numerator, denominator):
            if isinstance(part, bool) or not isinstance(part, int):
                raise TypeError("Numerator and denominator must be ints.")
        if denominator <= 0:
            raise ValueError("Denominator must be strictly positive.")

        # Divide both parts by their greatest common divisor.
        divisor = gcd(numerator, denominator)
        self.numerator: int = numerator // divisor
        self.denominator: int = denominator // divisor

    def __repr__(self) -> str:
        """Return an unambiguous text, e.g. Fraction(1, 2)."""
        return f"Fraction({self.numerator}, {self.denominator})"

    def __str__(self) -> str:
        """Return a readable text, e.g. 1/2 (or just 2 for 2/1)."""
        if self.denominator == 1:
            return str(self.numerator)
        return f"{self.numerator}/{self.denominator}"

    # ----- Comparisons -----
    # a/b compared with c/d is the same as a*d compared with c*b
    # (valid because both denominators are positive).

    def _difference(self, other: "Fraction") -> int:
        """Return self.numerator*other.denominator minus the cross product.

        The result is negative, zero or positive, which tells us whether
        self is smaller than, equal to, or greater than other.
        """
        return (self.numerator * other.denominator
                - other.numerator * self.denominator)

    def __eq__(self, other: object) -> bool:
        """Return True if both fractions have the same value."""
        if not isinstance(other, Fraction):
            return NotImplemented
        return self._difference(other) == 0

    def __ne__(self, other: object) -> bool:
        """Return True if the fractions have different values."""
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result

    def __lt__(self, other: "Fraction") -> bool:
        """Return True if self is smaller than other."""
        if not isinstance(other, Fraction):
            return NotImplemented
        return self._difference(other) < 0

    def __le__(self, other: "Fraction") -> bool:
        """Return True if self is smaller than or equal to other."""
        if not isinstance(other, Fraction):
            return NotImplemented
        return self._difference(other) <= 0

    def __gt__(self, other: "Fraction") -> bool:
        """Return True if self is greater than other."""
        if not isinstance(other, Fraction):
            return NotImplemented
        return self._difference(other) > 0

    def __ge__(self, other: "Fraction") -> bool:
        """Return True if self is greater than or equal to other."""
        if not isinstance(other, Fraction):
            return NotImplemented
        return self._difference(other) >= 0

    def __hash__(self) -> int:
        """Return a hash so fractions can be used in sets and dicts."""
        return hash((self.numerator, self.denominator))

    # ----- Other special methods -----

    def __add__(self, other: "Fraction") -> "Fraction":
        """Return self + other as a new Fraction."""
        if not isinstance(other, Fraction):
            return NotImplemented
        new_num = (self.numerator * other.denominator
                   + other.numerator * self.denominator)
        new_den = self.denominator * other.denominator
        return Fraction(new_num, new_den)

    def __sub__(self, other: "Fraction") -> "Fraction":
        """Return self - other as a new Fraction."""
        if not isinstance(other, Fraction):
            return NotImplemented
        return self + (-other)

    def __mul__(self, other: "Fraction") -> "Fraction":
        """Return self * other as a new Fraction."""
        if not isinstance(other, Fraction):
            return NotImplemented
        return Fraction(self.numerator * other.numerator,
                        self.denominator * other.denominator)

    def __truediv__(self, other: "Fraction") -> "Fraction":
        """Return self / other as a new Fraction.

        Raises ZeroDivisionError when dividing by zero.
        """
        if not isinstance(other, Fraction):
            return NotImplemented
        if other.numerator == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        new_num = self.numerator * other.denominator
        new_den = self.denominator * other.numerator
        # Keep the denominator positive by moving the sign to the top.
        if new_den < 0:
            new_num, new_den = -new_num, -new_den
        return Fraction(new_num, new_den)

    def __neg__(self) -> "Fraction":
        """Return the negative of this fraction, e.g. -(1/2) = -1/2."""
        return Fraction(-self.numerator, self.denominator)

    def __abs__(self) -> "Fraction":
        """Return the absolute value, e.g. abs(-1/2) = 1/2."""
        return Fraction(abs(self.numerator), self.denominator)

    def __float__(self) -> float:
        """Return the decimal value, e.g. float(1/4) = 0.25."""
        return self.numerator / self.denominator
