import time
import json

data = 'thisisoneday'

data = data.replace('day', 'mmmmmm')

t1 = time.time()
localtime = time.localtime(t1)


t2 = time.mktime((2020, 2, 12, 0, 0, 0, 0, 0, 0))

t3 = '{}-{:02d}-{:02d}'.format(localtime[0], localtime[1], localtime[2])
month = str(localtime[0]) + '0' + str(localtime[1])
print(localtime)



data = "{'day': '2019-12-30', 'open': '3.005', 'high': '3.058', 'low': '2.999', 'close': '3.051', 'volume': '571400064'}"
data = data.replace('\'', '\"')
data = json.loads(data)
pass 