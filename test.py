#!/usr/bin/env python3
import multiprocessing


def test1():
    print('I am thread 1')

def test2():
    print('I am thread 2')


if __name__ == "__main__":  # confirms that the code is under main function
    proc1 = multiprocessing.Process(target=test1)
    proc2 = multiprocessing.Process(target=test2)
    proc1.start()
    proc2.start()
    proc1.join()
    proc2.join()