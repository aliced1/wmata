#!/usr/bin/env python3

import pytz
from datetime import datetime, timedelta, date
import pytz


# def job():
#     print("I'm working...")
#     return

if __name__ == "__main__":  # confirms that the code is under main function
    # schedule.every().day.at("02:00", 'US/Eastern').do(job)
    # # schedule.every().minute.at(":47").do(job)

    # while True:
    #     schedule.run_pending()
    #     print(schedule.idle_seconds(), datetime.datetime.now(pytz.timezone('US/Eastern')))
    #     time.sleep(1) # wait one minute

    # now = datetime.datetime.now(pytz.timezone('US/Eastern'))
    # str_time = str(now.hour) + ':' + str(now.minute)
    # print(str_time == '19:49')

    # today_at_6 = datetime.combine(datetime.date.fromtimestamp(datetime.now(pytz.timezone('US/Eastern')).timestamp()), datetime.min.time()) + timedelta(hours=18)

    print(datetime.now(pytz.timezone('US/Eastern')).date())
    
    
# insertion_date = dateutil.parser.parse('2018-03-13T17:22:20.065Z')
# diffretiation = pytz.utc.localize(datetime.datetime.utcnow()) - insertion_date

    # print(today_at_6)
    # print(row_time)
    # print(now_local)
    # print(diffretiation)

    