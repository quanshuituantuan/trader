#!python3

import unittest
from utility import *

class TestUtility(unittest.TestCase):
    def setUp(self):
        self.category = '50ETF'
        self.date = '2020-02-02'

        self.single_quotation_value = "{'d': '2020-02-10', 'o': '0.1922', 'h': '0.2019', 'l': '0.1876', 'c': '0.1943', 'v': '1446471'}"
        self.double_quotation_value = "{\"d\": \"2020-02-10\", \"o\": \"0.1922\", \"h\": \"0.2019\", \"l\": \"0.1876\", \"c\": \"0.1943\", \"v\": \"1446471\"}"
        pass

    
    def tearDown(self):
        pass


    def test_etf_key(self):
        key = etf_key(self.category, self.date)
        self.assertEqual(key, '50ETF 2020-02-02')


    def test_option_key(self):
        key = option_key(self.category, '202002', self.date)
        self.assertEqual(key, '50ETF 202002 2020-02-02')
    

    def test_double_quotation(self):
        v = double_quotation(self.single_quotation_value)
        self.assertEqual(self.double_quotation_value, v)


    def test_get_remaining_day(self):
        end = '2020-02-26'
        now = '2020-02-13'
        remain  = get_remaining_day(end, now)
        self.assertEqual(13, remain)
