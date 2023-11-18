from ddt import ddt, unpack, data

import unittest
from allure_unittest import Run


@ddt
class Activity(unittest.TestCase):
    # # @classmethod
    # # def setUpClass(cls):
    # #     cls.d = 9/0
    # #
    # # @classmethod
    # def setUp(cls):
    #     cls.d = 9/0

    @data(*[1, 2, 3, 4, 5])
    def test_base(self, d):
        self._testMethodDoc = f"测试{d}配置表基础逻辑测试"
        self.d = 9 / 0


if __name__ == '__main__':
    # unittest.main()
    # activity().run()
    # a = Result('aaa')
    c = unittest.defaultTestLoader.loadTestsFromTestCase(Activity)
    # c.run(a)
    # Activity('test_base').run(a)
    # s = unittest.TestSuite()
    # s.addTest(activity('test_base'))
    Run('test', c, clean=True)
