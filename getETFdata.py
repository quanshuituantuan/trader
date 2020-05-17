#!python3
#from json import loads
#from requests import get
import json
import requests
import time

import redis
import re

 #https://blog.csdn.net/u013781175/article/details/54374798
 
def get_option_contracts(cate='50ETF', exchange='null'):
    url = f"http://stock.finance.sina.com.cn/futures/api/openapi.php/StockOptionService.getStockName?" \
          f"exchange={exchange}&cate={cate}"
    dates = requests.get(url).json()['result']['data']['contractMonth']
    return [''.join(i.split('-')) for i in dates][1:]
 
 
def get_option_expire_days(date, cate='50ETF', exchange='null'):
    url = "http://stock.finance.sina.com.cn/futures/api/openapi.php/StockOptionService.getRemainderDay?" \
          "exchange={exchange}&cate={cate}&date={year}-{month}"
    url2 = url.format(year=date[:4], month=date[4:], cate=cate, exchange=exchange)
    data = requests.get(url2).json()['result']['data']
    if int(data['remainderDays']) < 0:
        url2 = url.format(year=date[:4], month=date[4:], cate='XD' + cate, exchange=exchange)
        data = requests.get(url2).json()['result']['data']
    return data['expireDay'], int(data['remainderDays'])
 
 
def get_option_codes(date, underlying='510050'):
    url_up = ''.join(["http://hq.sinajs.cn/list=OP_UP_", underlying, str(date)[-4:]])
    url_down = ''.join(["http://hq.sinajs.cn/list=OP_DOWN_", underlying, str(date)[-4:]])
    data_up = str(requests.get(url_up).content).replace('"', ',').split(',')
    codes_up = [i[7:] for i in data_up if i.startswith('CON_OP_')]
    data_down = str(requests.get(url_down).content).replace('"', ',').split(',')
    codes_down = [i[7:] for i in data_down if i.startswith('CON_OP_')]
    return codes_up, codes_down
 

def get_option_price(code):
    url = "http://hq.sinajs.cn/list=CON_OP_{code}".format(code=code)
    data = requests.get(url).content.decode('gbk')
    data = data[data.find('"') + 1: data.rfind('"')].split(',')
    fields = ['买量', '买价', '最新价', '卖价', '卖量', '持仓量', '涨幅', '行权价', '昨收价', '开盘价', '涨停价',
              '跌停价', '申卖价五', '申卖量五', '申卖价四', '申卖量四', '申卖价三', '申卖量三', '申卖价二',
              '申卖量二', '申卖价一', '申卖量一', '申买价一', '申买量一 ', '申买价二', '申买量二', '申买价三',
              '申买量三', '申买价四', '申买量四', '申买价五', '申买量五', '行情时间', '主力合约标识', '状态码',
              '标的证券类型', '标的股票', '期权合约简称', '振幅', '最高价', '最低价', '成交量', '成交额',
              '分红调整标志', '昨结算价', '认购认沽标志', '到期日', '剩余天数', '虚实值标志', '内在价值', '时间价值']
    #result = list(zip(fields, data))
    result = dict(zip(fields, data))
    return result
 
 
def get_underlying_ETF_price(code='sh510050'):
    url = "http://hq.sinajs.cn/list=" + code
    data = requests.get(url).content.decode('gbk')
    data = data[data.find('"') + 1: data.rfind('"')].split(',')
    fields = ['证券简称', '今日开盘价', '昨日收盘价', '最近成交价', '最高成交价', '最低成交价', '买入价',
              '卖出价', '成交数量', '成交金额', '买数量一', '买价位一', '买数量二', '买价位二', '买数量三',
              '买价位三', '买数量四', '买价位四', '买数量五', '买价位五', '卖数量一', '卖价位一', '卖数量二',
              '卖价位二', '卖数量三', '卖价位三', '卖数量四', '卖价位四', '卖数量五', '卖价位五', '行情日期',
              '行情时间', '停牌状态']
    return list(zip(fields, data))
 

def get_option_greek_alphabet(code):
    url = "http://hq.sinajs.cn/list=CON_SO_{code}".format(code=code)
    data = requests.get(url).content.decode('gbk')
    data = data[data.find('"') + 1: data.rfind('"')].split(',')
    fields = ['期权合约简称', '成交量', 'Delta', 'Gamma', 'Theta', 'Vega', '隐含波动率', '最高价', '最低价',
              '交易代码', '行权价', '最新价', '理论价值']
    return list(zip(fields, [data[0]] + data[4:]))
 
 
def get_option_time_line(code):
    url = f"https://stock.finance.sina.com.cn/futures/api/openapi.php/StockOptionDaylineService.getOptionMinline?" \
          f"symbol=CON_OP_{code}"
    data = requests.get(url).json()['result']['data']
    return data
 
 
