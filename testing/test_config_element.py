__author__ = 'jingxuan'

import unittest
from config import Config

class TestConfig(unittest.TestCase):

  def test_config(self):
    config = Config("DEFAULT")
    consumer_key = config.consumer_key
    consumer_secret = config.consumer_secret
    print(consumer_key)
    print(consumer_secret)
    self.assertTrue(consumer_key is not None)
    self.assertTrue(consumer_secret is not None)

if __name__ == '__main__':
    unittest.main()