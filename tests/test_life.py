import sys
sys.path.append("..")

from life.life import Life  # noqa: E402
import unittest  # noqa: E402


class BasicTestSuite(unittest.TestCase):
    def setUp(self):
        pass
