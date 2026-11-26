"""pytest tests for the Temperature class. Run with: pytest -v"""

import pytest

from temperature import Temperature

# Reference points as (Celsius, Fahrenheit, Kelvin).
REFERENCE_POINTS = [
    (-273.15, -459.67, 0.0),    # absolute zero
    (-40.0, -40.0, 233.15),     # C and F cross over
    (0.0, 32.0, 273.15),        # water freezes
    (37.0, 98.6, 310.15),       # human body
    (100.0, 212.0, 373.15),     # water boils
]


# ----- 1. Initialisation -----

def test_default_unit_is_celsius():
    """No unit given means Celsius."""
    assert Temperature(25).unit == "C"


@pytest.mark.parametrize("unit", ["c", "C", "f", "F", "k", "K"])
def test_units_are_case_insensitive(unit):
    """Lower and upper case units both work."""
    assert Temperature(10, unit).unit == unit.upper()


def test_value_and_unit_are_read_only():
    """Trying to change value or unit raises AttributeError."""
    temp = Temperature(25, "C")
    with pytest.raises(AttributeError):
        temp.value = 3
    with pytest.raises(AttributeError):
        temp.unit = "K"


# ----- 2. Validation -----

@pytest.mark.parametrize("unit", ["X", "", "Celsius", "CC"])
def test_invalid_unit(unit):
    """Unknown units raise ValueError."""
    with pytest.raises(ValueError):
        Temperature(0, unit)


@pytest.mark.parametrize("value, unit",
                         [(-273.16, "C"), (-459.68, "F"), (-0.01, "K")])
def test_below_absolute_zero(value, unit):
    """Temperatures below 0 K raise ValueError in every unit."""
    with pytest.raises(ValueError):
        Temperature(value, unit)


def test_convert_to_invalid_unit():
    """convert_to rejects unknown units."""
    with pytest.raises(ValueError):
        Temperature(0).convert_to("X")


# ----- 3. Conversions -----

@pytest.mark.parametrize("celsius, fahrenheit, kelvin", REFERENCE_POINTS)
def test_conversions(celsius, fahrenheit, kelvin):
    """Every unit converts correctly at every reference point."""
    for value, unit in ((celsius, "C"), (fahrenheit, "F"), (kelvin, "K")):
        temp = Temperature(value, unit)
        assert temp.to_celsius() == pytest.approx(celsius, abs=1e-9)
        assert temp.to_fahrenheit() == pytest.approx(fahrenheit, abs=1e-9)
        assert temp.to_kelvin() == pytest.approx(kelvin, abs=1e-9)
        assert temp.convert_to("c") == Temperature(celsius, "C")


# ----- 4. Round trip -----

@pytest.mark.parametrize("celsius", [-273.15, -40, 0, 37, 100, 1234.5])
def test_round_trip(celsius):
    """C -> F -> K -> C gives back the original temperature."""
    original = Temperature(celsius, "C")
    back = original.convert_to("F").convert_to("K").convert_to("C")
    assert back == original
    assert back.unit == "C"


# ----- 5. Comparisons -----

def test_equality_across_units():
    """The same temperature in different units is equal."""
    assert Temperature(0, "C") == Temperature(32, "F")
    assert Temperature(0, "C") == Temperature(273.15, "K")
    assert Temperature(0, "C") != Temperature(33, "F")


def test_ordering_across_units():
    """<, <=, > and >= work between different units."""
    cold, warm = Temperature(0, "C"), Temperature(100, "F")
    assert cold < warm
    assert cold <= warm
    assert warm > cold
    assert warm >= cold
    assert not warm < cold
    assert Temperature(0, "C") <= Temperature(32, "F")
    assert Temperature(0, "C") >= Temperature(32, "F")


def test_tolerance():
    """Differences below 1e-9 count as equal, larger ones do not."""
    assert Temperature(0, "C") == Temperature(1e-10, "C")
    assert Temperature(0, "C") != Temperature(1e-6, "C")


def test_comparison_with_other_types():
    """Comparing with a non-Temperature returns NotImplemented."""
    temp = Temperature(0)
    assert temp.__eq__(5) is NotImplemented
    assert temp.__lt__(5) is NotImplemented
    assert temp != 5
    with pytest.raises(TypeError):
        temp < 5


# ----- 6. Formatting -----

def test_str():
    """str() gives two decimals and the unit."""
    assert str(Temperature(25, "C")) == "25.00 °C"
    assert str(Temperature(98.6, "f")) == "98.60 °F"
    assert str(Temperature(300, "K")) == "300.00 K"


def test_repr():
    """repr() looks like the constructor call."""
    assert repr(Temperature(25, "c")) == "Temperature(25.0, 'C')"