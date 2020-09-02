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
from genomeapi.elements import BoundingBox
from genomeapi.elements.exceptions import APIException

class TestBoundingBox(unittest.TestCase):
    def test_bounding_box(self):
        bounding_box = BoundingBox()
        res = bounding_box(max_coords=[150.835569, -34.238692], min_coords=[150.832936,-34.239866])
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
        self.assertEqual(res, expected)

    def test_bounding_box_error(self):
        bbox = BoundingBox()
        with self.assertRaises(APIException) as context:
            bbox(max_coords=105, min_coords=105)
        self.assertTrue("max_coords|min_coords only take list as input format", str(context.exception))

if __name__ == '__main__':
    unittest.main()