__author__ = 'jingxuan'

import unittest
from genomeapi.api import ODThroughLink
import json

class TestODThroughLink(unittest.TestCase):
  def test_od_through_link(self):
    od_thr_link = ODThroughLink("URL","token")
    od_thr_link.dates(begin_date="2018-07-11")
    od_thr_link.time_series_reference("arrival")
    od_thr_link.link("NSW513133313")
    od_thr_link.dimension_facets("mode")
    od_thr_link.granularity(period="PT6H")
    od_thr_link.aggregate(metric="unique_agents", described_as="unique_agents")
    od_thr_link.aggregate(metric="total_records", described_as="total_records")
    od_thr_link.dumps()
    res = od_thr_link.json
    expected ={
      "dates": {
      "type": "single",
      "value": "2018-07-11"
      },
      "timeSeriesReference": "arrival",
      "links": [
          "NSW513133313"
      ],
      "dimensionFacets": [
          "mode"
      ],
      "queryGranularity": {
          "type": "period",
          "period": "PT6H",
          "timeZone": "Australia/Sydney"
      },
      "aggregations": [
      {
        "metric": "unique_agents",
        "type": "hyperUnique",
        "describedAs": "unique_agents"
      },
      {
        "metric": "total_records",
        "type": "longSum",
        "describedAs": "total_records"
      }]
    }

    self.assertEqual(json.loads(res), expected)

if __name__ == '__main__':
    unittest.main()