def get_option_day_kline(code):
    url = f"http://stock.finance.sina.com.cn/futures/api/jsonp_v2.php//StockOptionDaylineService.getSymbolInfo?" \
          f"symbol=CON_OP_{code}"
    data = requests.get(url).content
    data = json.loads(data[data.find(b'(') + 1: data.rfind(b')')])
    return data

 #50ETF kdata
 #http://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol=sh510050&scale=240&ma=no&datalen=250
 
def my_test():
    dates = get_option_contracts(cate='300ETF')
    print('期权合约月份：{}'.format(dates))
    for date in dates:
        print('期权月份{}：到期日{} 剩余天数{}'.format(date, *get_option_expire_days(date, cate='300ETF')))
    demo_code = '10002002'
    for date in dates:
        call_codes, put_codes = get_option_codes(date, underlying='510300')
        print('期权月份{} 看涨期权代码：{}\n期权月份{} 看跌期权代码：{}'.format(date, call_codes, date, put_codes))
        demo_code = call_codes[0]
    for index, i in enumerate(get_option_price(demo_code)):
        print('期权' + demo_code, index, *i)
    for index, i in enumerate(get_underlying_ETF_price(code='sh510300')):
        print(index, *i)
    for index, i in enumerate(get_option_greek_alphabet(demo_code)):
        print('期权' + demo_code, index, *i)
    time_line = get_option_time_line(demo_code)
    for i in time_line[-10:]:
        print('时间:{i}, 价格:{p}, 成交:{v}, 持仓:{t}, 均价:{a}'.format(**i))
    day_kline = get_option_day_kline(demo_code)
    for i in day_kline:
        print('日期:{d}, 开盘:{o}, 最高:{h}, 最低:{l}, 收盘:{c}, 成交:{v}'.format(**i))
 
'''
calucate the year owning according the price
need consider the volume and sell one price and volume
'''
def caculateUpOptionYearOwning(optionContract, actualValueOptionData, outOftheMoneyOptionData):
    #print(actualValueOptionData[2])
    #print(actualValueOptionData[7])
    
    #print(outOftheMoneyOptionData[2])
    #print(outOftheMoneyOptionData[7])

    #print(outOftheMoneyOptionData[47])

    highPrice = (float(outOftheMoneyOptionData['最新价']) + float(outOftheMoneyOptionData['行权价']))
    lowPrice = (float(actualValueOptionData['最新价']) + float(actualValueOptionData['行权价']))
    expireDays = int(outOftheMoneyOptionData['剩余天数'])

    yearOwning = ((highPrice - lowPrice)/lowPrice)*(365/expireDays) * 100

    print('期权月份： {} 剩余时间：{}'.format(optionContract, expireDays))
    print('实值期权： {} {}'.format(actualValueOptionData['行权价'], actualValueOptionData['最新价']))
    print('虚值期权:  {} {}'.format(outOftheMoneyOptionData['行权价'], outOftheMoneyOptionData['最新价']))
    print('年化收益率：{}%'.format(yearOwning))

def caculateDownOptionYearOwning(actualValueOptionData, outOftheMoneyOptionData):
    return

def printOptionPrice(optionCode, optionPrice):
    for index, i in enumerate(optionPrice):
        print('期权' + optionCode, index, *i)   

def printOptionCode(optionContract, call_codes, put_codes):
    print('期权月份{} 看涨期权代码：{}\n期权月份{} 看跌期权代码：{}'.format(optionContract, call_codes, optionContract, put_codes))

def getOneOptionContractAllPrice(optionContract, underlying='510050'):
    call_codes, put_codes = get_option_codes(optionContract, underlying)
    allCallPrice = []
    allPutPrice = []

    #printOptionCode(optionContract, call_codes, put_codes)
    for call_code in call_codes:
        optionPrice = get_option_price(call_code)
        allCallPrice.append(optionPrice)
        #printOptionPrice(call_code, optionPrice)

    for put_code in put_codes:
        optionPrice = get_option_price(put_code)
        allPutPrice.append(optionPrice)
        #printOptionPrice(put_code, optionPrice)

    return allCallPrice, allPutPrice

'''
algorithm to find the actual value option and out of money option can change later
'''
def findActualValueAndOutOfMoneyOptions(allCallPrice):

    actualVauleOptionPrice = allCallPrice[0]
    outOfMoneyOptionPrice = allCallPrice[0]
    for call in allCallPrice[1:]:
        if float(call['时间价值']) <= 0 and float(call['行权价']) > float(actualVauleOptionPrice['行权价']):
            actualVauleOptionPrice = call

        if float(call['时间价值']) > float(outOfMoneyOptionPrice['时间价值']):
            outOfMoneyOptionPrice = call

    return actualVauleOptionPrice, outOfMoneyOptionPrice

