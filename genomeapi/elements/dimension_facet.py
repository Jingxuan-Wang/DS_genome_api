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
   This is basic operations for dimension facet query

   @author: jingxuan
   @maintainer: jingxuan
   @last editor: jingxuan
   @last edit time: 3/4/20
"""

from .element import Element
from .exceptions import APIException

class StringDimensionFacets(Element):
  def __call__(self, dimension=None, output_name=None, value=None, extraction_fn=None):
    if isinstance(dimension, str):
      return self.form_obj(dimensionFacets=[dimension])
    elif isinstance(dimension, list):
      v = dimension
      return self.form_obj(dimensionFacets=v)

class DefaultDimensionFacets(Element):
  def __call__(self, dimension=None, output_name=None, value=None, extraction_fn=None):
    if output_name:
      value = self.form_obj(dimension=dimension, outputName=output_name, type="default")
      return self.form_obj(dimensionFacets=[value])
    else:
      value = self.form_obj(dimension=dimension, type="default")
      return self.form_obj(dimensionFacets=[value])

class ExtractionDimensionFacets(Element):
  def __call__(self, dimension=None, output_name=None, value=None, extraction_fn=None):
    if extraction_fn is None:
      raise APIException("please set value to extraction_fn")

    if extraction_fn['type'] == 'timeFormat':
      if dimension != "__time":
        raise APIException("Time extraction must use '__time' as dimension")
      if output_name is None:
        raise APIException("Time extraction must have output_name attribute")
      value = self.form_obj(dimension=dimension, type="extraction", outputName=output_name,extractionFn=extraction_fn)
    elif output_name == None:
      value = self.form_obj(dimension=dimension, type="extraction", extractionFn=extraction_fn)
    else:
      value = self.form_obj(dimension=dimension, type="extraction", outputName=output_name, extractionFn=extraction_fn)
    return self.form_obj(dimensionFacets=[value])

class ListFilteredDimensionFacets(Element):
  def __call__(self, dimension=None, output_name=None, value=None, extraction_fn=None):
    delegate = self.form_obj(dimension=dimension, outputName=output_name, type='default')
    value = self.form_obj(delegate=delegate, dimension=dimension, values=value, type="listFiltered")
    return self.form_obj(dimensionFacets=[value])


class DimensionFacet:
  facets = {'string': StringDimensionFacets, 'default': DefaultDimensionFacets, 'list_filtered': ListFilteredDimensionFacets, 'extraction': ExtractionDimensionFacets}

  def __new__(cls, typ='default'):
    cls.typ = typ
    if typ in cls.facets.keys():
      return cls.facets[typ]()
    else:
      raise APIException("input type not recognized")