#!python3

import redis
import time
import json
#import sleeping
from option import OptionData
from utility import *

class ICollector:
    def __init__(self):
        pass

    
    def run(self):
        pass


class Collector:
    def __init__(self, category = '50ETF', host = 'localhost', port = 6379):
        self.r = redis.Redis(host, port, db=0)
        self.category = category
        self.option = OptionData(category)
        self.convertor = CodeToDescriptionName(category)

    
    def run(self):
        "collect options kline"
        "[{'name': 2700, sellprice': 0.11, 'buyprice':0.12, 'remainday':15, 'optionvalue':450, 'timevalue':200}, {}]"
        counter = 0
        contracts = self.option.get_option_contracts(self.category)
        for contract in contracts:
            end_day, remain = self.option.get_option_expire_days(contract)
            calls, puts = self.option.get_option_codes(contract)
            
            for call in calls:
                kdatas = self.option.get_option_day_kline(call)
                for kdata in kdatas:
                    remaining_day = get_remaining_day(end_day, kdata['d'])
                    description = self.convertor.code_to_name(call)
                    #(category, month, call, name)
                    key = option_key(self.category, contract, kdata['d'])
                    key +=' ' + description[2] + ' '+description[3]
                    kdata['remainday'] = remaining_day
                    value = double_quotation(str(kdata))

                    if not self.r.exists(key):
                        self.r.set(key, value)
                        #print('set new key {}'.format(key))
                        counter += 1
                    else:
                        #print('key already exist {}'.format(key))
                        pass

            for put in puts:
                kdatas = self.option.get_option_day_kline(put)
                for kdata in kdatas:
                    description = self.convertor.code_to_name(put)
                    #(category, month, call, name)
                    key = option_key(self.category, contract, kdata['d'])
                    key +=' ' + description[2] + ' '+description[3]
                    kdata['remainday'] = remaining_day
                    value = double_quotation(str(kdata))
                    if not self.r.exists(key):
                        self.r.set(key, value)
                        #print('set new key {}'.format(key))
                        counter += 1
                    else:
                        #print('key already exist {}'.format(key))
                        pass
        print('collect new data: {}'.format(counter))
 

class ETFCollector():
    def __init__(self, category = '50ETF', host = 'localhost', port = 6379):
        self.r = redis.Redis(host, port, db=0)
        self.category = category
        self.option = OptionData(category)
        self.fix=0
        pass

    def run(self):
        datas = self.option.get_etf_day_kline()

        for data in datas:
            key = self.category + ' ' + data['day']

            counter = 0
            if not self.r.exists(key):
                value = str(data)
                self.r.set(key, value)
                counter += 1
            else:
                pass

            self.fix_option_price(data)

        print('collect new data: {}'.format(counter))
        print("fix data: {}".format(self.fix))

    def fix_option_price(self, data):
        etf = data
        contracts = self.option.get_option_contracts()

        for contract in contracts:

            key = option_key(self.category, contract, etf['day'])
            key +='*'
            keys = self.r.keys(key)
            for key in keys:
                key=key.decode('GBK')
                option_data = self.r.get(key)
                option_data.decode('GBK')
                price = json.loads(option_data)
                if 'call' in key: 
                    price['name'] = key[-4:]
                    price['sellprice'] = price['c']
                    price['buyprice'] = price['c']
                    price['etfprice'] = etf['close']
    #                price['remainday'] = 10
                    if float(price['name'])/1000 > float(etf['close']): 
                        price['optionvalue'] = 0
                        price['timevalue'] = float(price['buyprice'])
                    else:
                        price['optionvalue'] = float(etf['close']) - float(price['name'])/1000
                        price['timevalue'] = float(price['buyprice']) - price['optionvalue']
                
                if 'put' in key:
                    price['name'] = key[-4:]
                    price['sellprice'] = price['c']
                    price['buyprice'] = price['c']
                    price['etfprice'] = etf['close']
    #                price['remainday'] = 10
                    if float(price['name'])/1000 < float(etf['close']): 
                        price['optionvalue'] = 0
                        price['timevalue'] = float(price['buyprice'])
                    else:
                        price['optionvalue'] = float(price['name'])/1000 - float(etf['close'])  
                        price['timevalue'] = float(price['buyprice']) - price['optionvalue']

                self.r.set(key, double_quotation(str(price)))
                self.fix += 1
                pass

            


def test_redis():
    r = redis.Redis(host='localhost', port=6379, db=0)
    r.set('foo', 'bar')

    result = r.get('foo')
    print(result)


def collector():
    c = Collector('50ETF')
    c1 = Collector('300ETF')
    
    last=time.time()
    while True:
        current = time.time()
        if current - last > 3600*24:
            c.run()
            c1.run()
            last = current
        else:
#            sleeping.sleep(3600*2)
            pass

def test_collector():
    c = Collector('50ETF')
    c.run()

 #   c = Collector('300ETF')
 #   c.run() 
def test_ETFCollector():
    c = ETFCollector('50ETF')
    c.run()

    c1 = ETFCollector('300ETF')
    c1.run()


if __name__ == '__main__':
#    test_collector()
    test_ETFCollector()
    #collector()
    pass


