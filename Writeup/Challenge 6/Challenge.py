import serial
import time
from rich.console import Console
import argparse

parser = argparse.ArgumentParser(description='VenderBender challenge solution script.')
parser.add_argument('-i', '--interface', required=True, help="UART inteface of the Arduino board.")
parser.add_argument('-b', '--baudrate', required=True, type=int, help="Baudrate of the UART port of the Arduino board.")

args = parser.parse_args()

serial_port = serial.Serial(args.interface, args.baudrate)

console = Console(log_path=False, log_time=False)
console.log("[green][+] Breaking vendor machine security...")

while True:
    result = serial_port.readline()
    serial_port.write(".".encode("ascii"))
    serial_port.flush()
    if "SUCCESS" in result.decode():
        break

while True:
    for i in range(700, 2500, 10):

        time.sleep(1125/1000)
        serial_port.write("ERR".encode("ascii"))
        serial_port.flush()
        
        while True:
            result = serial_port.readline()

            if "/5" in result.decode():
                console.print(f"[green][+] {result.decode()}", end='\r')

            if "5902" in result.decode():
                time.sleep(470/1000)
                serial_port.write("ERR".encode("ascii"))
                serial_port.flush()
                time.sleep(1650/1000)
                serial_port.write("ERR".encode("ascii"))
                serial_port.flush()
                time.sleep(1488/1000)
                serial_port.write("ERR".encode("ascii"))
                serial_port.flush()
                time.sleep(1630/1000)
                serial_port.write("ERR".encode("ascii"))
                serial_port.flush()
                time.sleep(i/1000)
                break

            if "BEAT" in result.decode():
                console.print(result.decode())
                while True:
                    result = serial_port.readline()
                    if len(result) > 0:
                        console.print(result.decode())
                    if "Congrats" in result.decode():
                        exit(0)
            
            if "ERR" in result.decode():
                console.print("[green][-] Attempt Failed")
                break
