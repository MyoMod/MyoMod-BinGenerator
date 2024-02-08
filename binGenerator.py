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
        data = np.load(filename, allow_pickle=True)

        if "timeArray" in data:
            emgTimes = data["timeArray"]
            emgValues = data["valueArray"]
        elif "eventTimes" in data:
            emgTimes = data["emgTimes"]
            emgValues = data["emgValues"]

            eventData = dict()
            if "eventTimes" in data:
                eventTimes = data["eventTimes"]
                eventValues = data["eventValues"]
            
            eventData["UI-Event"] = np.array([eventTimes, eventValues]).T
        else:
            emgTimes = data["emgTimes"]
            emgValues = data["emgValues"]

            eventData = dict( data)
            del eventData["emgTimes"]
            del eventData["emgValues"]

        # make sure that emgValues is a 2D array
        if len(emgValues.shape) == 1:
            emgValues = emgValues.reshape(1, -1)

        # close file
        data.close()

        return emgTimes, emgValues, eventData

def writeToBinaryFile(filename, data):
    with open(filename, 'wb') as file:
        maxChn = data.shape[0]
        for x in range(0, data.shape[1]):
            for chn in range(6):
                if chn < maxChn:
                    value = data[chn][x]
                else:
                    value = 0

                #invcert this: (((samples<<8)>>8).astype(np.float32)/ 2**23) * 3.
                value = int((value / 3.) * 2**23)
                bytes = value.to_bytes(4, 'little', signed=True)
                file.write(bytes)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='FreeThetics Bin File generator')

    parser.add_argument('fileIn', help='filename to load data to')
    parser.add_argument('fileOut', help='filename to save data to', nargs='?', default="")
    args = parser.parse_args()

    filenameIn = args.fileIn.strip()

    if not os.path.exists(filenameIn):
        print("File does not exist")
        sys.exit(1)

    filenameOut = args.fileOut.strip() if args.fileOut != "" else filenameIn + ".bin"

    _, data, _ = loadFromFile(filenameIn)

    # reverse 1. axis and concatenate
    reversedData = np.fliplr(data)
    
    concatenatedData = np.concatenate((data, reversedData), axis=1)

    writeToBinaryFile(filenameOut, concatenatedData)