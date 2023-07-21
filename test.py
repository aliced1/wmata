#!/usr/bin/env python3
from threading import Timer

def hello():
    print("hello, world")


t = Timer(2.0, hello)

while(True):
    t.start()  # after 30 seconds, "hello, world" will be printed