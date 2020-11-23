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
   @last edit time: 23/11/20
"""
import unittest
from genomeapi.elements import Map

class TestMap(unittest.TestCase):
    def test_group_map(self):
        vmap = Map()
        res = vmap(dimension="dominant_mode", output_name="main_mode", show_nulls=True,
                    map={
                           'Public Transport': ['BUS','RAIL','SUBWAY','TRAM','FERRY'],
                           'Car': ['CAR'],
                           'Walk': ['WALK']
                           })
        expected = {
            'maps': [
                {
                    'type': 'group',
                    'dimension': 'dominant_mode',
                    'output_name': 'main_mode',
                    'show_nulls': True,
                    'map': {
                        'Public Transport': ['BUS', 'RAIL', 'SUBWAY', 'TRAM', 'FERRY'],
                        'Car': ['CAR'],
                        'Walk': ['WALK']
                    }
                }
            ]
        }
        self.assertEqual(res.to_dict(), expected)

    def test_simple_map(self):
        vmap = Map()
        res = vmap(dimension="agent_gender", output_name="gender", show_nulls=True,
                   typ='simple',
                   map={
                       "BOY": "M",
                       "GIRL": "F"
                   })
        expected = {
            'maps': [
                {
                    'type': 'simple',
                    'dimension': 'agent_gender',
                    'output_name': 'gender',
                    'show_nulls': True,
                    'map': {
                        'BOY': 'M',
                        'GIRL': 'F'
                    }
                }
            ]
        }
        self.assertEqual(res.to_dict(), expected)

    def test_range_map(self):
        vmap = Map()
        res = vmap(dimension="__time", output_name="timeperiod",show_nulls=True, typ="range", map={
                   "Morning": ["00","11"],
                   "Afternoon": ["12","23"],
                   "Full day": ["00","23"]
                 })
        expected = {
            'maps': [
                {
                    'type': 'range',
                    'dimension': '__time',
                    'output_name': 'timeperiod',
                    'show_nulls': True,
                    'map': {
                        "Morning": ["00", "11"],
                        "Afternoon": ["12", "23"],
                        "Full day": ["00", "23"]
                    }
                }
            ]
        }
        self.assertEqual(res.to_dict(), expected)