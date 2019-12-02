"""Python Cookbook 2nd ed.

Chapter 11, recipe 3.
"""

from math import sqrt, pi, exp, erf


def phi(n: float) -> float:
    """
    Computes the cumulative distribution function of the standard,
    normal distribution for values <= n.

    >>> round(phi(0), 3)
    0.5
    >>> round(phi(-1), 3)
    0.159
    >>> round(phi(+1), 3)
    0.841

    """
    return (1 + erf(n / sqrt(2))) / 2


def frequency(n: float) -> float:
    """
    The frequency of a sample being in the range -n to +n

    >>> round(frequency(1), 3)
    0.683
    >>> round(frequency(2), 3)
    0.954
    >>> round(frequency(3), 3)
    0.997
    """
    return phi(n) - phi(-n)


import csv


def raw_reader(data_file):
    """
    Read from a given, open file.

    >>> from io import StringIO
    >>> mock_file = StringIO('''lat,lon,date,time
    ... 32.8321,-79.9338,2012-11-27,09:15:00
    ... ''')
    >>> row_iter = iter(raw_reader(mock_file))

    Does not work properly.
    >>> next(row_iter)  # doctest: +SKIP
    {'time': '09:15:00', 'lat': '32.8321', 'date': '2012-11-27', 'lon': '-79.9338'}

    Better approach.
    >>> row = next(row_iter)
    >>> sorted(row.items())
    [('date', '2012-11-27'), ('lat', '32.8321'), ('lon', '-79.9338'), ('time', '09:15:00')]
    >>> row['date']
    '2012-11-27'
    >>> row['lat']
    '32.8321'
    >>> row['lon']
    '-79.9338'
    >>> row['time']
    '09:15:00'
    """
    data_reader = csv.DictReader(data_file)
    for row in data_reader:
        yield row


__test__ = {
    "phi(x)": """
>>> round(phi(0), 4)
0.5
>>> round(phi(1), 4)
0.8413
>>> round(phi(2), 4)
0.9772
>>> round(phi(3), 4)
0.9987
>>> round(phi(4), 4)
1.0
"""
}
