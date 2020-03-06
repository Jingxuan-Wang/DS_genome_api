__author__ = 'jingxuan'
"""API exception classes.

Includes two main exceptions: :class:`.APIException` for when something goes
wrong on the server side, and :class:`.ClientException` when something goes
wrong on the client side. Both of these classes extend :class:`.PDAWException`.

"""

class APIException(Exception):
  """The base API Exception that all other exception classes extend."""

class ClientException(Exception):
  """Indicate exceptions that don't involve interaction with DataSpark's API."""

class RequestException(APIException):
  """Indicate that there was an error with the incomplete HTTP request."""

  def __init__(self, original_exception):
    """Initialize a RequestException instance.

    :param original_exception: The original exception that occurred.

    """
    self.original_exception = original_exception
    super(RequestException, self).__init__(
      "error with request {}".format(original_exception)
    )

class ResponseException(APIException):
  """Indicate that there was an error with the completed HTTP request."""

  def __init__(self, response):
    """Initialize a ResponseException instance.

    :param response: A requests.response instance.

    """
    self.response = response
    super(ResponseException, self).__init__(
      "received {} HTTP response: {}".format(response.status_code, response.text)
    )