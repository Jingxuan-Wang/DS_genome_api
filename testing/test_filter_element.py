__author__ = 'jingxuan'

import unittest
from genomeapi.elements.filter import Filter
from genomeapi.elements.extraction_fn import ExtractionFn
from functools import reduce

class TestFilter(unittest.TestCase):
  def test_selector(self):
    selector = Filter()
    res = selector.selector(dimension='agent_gender', value='M')
    expected = {
      'filter':{
        'type': 'selector',
        'dimension': 'agent_gender',
        'value': 'M'
      }
    }
    self.assertEqual(res.to_dict(), expected)

  def test_in_filter(self):
    filter = Filter()
    res = filter.in_filter("A", "B", "C", dimension='links')
    expected = {
      'filter': {
        'type': 'in',
        'dimension': 'links',
        'values': ['A', 'B', 'C']
      }
    }
    self.assertEqual(res.to_dict(), expected)

  def test_bound(self):
    filter = Filter()
    res = filter.bound(dimension='duration', lower=60, upper=180, ordering='numeric')
    expected = {
      "filter": {
        "type": "bound",
        "dimension": "duration",
        "lower": 60,
        "upper": 180,
        "ordering": "numeric"
      }
    }
    self.assertEqual(res.to_dict(), expected)

  def test_interval(self):
    filter = Filter()
    res = filter.interval(
      "2019-08-01T16:00:00.000+10/2019-08-01T18:59:59.999+10",
      "2019-08-02T18:00:00.000+10/2019-08-02T20:59:59.999+10",
      dimension='__time')
    expected = {
      "filter": {
        "type": "interval",
        "dimension": "__time",
        "intervals": [
          "2019-08-01T16:00:00.000+10/2019-08-01T18:59:59.999+10",
          "2019-08-02T18:00:00.000+10/2019-08-02T20:59:59.999+10"
        ]
      }
    }
    self.assertEqual(res.to_dict(), expected)

  def test_like(self):
    filter = Filter()
    res = filter.like(dimension='origin_building', pattern='%MALL%')
    expected = {
      "filter": {
        "type": "like",
        "dimension": "origin_building",
        "pattern": "%MALL%"
      }
    }
    self.assertEqual(res.to_dict(), expected)

  def test_reg(self):
    filter = Filter()
    res = filter.reg(dimension='parent_station', pattern='NSWPTPST1[1-4]00')
    expected = {
      "filter": {
        "type": "regex",
        "dimension": "parent_station",
        "pattern": "NSWPTPST1[1-4]00"
      }
    }
    self.assertEqual(res.to_dict(), expected)

  def test_and_logic(self):
    filter = Filter()
    res = filter.selector(dimension='agent_gender', value='M') & filter.selector(dimension='agent_home_state', value='1') & filter.bound(dimension='agent_year_of_birth', lower=1969, ordering='numeric')

    expected = {
      "filter": {
        "type": "and",
        "fields": [{
          "type": "selector",
          "dimension": "agent_gender",
          "value": "M"
        },
        {
          "type": "selector",
          "dimension": "agent_home_state",
          "value": "1"
        },
        {
          "type": "bound",
          "dimension": "agent_year_of_birth",
          "lower": 1969,
          "ordering": "numeric"
        }]
      }
    }
    self.assertEqual(res.to_dict(), expected)

  def test_or_logic(self):
    filter = Filter()
    res = filter.selector(dimension='sa2', value='117011325') \
          | filter.selector(dimension='sa2', value='210051248')

    expected = {
      "filter": {
        "type": "or",
        "fields": [{
          "type": "selector",
          "dimension": "sa2",
          "value": "117011325"
        },
        {
          "type": "selector",
          "dimension": "sa2",
          "value": "210051248"
        }]
      }
    }
    self.assertEqual(res.to_dict(), expected)

  def test_not_logic(self):
    filter1 = Filter()
    res = ~filter1.selector(dimension='country_name', value='AUSTRALIA')

    expected = {
      "filter":{
        "type": "not",
        "field": {
          "type": "selector",
          "dimension": "country_name",
          "value": "AUSTRALIA"
        }
      }
    }
    self.assertEqual(res.to_dict(), expected)

  def test_extraction_fn_in_filter(self):
    filter1 = Filter()
    extraction = ExtractionFn(typ='timeFormat')
    res = filter1.selector(dimension='__time', value='AUSTRALIA', extraction_fn=extraction(format="EEEE", timezone="Australia/Sydney"))
    expected = {
      'filter': {
        'dimension': '__time',
        'value': 'AUSTRALIA',
        'type': 'selector',
        'extractionFn': {
          'format': 'EEEE',
          'timeZone': 'Australia/Sydney',
          'locale': 'en',
          'type': 'timeFormat'}
      }
    }
    self.assertEqual(res.to_dict(), expected)

  def test_mix_operation(self):
    filter = Filter()
    listOfSA2 = ['305021115', '303021053', '303021055', '303021058']
    and_filter_list = list(map(lambda x: (filter.selector(dimension="origin_sa2", value=x)
                                          & filter.selector(dimension="destination_sa2",
                                                                   value=x)), listOfSA2))
    combined_filters = reduce(lambda a, b: a | b, and_filter_list)
    expected = {'filter': {'fields': [{'fields': [{'dimension': 'origin_sa2', 'value': '305021115', 'type': 'selector'}, {'dimension': 'destination_sa2', 'value': '305021115', 'type': 'selector'}], 'type': 'and'}, {'fields': [{'dimension': 'origin_sa2', 'value': '303021053', 'type': 'selector'}, {'dimension': 'destination_sa2', 'value': '303021053', 'type': 'selector'}], 'type': 'and'}, {'fields': [{'dimension': 'origin_sa2', 'value': '303021055', 'type': 'selector'}, {'dimension': 'destination_sa2', 'value': '303021055', 'type': 'selector'}], 'type': 'and'}, {'fields': [{'dimension': 'origin_sa2', 'value': '303021058', 'type': 'selector'}, {'dimension': 'destination_sa2', 'value': '303021058', 'type': 'selector'}], 'type': 'and'}], 'type': 'or'}}
    self.assertEqual(combined_filters.to_dict(), expected)

if __name__ == '__main__':
    unittest.main()