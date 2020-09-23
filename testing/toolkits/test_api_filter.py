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
import unittest
from genomeapi.toolkits.api_filter import *

class APIFilterTest(unittest.TestCase):
    def test_api_filter_during(self):
        filters = api_filter_during(start = "2020-03-02 09:00:00", end = "2020-03-02 10:00:00",\
                                           min_duration = 30, starting_within_hr = 1, tz="Australia/Brisbane")
        expected = [{'fields': [{'dimension': '__time', 'intervals': ['2020-03-02T08:00:00+1000/2020-03-02T08:14:59+1000'], 'type': 'interval'}, {'dimension': 'duration', 'lower': 90, 'ordering': 'numeric', 'type': 'bound'}], 'type': 'and'}, {'fields': [{'dimension': '__time', 'intervals': ['2020-03-02T08:15:00+1000/2020-03-02T08:29:59+1000'], 'type': 'interval'}, {'dimension': 'duration', 'lower': 75, 'ordering': 'numeric', 'type': 'bound'}], 'type': 'and'}, {'fields': [{'dimension': '__time', 'intervals': ['2020-03-02T08:30:00+1000/2020-03-02T08:44:59+1000'], 'type': 'interval'}, {'dimension': 'duration', 'lower': 60, 'ordering': 'numeric', 'type': 'bound'}], 'type': 'and'}, {'fields': [{'dimension': '__time', 'intervals': ['2020-03-02T08:45:00+1000/2020-03-02T08:59:59+1000'], 'type': 'interval'}, {'dimension': 'duration', 'lower': 45, 'ordering': 'numeric', 'type': 'bound'}], 'type': 'and'}, {'fields': [{'dimension': '__time', 'intervals': ['2020-03-02T09:00:00+1000/2020-03-02T09:14:59+1000'], 'type': 'interval'}, {'dimension': 'duration', 'lower': 30, 'ordering': 'numeric', 'type': 'bound'}], 'type': 'and'}, {'fields': [{'dimension': '__time', 'intervals': ['2020-03-02T09:15:00+1000/2020-03-02T09:29:59+1000'], 'type': 'interval'}, {'dimension': 'duration', 'lower': 30, 'ordering': 'numeric', 'type': 'bound'}], 'type': 'and'}]
        self.assertEqual(filters.to_dict()['filter']['fields'], expected)



