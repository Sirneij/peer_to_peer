import unittest
from os import system

from peer_to_peer.models import User


class ServerTest(unittest.TestCase):
    def setUp(self) -> None:
        user = User()
        user.set_user_data(
            {
                'id': 1,
                'username': 'John',
                'password': 'password',
            }
        )

    def test_index(self):
        pass


if __name__ == '__main__':
    system('gunicorn peer_to_peer.server:app')
    unittest.main()
