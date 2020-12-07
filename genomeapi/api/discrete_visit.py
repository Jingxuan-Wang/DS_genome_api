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
   This is operations for discrete visit related query

   @author: jingxuan
   @maintainer: jingxuan
   @last editor: jingxuan
   @last edit time: 3/4/20
"""

from .basic_query import BasicQuery


class DiscreteVisit(BasicQuery):
  
  def __init__(self, URL, token, proxies: dict={}, country="AU"):
    super().__init__(end_point='discretevisit', URL=URL,token=token, proxies=proxies, country=country)

