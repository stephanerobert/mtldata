import unittest

from mockserver_friendly import MockServerFriendlyClient

MOCKSERVER_URL = "http://localhost:38785"


class ServerMockingTestBase(unittest.TestCase):
    def setUp(self):
        super(ServerMockingTestBase, self).setUp()

        self.mock_server = MockServerFriendlyClient(MOCKSERVER_URL)
        self.mock_server.reset()

    def tearDown(self):
        super(ServerMockingTestBase, self).tearDown()

        self.mock_server.verify()
