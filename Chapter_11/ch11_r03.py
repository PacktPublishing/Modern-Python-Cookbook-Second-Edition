"""Python Cookbook 2nd ed.

Chapter 11, recipe 3, Handling common doctest issues
"""

# Issue 1 -- set order

import csv
from typing import Iterator, NamedTuple, TextIO, Sequence, cast

class Row(NamedTuple):
    date: str
    lat: str
    lon: str
    time: str


def raw_reader(data_file: TextIO) -> Iterator[Row]:
    """
    Read from a given file if the data has columns that match Row's definition.
    """
    row_field_names = set(Row._fields)
    data_reader = csv.DictReader(data_file)
    reader_field_names = set(cast(Sequence[str], data_reader.fieldnames))
    if not (reader_field_names >= row_field_names):
        raise ValueError(f"Expected {row_field_names}")
    for row in data_reader:
        yield Row(**{k: row[k] for k in row_field_names})


test_good_reader = """
>>> from io import StringIO
>>> mock_good_file = StringIO('''lat,lon,date,time
... 32.8321,-79.9338,2012-11-27,09:15:00
... ''')
>>> good_row_iter = iter(raw_reader(mock_good_file))
>>> next(good_row_iter)
Row(date='2012-11-27', lat='32.8321', lon='-79.9338', time='09:15:00')
"""


test_bad_reader_problem = """
    The following is difficult to reproduce because the set ordering varies.

    ::

        ValueError: Expected {'lat', 'lon', 'time', 'date'}

>>> from io import StringIO
>>> mock_bad_file = StringIO('''lat,lon,date-time,notes
... 32.8321,-79.9338,2012-11-27T09:15:00,Cooper River"
... ''')
>>> bad_row_iter = iter(raw_reader(mock_bad_file))
>>> next(bad_row_iter)  # doctest: +SKIP
Traceback (most recent call last):
  File "/Applications/PyCharm CE.app/Contents/plugins/python-ce/helpers/pycharm/docrunner.py", line 138, in __run
    exec(compile(example.source, filename, "single",
  File "<doctest ch11_r03.raw_reader[6]>", line 1, in <module>
    next(bad_row_iter)
  File "Chapter_11/ch11_r03.py", line 74, in raw_reader
    raise ValueError(f"Expected {expected}")
ValueError: Expected {'lat', 'lon', 'time', 'date'}
"""


test_bad_reader = """
>>> from io import StringIO
>>> mock_bad_file = StringIO('''lat,lon,date-time,notes
... 32.8321,-79.9338,2012-11-27T09:15:00,Cooper River"
... ''')
>>> bad_row_iter = iter(raw_reader(mock_bad_file))
>>> next(bad_row_iter)  # doctest: +ELLIPSIS
Traceback (most recent call last):
  File "/Applications/PyCharm CE.app/Contents/plugins/python-ce/helpers/pycharm/docrunner.py", line 138, in __run
    exec(compile(example.source, filename, "single",
  File "<doctest ch11_r03.raw_reader[6]>", line 1, in <module>
    next(bad_row_iter)
  File "Chapter_11/ch11_r03.py", line 74, in raw_reader
    raise ValueError(f"Expected {expected}")
ValueError: Expected {...}
"""

# Issue 2 -- repr() strings


class Point:
    def __init__(self, lat: float, lon: float) -> None:
        self.lat = lat
        self.lon = lon

    @property
    def text(self):
        ns_hemisphere = "S" if self.lat < 0 else "N"
        ew_hemisphere = "W" if self.lon < 0 else "E"
        lat_deg, lat_ms = divmod(abs(self.lat), 1.0)
        lon_deg, lon_ms = divmod(abs(self.lon), 1.0)
        return (
            f"{lat_deg:02.0f}°{lat_ms*60:4.3f}′{ns_hemisphere} "
            f"{lon_deg:03.0f}°{lon_ms*60:4.3f}′{ew_hemisphere}"
        )


test_point = """
>>> Point(36.8439, -76.2936).text
'36°50.634′N 076°17.616′W'
>>> Point(36.8439, -76.2936)  # doctest: +SKIP
<ch11_r03.Point object at 0x107910610>
>>> Point(36.8439, -76.2936)  # doctest: +ELLIPSIS
<...ch11_r03.Point object at ...
"""

# Issue 3 -- float computations

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


test_phi = """
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

test_phi_approx = """
>>> from math import isclose
>>> isclose(phi(0), 0.5)
True
>>> isclose(phi(1), 0.8413, rel_tol=.0001)
True
>>> isclose(phi(2), 0.9772, rel_tol=1e-4)
True
>>> isclose(phi(3), 0.9987, rel_tol=1e-4)
True
>>> isclose(phi(4), 1.0, rel_tol=1e-4)
True
"""




__test__ = {n: v for n, v in locals().items() if n.startswith("test_")}
