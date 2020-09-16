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
def period(day=None, hour=None, minute=None):
    per = "P"
    if day is not None:
        per += str(day)+"D"
    if hour is not None or minute is not None:
        if hour is not None:
            per += "T"+str(hour)+"H"
            if minute is not None:
                per += str(minute)+"M"
        else:
            per += "T"+str(minute)+"M"
    return per
