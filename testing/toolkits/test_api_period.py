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
   @last edit time: 16/9/20
"""
import unittest
from genomeapi.toolkits.api_period import *

class APIPeriodTest(unittest.TestCase):
    def test_period_day(self):
        res = period(day=1)
        expected = "P1D"
        self.assertEqual(res, expected)

    def test_period_hour(self):
        res = period(hour=1)
        expected = "PT1H"
        self.assertEqual(res, expected)

    def test_period_min(self):
        res = period(minute=15)
        expected = "PT15M"
        self.assertEqual(res, expected)

    def test_period_mix1(self):
        res = period(day=1, hour=2, minute=15)
        expected = "P1DT2H15M"
        self.assertEqual(res, expected)

    def test_period_mix2(self):
        res = period(day=1, minute=15)
        expected = "P1DT15M"
        self.assertEqual(res, expected)
