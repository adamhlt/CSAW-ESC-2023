import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import argparse

sample_freq = {1722 : "0", 953 : "1", 1012 : "2", 1063 : "3", 1187 : "4", 1247 : "5", 1305 : "6", 1429 : "7", 1486 : "8", 1540 : "9", 1131 : "A", 1363 : "B", 1606 : "C", 1835 : "D", 1664: "*"}

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
            plt.yticks([])

        found_frequencies.append(best)

        if debug:
            plt.show()

    return found_frequencies

def regroup_freq(freqs):

    if not freqs:
        return []

    resultat = []
    count = 1

    for i in range(1, len(freqs)):
        
        if freqs[i] != freqs[i - 1] and freqs[i] != 0 and freqs[i-1] != 0:
            
            if freqs[i-1] == 0:
                pass

            if count >= 8:
                resultat.append(freqs[i-1])
                resultat.append(freqs[i-1])
                count = 1
            else:
                resultat.append(freqs[i-1])
                count = 1
        else:
            count += 1

    for i in range(len(freqs) - 1, -1, -1):
        if freqs[i] != 0:
            resultat.append(freqs[i])
            break

    return resultat
        
def get_key_from_freqs(freqs):

    key = ""
    for freq in freqs:
        key += sample_freq[freq]

    return key

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Extract phone numbers from an audio recording of the dial tones.")
    parser.add_argument("-d", "--debug", help="show graphs to debug", action="store_true")
    parser.add_argument('file', type=argparse.FileType('r'))

    args = parser.parse_args()

    fps, data = wavfile.read(args.file.name)
    freqs = get_freq_seq(data, args.debug)

    final_freqs = regroup_freq(freqs)

    key = get_key_from_freqs(final_freqs)
    print(key)