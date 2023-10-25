import argparse
import serial
import matplotlib.pyplot as plt
import numpy
import time
import string
import itertools
import hashlib
from rich.console import Console

KEYS = list("0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~")

def print_graph(counts):
    fig, ax = plt.subplots()

    ax.bar(KEYS, counts, label=KEYS)

    ax.set_ylabel('Response times')
    ax.set_title('Response times per key')
    ax.set_ylim([0,max(counts)])

    plt.show()

def get_username(serial_port, symbol, debug):
    console = Console(log_path=False, log_time=False)
    console.log("[green][+] Start finding username...")

    prefix = ""

    while True:
        current_symbol = []

        while(True):
            result = serial_port.readline()
            if("Invalid" in result.decode()):
                break;
            else:
                serial_port.write(serial_port.write((".").encode("ascii")))
                serial_port.flush()

        for i in range(len(symbol)):
            console.print(f"[green][+] Testing symbol: [cyan][bold]{symbol[i]}[/bold][/cyan] ({i+1} of {len(KEYS)})", end="\r")
            start = time.perf_counter_ns()
            serial_port.write((prefix + symbol[i]).encode("ascii"))
            serial_port.flush()

            while(True):
                result = serial_port.readline()
                if("Invalid" in result.decode()):
                    break;
            
                if("10-digit" in result.decode()):
                    prefix = prefix + symbol[i]
                    console.print("\x20"*50, end="\r")
                    console.log(f"[green][+] Username found : [cyan][bold]{prefix}[/bold][/cyan] !")
                    return prefix
            
            stop = time.perf_counter_ns()
            result = stop - start
            current_symbol.append(result)

        average = numpy.mean(current_symbol)
        for i in range(len(current_symbol)):
            current_symbol[i] = current_symbol[i] - average

        prefix += symbol[current_symbol.index(numpy.max(current_symbol))]
        console.print("\x20"*50, end="\r")
        console.log(f"[green][+] Symbol found : [cyan][bold]{prefix}[/bold][/cyan] !")
        if debug:
            print_graph(current_symbol)

def generate_keypass_hash_list(count=1024):
    console = Console(log_path=False, log_time=False)
    console.log("[green][+] Start generating hash list...")

    hashs = {}
    s = time.time()
    for keypass in itertools.combinations_with_replacement("0123456789", 10):
        if len(hashs)>=count: break
        keypass_str     = str(''.join(keypass))
        hash_hex        = hashlib.sha1(keypass_str.encode('ascii', 'replace')).hexdigest()[:10]
        hashs[hash_hex] = keypass_str
    console.log(f"[green][+] Generate [cyan]{count}[/cyan] pincodes and hashes in [cyan]{(time.time()-s)*1000:0.2f}[/cyan] ms !")
    return hashs

def try_collide(hashs, username):
    console = Console(log_path=False, log_time=False)
    console.log("[green][+] Start finding a collision...")

    c = 0
    temp_speed = time.time()
    s = time.time()
    for i in range(30):
        for passcode in itertools.combinations_with_replacement(string.ascii_lowercase, i):
            passcode_str = username + str(''.join(passcode))
            hash_hex = hashlib.sha1(passcode_str.encode('ascii', 'replace')).hexdigest()[:10]
            if hash_hex in hashs:
                console.log(f'[green][+] Collision found ! hash=[cyan][bold]0x{hash_hex}[/bold][/cyan] pin_code=[cyan][bold]{hashs[hash_hex]}[/bold][/cyan] username=[cyan][bold]{passcode_str}[/bold][/cyan] it took [cyan]{(time.time()-s):0.2f}[/cyan] seconds !')
                return [passcode_str, hashs[hash_hex]]
            
            if c==100000:
                console.print(f"[green][+] Iterations per second :  [cyan]{100000/(time.time()-temp_speed):0.2f}[/cyan] it/s", end='\r')
                temp_speed=time.time()
                c=0

            c += 1

def display_uart(interface, baudrate, credentials):
    serial_port = serial.Serial(interface, baudrate, timeout=1)

    console = Console(log_path=False, log_time=False)
    console.log("[green][+] Start displaying UART output...")
    console.log("[green][+] Reset the board using [cyan][bold]reset[/bold][/cyan] button.", end="\n\n")

    print_mode = 0
    print_count = 0

    while True:
        while True:
            result = serial_port.readline()
            if(len(result) > 0):
                if print_mode == 0:
                    console.log(result.decode(), highlight=False)
                else:
                    console.print(result.decode(), end="", highlight=False)
                    if print_count == 10:
                        print_mode = 0
                        print_count = 0
                        console.print("\n")
                    else:
                        print_count += 1

            if("10-digit MFA" in result.decode()):
                console.log(f"[green][+] Enter pin: [cyan]{credentials[1]}[/cyan]", end="\n\n")
                print_mode = 1

            if("over serial" in result.decode()):
                break

            if("Congrats!!!" in result.decode()):
                exit(0)

        serial_port.write(credentials[0].encode("ascii"))
        serial_port.flush()

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='All White Party challenge solution script.')
    parser.add_argument('-i', '--interface', required=True, help="UART inteface of the Arduino board.")
    parser.add_argument('-b', '--baudrate', required=True, type=int, help="Baudrate of the UART port of the Arduino board.")
    parser.add_argument('-d', '--debug', action='store_true', required=False, default=False, help="Display plot of the timming attack (need to close it to continue the attack).")
    parser.add_argument('-u', '--username', required=False, help="Username you want to try (that will skip the timming attack).")
    args = parser.parse_args()

    serial_port = serial.Serial(args.interface, args.baudrate, timeout=1)
    if(args.username):
        username = args.username
    else:
        username = get_username(serial_port, KEYS, args.debug)

    hash_list = generate_keypass_hash_list(2**16)
    credentials = try_collide(hash_list, username)
    serial_port.close()

    display_uart(args.interface, args.baudrate, credentials)
