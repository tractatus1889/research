import unittest
import api

class ApiTestCase(unittest.TestCase):
  def test_get_response(self):
    response1 = api.get_response("My name is John.")
    response2 = api.get_response("What is my name?")
    self.assertNotIn("John", response2["content"])

  def test_get_response_continue(self):
    response1 = api.get_response_continue("My name is Joe.")
    response2 = api.get_response_continue("What is my name?")
    self.assertIn("John", response2["content"])

if __name__ == '__main__':
  unittest.main()
