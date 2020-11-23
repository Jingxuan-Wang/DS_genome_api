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
   This is basic operations for location

   @author: richard
   @maintainer: richard
   @last editor: richard
   @last edit time: 2020-11-18
"""

from .element import Element
from .exceptions import APIException

class BasicMap(Element):
    _value = None
    _types = ['group', 'simple', 'range']
    _map = None
    def __call__(self, dimension, output_name, map:dict = None, show_nulls=False, extraction_fn=None, typ="group"):
        if map is None and self._map is None:
            raise APIException("A map for the values must be provided, or map function need to executed")
        elif typ not in self._types:
            raise APIException("% is not allowed"%(typ))
        else:
            _map = self._map if self._map is not None else map
            if extraction_fn is None:
                self._value = self.form_obj(type=typ, dimension=dimension, output_name=output_name,
                                            show_nulls=show_nulls, map=_map)
            else:
                self._value = self.form_obj(type=typ, dimension=dimension, output_name=output_name,
                                            show_nulls=show_nulls, map=_map, extractionFn=extraction_fn)
        return self

    def map(self, **kwargs):
        self._map = self.form_obj(**kwargs)

    def to_dict(self):
        if isinstance(self._value, dict):
            return self.form_obj(maps=[self._value])
        elif isinstance(self._value, list):
            return self.form_obj(maps=self._value)


class Map:
    def __init__(self):
        pass

    def __call__(self, dimension, output_name, map:dict = None, show_nulls=False, extraction_fn=None, typ="group"):
        m = BasicMap()
        m(dimension=dimension, output_name=output_name, map=map, show_nulls=show_nulls, extraction_fn=extraction_fn, typ=typ)
        return m
