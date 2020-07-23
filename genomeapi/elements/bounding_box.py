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
   This is for link meta api

   @author: jingxuan
   @maintainer: jingxuan
   @last editor: jingxuan
   @last edit time: 23/7/20
"""

from .element import Element
from .exceptions import APIException

class BoundingBox(Element):
    def validating(self, max_coords, min_coords):
        if not isinstance(max_coords, list) or not isinstance(min_coords, list):
            raise APIException("max_coords|min_coords only take list as input format")

    def __call__(self, max_coords, min_coords):
        self.validating(max_coords=max_coords,min_coords=min_coords)
        value = self.form_obj(maxCoords=max_coords, minCoords=min_coords)
        return self.form_obj(boundingBox=value)
