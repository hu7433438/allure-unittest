import unittest
from allure_unittest import Run


class Activity(unittest.TestCase):
    def test_1(self):
        self._testMethodDoc = "test 1 == 1"
        self.assertEqual(1, 1)

    def test_2(self):
        self._testMethodDoc = "test 1 == 2"
        self.assertEqual(1, 2)

    def test_3(self):
        self._testMethodDoc = "test 2 == 3"
        self.assertEqual(2, 3, "2 not Equal 3")


if __name__ == '__main__':
    c = unittest.defaultTestLoader.loadTestsFromTestCase(Activity)
    Run('test', c, clean=True)
