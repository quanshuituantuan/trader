#!python3
#from json import loads
#from requests import get
import json
import requests
import time

class OptionData:
    def __init__(self, category='50ETF'):
        self.category = category
        self.underlying = '510050'
        if category == '50ETF':
            self.underlying = '510050'
        elif category == '300ETF':
            self.underlying = '510300'
        
        self.contract = {}

    def get_option_contracts(self, exchange='null'):
        url = f"http://stock.finance.sina.com.cn/futures/api/openapi.php/StockOptionService.getStockName?" \
            f"exchange={exchange}&cate={self.category}"
        dates = requests.get(url).json()['result']['data']['contractMonth']
        self.contracts = [''.join(i.split('-')) for i in dates][1:]
        return self.contracts
    
    
    def get_option_expire_days(self, date, exchange='null'):
        url = "http://stock.finance.sina.com.cn/futures/api/openapi.php/StockOptionService.getRemainderDay?" \
            "exchange={exchange}&cate={cate}&date={year}-{month}"
        url2 = url.format(year=date[:4], month=date[4:], cate=self.category, exchange=exchange)
        data = requests.get(url2).json()['result']['data']
        if int(data['remainderDays']) < 0:
            url2 = url.format(year=date[:4], month=date[4:], cate='XD' + self.category, exchange=exchange)
            data = requests.get(url2).json()['result']['data']
        
        self.expire_day = data['expireDay']
        self.remainder_days = data['remainderDays']
        return self.expire_day, self.remainder_days
    
    
    def get_option_codes(self, date):
        url_up = ''.join(["http://hq.sinajs.cn/list=OP_UP_", self.underlying, str(date)[-4:]])
        url_down = ''.join(["http://hq.sinajs.cn/list=OP_DOWN_", self.underlying, str(date)[-4:]])
        data_up = str(requests.get(url_up).content).replace('"', ',').split(',')
        codes_up = [i[7:] for i in data_up if i.startswith('CON_OP_')]
        data_down = str(requests.get(url_down).content).replace('"', ',').split(',')
        codes_down = [i[7:] for i in data_down if i.startswith('CON_OP_')]
        self.call_codes = codes_up
        self.put_codes = codes_down

        return self.call_codes, self.put_codes
    

    def get_option_price(self, code):
        url = "http://hq.sinajs.cn/list=CON_OP_{code}".format(code=code)
        data = requests.get(url).content.decode('gbk')
        data = data[data.find('"') + 1: data.rfind('"')].split(',')
        fields = ['买量', '买价', '最新价', '卖价', '卖量', '持仓量', '涨幅', '行权价', '昨收价', '开盘价', '涨停价',
                '跌停价', '申卖价五', '申卖量五', '申卖价四', '申卖量四', '申卖价三', '申卖量三', '申卖价二',
                '申卖量二', '申卖价一', '申卖量一', '申买价一', '申买量一 ', '申买价二', '申买量二', '申买价三',
                '申买量三', '申买价四', '申买量四', '申买价五', '申买量五', '行情时间', '主力合约标识', '状态码',
                '标的证券类型', '标的股票', '期权合约简称', '振幅', '最高价', '最低价', '成交量', '成交额',
                '分红调整标志', '昨结算价', '认购认沽标志', '到期日', '剩余天数', '虚实值标志', '内在价值', '时间价值']
        self.result = dict(zip(fields, data))
        return self.result
    
    
    def get_underlying_ETF_price(self):
        url = "http://hq.sinajs.cn/list=sh" + self.underlying
        data = requests.get(url).content.decode('gbk')
        data = data[data.find('"') + 1: data.rfind('"')].split(',')
        fields = ['证券简称', '今日开盘价', '昨日收盘价', '最近成交价', '最高成交价', '最低成交价', '买入价',
                '卖出价', '成交数量', '成交金额', '买数量一', '买价位一', '买数量二', '买价位二', '买数量三',
                '买价位三', '买数量四', '买价位四', '买数量五', '买价位五', '卖数量一', '卖价位一', '卖数量二',
                '卖价位二', '卖数量三', '卖价位三', '卖数量四', '卖价位四', '卖数量五', '卖价位五', '行情日期',
                '行情时间', '停牌状态']
        self.etf_price = dict(zip(fields, data))
        return self.etf_price
    

    def get_option_greek_alphabet(self, code):
        url = "http://hq.sinajs.cn/list=CON_SO_{code}".format(code=code)
        data = requests.get(url).content.decode('gbk')
        data = data[data.find('"') + 1: data.rfind('"')].split(',')
        fields = ['期权合约简称', '成交量', 'Delta', 'Gamma', 'Theta', 'Vega', '隐含波动率', '最高价', '最低价',
                '交易代码', '行权价', '最新价', '理论价值']
        self.alphabet = list(zip(fields, [data[0]] + data[4:])) 
        return self.alphabet
 
    def get_option_time_line(self, code):
        url = f"https://stock.finance.sina.com.cn/futures/api/openapi.php/StockOptionDaylineService.getOptionMinline?" \
            f"symbol=CON_OP_{code}"
        data = requests.get(url).json()['result']['data']
        return data
    
    
    def get_option_day_kline(self, code):
        url = f"http://stock.finance.sina.com.cn/futures/api/jsonp_v2.php//StockOptionDaylineService.getSymbolInfo?" \
            f"symbol=CON_OP_{code}"
        data = requests.get(url).content
        data = json.loads(data[data.find(b'(') + 1: data.rfind(b')')])
        return data

    #50ETF kdata
    #http://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol=sh510050&scale=240&ma=no&datalen=250
    def get_etf_day_kline(self):
        url = f"http://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?" \
            f"symbol=sh{self.underlying}&scale=240&ma=no&datalen=250"
        data = requests.get(url).content
        data = data.decode('GBK')
        # data = data.replace('day', '\"day\"').replace('volume', '\"volume\"')
        # data = data.replace('open', '\"open\"').replace('close', '\"close\"')
        # data = data.replace('high', '\"high\"').replace('low', '\"low\"')

        data = json.loads(data)
        return data

    def getOneOptionContractAllPrice(self, optionContract):
        call_codes, put_codes = self.get_option_codes(optionContract)
        etf_price = self.get_underlying_ETF_price()

        allCallPrice = []
        allPutPrice = []

        #printOptionCode(optionContract, call_codes, put_codes)
        for call_code in call_codes:
            optionPrice = self.get_option_price(call_code)

            #optionPrice['bail'] = self.call_bail(call_code)
            name = float(optionPrice['行权价'])
            price = float(optionPrice['最新价'])
            etf = float(etf_price['最近成交价'])
            bail = (price+max((0.12*etf-max(0, (name-etf))), 0.07*etf ))*10000
            optionPrice['bail'] = bail
            allCallPrice.append(optionPrice)
            #printOptionPrice(call_code, optionPrice)

        for put_code in put_codes:
            optionPrice = self.get_option_price(put_code)

            #optionPrice['bail'] = self.put_bail(put_code)
            name = float(optionPrice['行权价'])
            price = float(optionPrice['最新价'])
            etf = float(etf_price['最近成交价'])
            bail = min(price+max((0.12*etf-max(0, etf - name)), 0.07*name), name)*10000
            optionPrice['bail'] = bail
            allPutPrice.append(optionPrice)
            #printOptionPrice(put_code, optionPrice)

        return allCallPrice, allPutPrice

    '''
    data structure for all call prices or put prices

    [{'name': 2700, sellprice': 0.11, 'buyprice':0.12, 'remainday':15, 'optionvalue':450, 'timevalue':200}, {}]
    '''
    def get_option_all_prices(self, optionContract):
        call_prices, put_prices = self.getOneOptionContractAllPrice(optionContract)
        
        new_call_prices = []
        for call in call_prices:
            price = {}
            price['name'] = float(call['行权价'])*1000
            price['sellprice'] = float(call['申卖价一'])
            price['buyprice'] = float(call['申买价一']) 
            price['remainday'] = int(call['剩余天数'])
            price['optionvalue'] = float(call['内在价值'])
            price['timevalue'] = float(call['时间价值'])
            price['bail'] = call['bail']
            new_call_prices.append(price)

        new_put_prices = []
        for put in put_prices:
            price = {}
            price['name'] = float(put['行权价'])*1000
            price['sellprice'] = float(put['申卖价一'])  
            price['buyprice'] = float(put['申买价一'])
            price['remainday'] = int(put['剩余天数'])
            price['optionvalue'] = float(put['内在价值'])
            price['timevalue'] = float(put['时间价值'])
            price['bail'] = put['bail']
            new_put_prices.append(price)

        self.contract[str(optionContract) + 'call'] = new_call_prices
        self.contract[str(optionContract) + 'put'] = new_put_prices  

        #print(self.contract)
        for call in self.contract[str(optionContract)+'call']:
            print(call)
        
        return new_call_prices, new_put_prices

