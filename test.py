#!/usr/bin/env python3
import multiprocessing
import time
import datetime
import pytz
import subprocess


# def test1():
#     print('I am thread 1')

# def test2():
#     print('I am thread 2')


def profile_test():
    current_time = datetime.datetime.now(pytz.timezone('US/Eastern'))
    print(current_time)    

if __name__ == "__main__":  # confirms that the code is under main function
    # flag = multiprocessing.Value('i', 0)
    # proc1 = multiprocessing.Process(target=test1, args=(flag,))
    # proc2 = multiprocessing.Process(target=test2)
    # proc1.start()
    # proc2.start()
    # proc1.join()
    # proc2.join()
    profile_test()