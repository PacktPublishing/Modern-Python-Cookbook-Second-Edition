"""Python Cookbook 2nd ed.

Chapter 9, recipe 3, Using stacked generator expressions.
"""
import datetime
from typing import Iterable, Iterator, List, Union, cast, NamedTuple
from pprint import pprint

log_rows = [
    ["date", "engine on", "fuel height"],
    ["", "engine off", "fuel height"],
    ["", "Other notes", ""],
    ["10/25/13", "08:24:00 AM", "29"],
    ["", "01:15:00 PM", "27"],
    ["", "calm seas -- anchor solomon's island", ""],
    ["10/26/13", "09:12:00 AM", "27"],
    ["", "06:25:00 PM", "22"],
    ["", "choppy -- anchor in jackson's creek", ""],
]

RawRow = List[str]


class CombinedRow(NamedTuple):
    # Line 1
    date: str
    engine_on_time: str
    engine_on_fuel_height: str
    # Line 2
    filler_1: str
    engine_off_time: str
    engine_off_fuel_height: str
    # Line 3
    filler_2: str
    other_notes: str
    filler_3: str


def row_merge(source: Iterable[RawRow]) -> Iterator[CombinedRow]:
    cluster: RawRow = []
    for row in source:
        if len(row[0]) != 0:
            if len(cluster) == 9:
                yield CombinedRow(*cluster)
            cluster = row.copy()
        else:
            cluster.extend(row)
    if len(cluster) == 9:
        yield CombinedRow(*cluster)


def skip_header_1(source: Iterable[CombinedRow]) -> Iterator[CombinedRow]:
    row_iter = iter(source)
    next(row_iter)
    return row_iter


def skip_header_date(source: Iterable[CombinedRow]) -> Iterator[CombinedRow]:
    for row in source:
        if row.date == "date":
            continue
        yield row


import datetime


class DatetimeRow(NamedTuple):
    date: datetime.date
    engine_on: datetime.datetime
    engine_on_fuel_height: str
    engine_off: datetime.datetime
    engine_off_fuel_height: str
    other_notes: str


def convert_datetime(row: CombinedRow) -> DatetimeRow:
    travel_date = datetime.datetime.strptime(row.date, "%m/%d/%y").date()
    start_time = datetime.datetime.strptime(row.engine_on_time, "%I:%M:%S %p").time()
    start_datetime = datetime.datetime.combine(travel_date, start_time)

    end_time = datetime.datetime.strptime(row.engine_off_time, "%I:%M:%S %p").time()
    end_datetime = datetime.datetime.combine(travel_date, end_time)

    return DatetimeRow(
        date=travel_date,
        engine_on=start_datetime,
        engine_off=end_datetime,
        engine_on_fuel_height=row.engine_on_fuel_height,
        engine_off_fuel_height=row.engine_off_fuel_height,
        other_notes=row.other_notes,
    )


class DurationRow(NamedTuple):
    date: datetime.date
    engine_on: datetime.datetime
    engine_on_fuel_height: str
    engine_off: datetime.datetime
    engine_off_fuel_height: str
    duration: float
    other_notes: str


def duration(row: DatetimeRow) -> DurationRow:
    travel_hours = round((row.engine_off - row.engine_on).total_seconds() / 60 / 60, 1)
    return DurationRow(
        date=row.date,
        engine_on=row.engine_on,
        engine_off=row.engine_off,
        engine_on_fuel_height=row.engine_on_fuel_height,
        engine_off_fuel_height=row.engine_off_fuel_height,
        other_notes=row.other_notes,
        duration=travel_hours,
    )


class Leg(NamedTuple):
    date: datetime.date
    engine_on: datetime.datetime
    engine_on_fuel_height: float
    engine_off: datetime.datetime
    engine_off_fuel_height: float
    duration: float
    other_notes: str


def convert_height(row: DurationRow) -> Leg:
    return Leg(
        date=row.date,
        engine_on=row.engine_on,
        engine_off=row.engine_off,
        duration=row.duration,
        engine_on_fuel_height=float(row.engine_on_fuel_height),
        engine_off_fuel_height=float(row.engine_off_fuel_height),
        other_notes=row.other_notes,
    )


# Stack of conversions.
def leg_duration_iter(source: Iterable[str]) -> Iterator[Leg]:
    merged_rows = row_merge(log_rows)
    tail_gen = skip_header_date(merged_rows)
    datetime_gen = (convert_datetime(row) for row in tail_gen)
    duration_gen = (duration(row) for row in datetime_gen)
    height_gen = (convert_height(row) for row in duration_gen)
    return height_gen


test_row_merge = """
>>> pprint(list(row_merge(log_rows)))
[CombinedRow(date='date', engine_on_time='engine on', engine_on_fuel_height='fuel height', filler_1='', engine_off_time='engine off', engine_off_fuel_height='fuel height', filler_2='', other_notes='Other notes', filler_3=''),
 CombinedRow(date='10/25/13', engine_on_time='08:24:00 AM', engine_on_fuel_height='29', filler_1='', engine_off_time='01:15:00 PM', engine_off_fuel_height='27', filler_2='', other_notes="calm seas -- anchor solomon's island", filler_3=''),
 CombinedRow(date='10/26/13', engine_on_time='09:12:00 AM', engine_on_fuel_height='27', filler_1='', engine_off_time='06:25:00 PM', engine_off_fuel_height='22', filler_2='', other_notes="choppy -- anchor in jackson's creek", filler_3='')]
"""

