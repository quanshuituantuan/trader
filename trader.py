#!python3

class ITrader():
    def __init__(self):
        pass

    def order(self):
        pass


class FakeOptionTrader(ITrader):
    def __init__(self):
        self.balance = {}
        self.balance['owning'] = 0.0
        self.history = []


    def order(self, type, price, num):
        " type: buy call, buy call close, sell call, sell call close"
        
        event = type + ' ' + str(price['name']) + ' '+str(price['sellprice']) + ' '+str(num)
        self.history.append(event)

        if type == 'buy call':
            type = type + ' ' + str(price['name'])
            if type in self.balance.keys():
                self.balance[type][1] += num
            else:
                self.balance[type] = [price['sellprice'], num]
                
        elif type == 'sell call':
            type = type + ' ' + str(price['name'])
            if type in self.balance.keys():
                self.balance[type][1] += num
            else:
                self.balance[type] = [price['buyprice'], num]
        elif type.find('close') :
            type = type.replace('close', '') + str(price['name'])
            data = self.balance[type]
            if data :
                if 'buy' in type: 
                    own = (float(price['sellprice'])- float(data[0]))*num
                    self.balance[type][1] -= num
                    self.balance['owning'] +=own
                else:
                    own = (float(data[0])-float(price['sellprice']))*num
                    self.balance[type][1] -= num
                    self.balance['owning'] +=own
            else:
                print('error, can not close contract')

        pass



    def get_balance(self):
        return self.balance

    def get_owning(self):
        return self.balance['owning']*10000

    def get_fee(self):

        pass