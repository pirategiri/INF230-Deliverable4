"""Temperature class that supports Celsius, Fahrenheit and Kelvin."""

# Two temperatures closer than this are treated as equal. Floating-point
# numbers are not exact, so we never compare them with a plain ==.
TOLERANCE = 1e-9

# The only units the class accepts.
VALID_UNITS = ("C", "F", "K")


def is_close(a, b):
    """Return True if the numbers a and b differ by less than TOLERANCE."""
    return abs(a - b) <= TOLERANCE


def to_kelvin_from(value, unit):
    """Convert a number in the given unit ("C", "F" or "K") to Kelvin.

    Every comparison and conversion goes through Kelvin, so we only need
    one formula per unit instead of one for every pair of units.
    """
    if unit == "C":
        return value + 273.15
    if unit == "F":
        return (value - 32) * 5 / 9 + 273.15
    return value  # already Kelvin


class Temperature:
    """A temperature with a value and a unit (C, F or K)."""

    def __init__(self, value, unit="C"):
        """Create a temperature.

        Raises ValueError if the unit is not C, F or K (any letter case),
        or if the temperature is below absolute zero (0 K).
        """
        # Check the unit first; .upper() makes "c" and "C" the same.
        if not isinstance(unit, str) or unit.upper() not in VALID_UNITS:
            raise ValueError("Unit must be 'C', 'F' or 'K'.")
        unit = unit.upper()

        # Check the value is a real number (bool is excluded on purpose).
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError("Value must be a number.")

        # Absolute zero check: nothing can be colder than 0 K.
        kelvin = to_kelvin_from(value, unit)
        if kelvin < 0 and not is_close(kelvin, 0):
            raise ValueError("Temperature is below absolute zero.")

        # A leading underscore is a Python convention for "private".
        self._value = float(value)
        self._unit = unit

    @property
    def value(self):
        """Return the numeric value (read-only, there is no setter)."""
        return self._value

    @property
    def unit(self):
        """Return the unit letter (read-only, there is no setter)."""
        return self._unit

    def to_kelvin(self):
        """Return this temperature as a float in Kelvin."""
        return to_kelvin_from(self._value, self._unit)

    def to_celsius(self):
        """Return this temperature as a float in Celsius."""
        return self.to_kelvin() - 273.15

    def to_fahrenheit(self):
        """Return this temperature as a float in Fahrenheit."""
        return (self.to_kelvin() - 273.15) * 9 / 5 + 32

    def convert_to(self, target_unit):
        """Return a NEW Temperature in target_unit (case-insensitive).

        Raises ValueError if target_unit is not C, F or K.
        """
        if (not isinstance(target_unit, str)
                or target_unit.upper() not in VALID_UNITS):
            raise ValueError("Unit must be 'C', 'F' or 'K'.")
        target_unit = target_unit.upper()

        if target_unit == "C":
            new_value = self.to_celsius()
        elif target_unit == "F":
            new_value = self.to_fahrenheit()
        else:
            # Tiny rounding errors could give -0.0000000001 K.
            new_value = max(self.to_kelvin(), 0.0)
        return Temperature(new_value, target_unit)

    def __repr__(self):
        """Return an unambiguous text, e.g. Temperature(25.0, 'C')."""
        return f"Temperature({self._value}, '{self._unit}')"

    def __str__(self):
        """Return a readable text with two decimals, e.g. 25.00 °C."""
        if self._unit == "K":
            return f"{self._value:.2f} K"
        return f"{self._value:.2f} °{self._unit}"

    def __eq__(self, other):
        """Return True if both temperatures are equal (any unit)."""
        if not isinstance(other, Temperature):
            return NotImplemented  # lets Python try other options
        return is_close(self.to_kelvin(), other.to_kelvin())

    def __ne__(self, other):
        """Return True if the temperatures are not equal."""
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result

    def __lt__(self, other):
        """Return True if this temperature is colder than other."""
        if not isinstance(other, Temperature):
            return NotImplemented
        # Smaller AND not "equal within tolerance".
        return (self.to_kelvin() < other.to_kelvin()
                and not is_close(self.to_kelvin(), other.to_kelvin()))

    def __le__(self, other):
        """Return True if this temperature is colder than or equal."""
        if not isinstance(other, Temperature):
            return NotImplemented
        return self < other or self == other

    def __gt__(self, other):
        """Return True if this temperature is warmer than other."""
        if not isinstance(other, Temperature):
            return NotImplemented
        return other < self

    def __ge__(self, other):
        """Return True if this temperature is warmer than or equal."""
        if not isinstance(other, Temperature):
            return NotImplemented
        return other <= self

    # Because equality uses a tolerance, we cannot give a reliable hash.
    __hash__ = None