import serial
import itertools
import matplotlib.pyplot as plt
import numpy
import time
from rich.console import Console
from rich.progress import Progress

KEYS = list("0123456789abcdef")

def print_graph(counts):
    fig, ax = plt.subplots()

    ax.bar(KEYS, counts, label=KEYS)

    ax.set_ylabel('Response times (ns)')
    ax.set_title('Response times per key')
    ax.set_ylim([0,max(counts)])

    plt.show()

def get_header(serial_port, symbol):

    console = Console(log_path=False)
    console.log("[green]Start finding header", log_locals=False)
    while True:
        while(True):
            result = serial_port.readline()
            if("Error" in result.decode()):
                break;
            else:
                serial_port.write((".").encode("ascii"))
                serial_port.flush()

            for combinaison in itertools.product(symbol, repeat=2):
                combinaison_str = ''.join(combinaison)
                console.log(f"Symbol tested : {combinaison_str}", log_locals=False);
                serial_port.write((combinaison_str).encode("ascii"))
                serial_port.flush()

                while(True):
                    result = serial_port.readline()
                    if("Incorrect Header" in result.decode()):
                        break;

                    if("Incorrect Length" in result.decode()):
                        console.log(f"Header found : {combinaison_str}", log_locals=False);
                        return combinaison_str

def find_length(serial_port, prefix):
    console = Console(log_path=False)
    console.log("[green]Start finding length", log_locals=False)
    while True:
        while(True):
            result = serial_port.readline()
            if("over serial" in result.decode()):
                break;
            else:
                serial_port.write((".").encode("ascii"))
                serial_port.flush()

            for i in range(100):
                combinaison_str = prefix + "0"*i
                console.log(f"Symbol tested : {combinaison_str} ({len(combinaison_str)})", log_locals=False);
                serial_port.write((combinaison_str).encode("ascii"))
                serial_port.flush()

                while(True):
                    result = serial_port.readline()
                    if(len(result) > 0):
                        console.log(result.decode())

                    if("Bad CRC" in result.decode()):
                        return combinaison_str

                    if("over serial" in result.decode()):
                        break

def get_CRC(serial_port, symbol):
    prefix = "a504464c4147"

    console = Console()
    console.log("[green]Start finding CRC", log_locals=False)
    while True:
        current_symbol = []

        while(True):
            result = serial_port.readline()
            if("over serial" in result.decode()):
                break;
            else:
                serial_port.write(serial_port.write((".").encode("ascii")))
                serial_port.flush()

        time.sleep(1)
        serial_port.flush()

        for passcode in itertools.combinations_with_replacement(symbol, 2):
            passcode
            while True:
                result = ser.readline()
                if(len(result) > 0):
                    print(result.decode())

                if("over serial" in result.decode()):
                    break

            console.log(f"Testing symbol : {prefix + passcode}")
            serial_port.write(serial_port.write((prefix + passcode).encode("ascii")))
            serial_port.flush()
            start = time.perf_counter_ns()

            while(True):
                result = serial_port.readline()
                if("Incorrect Header" in result.decode()):
                    console.log(result.decode())
                    break

                if("Incorrect Length" in result.decode()):
                    console.log(result.decode())
                    break

                if("not exceed 10" in result.decode()):
                    console.log(result.decode())
                    break

                if("Bad CRC" in result.decode()):
                    console.log(result.decode())
                    break
            
            stop = time.perf_counter_ns()
            result = stop - start
            current_symbol.append(result)

        average = numpy.mean(current_symbol)
        for i in range(len(current_symbol)):
            current_symbol[i] = current_symbol[i] - average

        prefix += symbol[current_symbol.index(numpy.max(current_symbol))]
        console.log(f"Symbol found : {prefix}", log_locals=False);
        print_graph(current_symbol)

ser = serial.Serial('COM3', 115200, timeout=1)
#CRC = get_CRC(ser, KEYS)
#header = get_header(ser, KEYS)
#length = find_length(ser, "a50464c4147")

while True:
    while True:
        result = ser.readline()
        if(len(result) > 0):
            print(result.decode())

        if("over serial" in result.decode()):
            break

    #ser.write(ser.write(("a5" + "f"*16).encode("ascii")))
    ser.write(("a504464c4147da").encode("ascii"))
    ser.flush()
