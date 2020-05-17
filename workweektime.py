
import time,datetime

def get_week_day(date):
    week_day_dict = {
      0 : '星期一',
      1 : '星期二',
      2 : '星期三',
      3 : '星期四',
      4 : '星期五',
      5 : '星期六',
      6 : '星期天',
    }
    day = date.weekday()
    return week_day_dict[day]

if __name__ == "__main__":
    print(get_week_day(datetime.datetime.now()))

    now = datetime.datetime.now()
    print(now)
    print(now.hour)
    # h = now.tm_hour
    # print(h)
    pass
