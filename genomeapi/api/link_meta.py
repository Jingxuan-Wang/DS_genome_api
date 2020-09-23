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
   This is operations for link meta related query

   @author: jingxuan
   @maintainer: jingxuan
   @last editor: jingxuan
   @last edit time: 3/4/20
"""

from .basic_query import BasicQuery
from genomeapi.elements import BoundingBox
from genomeapi.elements import APIException
import json


class LinkMeta(BasicQuery):
  def __init__(self, URL, token, proxies: dict={}, version: str = None):
    super().__init__(end_point='linkmeta', URL=URL, token=token,version = version, proxies=proxies)
    self._bbox = None

  def bbox(self, max_coords, min_coords):
    bounding_box = BoundingBox()
    self._bbox = bounding_box(max_coords=max_coords, min_coords=min_coords)
    return self

  def dumps(self):
    if self._filt is not None:
      self._req.update(self._filt)
    elif self._bbox is not None:
      self._req.update(self._bbox)
    else:
      raise APIException("For link meta api, must specify either filter or bounding box")

    self.json = json.dumps(self._req)
