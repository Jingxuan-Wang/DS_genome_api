#  Copyright © DataSpark Pte Ltd 2014 - 2020.
#
#  This software and any related documentation contain confidential and proprietary information of
#  DataSpark and its licensors (if any). Use of this software and any related documentation is
#  governed by the terms of your written agreement with DataSpark. You may not use, download or
#  install this software or any related documentation without obtaining an appropriate licence
#  agreement from DataSpark.
#
#  All rights reserved.

"""
   This is toolkits for all the basic temporal data related operations

   @author: jingxuan
   @maintainer: jingxuan
   @last editor: jingxuan
   @last edit time: 2/9/20
"""

import pytz
from datetime import datetime, timedelta

INPUT_DATETIME_FORMAT = ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M:%S,%f", "%Y-%m-%d %H:%M:%S.%f",
                         "%Y-%m-%d %H:%M:%S%z"]
DATETIME_FORMAT_TZ = "%Y-%m-%d %H:%M:%S%z"
DATETIME_FORMAT_TZ2 = "%Y-%m-%dT%H:%M:%S%z"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
DATE_FORMAT = "%Y-%m-%d"

def parse(dt, tz=""):
  """
  parse datetime string with multiple format selection
  Args:
    dt: datetime string

  Returns:
    dt in datetime format
  """
  for format in INPUT_DATETIME_FORMAT:
    try:
      dt = datetime.strptime(dt, format)
      if tz != "" and dt.tzinfo == None:
        dt = pytz.timezone(tz).localize(dt)
      return dt
    except ValueError:
      pass
  raise ValueError('no valid datetime format found')

def parseToUTC(dt_str, tz="UTC"):
  """
  convert dt_str with given timezone tz to dt str in UTC timezone
  Args:
    dt_str: datetime string
    tz(str): timezone for input tz, necessary when dt_str doesn't contain timezone info

  Returns:
    datetime string with UTC timezone

  """
  dt = parse(dt_str)
  utc = pytz.timezone("UTC")
  if dt.tzinfo == None: ## when timezone info is missing in dt_str
    input_tz = pytz.timezone(tz)
    dt = input_tz.localize(dt)
  new_dt = dt.astimezone(tz=utc)
  return new_dt.strftime(DATETIME_FORMAT_TZ)

def zdt_to_dt(zdt, target_tz="Australia/Sydney"):
  """
  converting datetime string with timezone info to target_tz
  Args:
    zdt(str): datetime string in "%Y-%m-%d %H:%M:%S%z" format
    target_tz(str): target timezone info

  Returns:
    datetime format
  """
  target_timezone = pytz.timezone(target_tz)
  dt = datetime.strptime(zdt, DATETIME_FORMAT_TZ)
  new_dt = dt.astimezone(tz=target_timezone)
  return new_dt

def zdt_to_dt_str(zdt, target_tz="Australia/Sydney"):
  """
  converting datetime string with timezone info to target_tz and output as string
  Args:
    zdt(str): datetime string in "%Y-%m-%d %H:%M:%S%z" format
    target_tz(str): target timezone info

  Returns:
    datetime string with new tz in "%Y-%m-%d %H:%M:%S" format

  """
  dt = zdt_to_dt(zdt, target_tz=target_tz)
  return dt.strftime(DATETIME_FORMAT)

def temporal_gap(t1, t2):
  """
  calculate gap betwee two time string
  Args:
    t1(str): datetime string 1
    t2(str): datetime string 2

  Returns:
    gap in second
  """
  t1 = t1 if isinstance(t1, datetime) else parse(t1)
  t2 = t2 if isinstance(t2, datetime) else parse(t2)
  gap = t2 - t1
  return gap.total_seconds()


def date_range(start: str, end: str, interval: int):
  """
  creating a list of date string from f to t with given interval
  Args:
    start(str): starting date
    end(str): ending date
    interval(int): num of days as gap

  Returns:
    list of date string

  """
  start_date = datetime.strptime(start, DATE_FORMAT)
  end_date = datetime.strptime(end, DATE_FORMAT)
  num_days = (end_date - start_date).days
  num_steps = int(num_days / interval) + 1
  for i in range(num_steps):
    yield (start_date + timedelta(days=i*interval)).strftime(DATE_FORMAT)

def temporal_range(start, end, interval):
  """
  creating a list of datetime from start to end with given interval
  Args:
    start(str|datetime):
    end(str|datetime):
    interval(int): interval in seconds

  Returns:
    list of datetime
  """
  current = start if isinstance(start, datetime) else parse(start)
  end = end if isinstance(end, datetime) else parse(end)
  while current < end:
    yield current
    current += timedelta(seconds=interval)