def timeValueEclapsePolicy(category='50ETF'):
    underlying = 'none'
    if category == '50ETF':
        underlying = '510050'
    elif category == '300ETF':
        underlying = '510300'

    optionContracts = get_option_contracts(category)
    for optionContract in optionContracts: 
        allCallPrice, allPutPrice = getOneOptionContractAllPrice(optionContract, underlying)
        actualVauleOptionPrice, outOfMoneyOptionPrice = findActualValueAndOutOfMoneyOptions(allCallPrice)
        caculateUpOptionYearOwning(optionContract, actualVauleOptionPrice, outOfMoneyOptionPrice)
    
def newTest():
    dates = get_option_contracts(cate='300ETF')
    print('期权合约月份：{}'.format(dates))
 #   for date in dates:
    date = dates[0]
    print('期权月份{}：到期日{} 剩余天数{}'.format(date, *get_option_expire_days(date, cate='300ETF')))
    demo_code = '10002002'

    allCallPrice, allPutPrice = getOneOptionContractAllPrice(date, underlying='510300')

codes={}
def get_option_description_name(code):
    global codes
    price = get_option_price(code)
    '''
    todo: price['期权合约简称'][6:7] is wrong, if month is 2 or 11month, then one is woring, need fix
    '''
    description = str(code) + ' ' + price['期权合约简称'][0:5] + ' ' + price['期权合约简称'][-6:-5] +'month' + price['期权合约简称'][-1:-4]
    if code in codes.keys():
        return codes[code]
    else: 
        codes[code] = description
        return description

def get_current_month_contract():
    '''
    todo: fix this bug month shall format as 01 or 12
    '''
    localtime = time.localtime(time.time())
    month = str(localtime[0]) + '0' + str(localtime[1])

    return '1000' + month[2:]


def get_date():
    '''
    todo: fix this bug month shall format as 01 or 12
    '''
    localtime = time.localtime(time.time())
    date = str(localtime[0])+'-'+ '0' + str(localtime[1])+'-' + str(localtime[2])
    return date

def get_underlying(category='50ETF'):
    underlying = 'none'
    if category == '50ETF':
        underlying = '510050'
    elif category == '300ETF':
        underlying = '510300'
    return  underlying

def store_current_month_contract_kdata(category = '50ETF'):
    underlying = get_underlying(category)
    r = redis.Redis(host='localhost', port=6379, db=0)

    month = get_current_month_contract()
    calls, puts = get_option_codes(month, underlying)

    for call in calls:
        description_name = get_option_description_name(call)
        kdatas = get_option_day_kline(call)
        for kdata in kdatas:
            key = str(description_name) + ' ' + kdata['d']
            value = str(kdata)
            if not r.exists(key):
                r.set(key, value)
                print('set new key {}'.format(key))
            else:
                print('key already exist {}'.format(key))

balance={}
def order(code, type, num):
    global balance
    description = get_option_description_name(code)
    price = get_option_price(code)
    
    if type == 'buy':
        key = (description, price['申卖价一'])
        if key in balance.keys():
            balance[key] += num
        else:
            balance[key] = num
    elif type == 'sell':
        key = (description, price['申买价一'])
        if key in balance.keys():
            balance[key] -= num
        else:
            balance[key] = -num


def caculate_balance(date):
    global balance
    
    pattern = re.compile(r'.*c.*(\d+\.\d+)')
    
    r = redis.Redis(host='localhost', port=6379, db=0)
    #date = get_date()
    owning = 0
    for key in balance.keys():
        num = balance[key]
        old_price = float(key[1])    

        '''
        todo: need use regex to find the price
        '''
        db_key= key[0]+ ' ' + date
        value = str(r.get(db_key))
        m= pattern.match(value)
        new_price = float(m.group(1))
        owning += (new_price - old_price) * num * 10000

        return owning

if __name__ == '__main__':
#    my_test()
#    newTest()
 #   print('start caculate 50ETF owning: ')
 #   timeValueEclapsePolicy(category='50ETF')

  #  print('start caculate 300ETF owning: ')
   # timeValueEclapsePolicy(category='300ETF')


    calls, puts = get_option_codes('10002001', '510300')
 #   printOptionCode(calls)

#     data = get_option_day_kline('10002309')
#     print(data)

#    store_current_month_contract_kdata('50ETF')
#    store_current_month_contract_kdata('300ETF')

    #order('10002196', 'sell', 1)
    #owning = caculate_balance('2020-01-10')
    #print(owning)
    pass