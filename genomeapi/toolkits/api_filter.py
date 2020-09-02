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
   This is for

   @author: jingxuan
   @maintainer: jingxuan
   @last editor: jingxuan
   @last edit time: 2/9/20
"""
from datetime import datetime, timedelta
import pytz
from functools import reduce
import operator
from genomeapi.elements import Filter
from genomeapi.toolkits.time_common import parse, temporal_range, DATETIME_FORMAT_TZ2

def api_filter_during(start, end, tz, min_duration = 5, starting_within_hr = 24):
    """
    constructing a combination of filters that can be used to detect who is staying in a period of time,
    which is a common task related to StayPoint API
    Args:
        start(str): starting timestamp
        end(str): ending timestamp
        tz(str): local timezone
        min_duration(int):
        starting_within_hr(int):

    Returns:
        filter object
    """
    filter = Filter()
    local_tz = pytz.timezone(tz)
    start_fmt = parse(start)
    end_fmt = parse(end)
    assert start_fmt < end_fmt, "start time greater than end time"
    assert start_fmt + timedelta(minutes=min_duration) < end_fmt, "start time greater than end time"
    assert starting_within_hr > 0, "starting within hour has to be greater than 0"
    assert min_duration >= 5, "min_duration has to be greater than 5"
    # generate increments
    last_start = end_fmt - timedelta(minutes=min_duration)
    first_start = start_fmt - timedelta(hours=starting_within_hr)
    # all times between of 15 minute intervals
    starts = [dt for dt in temporal_range(first_start, last_start, 15*60)]
    ends = list(map(lambda x: x + timedelta(minutes=15) - timedelta(seconds=1), starts))
    starts_final = list(map(lambda x: local_tz.localize(x).strftime(DATETIME_FORMAT_TZ2), starts))
    end_final = list(map(lambda x: local_tz.localize(x).strftime(DATETIME_FORMAT_TZ2), ends))
    # durations required for each interval
    #  - start - individual period starts
    #  - must be non-negative
    #  - add min duration
    durations_tmp = list(map(lambda x: int((start_fmt - x).total_seconds() / 60), starts))
    durations = [(0 + min_duration) if i <= 0 else (i + min_duration) for i in durations_tmp]
    # create time intervals
    intervals = [i + '/' + j for i, j in zip(starts_final, end_final)]
    # convert to filters
    interval_filters = list(map(lambda x: filter.interval(x, dimension='__time'), intervals))
    # create duration filters
    duration_filters = list(map(lambda x: filter.bound(dimension="duration", lower=x, ordering="numeric"), durations))
    # zip with AND logic, then combine all with OR logic
    filters = [i & j for i, j in zip(interval_filters, duration_filters)]
    combine_filters = reduce(operator.or_, filters)
    return combine_filters