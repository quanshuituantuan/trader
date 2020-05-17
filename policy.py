#!python3
from option import OptionData
from exception import BigOwningAlarm


class IPolicy():
    def __init__(self):
        pass


    def run(self):
        pass


class BigYearOwning(IPolicy):
    def __init__(self, owning = 30):
        self.owning = owning
        self.buy_option = None
        self.sell_option = None

    def run(self, contracts_prices):
  
        for key in contracts_prices.keys():

            actualValueOptionData = find_most_option_value_option(contracts_prices[key][0])
            outOftheMoneyOptionData = find_most_time_value_option(contracts_prices[key][0])
            highPrice = (float(outOftheMoneyOptionData['sellprice']) + float(outOftheMoneyOptionData['name'])/1000)
            lowPrice = (float(actualValueOptionData['buyprice']) + float(actualValueOptionData['name'])/1000)
            expireDays = int(outOftheMoneyOptionData['remainday'])

            yearOwning = ((highPrice - lowPrice)/lowPrice)*(365/expireDays) * 100

            print('name {} remainday：{}'.format(key, outOftheMoneyOptionData['remainday']))
            print('optionvalue {} {}'.format(actualValueOptionData['name'], actualValueOptionData['sellprice']))
            print('timevalue:  {} {}'.format(outOftheMoneyOptionData['name'], outOftheMoneyOptionData['buyprice']))
            print('year owning:  {}%'.format(yearOwning))

            if yearOwning > self.owning:
                self.buy_option = actualValueOptionData
                self.sell_option = outOftheMoneyOptionData
                raise BigOwningAlarm

        pass

class BigYearOwningImprove(IPolicy):
    def __init__(self, low = 10, high = 30, fee = 8):
        self.low = low
        self.high = high
        self.fee = 8 


    def run(self, contracts_prices):
        for key in contracts_prices.keys():

            actualValueOptionData = find_most_option_value_option(contracts_prices[key][0])
            save_key, buy = find_most_time_value_option_internal(contracts_prices)
            outOftheMoneyOptionData = contracts_prices[key][0][save_key]
            fee = 3*self.fee
            high_own = contracts_prices[key][0][save_key]['buyprice'] + contracts_prices[key][1][save_key]['buyprice'] - fee 
                
            bail = actualValueOptionData['sellprice'] + outOftheMoneyOptionData['bail'] + contracts_prices[key][1][save_key]['bail']
            expireDays = int(outOftheMoneyOptionData['remainday'])
            high_yearOwning = (high_own/bail)*(365/expireDays) * 100


            low_own = high_own - buy['sellprice']
            low_yearOwning = (low_own/bail)*(365/expireDays) * 100

            print('name {} remainday：{}'.format(key, outOftheMoneyOptionData['remainday']))
            print('optionvalue {} {}'.format(actualValueOptionData['name'], actualValueOptionData['sellprice']))
            print('timevalue:  {} {}'.format(outOftheMoneyOptionData['name'], outOftheMoneyOptionData['buyprice']))
            print('low year owning:  {}% , high: {}%'.format(low_yearOwning, high_yearOwning))


def find_most_time_value_option_internal(contracts_prices):
    prices = contracts_prices[0]
    keys = list(prices.keys())
    keys.sort()
    price = prices[keys[0]]
    for key in keys:
        if float(prices[key]['timevalue']) > price['timevalue']:
            sell = prices[key]
            save_key = key

    prices = contracts_prices[key][1]
    keys = list(prices.keys())
    keys.sort()
    index = keys.find(save_key)
    buy = prices[keys[index-1]]
    return save_key, buy


def find_most_option_value_option(prices):
    keys = list(prices.keys())
    keys.sort()
    price = prices[keys[0]]
    for key in keys :
        if float(prices[key]['timevalue']) < float(price['timevalue']):
            price = prices[key]
    
    return key, price
    
    return price


def find_most_time_value_option(prices):
    keys = list(prices.keys())
    keys.sort()
    price = prices[keys[0]]
    for key in keys:
        if float(prices[key]['timevalue']) > price['timevalue']:
            price = prices[key]
    return price


def testBigYearOwning_policy():

    pass

if __name__ == '__main__':
    pass
