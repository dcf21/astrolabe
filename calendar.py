# calendar.py
# -*- coding: utf-8 -*-
#
# The python script in this file makes the various parts of a model astrolabe.
#
# Copyright (C) 2014-2024 Dominic Ford <https://dcford.org.uk/>
#
# This code is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# You should have received a copy of the GNU General Public License along with
# this file; if not, write to the Free Software Foundation, Inc., 51 Franklin
# Street, Fifth Floor, Boston, MA  02110-1301, USA

# ----------------------------------------------------------------------------

"""
Various helper functions for turning calendar dates into Unix times, and vice versa.
"""

from math import floor, fmod
from typing import List, Tuple

# The day of the year on which each month begins
month_day: List[int] = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334, 999]

# The three-letter names of each month of the year
month_name: List[str] = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# The full names of each month of the year
month_name_full: List[str] = ["January", "February", "March", "April", "May", "June",
                              "July", "August", "September", "October", "November", "December"]


def julian_day(year: int, month: int, day: int, hour: int = 0, minute: int = 0, sec: float = 0) -> float:
    """
    Convert a calendar date into a Julian Date.

    :param year:
        Integer year number.
    :param month:
        Integer month number (1-12)
    :param day:
        Integer day of month (1-31)
    :param hour:
        Integer hour of day (0-23)
    :param minute:
        Integer minutes past the hour (0-59)
    :param sec:
        Floating point seconds past minute (0-60)
    :return:
        float Julian date
    """
    last_julian: float = 15821209.0
    first_gregorian: float = 15821220.0
    req_date: float = 10000.0 * year + 100 * month + day

    if month <= 2:
        month += 12
        year -= 1

    if req_date <= last_julian:
        b: float = -2 + floor((year + 4716) / 4) - 1179  # Julian calendar
    elif req_date >= first_gregorian:
        b = floor(year / 400) - floor(year / 100) + floor(year / 4)  # Gregorian calendar
    else:
        raise IndexError("The requested date never happened")

    jd: float = 365.0 * year - 679004.0 + 2400000.5 + b + floor(30.6001 * (month + 1)) + day
    day_fraction: float = (int(hour) + int(minute) / 60.0 + sec / 3600.0) / 24.0
    return jd + day_fraction


def inv_julian_day(jd: float) -> Tuple[int, int, int, int, int, float]:
    """
    Convert a Julian date into a calendar date.

    :param jd:
        Julian date
    :return:
        Calendar date
    """
    day_fraction: float = (jd + 0.5) - floor(jd + 0.5)
    hour: int = int(floor(24 * day_fraction))
    minute: int = int(floor(fmod(1440 * day_fraction, 60)))
    sec: float = fmod(86400 * day_fraction, 60)

    # Number of whole Julian days. b = Number of centuries since the Council of Nicaea.
    # c = Julian Day number as if century leap years happened.
    a: int = int(jd + 0.5)
    if a < 2361222.0:
        c: int = int(a + 1524)  # Julian calendar
    else:
        b: int = int((a - 1867216.25) / 36524.25)
        c: int = int(a + b - (b / 4) + 1525)  # Gregorian calendar
    d: int = int((c - 122.1) / 365.25)  # Number of 365.25 periods, starting the year at the end of February
    e_: int = int(365 * d + d / 4)  # Number of days accounted for by these
    f: int = int((c - e_) / 30.6001)  # Number of 30.6001 days periods (a.k.a. months) in remainder
    day: int = int(floor(c - e_ - int(30.6001 * f)))
    month: int = int(floor(f - 1 - 12 * (f >= 14)))
    year: int = int(floor(d - 4715 - int(month >= 3)))

    return year, month, day, hour, minute, sec


def date_string(utc: float) -> str:
    """
    Create a human-readable date from a unix time.

    :param utc:
        Unix time
    :return:
        Human-readable string
    """
    jd: float = jd_from_unix(utc)
    x = inv_julian_day(jd)
    return "{:02d}/{:02d}/{:04d} {:02d}:{:02d}".format(x[2], x[1], x[0], x[3], x[4])


# Returns a Unix timestamp from a Julian Day number
def unix_from_jd(jd: float) -> float:
    """
    Convert a Julian date into a unix time.

    :param jd:
        Julian date
    :return:
        Float unix time
    """
    return 86400.0 * (jd - 2440587.5)


def jd_from_unix(utc: float) -> float:
    """
    Convert a unix time into a Julian date.

    :param utc:
        Unix time

    :type utc:
        float

    :return:
        Float Julian date
    """
    return (utc / 86400.0) + 2440587.5
