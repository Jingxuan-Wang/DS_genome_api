__author__ = 'jingxuan'

from .element import Element
from .exceptions import APIException
from .extraction_fn import ExtractionFn

class StringDimensionFacets(Element):
  def __call__(self, *dimensions):
    if len(dimensions) == 1:
      return self.form_obj(dimensionFacets=dimensions[0])
    else:
      v = list(dimensions)
      return self.form_obj(dimensionFacets=v)

class DefaultDimensionFacets(Element):
  def __call__(self, dimension=None, output_name=None):
    if output_name:
      value = self.form_obj(dimension=dimension, outputName=output_name, type="default")
      return self.form_obj(dimensionFacets=[value])
    else:
      value = self.form_obj(dimension=dimension, type="default")
      return self.form_obj(dimensionFacets=[value])

class ExtractionDimensionFacets(Element):
  def __call__(self, dimension:str,  extraction_fn, output_name=None):
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
  def __call__(self, dimension=None, output_name=None, values=None):
    delegate = self.form_obj(dimension=dimension, outputName=output_name, type='default')
    value = self.form_obj(delegate=delegate, dimension=dimension, values=values, type="listFiltered")
    return self.form_obj(dimensionFacets=[value])


class DimensionFacet:
  facets = {'string': StringDimensionFacets, 'default': DefaultDimensionFacets, 'list_filtered': ListFilteredDimensionFacets, 'extraction': ExtractionDimensionFacets}

  def __new__(cls, typ='default'):
    cls.typ = typ
    if typ in cls.facets.keys():
      return cls.facets[typ]()
    else:
      raise APIException("input type not recognized")