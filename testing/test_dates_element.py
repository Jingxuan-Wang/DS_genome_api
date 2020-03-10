__author__ = 'jingxuan'

import unittest
from genomeapi.elements.dates import Dates

class DateTest(unittest.TestCase):

  def test_single_date(self):
    date = Dates()
    res = date("2020-01-02")
    expected = {"dates": {"type": "single", "value": "2020-01-02"}}
    self.assertEqual(res, expected)

  def test_date_range(self):
    date = Dates()
    res = date(begin_date="2020-01-02", end_date="2020-01-05")
    expected = {"dates": {"type": "range", "beginDate": "2020-01-02", "endDate": "2020-01-05"}}
    self.assertEqual(res, expected)

if __name__ == '__main__':
    unittest.main()