#  Copyright © DataSpark Pte Ltd 2014 - 2020.
#
#  This software and any related documentation contain confidential and proprietary information of
#  DataSpark and its licensors (if any). Use of this software and any related documentation is
#  governed by the terms of your written agreement with DataSpark. You may not use, download or
#  install this software or any related documentation without obtaining an appropriate licence
#  agreement from DataSpark.
#
#  All rights reserved.

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