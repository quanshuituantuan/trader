#!python

import redis
import time
import re
import json
from exception import *
from option import OptionData
from utility import *
'''
{"50ETF 202002": (call, put) }
{2500:price, 2600:price, }


'''

class IGenerator():
    def __init__(self):
        pass

    
    def run(self, contract):
        pass


class RTOptionGenerator(IGenerator):
    def __init__(self, category = '50ETF', contract = '202002'):
        super(RTOptionGenerator).__init__()
        self.category = category
        self.option = OptionData(category)
        self.contract = contract

    def run(self):
        calls, puts = self.option.get_option_all_prices(self.contract)

        new_calls = {}
        for call in calls:
            name = call['name']
            new_calls[name] = call

        new_puts = {}
        for put in puts:
            name = put['name']
            new_puts[name] = put
        
        contract_prices = {}
        name = self.category +' '+self.contract
        contract_prices[name] = (new_calls, new_puts)

        return contract_prices

class KdayGenerator(IGenerator):
    def __init__(self, category = '50ETF', contract = '202002', start = '2020-02-01', end = '2020-02-29', host = 'localhost', port = 6379):
        self.category = category
        self.contract = contract
        self.r = redis.Redis(host, port, db=0)
        regex = re.compile(r'^(\d+)-(\d+)-(\d+)$')
        m = regex.match(start)
        self.start_year = m.group(1)
        self.start_month = m.group(2)
        self.start_day = m.group(3)
        m = regex.match(end)
        self.end_year = m.group(1)
        self.end_month = m.group(2)
        self.end_day = m.group(3)
        self.start = time.mktime((int(self.start_year), int(self.start_month), int(self.start_day), 0, 0, 0, 0, 0, 0))
        self.next = self.start
        self.end = time.mktime((int(self.end_year), int(self.end_month), int(self.end_day), 0, 0, 0, 0, 0, 0))


    def day_to_string(self):
        localtime = time.localtime(self.next)
        t = '{}-{:02d}-{:02d}'.format(localtime[0], localtime[1], localtime[2])
        return t

    def next_day(self):
        self.next += 3600*24

    def run(self):
        while True:
            if self.next < self.end:
                key = option_key(self.category, self.contract, self.day_to_string())
                key += '*'
                keys = self.r.keys(key)

                '''
                not working day, get next day price
                '''
                if not keys: 
                    self.next_day()
                    continue

                calls = {}
                puts = {}
                contract_prices = {}
                for key in keys:
                    key = key.decode('GBK')
                    option_data = self.r.get(key)
                    option_data = option_data.decode('GBK')
                    price = json.loads(option_data)

                    if 'call' in key: 
                        calls[price['name']] = price

                    elif 'put' in key:
                        puts[price['name']] = price
                name = self.category + ' ' +self.contract
                contract_prices[name] = (calls, puts)
                self.next_day()

                return contract_prices
            else:
                raise ReachTheEndDay


def testRTOptionGenerator():
    gen = RTOptionGenerator('50ETF', '202002')
    prices = gen.run()
    
    pass

def testKdayGenerator():
    gen = KdayGenerator('50ETF', '202003', '2020-01-01', '2020-02-12')
    
    counter = 0
    while True:
        try: 
            prices = gen.run()
            counter += 1
            pass
        except ReachTheEndDay:
            print("finish, get price: {}".format(counter))
            break

    pass 


if __name__ == '__main__':
    testRTOptionGenerator()
 #   testKdayGenerator()
    pass