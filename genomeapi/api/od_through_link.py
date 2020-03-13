__author__ = 'jingxuan'

from .basic_query import BasicQuery
from genomeapi.elements import Link

import json


class ODThroughLink(BasicQuery):
  def __init__(self, token):
    super().__init__(end_point='odthroughlink', token=token)
    self._link = None

  def link(self, *links):
    lin = Link()
    self._link = lin(*links)
    return self

  def dumps(self):
    self._req.update(self._dt)
    self._req.update(self._aggs.to_dict())
    self._req.update(self._grant)
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


