import random
import curses
import time
from Menu import MyApp

def main(sc):
    myApp = MyApp(sc)

if __name__ == '__main__':
    curses.wrapper(main)
