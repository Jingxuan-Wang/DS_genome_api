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

   @author: jingxuan
   @maintainer: jingxuan
   @last editor: jingxuan
   @last edit time: 3/4/20
"""

from .element import Element
from .exceptions import APIException

class Location(Element):
    _LOCATION_TYPES = ['locationHierarchyLevel']
    _LEVEL_TYPES = []
    def __init__(self, country="AU"):
        if country == "SG":
            self._LEVEL_TYPES = ['staypoint_subzone', 'staypoint_planningarea',
                                 'staypoint_planningregion', 'building']
        elif country == "AU":
            self._LEVEL_TYPES = ['sa2', 'sa3', 'sa4', 'gcc', 'state', 'building', 'gcc', 'poa']


    def validating(self, location_type, level_type):
        if location_type not in self._LOCATION_TYPES:
            raise APIException("Sorry, we don't support this location type for now")
        elif level_type.replace("origin_", "").replace("destination_", "") not in self._LEVEL_TYPES:
            raise APIException("Sorry, we don't have such type for location")
        else:
            pass

    def __call__(self, location_type, level_type, id, direction=None):
        level_type = level_type if direction is None else direction+"_"+level_type
        self.validating(location_type, level_type)
        value = self.form_obj(locationType=location_type, levelType=level_type, id=id)
        return self.form_obj(location=value)