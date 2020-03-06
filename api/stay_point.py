__author__ = 'jingxuan'

from .basic_query import BasicQuery

import json

class StayPoint(BasicQuery):
  def __init__(self, token):
    super().__init__(end_point='staypoint', token=token)

