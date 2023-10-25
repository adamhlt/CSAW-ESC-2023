import serial
import argparse
from rich.console import Console

def A008336(n):
    a008336_list = [1]
    for i in range(1, n):
        a008336_list.append(a008336_list[i-1] // i if a008336_list[i-1] % i == 0 else a008336_list[i-1] * i)
    return a008336_list[n-1]

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='czNxdTNuYzM challenge solution script.')
    parser.add_argument('-i', '--interface', required=True, help="UART inteface of the Arduino board.")
    parser.add_argument('-b', '--baudrate', required=True, type=int, help="Baudrate of the UART port of the Arduino board.")
    args = parser.parse_args()

    console = Console(log_path=False, log_time=False)
    console.log("[green][+] Start sending the flag...")

    serial_port = serial.Serial(args.interface, args.baudrate, timeout=1)

    while True:
        while True:
            result = serial_port.readline()
            if(len(result) > 0):
                print(result.decode())

            if("over serial" in result.decode()):
                break

            if("Congrats!!!" in result.decode()):
                exit(0)

        flag = A008336(25)
        console.log(f"[green][+] Sending the flag: [cyan][bold]{flag}[/bold][/cyan] (element 25 of OEIS A008336) !")
        serial_port.write(str(flag).encode("ascii"))
        serial_port.flush()