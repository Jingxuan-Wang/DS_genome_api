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
##TODO - in json, what is the format for boolean.

from .element import Element
from .exceptions import APIException

class BasicMap(Element):
    _value = None
    def __init__(self):
        pass

    def __add__(self, other):
        self._value = self._value + other._value
        return self

    def map(self, **kwargs):
        self._map = self.form_obj(**kwargs)
        return self

    def to_dict(self):
        return self.form_obj(maps=self._value)

class SimpleMap(BasicMap):
    def __call__(self, dimension: str = None, output_name: str = None, show_nulls=False, extraction_fn=None):
        if dimension is None:
            raise APIException("")
        elif output_name is None:
            raise APIException("Please provide a name for this map")
        elif map is None:
            raise APIException("A map for the values must be provided")
        else:
            if extraction_fn is None:
                self._value = [self.form_obj(type="simple", dimension=dimension, output_name=output_name,
                                            show_nulls=show_nulls, map=self._map)]
            else:
                self._value = [self.form_obj(type="simple", dimension=dimension, output_name=output_name,
                                            show_nulls=show_nulls, map=self._map, extractionFn=extraction_fn)]

        return self


class GroupMap(BasicMap):
    def __call__(self, dimension: str = None, output_name: str = None, show_nulls=False, extraction_fn=None):
        if dimension is None:
            raise APIException("")
        elif output_name is None:
            raise APIException("Please provide a name for this map")
        elif map is None:
            raise APIException("A map for the values must be provided")
        else:
            if extraction_fn is None:
                self._value = [self.form_obj(type="group", dimension=dimension, output_name=output_name,
                                            show_nulls=show_nulls, map=self._map)]
            else:
                self._value = [self.form_obj(type="group", dimension=dimension, output_name=output_name,
                                            show_nulls=show_nulls, map=self._map, extractionFn=extraction_fn)]
        return self

class RangeMap(BasicMap):
    def __call__(self, dimension: str = None, output_name: str = None, show_nulls=False, extraction_fn=None):
        if dimension is None:
            raise APIException("")
        elif output_name is None:
            raise APIException("Please provide a name for this map")
        elif map is None:
            raise APIException("A map for the values must be provided")
        else:
            if extraction_fn is None:
                self._value = [self.form_obj(type="range", dimension=dimension, output_name=output_name,
                                            show_nulls=show_nulls, map=self._map)]
            else:
                self._value = [self.form_obj(type="range", dimension=dimension, output_name=output_name,
                                            show_nulls=show_nulls, map=self._map, extractionFn=extraction_fn)]
        return self

class ValueMap:
    fns = {'simple': SimpleMap, 'group': GroupMap, 'range': RangeMap}
    def __new__(cls, typ='group'):
        cls.typ = typ
        if typ in cls.fns.keys():
            return cls.fns[typ]()
        else:
            raise APIException("Map type not recognised")
