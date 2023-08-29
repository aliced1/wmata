#!/usr/bin/env python3
import multiprocessing
import time
import datetime
import pytz
import subprocess
import csv
import schedule

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

    now = datetime.datetime.now(pytz.timezone('US/Eastern'))
    str_time = str(now.hour) + ':' + str(now.minute)
    print(str_time == '19:49')

    