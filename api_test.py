import unittest
import api

class ApiTestCase(unittest.TestCase):
  def test_get_response(self):
    response1 = api.get_response("My name is John.")
    response2 = api.get_response("What is my name?")
    self.assertNotIn("John", response2["content"])
    self.assertEqual(len(api.CONVERSATION), 1)
    self.assertEqual(len(api.MESSAGE_LOG), 4)

  def test_get_response_continue(self):
    response1 = api.get_response_continue("My name is John.")
    response2 = api.get_response_continue("What is my name?")
    self.assertIn("John", response2["content"])
    self.assertEqual(len(api.CONVERSATION), 5)
    # TODO: Once implemented properly this should be 4.
    self.assertEqual(len(api.MESSAGE_LOG), 8)

if __name__ == '__main__':
  unittest.main()
