__author__ = 'jingxuan'

class APIException(Exception):
  def __init__(self, exp):
    super().__init__("APIException: {}".format(exp))

class RequestException(Exception):
  def __init__(self, exp):
    super().__init__("RequestException: {}".format(exp))

class ResponseException(Exception):
  def __init__(self, response):
    super().__init__(
      "ResponseException: {} with error code {}".format(response.text, response.status_code)
    )