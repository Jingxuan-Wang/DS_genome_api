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
   @last edit time: 23/7/20
"""

import unittest
from genomeapi.api import LinkMeta
from genomeapi.elements import Filter
import json

class TestLinkMeta(unittest.TestCase):
    def test_link_meta_with_filter1(self):
        filter = Filter()
        link_meta = LinkMeta("URL","token")
        link_meta.filter(filter.selector(dimension="link_id", value="NSW513133313"))
        link_meta.dumps()
        expected = {
        "filter": {
            "type": "selector",
            "dimension": "link_id",
            "value": "NSW513133313"
            }
        }
        self.assertEqual(json.loads(link_meta.json), expected)

    def test_link_meta_with_filter2(self):
        filter = Filter()
        link_meta = LinkMeta("URL","token")
        link_meta.filter(filter.selector(dimension="link_name", value="Elizabeth Street"))
        link_meta.dumps()
        expected = {
            "filter": {
                "type": "selector",
                "dimension": "link_name",
                "value": "Elizabeth Street"
            }
        }
        self.assertEqual(json.loads(link_meta.json), expected)

    def test_link_meat_with_bbox(self):
        link_meta = LinkMeta("URL", "token")
        link_meta.bbox(max_coords=[150.835569, -34.238692], min_coords=[150.832936, -34.239866])
        link_meta.dumps()
        expected = {
            "boundingBox": {
                "maxCoords": [
                    150.835569,
                    -34.238692
                ],
                "minCoords": [
                    150.832936,
                    -34.239866
                ]
            }
        }
        self.assertEqual(json.loads(link_meta.json), expected)


if __name__ == '__main__':
    unittest.main()
