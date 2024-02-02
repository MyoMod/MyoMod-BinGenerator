import math
P = 2 * math.pi
channelNum = 6
channelOffset = 1 / channelNum
dataLen = 1000000
sampleRate = 1000
f = 0.1

fileName = 'binaryfile2.bin'

file = open(fileName, 'wb')
try:

    for x in range(0, dataLen):
        for chn in range(6):
            phase = f * x / sampleRate
            value = math.sin(P * (phase + chn * channelOffset)) * ((1<<20))
            value = int(value)
            bytes = value.to_bytes(4, 'little', signed=True)
            file.write(bytes)
finally:
    ### Close the file

    file.close()