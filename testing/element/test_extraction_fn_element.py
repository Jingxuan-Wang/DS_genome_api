__author__ = 'jingxuan'
import unittest
from genomeapi.elements.extraction_fn import ExtractionFn

class TestExtractionFn(unittest.TestCase):
  def test_string_extraction_fn(self):
    string_extraction_fn = ExtractionFn(typ='substring')
    res = string_extraction_fn(index=1, length=4)
    expected = {
        "type": "substring",
        "index": 1,
        "length": 4
    }
    self.assertEqual(res, expected)

  def test_time_format_extraction_fn(self):
    time_format_extraction_fn = ExtractionFn(typ='timeFormat')
    res = time_format_extraction_fn(format='EEEE', timezone='Australia/Sydney')
    expected = {
        "type": "timeFormat",
        "format": "EEEE",
        "timeZone": "Australia/Sydney",
        "locale": "en"
    }
    self.assertEqual(res, expected)

if __name__ == '__main__':
    unittest.main()