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
   @last edit time: 21/11/20
"""
import unittest
from genomeapi.elements import ValueMap, BasicMap

class TestMaps(unittest.TestCase):
    def test_map_function(self):
        maps = ValueMap("group")
        res = maps.map(public_transport = ["BUS", "TRAM", "FERRY", "SUBWAY", "TRAIN"])
        expected = {
            'public_transport': [
                "BUS",
                "TRAM",
                "FERRY",
                "SUBWAY",
                "TRAIN"
            ]
        }
        self.assertTrue(isinstance(maps, BasicMap))
        self.assertEqual(res._map, expected)

    def test_range_map(self):
        range_map = ValueMap("range")
        range_map.map(Morning=["00", "11"], Afternoon=["12","23"], Full_Day=["00", "23"])
        res = range_map(dimension="__time", output_name="timeperiod", show_nulls=True)
        expected = \
            {'maps':[
                {'type': 'range',
                'dimension': '__time',
                'output_name': 'timeperiod',
                'show_nulls': True,
                'map': {
                    'Morning': ['00', '11'],
                    'Afternoon': ['12', '23'],
                    'Full_Day': ['00', '23']
                    }
                }
        ]}
        self.assertEqual(res.to_dict(), expected)

    ## if show_nulls is not given, do we need to show in the output
    def test_simple_map(self):
        simple_map = ValueMap("simple")
        simple_map.map(BOY="M", GIRL="F")
        res = simple_map(dimension="agent_gender", output_name="gender")

        expected = \
        {
            'maps':[{
                "dimension": "agent_gender",
                "output_name": "gender",
                'show_nulls': False,
                'type': 'simple',
                'map': {
                    'BOY': 'M',
                    'GIRL': 'F'
                }
            }]
        }

        self.assertEqual(res.to_dict(), expected)

    def test_group_map(self):
        group_map = ValueMap("group")
        group_map.map(public_transport=["BUS", "TRAM", "FERRY"])
        res = group_map(dimension="dominant_mode", output_name="transport")
        expected = \
            {
                "maps": [
                    {
                        "type": "group",
                        "dimension": "dominant_mode",
                        "output_name": "transport",
                        "show_nulls": False,
                        "map": {
                            'public_transport': [
                                "BUS",
                                "TRAM",
                                "FERRY"
                            ]
                        }
                    }
                ]
            }

        self.assertEqual(res.to_dict(), expected)

    def test_multiple_maps(self):
        simple_map = ValueMap("simple")
        simple_map.map(BOY="M", GIRL="F")
        map1 = simple_map(dimension="agent_gender", output_name="gender")
        group_map = ValueMap("group")
        group_map.map(public_transport=["BUS", "TRAM", "FERRY"])
        map2 = group_map(dimension="dominant_mode", output_name="transport")

        res = map1 + map2
        expected = {
            'maps':[
                {
                "dimension": "agent_gender",
                "output_name": "gender",
                'show_nulls': False,
                'type': 'simple',
                'map': {
                    'BOY': 'M',
                    'GIRL': 'F'
                }},
                {
                "type": "group",
                "dimension": "dominant_mode",
                "output_name": "transport",
                "show_nulls": False,
                "map": {
                    'public_transport': [
                        "BUS",
                        "TRAM",
                        "FERRY"
                    ]
                }}
            ]
        }
        self.assertEqual(res.to_dict(), expected)


