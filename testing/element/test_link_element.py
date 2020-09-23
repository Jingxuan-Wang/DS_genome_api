__author__ = 'jingxuan'

import unittest
from genomeapi.elements.link import Link

class TestLink(unittest.TestCase):
  def test_link(self):
    lin = Link()
    res = lin("NSW513133313")
    expected = {
      "links": ["NSW513133313"]
    }
    self.assertEqual(res, expected)

if __name__ == '__main__':
    unittest.main()
