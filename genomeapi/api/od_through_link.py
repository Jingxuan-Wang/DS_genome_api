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
   This is operations for od through link related query

   @author: jingxuan
   @maintainer: jingxuan
   @last editor: jingxuan
   @last edit time: 3/4/20
"""

import json

from .basic_query import BasicQuery
from genomeapi.elements import Link



class ODThroughLink(BasicQuery):
  def __init__(self, URL, token):
    super().__init__(end_point='odthroughlink', URL=URL, token=token)
    self._link = None

  def link(self, *links):
    lin = Link()
    self._link = lin(*links)
    return self

  def dumps(self):
    self._req.update(self._dt)
    self._req.update(self._aggs.to_dict())
    self._req.update(self._grant)
    if self._link is not None:
      self._req.update(self._link)

    if self._loc is not None:
      self._req.update(self._loc)

    if self._ts_reference is not None:
      self._req.update(self._ts_reference)

    if self._filt is not None:
      self._req.update(self._filt)

    if self._d_facets is not None:
      self._req.update(self._d_facets)

    self.json = json.dumps(self._req)


