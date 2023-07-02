#!/usr/bin/python3
import random
import time

from simplecanvas import run_function


def func(canvas):
    for i in range(canvas.height):
        canvas[i, i] = i

    while True:
        canvas[random.randrange(canvas.width), random.randrange(canvas.height)] = random.randrange(128)
        time.sleep(0.1)


if "__main__" == __name__:
    run_function(func, width=100, height=100)