import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import argparse
from collections import Counter


sample_freq = {1722 : "0", 953 : "1", 1012 : "2", 1063 : "3", 1187 : "4", 1247 : "5", 1305 : "6", 1429 : "7", 1486 : "8", 1546 : "9", 1131 : "A", 1363 : "B", 1606 : "C", 1835 : "D", 1664: "E"}

def get_freq(data):

    found_frequencies = []

    duration = len(data)/fps
    step = int(len(data)//(duration//0.1))

    for i in range(0, len(data)-step, step):
        signal = data[i:i+step]
        
        frequencies = np.fft.fftfreq(signal.size, d=1/fps)
        amplitudes = np.fft.fft(signal)

        # Low
        i_min = np.where(frequencies > 50)[0][0]
        i_max = np.where(frequencies > 2000)[0][0]
        
        freq = frequencies[i_min:i_max]
        amp = abs(amplitudes.real[i_min:i_max])

        lf = freq[np.where(amp == max(amp))[0][0]]

        delta = 20
        best = 0

        for f in sample_freq:
            if abs(lf-f) < delta:
                delta = abs(lf-f)
                best = f

        found_frequencies.append(best)

    frequencies_count = Counter(found_frequencies)
    found_freq, _ = frequencies_count.most_common(1)[0]
    return found_freq

def get_freq_seq(data, debug):

    found_frequencies = []

    duration = len(data)/fps
    step = int(len(data)//(duration//0.1))

    for i in range(0, len(data)-step, step):
        signal = data[i:i+step]

        if debug:
            plt.subplot(211)
            plt.subplots_adjust(hspace=0.5)
            plt.title("audio (entire signal)")
            plt.plot(data)
            plt.xticks([])
            plt.yticks([])
            plt.axvline(x=i, linewidth=1, color='red')
            plt.axvline(x=i+step, linewidth=1, color='red')
        
        
        frequencies = np.fft.fftfreq(signal.size, d=1/fps)
        amplitudes = np.fft.fft(signal)

        # Low
        i_min = np.where(frequencies > 50)[0][0]
        i_max = np.where(frequencies > 2000)[0][0]
        
        freq = frequencies[i_min:i_max]
        amp = abs(amplitudes.real[i_min:i_max])

        lf = freq[np.where(amp == max(amp))[0][0]]

        delta = 20
        best = 0

        for f in sample_freq:
            if abs(lf-f) < delta:
                delta = abs(lf-f)
                best = f

        if debug:
            plt.subplot(212)
            plt.title("Fourier transform")
            plt.plot(freq, amp)
            plt.annotate(str(int(lf))+"Hz", xy=(lf, max(amp)))

        found_frequencies.append(best)

        if debug:
            plt.show()

    return found_frequencies

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Extract phone numbers from an audio recording of the dial tones.")
    parser.add_argument("-d", "--debug", help="show graphs to debug", action="store_true")
    parser.add_argument('file', type=argparse.FileType('r'))

    args = parser.parse_args()

    fps, data = wavfile.read(args.file.name)
    fps2, data2 = wavfile.read("0.wav")
    print(get_freq(data2))
    print(get_freq_seq(data, args.debug))