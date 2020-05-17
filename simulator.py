#!python3

from Generator import KdayGenerator
from policy import BigYearOwning
from trader import FakeOptionTrader
from exception import *

class Simulator():
    def __init__(self):
        self.g = KdayGenerator('50ETF', contract='202003', start='2020-02-1', end='2020-02-12')
        self.price = {}
        self.p = BigYearOwning(owning=30)
        self.t = FakeOptionTrader()
        self.duration = 12
        pass


    def run(self):

        while True:
            try:
                self.price = self.g.run()
                self.p.run(self.price)
            except ReachTheEndDay:
                '''
                close all blance
                '''
                self.close_all_balance()
                print(self.t.history)
                print('duraing: {}, owning: {}', self.duration, self.t.get_owning())
                break
                
            except BigOwningAlarm:
                self.t.order('buy call', self.p.buy_option, 1)
                self.t.order('sell call', self.p.sell_option, 1)
                
        
    def close_all_balance(self):
        b = self.t.get_balance()
        for key in b.keys():
            if 'buy' in key:
                self.t.order('buy call close', self.price['50ETF 202002'][0][key[-4:]], b[key][1])
            elif 'sell' in key:
                self.t.order('sell call close', self.price['50ETF 202002'][0][key[-4:]], b[key][1])
            else:
                print('wrong type, can not close')

        
def test_simulator():
    s = Simulator()
    s.run()

    pass

if __name__ == '__main__':
    test_simulator()

    pass

