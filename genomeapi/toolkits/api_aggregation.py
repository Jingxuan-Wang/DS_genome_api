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
   This is for

   @author: jingxuan
   @maintainer: jingxuan
   @last editor: jingxuan
   @last edit time: 16/9/20
"""
from genomeapi.api import *
from genomeapi.elements import APIException

def match_aggregate_type(obj, metric):
  if isinstance(obj, DiscreteVisit):
    obj_type = "DiscreteVisit"
    mapper = {'unique_agents': 'hyperUnique', 'total_records': 'longSum'}
  elif isinstance(obj, ODMatrix):
    obj_type = "ODMatrix"
    mapper = {'unique_agents': 'hyperUnique', 'sum_duration': 'longSum', 'sum_distance': 'longSum', 'total_records': 'longSum'}
  elif isinstance(obj, ODThroughLink):
    obj_type = "ODThroughLink"
    mapper = {'unique_agents': 'hyperUnique', 'sum_duration': 'longSum', 'total_records': 'longSum'}
  elif isinstance(obj, StayPoint):
    obj_type = "StayPoint"
    mapper = {'unique_agents': 'hyperUnique', 'sum_stay_duration': 'longSum', 'total_stays': 'longSum'}

  if metric not in mapper.keys():
    raise APIException("given metric is not supported by %s API"%(obj_type))
  else:
    return mapper[metric]
