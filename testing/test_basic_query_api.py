__author__ = 'jingxuan'

import unittest
from genomeapi.api.basic_query import BasicQuery
from genomeapi.elements.filter import Filter
from genomeapi.elements.extraction_fn import ExtractionFn

class TestBasicQuery(unittest.TestCase):
  def test_query1(self):
    query = BasicQuery('linkmeta')
    query.dates(begin_date="2019-07-01", end_date="2019-07-31")
    query.location(location_type="locationHierarchyLevel", level_type="building", id="SYDNEY CENTRAL PLAZA IBC")
    query.aggregate(metric="unique_agents", typ="hyperUnique", described_as="unique_agents")
    query.aggregate(metric="total_stays", typ="doubleSum", described_as="total_stays")
    query.granularity(period="P31D", typ="period")
    query.dumps()

    expected = {
      "dates": {
        "type": "range",
        "beginDate": "2019-07-01",
        "endDate": "2019-07-31"
      },
      "location": {
        "locationType": "locationHierarchyLevel",
        "levelType": "building",
        "id": "SYDNEY CENTRAL PLAZA IBC"
      },
      "aggregations": [
        {
          "metric": "unique_agents",
          "type": "hyperUnique",
          "describedAs": "unique_agents"
        },
        {
          "metric": "total_stays",
          "type": "doubleSum",
          "describedAs": "total_stays"
        }
      ],
      "queryGranularity": {
        "type": "period",
        "period": "P31D"
      }
    }
    self.assertEqual(query._req, expected)

  def test_query2(self):
    query = BasicQuery('linkmeta')
    query.dates(begin_date="2019-08-01")
    query.time_series_reference("origin")
    query.location(location_type="locationHierarchyLevel", level_type="sa2", id="117011325")
    query.granularity(period="PT15M", typ="period")
    query.aggregate(metric="total_records",typ="longSum", described_as="Trips")
    query.dumps()
    expected ={
    "dates": {
      "type": "single",
      "value": "2019-08-01"
    },
    "timeSeriesReference": "origin",
    "location": {
      "locationType": "locationHierarchyLevel",
      "levelType": "sa2",
      "id": "117011325"
    },
    "queryGranularity": {
      "type": "period",
      "period": "PT15M"
    },
    "aggregations": [
      {
        "metric": "total_records",
        "type": "longSum",
        "describedAs": "Trips"
      }
    ]}
    self.assertEqual(query._req, expected)

  def test_query3(self):
    query = BasicQuery('linkmeta')
    query.dates(begin_date="2019-07-01", end_date="2019-07-28")
    query.time_series_reference("arrival")
    query.granularity(period="P7D")
    filter = Filter()
    query.filter(filter.in_filter("VIC17483860", "VIC6052402","NSW500187142", dimension="link_id"))
    query.aggregate(metric="unique_agents", typ="hyperUnique", described_as="unique_agents")
    query.aggregate(metric="total_records", typ="longSum")
    query.dumps()

    expected = {
      "dates": {
        "beginDate": "2019-07-01",
        "endDate": "2019-07-28",
        "type": "range"
      },
      "aggregations": [
        {
          "metric": "unique_agents",
          "type": "hyperUnique",
          "describedAs": "unique_agents"
        },
        {
          "metric": "total_records",
          "type": "longSum"
        }
      ],
      "queryGranularity": {
        "period": "P7D",
        "type": "period"
      },
      "filter": {
        "dimension": "link_id",
        "type": "in",
        "values": ["VIC17483860", "VIC6052402", "NSW500187142"]
      },
      "timeSeriesReference": "arrival"
    }

    self.assertEqual(query._req, expected)

  def test_query4(self):
    extraction = ExtractionFn(typ='time')
    extract = extraction(format='EEEE', timezone='Australia/Sydney')
    filter = Filter()
    filter = filter.selector(dimension='__time', extraction_fn=extract, value="Monday") \
            | filter.selector(dimension='__time', extraction_fn=extract, value="Tuesday") \
            | filter.selector(dimension='__time', extraction_fn=extract, value="Wednesday") \
            | filter.selector(dimension='__time', extraction_fn=extract, value="Thursday") \
            | filter.selector(dimension='__time', extraction_fn=extract, value="Friday")
    query = BasicQuery('linkmeta')
    query.dates(begin_date="2019-07-07", end_date="2019-08-03")
    query.location(location_type="locationHierarchyLevel", level_type="sa2", id="117031337")
    query.filter(filt= filter)
    query.aggregate(metric="unique_agents", typ="hyperUnique", described_as="unique_agents")
    query.aggregate(metric="total_stays", typ="doubleSum", described_as="total_stays")
    query.granularity(period="P7D")
    query.dumps()

    expected = {
      "dates": {
        "type": "range",
        "beginDate": "2019-07-07",
        "endDate": "2019-08-03"
      },
      "location": {
        "locationType": "locationHierarchyLevel",
        "levelType": "sa2",
        "id": "117031337"
      },
      "filter": {
        "type": "or",
        "fields": [
          {
            "type": "selector",
            "dimension": "__time",
            "value": "Monday",
            "extractionFn": {
              "type": "timeFormat",
              "format": "EEEE",
              "timeZone": "Australia/Sydney",
              "locale": "en"
            }
          },
          {
            "type": "selector",
            "dimension": "__time",
            "value": "Tuesday",
            "extractionFn": {
              "type": "timeFormat",
              "format": "EEEE",
              "timeZone": "Australia/Sydney",
              "locale": "en"
            }
          },
          {
            "type": "selector",
            "dimension": "__time",
            "value": "Wednesday",
            "extractionFn": {
              "type": "timeFormat",
              "format": "EEEE",
              "timeZone": "Australia/Sydney",
              "locale": "en"
            }
          },
          {
            "type": "selector",
            "dimension": "__time",
            "value": "Thursday",
            "extractionFn": {
              "type": "timeFormat",
              "format": "EEEE",
              "timeZone": "Australia/Sydney",
              "locale": "en"
            }
          },
          {
            "type": "selector",
            "dimension": "__time",
            "value": "Friday",
            "extractionFn": {
              "type": "timeFormat",
              "format": "EEEE",
              "timeZone": "Australia/Sydney",
              "locale": "en"
            }
          }
        ]
      },
      "aggregations": [
        {
          "metric": "unique_agents",
          "type": "hyperUnique",
          "describedAs": "unique_agents"
        },
        {
          "metric": "total_stays",
          "type": "doubleSum",
          "describedAs": "total_stays"
        }
      ],
      "queryGranularity": {
        "type": "period",
        "period": "P7D"
      }
      }

    self.assertEqual(query._req, expected)

if __name__ == '__main__':
    unittest.main()
