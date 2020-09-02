__author__ = 'jingxuan'
import unittest
from genomeapi.elements.aggregation import Aggregation
from genomeapi.elements.exceptions import APIException


class AggregationTest(unittest.TestCase):

  def test_single_aggregation(self):
    agg = Aggregation()
    res = agg(metric="total_records", typ="longSum", described_as="Trips").to_dict()
    expected ={"aggregations":[{
        "metric": "total_records",
        "type": "longSum",
        "describedAs": "Trips"}]
    }
    self.assertEqual(res, expected)

  def test_multiple_aggregations(self):
    agg1 = Aggregation()
    agg2 = Aggregation()
    res1 = agg1(metric="total_records", typ="longSum", described_as="Trips")
    res2 = agg2(metric="unique_agents", typ="hyperUnique", described_as="People")
    res = (res1 + res2).to_dict()
    expected = {
      "aggregations": [
        {
          "metric": "total_records",
          "type": "longSum",
          "describedAs": "Trips"
        },
        {
          "metric": "unique_agents",
          "type": "hyperUnique",
          "describedAs": "People"
        }
      ]}
    self.assertEqual(res, expected)
    
  def test_exception(self):
    agg = Aggregation()
    with self.assertRaises(APIException) as context:
      agg(metric="total_records", typ="longUnique")
    self.assertTrue("Sorry, we don't have such type for aggregation!", str(context.exception))

if __name__ == '__main__':
   unittest.main()