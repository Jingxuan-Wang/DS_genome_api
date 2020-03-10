__author__ = 'jingxuan'

from .basic_query import BasicQuery


class StayPoint(BasicQuery):
  def __init__(self, token):
    super().__init__(end_point='staypoint', token=token)

