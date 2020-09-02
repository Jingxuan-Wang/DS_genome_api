#  Copyright © DataSpark Pte Ltd 2014 - 2020.
#
#  This software and any related documentation contain confidential and proprietary information of
#  DataSpark and its licensors (if any). Use of this software and any related documentation is
#  governed by the terms of your written agreement with DataSpark. You may not use, download or
#  install this software or any related documentation without obtaining an appropriate licence
#  agreement from DataSpark.
#
#  All rights reserved.
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
import unittest
from genomeapi.toolkits.time_common import *
from datetime import datetime
import pytz

class TimeCommonTest(unittest.TestCase):
    def test_parse(self):
        dt_str1 = "2020-08-01 00:00:01"
        dt_str2 = "2020-08-01 00:00:01+1000"
        timezone = "Australia/Sydney"
        res1 = parse(dt_str1) # datetime string without timezone
        res2 = parse(dt_str1, tz=timezone) # adding timezone when parsing
        res3 = parse(dt_str2) # datetime string with timezone
        expected1 = datetime.strptime(dt_str1, DATETIME_FORMAT)
        expected2 = pytz.timezone(timezone).localize(datetime.strptime(dt_str1, DATETIME_FORMAT))
        time_diff = (res3 - expected2).total_seconds()
        self.assertEqual(res1, expected1)
        self.assertEqual(res2, expected2)
        self.assertEqual(time_diff, 0)

    def test_parseToUTC(self):
        dt_str = "2020-08-01 00:00:01"
        res = parseToUTC(dt_str, tz="Australia/Sydney")
        expected = "2020-07-31 14:00:01+0000"
        self.assertEqual(res, expected)

    def test_zdt_to_dt(self):
        zdt_str = "2020-07-31 14:00:01+0000"
        res = zdt_to_dt(zdt_str, target_tz="Australia/Sydney")
        expected = datetime.strptime("2020-08-01 00:00:01+1000", DATETIME_FORMAT_TZ)
        self.assertEqual(res, expected)

    def test_zdt_to_dt_str(self):
        zdt_str = "2020-07-31 14:00:01+0000"
        res = zdt_to_dt_str(zdt_str, target_tz="Australia/Sydney")
        expected = "2020-08-01 00:00:01"
        self.assertEqual(res, expected)

    def test_temporal_gap(self):
        dt_str1 = "2020-08-01 00:00:01"
        dt_str2 = "2020-08-01 00:00:03"
        dt1 = parse(dt_str1)
        dt2 = parse(dt_str2)
        res1 = temporal_gap(dt_str1, dt_str2) # input as string
        res2 = temporal_gap(dt1, dt2) # input as datetime
        expected1 = 2
        self.assertEqual(res1, expected1)
        self.assertEqual(res2, expected1)

    def test_date_range(self):
        res = date_range("2020-10-01", "2020-10-03", 1)
        expected = ["2020-10-01", "2020-10-02", "2020-10-03"]
        self.assertEqual(list(res), expected)

    def test_temporal_range(self):
        res = temporal_range("2020-10-01 00:00:00", "2020-10-01 00:00:05", interval=1)
        expected = parse("2020-10-01 00:00:01")
        self.assertEqual(list(res)[1], expected)
