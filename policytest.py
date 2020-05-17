#!python3
'''
import unittest
from policy import *
from Generator import KdayGenerator
from Generator import RTOptionGenerator

class TestPolicy(unittest.TestCase):
    def setUp(self):
        self.gen = KdayGenerator()
        self.contracts_prices = self.gen.run()

        self.rt = RTOptionGenerator()
        self.rt_price = self.rt.run()


    def tearDown(self):
        pass

    def test_find_most_option_value_option(self):
        price = find_most_option_value_option(self.contracts_prices['50ETF 202002'][0])
    
        self.assertEqual(1, 1)

    def test_find_most_time_value_option(self):
        price = find_most_time_value_option(self.contracts_prices['50ETF 202002'][1])
    
        self.assertEqual(1, 1)


    def test_bigyearowningpolicy(self):
        p = BigYearOwning(100)
        p.run(self.rt_price)
'''