from scipy.io import wavfile
import numpy as np
import argparse
from rich.console import Console
import matplotlib.pyplot as plt

FREQUENCY              = 5    # Hz
HEADER                 = 0xa5 # Message header const
STATE_WAIT_RISING_EDGE = 0x00
STATE_FALLING_EDGE     = 0x01

def print_graph(data, title):
    fig, ax = plt.subplots()

    ax.plot(data)

    ax.set_title(title)
    ax.set_ylim([0,max(data)])

    plt.show()

def moving_average(a, n=3):
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

def sound_to_logicsignal(data, debug):
    """
    This function convert a sound signal to a logic signal, each
    sound peak correspond to a switch of the signal from HIGH to LOW
    or from LOW TO HIGH.

    Parameters
    ----------
        data : list[float] of length n

    Return
    ------
        data : list[int] of length n

    """

    if debug:
        print_graph(data, "Recorded message (raw)")

    # Smooth and normalize the sound signal
    data  = moving_average(abs(data),500)
    data  = data/max(data)

    if debug:
        print_graph(data, "Recorded message (normalized)")

    # Convert the sound signal to a logic signal using 4 states machine
    state   = STATE_WAIT_RISING_EDGE
    is_high = False
    for i in range(len(data)):
        if state == STATE_WAIT_RISING_EDGE:
            if data[i] >= 0.3:
                state   = STATE_FALLING_EDGE
                is_high = not is_high

        elif state == STATE_FALLING_EDGE:
            if data[i] < 0.2:
                state = STATE_WAIT_RISING_EDGE

        # Convert the current float sound value to a logic value of 0 or 1
        data[i] = int(is_high)

    # Return the signal converted to int type
    return np.array(data, dtype='int')

def decode_message(data, debug):
    """
    Read message from signal return a dict with header, msg length, data crc

    Parameters
    ----------
        data : list[int] of length n

    Return
    ------
        msg : dict() ['header','len','data','crc','raw']
    """

    # Skip leading zero
    for i in range(len(data)):
        if data[i] == 1:
            data = data[i::]
            break

    if debug:
        print_graph(data, "Message as binary")
    
    # Cut the signal into array of bytes
    data = [''.join(map(str,np.array(data[i:i + 8],dtype='int'))) for i in range(0, len(data), 8)]
    data = [int(x, 2) for x in data]

    # Create the message dict
    msg = {}
    msg['header'] = data[0]
    msg['len']    = data[1]
    msg['data']   = ''.join([chr(x) for x in data[2:2+msg['len']]])
    msg['crc']    = data[2+ msg['len']]
    msg['raw']    = ''.join([f"{x:02x}" for x in data[:msg['len']+3]])

    return msg

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='SPItFire challenge solution script.')
    parser.add_argument('file', help=".WAV file you want to analyze")
    parser.add_argument('-d', '--debug', action='store_true', required=False, default=False, help="Display plot of the data (need to close it to continue the decode).")
    args = parser.parse_args()

    console = Console(log_path=False, log_time=False)
    console.log("[green][+] Start decoding the audio file...")

    rate, data = wavfile.read(args.file)

    # Retreive only one channel of the wavfile
    data = data.T[0]

    # Convert the sound to a logic signal
    data = sound_to_logicsignal(data, args.debug)

    # Set the sampling frequency to 5Hz
    sampling_freq = rate // FREQUENCY
    data = data[::sampling_freq]

    # Decode the message from the logic signal
    msg = decode_message(data, args.debug)

    # Check if the header is correct (0xa5)
    assert msg['header'] == HEADER, "Header is not valid !"

    console.log(f"[green][+] Decoded message {{length=[cyan][bold]{msg['len']}[/bold][/cyan] data='[cyan][bold]{msg['data']}[/bold][/cyan]' CRC=[cyan][bold]{msg['crc']:#02x}[/bold][/cyan] raw='[cyan][bold]{msg['raw']}[/bold][/cyan]'}}")