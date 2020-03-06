__author__ = 'jingxuan'
import unittest
from elements.extraction_fn import ExtractionFn

class TestExtractionFn(unittest.TestCase):
  def test_string_extraction_fn(self):
    string_extraction_fn = ExtractionFn(typ='string')
    res = string_extraction_fn(index=1, length=4)
    expected = {
      "extractionFn": {
        "type": "substring",
        "index": 1,
        "length": 4
      }
    }
    self.assertEqual(res, expected)

  def test_time_format_extraction_fn(self):
    time_format_extraction_fn = ExtractionFn(typ='time')
    res = time_format_extraction_fn(format='EEEE', timezone='Australia/Sydney')
    expected = {
      "extractionFn": {
        "type": "timeFormat",
        "format": "EEEE",
        "timeZone": "Australia/Sydney",
        "locale": "en"
      }
    }
    self.assertEqual(res, expected)

if __name__ == '__main__':
    unittest.main()