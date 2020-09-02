__author__ = 'jingxuan'

import unittest
from genomeapi.elements.granularity import Granularity
from genomeapi.elements.exceptions import APIException

class TestGranularity(unittest.TestCase):
  def test_granularity(self):
    grant = Granularity()
    res = grant(period='PT1H', typ='period')
    expected = {
      "queryGranularity": {
        "type": "period",
        "period": "PT1H"
      }
    }
    self.assertEqual(res, expected)

  def test_granularity_false_case1(self):
    grant = Granularity()
    with self.assertRaises(APIException) as context:
      grant(period='PT1H20M', typ='period')
    self.assertTrue("Period must be defined in buckets of 15 minutes", str(context.exception))

  def test_granularity_false_case2(self):
    grant = Granularity()
    with self.assertRaises(APIException) as context:
      grant(period='PT1D', typ='period')
    self.assertTrue("wrong format for the period", str(context.exception))

  def test_granularity_false_case3(self):
    grant = Granularity()
    with self.assertRaises(APIException) as context:
      grant(period='P1D', typ='other')
    self.assertTrue("wrong type for granularity", str(context.exception))



if __name__ == '__main__':
    unittest.main()
