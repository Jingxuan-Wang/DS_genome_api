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
   This is basic operations for API query

   @author: jingxuan
   @maintainer: jingxuan
   @last editor: jingxuan
   @last edit time: 3/4/20
"""

import json
import requests
from requests.status_codes import codes
try:
  from pandas import json_normalize
except:
  from pandas.io.json import json_normalize

from genomeapi.elements import Dates, Aggregation, DimensionFacet, LogicFilter, ResponseException, APIException, RequestException, ExtractionFn
from genomeapi.elements import Granularity, Location, TimeSeriesReference

class BasicQuery:
  #_URLS = "https://apistore.dsparkanalytics.com.au"

  _API_ENDPOINT = {"discretevisit": "v2",
                   "staypoint": "v2",
                   "odmatrix": "v3",
                   "odthroughlink": "v1",
                   "linkmeta": "v1"}
  _AGG_MAPPER = {'unique_agents': 'hyperUnique', 'total_records': 'longSum'}

  def __init__(self, end_point:str, URL:str = "https://apistore.dsparkanalytics.com.au", token:str = "", proxies:dict = {}, version=None,):
    if version is not None:
      self._query_path = "/".join([URL, end_point, 'v' + version, 'query'])
    else:
      self._query_path = "/".join([URL, end_point, self._API_ENDPOINT[end_point], 'query'])

    self._token = token
    self._dt = None
    self._aggs = None
    self._ts_reference = None
    self._d_facets = None
    self._grant = None
    self._loc = None
    self._filt = None
    self._req = {}
    self._proxies = proxies
    self._d_facets_multitimeexfn = None

  def dates(self, begin_date: str, end_date: str = None):
    dt = Dates()
    self._dt = dt(begin_date, end_date=end_date)
    return self

  def aggregate(self, metric: str, described_as=None):
    agg = Aggregation()
    if metric not in self._AGG_MAPPER.keys():
      raise APIException("given metric is not supported by this api")
    typ = self._AGG_MAPPER[metric]
    if self._aggs is None:
      self._aggs = agg(metric=metric, typ=typ, described_as=described_as) ## assign self.aggs as Aggregations Object
    else:
      self._aggs += agg(metric=metric, typ=typ, described_as=described_as) ## adding other Aggregations Object to self.aggs
    return self

  def checkdimfacettyp(self, value):
    if isinstance(value, str):
      dfacet = DimensionFacet(typ="string")
      return dfacet(dimension=value)
    else:
      return value

  def dimension_facets(self, *dimension, output_name=None, value=None, extraction_fn=None, typ="string"):
    if len(dimension) == 1 and isinstance(dimension[0],list):
      dimension=dimension[0]
    else:
      dimension=list(dimension)

    dictdimensions = list(filter(None, list(map(lambda x: x if isinstance(x, dict) else None, dimension))))
    timedimensions = list(filter(None, map(lambda x: x if x["type"] == "extraction" and x["dimension"] == "__time" else None, dictdimensions)))
    if len(timedimensions) > 1:
      timeformats = "_____".join([d['extractionFn']["format"] for d in timedimensions])
      exfntimezone = [d['extractionFn']["timeZone"] for d in timedimensions][0]
      output_name = "_____".join([d['outputName'] for d in timedimensions])
      tempdfacet = DimensionFacet(typ="extraction")
      tempextraction = ExtractionFn("timeFormat")
      tempfacet = tempdfacet(dimension="__time", output_name=output_name, extraction_fn=tempextraction(format=timeformats, timezone=exfntimezone))
      nontimedimensions = [thisfacet for thisfacet in dimension if (isinstance(thisfacet, dict) and thisfacet['type'] == "extraction" and thisfacet["dimension"] == "__time") == False]
      dimension = nontimedimensions + [tempfacet]
      self._d_facets_multitimeexfn = output_name

    dfacet = DimensionFacet(typ=typ)
    dfacet(dimension=dimension, value=value, output_name=output_name, extraction_fn=extraction_fn)
    self._d_facets = dfacet.to_dict()
    return self

  def granularity(self, period, typ="period"):
    grant = Granularity()
    self._grant = grant(period, typ)
    return self

  def location(self, location_type, level_type, id, country="AU", direction=None):
    loc = Location(country=country)
    self._loc = loc(location_type, level_type, id, direction)
    return self

  def filter(self, filt):
    if isinstance(filt, LogicFilter):
      self._filt = filt.to_dict()
    elif isinstance(filt, dict):
      self._filt = filt
    return self

  def time_series_reference(self,v):
    ts = TimeSeriesReference()
    self._ts_reference = ts(v)
    return self

  def dumps(self):
    self._req.update(self._dt)
    self._req.update(self._aggs.to_dict())
    self._req.update(self._grant)

    if self._loc is not None:
      self._req.update(self._loc)

    if self._ts_reference is not None:
      self._req.update(self._ts_reference)

    if self._filt is not None:
      self._req.update(self._filt)

    if self._d_facets is not None:
      self._req.update(self._d_facets)

    self.json = json.dumps(self._req)

  def splitmultiexfnresult(self, elem):
    elem["event"].update(dict(zip(self._d_facets_multitimeexfn.split("_____"), elem["event"][self._d_facets_multitimeexfn].split("_____"))))
    elem["event"].pop(self._d_facets_multitimeexfn,None)
    return elem
    
  def request(self):
    if len(self._req) == 0:
      self.dumps()

    if len(self._proxies) > 0:
      response = requests.post(self._query_path,
                              data=self.json,
                              headers={
                               'Authorization': 'Bearer ' + self._token,
                                'Content-Type': 'application/json'
                              },
                               proxies=self._proxies)
    else:
      response = requests.post(self._query_path,
                               data=self.json,
                               headers={
                                 'Authorization': 'Bearer ' + self._token,
                                 'Content-Type': 'application/json'
                               })

    if response.status_code != codes['ok']:
      raise ResponseException(response)
    else:
      if len(response.json()) == 0:
        raise RequestException("API return is empty, please check your query, especially the date you are querying")
      else:
        if self._d_facets_multitimeexfn is None:
          return response.json()
        else:
          return list(map(self.splitmultiexfnresult, response.json()))


  def to_df(self, json_data):
    df = json_normalize(json_data)
    return df

  def clear_all(self):
    self._dt = None
    self._aggs = None
    self._ts_reference = None
    self._d_facets = None
    self._grant = None
    self._loc = None
    self._filt = None
    self._req = {}
    return self
