# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: jernej@reciprocitylabs.com
# Maintained By: jernej@reciprocitylabs.com
    
import calendar
from datetime import datetime


def get_days_in_current_month():
    """Gets days in current month

    Returns:
        int
    """
    now = datetime.now()
    weekday, days_in_month = calendar.monthrange(now.year, now.month)
    return days_in_month


def get_from_string(date, format):
    """Creates a date object from given string

    Args:
        date (str): date string
        format (str): date format specs

    Returns:
        datetime
    """
    return datetime.strptime(date, format)


def get_month_start(date):
    """Gets a date object with the date of the first of the month.

    Args:
        date (datetime)

    Returns:
        datetime
    """
    return date.replace(day=1)


def get_month_end(date):
    """Gets month end of the input date object.

    Args:
         date (datetime)

    Returns:
        datetime
    """
    return date.replace(day=calendar.monthrange(date.year, date.month)[1])


def get_current():
    """Gets a date object with current date

    Returns:
        datetime
    """
    return datetime.now()
