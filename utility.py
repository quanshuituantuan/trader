#!python
import re
import datetime
import time

from option import OptionData

class CodeToDescriptionName:
    def __init__(self, category = '50ETF'):
        self.category = category
        self.codes={}
        self.etf = OptionData(category)
        
    def code_to_name(self, code):
        price = self.etf.get_option_price(code)

        r = re.compile(r'^(\d+ETF)(.*)(\d+)月(\d+)')
        m = r.match(price['期权合约简称'])
        category = m.group(1)
        call = m.group(2)
        month = m.group(3)
        name = m.group(4)
        if call == '购':
            call = 'call'
        else:
            call = 'put'
        description = (category, month, call, name)

        if code in self.codes.keys():
            return self.codes[code]
        else: 
            self.codes[code] = description
            return description

def etf_key(category, date):
    return category + ' ' +date


def option_key(category, contract, date):
    key = '{} {} {}'.format(category, contract, date)
    return key

def double_quotation(data):
    data = str(data).replace('\'', '\"')
    return data


def test_code_to_name():
    convertor = CodeToDescriptionName('50ETF')
    name = convertor.code_to_name(10002082)
    print(name)
    pass


def get_remaining_day(end, now):
    end = datetime.date.fromisoformat(end)
    now = datetime.date.fromisoformat(now)

    end = time.mktime((int(end.year), int(end.month), int(end.day), 0, 0, 0, 0, 0, 0))
    now = time.mktime((int(now.year), int(now.month), int(now.day), 0, 0, 0, 0, 0, 0))

    remaining_day = int((end - now)/3600/24)
    return remaining_day


if __name__ == '__main__':
    test_code_to_name()

