__author__ = 'jingxuan'
from genome_api.elements import Dates, Aggregation, DimensionFacet, LogicFilter, RequestException
from genome_api.elements import Granularity, Location, TimeSeriesReference

import json
import requests
from requests.status_codes import codes
from pandas import json_normalize

class BasicQuery:
  _URLS = "https://apistore.dsparkanalytics.com.au"
  _API_ENDPOINT = {"discretevisit": "v2",
                   "staypoint": "v2",
                   "odmatrix": "v3",
                   "odthroughlink": "v1",
                   "linkmeta": "v1"}
  def __init__(self, end_point:str, token:str = ""):
    self.query_path = "/".join([self._URLS, end_point, self._API_ENDPOINT[end_point], 'query'])
    self.token = token
    self.dt = None
    self.aggs = None
    self.ts_reference = None
    self.d_facets = None
    self.grant = None
    self.loc = None
    self.filt = None
    self.req = {}

  def dates(self, begin_date: str, end_date: str = None):
    dt = Dates()
    self.dt = dt(begin_date, end_date=end_date)
    return self

  def aggregate(self, metric: str, typ: str, described_as=None):
    agg = Aggregation()
    if self.aggs is None:
      self.aggs = agg(metric=metric, typ=typ, described_as=described_as) ## assign self.aggs as Aggregations Object
    else:
      self.aggs += agg(metric=metric, typ=typ, described_as=described_as) ## adding other Aggregations Object to self.aggs
    return self

  def dimension_facets(self, *dimension, output_name=None, typ="String"):
    d_facets = DimensionFacet()
    self.d_facets = d_facets(*dimension, output_name=output_name, typ=typ)
    return self

  def granularity(self, period, typ="period"):
    grant = Granularity()
    self.grant = grant(period, typ)
    return self

  def location(self, location_type, level_type, id, country="AU"):
    loc = Location(country=country)
    self.loc = loc(location_type, level_type, id)
    return self

  def filter(self, filt):
    if isinstance(filt, LogicFilter):
      self.filt = filt.to_dict()
    elif isinstance(filt, dict):
      self.filt = filt
    return self

  def time_series_reference(self,v):
    ts = TimeSeriesReference()
    self.ts_reference = ts(v)
    return self

  def dumps(self):
    self.req.update(self.dt)
    self.req.update(self.aggs.to_dict())
    self.req.update(self.grant)

    if self.loc is not None:
      self.req.update(self.loc)

    if self.ts_reference is not None:
      self.req.update(self.ts_reference)

    if self.filt is not None:
      print("filter")
      self.req.update(self.filt)

    if self.d_facets is not None:
      self.req.update(self.d_facets)

    self.json = json.dumps(self.req)
    
  def request(self, method:str="POST"):
    if len(self.req) == 0:
      self.dumps()
    if method == "POST":
      response = requests.post(self.query_path,
                              data=self.json,
                              headers={
                               'Authorization': 'Bearer '+ self.token,
                                'Content-Type': 'application/json'
                              })
    if method == "GET":
      response = requests.post(self.query_path,
                              data=self.json,
                              headers={
                                'Authorization': 'Bearer '+ self.token,
                                'Content-Type': 'application/json'
                              })

    if response.status_code != codes['ok']:
      raise RequestException(response)
    else:
      return response.json()

  def to_df(self, json_data):
    df = json_normalize(json_data)
    return df

  def clear_all(self):
    self.dt = None
    self.aggs = None
    self.ts_reference = None
    self.d_facets = None
    self.grant = None
    self.loc = None
    self.filt = None
    self.req = {}
    return self
