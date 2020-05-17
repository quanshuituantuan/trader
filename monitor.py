#!python3


from Generator import RTOptionGenerator
from policy import BigYearOwningImprove
from weblof import *
from sendmsg import *
from workweektime import *
import time

class IMonitor():
    def __init__(self):
        pass 

    def run(self):
        pass


class ETFOptoinMonitor(IMonitor):
    def __init__(self, category = '50ETF', contract='202006'):
        self.category = category
        self.contract = contract
        self.option = RTOptionGenerator(self.category, self.contract)
        self.p = BigYearOwningImprove()

    def run(self):

        contract_prices = self.option.run()
        self.p.run(contract_prices)

        pass

class LOFMonitor(IMonitor):
    def __init__(self):
        self.sp500 = 0.1
        self.nq100 = 0.1
        self.premium = -0.9

    def check_price(self):
        sp500, nq100 = get_SP500_NQ100_discount()

        if sp500 < self.premium and self.sp500 > 0.0:
            self.sp500 = sp500
            msg = "sp500 premium rate: " + str(self.sp500) 
            print(msg)
            send_sms()
        elif sp500 > 0.0 and self.sp500 < self.premium: 
            self.sp500 = sp500
            msg = "sp500 premium rate: " + str(self.sp500) 
            print(msg)
            send_sms()
        else:
            # do nothing
            pass

        if nq100 < self.premium and self.nq100 > 0.0:
            self.nq100 = nq100
            msg = "nq100 premium rate: " + str(self.nq100) 
            print(msg)
            send_sms()
        elif nq100 > 0.0 and self.nq100 < self.premium: 
            self.nq100 = nq100
            msg = "nq100 premium rate: " + str(self.nq100) 
            print(msg)
            send_sms()
        else:
            # do nothing
            pass
    
    def check_timedata(self):
        pass

    def run(self):
        while(True):
            now = datetime.datetime.now()
            workday = get_week_day(now)
            h = now.hour
            m = now.minute

            if workday == '星期六' or workday == '星期天':
                print('sleep')
                time.sleep(1*60*60)
                continue
            elif h > 9 and h < 15:
                self.check_price()
                time.sleep(5*60)
            elif h == 9 and m > 31:
                self.check_price()
                time.sleep(5*60)


def test_monitor():
    m = ETFOptoinMonitor()
    m.run()


if __name__ == '__main__':
    # test_monitor()
    m = LOFMonitor()
    m.run()

    pass
