__author__ = 'jingxuan'

import unittest
from api.auth import Authorize

class TestAuthorize(unittest.TestCase):
  def test_auth(self):
    auth = Authorize("https://apistore.dsparkanalytics.com.au/token", 
                     "consumer_key",
                     "consumer_secret" )
    auth.request_token()
    self.assertTrue(auth.access_token is not None)

if __name__ == '__main__':
    unittest.main()