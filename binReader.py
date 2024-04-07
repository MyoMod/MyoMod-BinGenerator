# import
import numpy as np
import os
import time
from time import perf_counter
import argparse
import tty
import sys
import termios
import threading 

def loadFromFile(filename):
    with open(filename, 'rb') as file:
        fileEnd = False
        minValue = 10000
        maxValue = 0
        while True:
            for chn in range(6):
                bytes = file.read(4)
                if len(bytes) == 0:
                    fileEnd = True
                    break
                value = int.from_bytes(bytes, 'little', signed=True)
                value = value / 2**23 * 3
                if value < minValue:
                    minValue = value
                if value > maxValue:
                    maxValue = value
            if fileEnd:
                break
        print ("Min: ", minValue, "Max: ", maxValue)
        

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='FreeThetics Bin File reader')

    parser.add_argument('fileIn', help='filename to load data to')
    args = parser.parse_args()

    filenameIn = args.fileIn.strip()

    if not os.path.exists(filenameIn):
        print("File does not exist")
        sys.exit(1)

    loadFromFile(filenameIn)