test_goal = """
>>> row_gen = row_merge(log_rows)
>>> tail_gen = skip_header_date(row_gen)
>>> datetime_gen = (convert_datetime(row) for row in tail_gen)
>>> total_time = datetime.timedelta(0) 
>>> total_fuel = 0
>>> for row in datetime_gen: 
...     total_time += row.engine_off-row.engine_on
...     total_fuel += (
...         float(row.engine_on_fuel_height)-
...         float(row.engine_off_fuel_height)
...    )
>>> print(
...     f"{total_time.total_seconds()/60/60 =:.2f}, "
...     f"{total_fuel =:.2f}")
total_time.total_seconds()/60/60 =14.07, total_fuel =7.00

"""

test_skip_header_1 = """
>>> row_gen = row_merge(log_rows)
>>> tail_gen = skip_header_1(row_gen)
>>> pprint(list(tail_gen))
[CombinedRow(date='10/25/13', engine_on_time='08:24:00 AM', engine_on_fuel_height='29', filler_1='', engine_off_time='01:15:00 PM', engine_off_fuel_height='27', filler_2='', other_notes="calm seas -- anchor solomon's island", filler_3=''),
 CombinedRow(date='10/26/13', engine_on_time='09:12:00 AM', engine_on_fuel_height='27', filler_1='', engine_off_time='06:25:00 PM', engine_off_fuel_height='22', filler_2='', other_notes="choppy -- anchor in jackson's creek", filler_3='')]
"""

test_skip_header_date = """
>>> row_gen = row_merge(log_rows)
>>> tail_gen = skip_header_date(row_gen)
>>> pprint(list(tail_gen))
[CombinedRow(date='10/25/13', engine_on_time='08:24:00 AM', engine_on_fuel_height='29', filler_1='', engine_off_time='01:15:00 PM', engine_off_fuel_height='27', filler_2='', other_notes="calm seas -- anchor solomon's island", filler_3=''),
 CombinedRow(date='10/26/13', engine_on_time='09:12:00 AM', engine_on_fuel_height='27', filler_1='', engine_off_time='06:25:00 PM', engine_off_fuel_height='22', filler_2='', other_notes="choppy -- anchor in jackson's creek", filler_3='')]
"""

test_convert_datetime = """
>>> row_gen = row_merge(log_rows)
>>> tail_gen = skip_header_date(row_gen)
>>> datetime_gen = (convert_datetime(row) for row in tail_gen)
>>> pprint(list(datetime_gen))
[DatetimeRow(date=datetime.date(2013, 10, 25), engine_on=datetime.datetime(2013, 10, 25, 8, 24), engine_on_fuel_height='29', engine_off=datetime.datetime(2013, 10, 25, 13, 15), engine_off_fuel_height='27', other_notes="calm seas -- anchor solomon's island"),
 DatetimeRow(date=datetime.date(2013, 10, 26), engine_on=datetime.datetime(2013, 10, 26, 9, 12), engine_on_fuel_height='27', engine_off=datetime.datetime(2013, 10, 26, 18, 25), engine_off_fuel_height='22', other_notes="choppy -- anchor in jackson's creek")]
"""


test_start_time_end_time_height = """
>>> row_gen = row_merge(log_rows)
>>> tail_gen = skip_header_date(row_gen)
>>> datetime_gen = (convert_datetime(row) for row in tail_gen)
>>> d = (duration(row) for row in datetime_gen)
>>> pprint(list(d))
[DurationRow(date=datetime.date(2013, 10, 25), engine_on=datetime.datetime(2013, 10, 25, 8, 24), engine_on_fuel_height='29', engine_off=datetime.datetime(2013, 10, 25, 13, 15), engine_off_fuel_height='27', duration=4.8, other_notes="calm seas -- anchor solomon's island"),
 DurationRow(date=datetime.date(2013, 10, 26), engine_on=datetime.datetime(2013, 10, 26, 9, 12), engine_on_fuel_height='27', engine_off=datetime.datetime(2013, 10, 26, 18, 25), engine_off_fuel_height='22', duration=9.2, other_notes="choppy -- anchor in jackson's creek")]

"""

test_data_conversion = """
>>> converted = leg_duration_iter(log_rows)
>>> pprint(list(converted))
[Leg(date=datetime.date(2013, 10, 25), engine_on=datetime.datetime(2013, 10, 25, 8, 24), engine_on_fuel_height=29.0, engine_off=datetime.datetime(2013, 10, 25, 13, 15), engine_off_fuel_height=27.0, duration=4.8, other_notes="calm seas -- anchor solomon's island"),
 Leg(date=datetime.date(2013, 10, 26), engine_on=datetime.datetime(2013, 10, 26, 9, 12), engine_on_fuel_height=27.0, engine_off=datetime.datetime(2013, 10, 26, 18, 25), engine_off_fuel_height=22.0, duration=9.2, other_notes="choppy -- anchor in jackson's creek")]
"""


__test__ = {n: v for n, v in locals().items() if n.startswith("test_")}
