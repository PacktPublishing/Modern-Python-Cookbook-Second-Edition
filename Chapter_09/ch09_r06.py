"""Python Cookbook 2nd ed.

Chapter 9, recipe 6, Combining map and reduce transformations.

"""
import datetime
from typing import List, Iterable, Iterator
from Chapter_09.ch09_r03 import row_merge, CombinedRow, log_rows

# from types import SimpleNamespace as Leg
from dataclasses import dataclass, field


@dataclass
class Leg:
    date: str
    start_time: str
    start_fuel_height: str
    end_time: str
    end_fuel_height: str
    other_notes: str
    start_timestamp: datetime.datetime = field(init=False)
    end_timestamp: datetime.datetime = field(init=False)
    travel_hours: float = field(init=False)
    fuel_change: float = field(init=False)
    fuel_per_hour: float = field(init=False)


def make_Leg(row: CombinedRow) -> Leg:
    return Leg(
        date=row.date,
        start_time=row.engine_on_time,
        start_fuel_height=row.engine_on_fuel_height,
        end_time=row.engine_off_time,
        end_fuel_height=row.engine_off_fuel_height,
        other_notes=row.other_notes,
    )


def timestamp(date_text: str, time_text: str) -> datetime.datetime:
    date = datetime.datetime.strptime(date_text, "%m/%d/%y").date()
    time = datetime.datetime.strptime(time_text, "%I:%M:%S %p").time()
    combined_date_time = datetime.datetime.combine(date, time)
    return combined_date_time


def start_datetime(row: Leg) -> Leg:
    row.start_timestamp = timestamp(row.date, row.start_time)
    return row


def end_datetime(row: Leg) -> Leg:
    row.end_timestamp = timestamp(row.date, row.end_time)
    return row


def duration(row: Leg) -> Leg:
    travel_time = row.end_timestamp - row.start_timestamp
    row.travel_hours = round(travel_time.total_seconds() / 60 / 60, 1)
    return row


def fuel_use(row: Leg) -> Leg:
    end_height = float(row.end_fuel_height)
    start_height = float(row.start_fuel_height)
    row.fuel_change = start_height - end_height
    return row


def fuel_per_hour(row: Leg) -> Leg:
    row.fuel_per_hour = row.fuel_change / row.travel_hours
    return row


def reject_date_header(row: Leg) -> bool:
    """Reject "date" means pass rows without "date"."""
    return not (row.date == "date")


def clean_data_iter(source: Iterable[CombinedRow]) -> Iterator[Leg]:
    leg_iter = map(make_Leg, source)
    fitered_source = filter(reject_date_header, leg_iter)
    start_iter = map(start_datetime, fitered_source)
    end_iter = map(end_datetime, start_iter)
    delta_iter = map(duration, end_iter)
    fuel_iter = map(fuel_use, delta_iter)
    per_hour_iter = map(fuel_per_hour, fuel_iter)
    return per_hour_iter


def total_fuel(source: Iterable[Leg]) -> float:
    """
    >>> round(total_fuel(clean_data_iter(row_merge(log_rows))), 3)
    7.0
    """
    return sum(row.fuel_change for row in source)


from statistics import mean


def avg_fuel_per_hour(source: Iterable[Leg]) -> float:
    """
    >>> round(
    ...     avg_fuel_per_hour(clean_data_iter(row_merge(log_rows))),
    ...     3)
    0.48
    """
    return mean(row.fuel_per_hour for row in source)


from statistics import stdev


def stdev_fuel_per_hour(source: Iterable[Leg]) -> float:
    """
    >>> round(stdev_fuel_per_hour(clean_data_iter(row_merge(log_rows))), 4)
    0.0897
    """
    return stdev(row.fuel_per_hour for row in source)


def summary(raw_data: Iterable[List[str]]) -> None:
    """
    >>> summary(log_rows)
    Fuel use 0.48 ±0.18
    """
    data = tuple(clean_data_iter(row_merge(raw_data)))
    m = avg_fuel_per_hour(data)
    s = 2 * stdev_fuel_per_hour(data)

    print(f"Fuel use {m:.2f} ±{s:.2f}")


def summary_t(raw_data: Iterable[List[str]]):
    """
    >>> summary_t(log_rows)
    Fuel use 0.48 ±0.18
    """
    from itertools import tee

    data1, data2 = tee(clean_data_iter(row_merge(raw_data)), 2)
    m = avg_fuel_per_hour(data1)
    s = 2 * stdev_fuel_per_hour(data2)
    print(f"Fuel use {m:.2f} ±{s:.2f}")


from pprint import pprint


def details(iterable):
    """
    >>> details(clean_data_iter(row_merge(log_rows))) # doctest: +NORMALIZE_WHITESPACE
    Leg(date='10/25/13',
     start_time='08:24:00 AM', start_fuel_height='29',
     end_time='01:15:00 PM', end_fuel_height='27',
     other_notes="calm seas -- anchor solomon's island",
     start_timestamp=datetime.datetime(2013, 10, 25, 8, 24),
     end_timestamp=datetime.datetime(2013, 10, 25, 13, 15),
     travel_hours=4.8, fuel_change=2.0, fuel_per_hour=0.4166666666666667)
    Leg(date='10/26/13',
     start_time='09:12:00 AM', start_fuel_height='27',
     end_time='06:25:00 PM', end_fuel_height='22',
     other_notes="choppy -- anchor in jackson's creek",
     start_timestamp=datetime.datetime(2013, 10, 26, 9, 12),
     end_timestamp=datetime.datetime(2013, 10, 26, 18, 25),
     travel_hours=9.2, fuel_change=5.0, fuel_per_hour=0.5434782608695653)
    """
    for row in iterable:
        pprint(row)
