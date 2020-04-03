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
   This is for all exceptions

   @author: jingxuan
   @maintainer: jingxuan
   @last editor: jingxuan
   @last edit time: 3/4/20
"""

class APIException(Exception):
  def __init__(self, exp):
    super().__init__("APIException: {}".format(exp))

class RequestException(Exception):
  def __init__(self, exp):
    super().__init__(
      "RequestException: {}".format(exp)
    )

class ResponseException(Exception):
  def __init__(self, response):
    super().__init__(
      "ResponseException: {} with error code {}".format(response.text, response.status_code)
    )