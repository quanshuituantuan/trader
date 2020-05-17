#!python3
import unittest
from trader import FakeOptionTrader

class TraderTest(unittest.TestCase):
    def setUp(self):
        self.t = FakeOptionTrader()
        self.price = {"d": "2019-12-18", "o": "0.3853", "h": "0.3941", "l": "0.3784", "c": "0.4270", "v": "2563533", "remainday": 133, "name": "3444", "sellprice": "0.4270", "buyprice": "0.4270", "etfprice": "3.017", "optionvalue": 0.42700000000000005, "timevalue": -5.551115123125783e-17}
        pass


    def tearDown(self):
        pass


    def test_order(self):
        self.t.order('buy call', self.price, 1)
        self.t.order('buy call close', self.price, 1)
        own = self.t.get_owning()
        self.assertEqual(0.0, own)


    def test_order_sell(self):
        self.t.order('sell call', self.price, 1)
        self.t.order('sell call close', self.price, 1)
        own = self.t.get_owning()
        self.assertEqual(0.0, own)
