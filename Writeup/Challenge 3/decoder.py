from scipy.io import wavfile
import numpy as np
from matplotlib import pyplot as plt

FREQUENCY = 5    # Hz
HEADER    = 0xa5 # Message header const

def moving_average(a, n=3):
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

def process_sound(rate, data):
    data  = moving_average(abs(data),500)
    max_v = max(data)
    data  = data/max_v

    state = 0
    for i in range(len(data)):
        if state == 0:
            if data[i] >= 0.3:
                state = 1
        elif state == 1:
            if data[i] < 0.2:
                state = 2
        elif state == 2:
            if data[i] >= 0.3:
                state = 3
        elif state == 3:
            if data[i] < 0.2:
                state = 0

        data[i] = 1 if state in [1,2] else 0

    sampling_freq = rate // FREQUENCY
    data = data[::sampling_freq]

    for i in range(len(data)):
        if data[i] == 1:
            data = data[i::]
            break

    data = [''.join(map(str,np.array(data[i:i + 8],dtype='int'))) for i in range(0, len(data), 8)]
    data = [int(x, 2) for x in data]

    msg_header = data[0]
    msg_len    = data[1]
    msg_data   = ''.join([chr(x) for x in data[2:2+msg_len]])
    msg_crc    = data[2+msg_len]
    msg_raw    = ''.join([f"{x:02x}" for x in data[:msg_len+3]])

    if(msg_header != HEADER):
        raise Exception("Header is not valid !")

    print(f"Message{{length={msg_len} data='{msg_data}' CRC={msg_crc:#02x} raw='{msg_raw}'}}")

    return msg_raw


if __name__ == '__main__':
    rate, data = wavfile.read('flag.wav')
    process_sound(rate, data.T[0])

