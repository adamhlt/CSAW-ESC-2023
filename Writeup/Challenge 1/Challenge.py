import serial
import matplotlib.pyplot as plt
import numpy
import time

def print_graph(counts):
    fig, ax = plt.subplots()

    ax.bar(KEYS, counts, label=KEYS)

    ax.set_ylabel('Response times (ns)')
    ax.set_title('Response times per key')
    ax.set_ylim([0,max(counts)])

    plt.show()

KEYS = list("123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~")
#KEYS = ''.join([chr(i) for i in range(128)])

ser = serial.Serial('COM3', 115200, timeout=1)
graph = []

while(True):
    result = ser.readline()
    if("Invalid" in result.decode()):
        break;
    else:
        ser.write(ser.write(("test").encode()))
        ser.flush()

for i in range(len(KEYS)):
    start = time.perf_counter_ns()
    ser.write(("Barr" + KEYS[i] + '\n').encode())
    ser.flush()

    while(True):
        result = ser.readline()
        if("Invalid" in result.decode() or "10-digit" in result.decode()):
            break;
    
    stop = time.perf_counter_ns()
    result = stop - start
    print(f"Result for {KEYS[i]} is : {result}")
    graph.append(result)

average = numpy.mean(graph)
for i in range(len(graph)):
    graph[i] = graph[i] - average

print_graph(graph)