"""Python Cookbook 2nd ed.

Chapter 3, Recipe 9, Writing clear documentation strings with RST markup
"""


def Twc(T: float, V: float) -> float:
    """Computes the wind chill temperature

    The wind-chill, :math:`T_{wc}`, is based on
    air temperature, T, and wind speed, V.

    See https://en.wikipedia.org/wiki/Wind_chill

    .. math::

        T_{wc}(T_a, V) = 13.12 + 0.6215 T_a - 11.37 V^{0.16} + 0.3965
        T_a V^{0.16}

    :param T: Temperature in °C
    :param V: Wind Speed in kph
    :returns: Wind-Chill temperature in °C
    :raises ValueError: for wind speeds under  4.8 kph or T above 10°C

    >>> round(Twc(-10, 25), 1)
    -18.8
    """
    if V < 4.8 or T > 10.0:
        raise ValueError(
            "V must be over 4.8 kph, T must be below 10°C")
    return (
        13.12 + 0.6215 * T
        - 11.37 * V ** 0.16 + 0.3965 * T * V ** 0.16
    )


from pytest import approx  # type: ignore


def test_Twc():
    assert Twc(-10, 25) == approx(-18.76076)
