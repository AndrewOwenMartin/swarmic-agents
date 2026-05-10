import unittest
from unittest import mock
import chat

class TestChat(unittest.TestCase):

    def setUp(self):
        with mock.patch('chat.send_payload') as mock_send_payload:
            mock_send_payload.return_value = {
                "hello": "world",
            }
            yield
        

    def test_chat(self):
        response = chat.send_payload(payload={})
        assert response == {"hello", "world"}

