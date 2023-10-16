import serial
import matplotlib.pyplot as plt
import numpy
import time

KEYS="1234567890"

def print_graph(counts):
    fig, ax = plt.subplots()

    ax.bar(KEYS, counts, label=KEYS)

    ax.set_ylabel('Response times (ns)')
    ax.set_title('Response times per key')
    ax.set_ylim([0,max(counts)])

    plt.show()

ser = serial.Serial('COM3', 115200, timeout=1)
graph = []

for i in range(10):
    while(True):
        result = ser.readline()
        if("10-digit" in result.decode()):
            break;
        else:
            ser.write(ser.write(("Barry").encode()))
            ser.flush()

    pin = 0
    print("Waiting for input\n")
    while(True):
        result = ser.readline()
        if(len(result)>0 and result.decode() in "0123456789"):
            pin = pin+1

        if(pin <= 10):
            break;
    
    start = time.perf_counter_ns()

    while(True):
        result = ser.readline()
        if("not match" in result.decode()):
            break;

    stop = time.perf_counter_ns()
    result = stop - start
    print(f"Result {result}")
    graph.append(result)

average = numpy.mean(graph)
for i in range(len(graph)):
    graph[i] = graph[i] - average

print_graph(graph)