#公式：
#1、认购期权义务仓开仓保证金=[合约前结算价+Max(12%×合约标的前收盘价-认购期权虚值，7%×合约标的前收盘价)]×合约单位
#2、认沽期权义务仓开仓保证金=Min[合约前结算价+Max(12%×合约标的前收盘价-认沽期权虚值，7%×行权价格)，行权价格] ×合约单位
#例子：
#投资者卖出行权价是2.3的认购实值期权合约为例，其权利金为0.332点，50ETF价格
#此时为2.635， 该认购期权的虚值为0【max（2.3-2.635， 0）】则其维持保证金需缴纳
#【0.332+max（12%*2.635 -0， 7% *2.635）】*1000， 既投资者账号保证金至少为6482.
#若卖出行权价是2.3点的虚值认沽期权，权利金是0.0001，该认沽期权的虚值为
#0.335【max（2.635-2.3， 0）】，则其保证金是
#Min{【0.0001+max（12%*2.635-0.335，7%*2.3）】，2.3}*10000， 既保证金需要1611元
    def call_bail(self, code):
        price_temp = self.get_option_price(code)
        etf = self.get_underlying_ETF_price()

        name = float(price_temp['行权价'])
        price = float(price_temp['最新价'])
        etf = float(etf['最近成交价'])
        bail = (price+max((0.12*etf-max(0, (name-etf))), 0.07*etf ))*10000
        print('行权价：{}， 保证金：{}'.format(price_temp['行权价'], bail))
        return bail


    def put_bail(self, code):
        price = self.get_option_price(code)
        etf = self.get_underlying_ETF_price()

        name = float(price['行权价'])
        price = float(price['最新价'])
        etf = float(etf['最近成交价'])
        bail = min(price+max((0.12*etf-max(0, etf - name)), 0.07*name), name)*10000
        print('行权价：{}， 保证金：{}'.format(name, bail))
        return bail


def testETFdata():
    etf = OptionData(category = '50ETF')
    contracts = etf.get_option_contracts()
    print('期权合约月份：{}'.format(contracts))
    for contract in contracts:
        print('期权月份{}：到期日：{} 剩余天数{}'.format(contract, *etf.get_option_expire_days(contract)))
#        call_codes, put_codes = etf.get_option_codes(contract)
#        for call in call_codes:
#            Price = etf.get_option_price(call)
 
        #self.call_prices, self.put_prices = etf.getOneOptionContractAllPrice(contract)
        etf.get_option_all_prices(contract)

if __name__ == '__main__':
    #testETFdata()
    etf = OptionData('50ETF')
 #   data = etf.get_etf_day_kline()
    call_codes, put_codes = etf.get_option_codes('202002')
    for call in call_codes: 
        etf.call_bail(call)
    
    for put in put_codes:
        etf.put_bail(put)
 #   print(etf.call_bail(10002309))
 #   print(etf.put_bail(10002312))
    pass
     