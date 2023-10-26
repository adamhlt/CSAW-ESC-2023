#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import argparse

dtmf = {(697, 1209): "1", (697, 1336): "2", (697, 1477): "3", (770, 1209): "4", (770, 1336): "5", (770, 1477): "6", (852, 1209): "7", (852, 1336): "8", (852, 1477): "9", (941, 1209): "*", (941, 1336): "0", (941, 1477): "#", (697, 1633): "A", (770, 1633): "B", (852, 1633): "C", (941, 1633): "D"}


parser = argparse.ArgumentParser(description="Extract phone numbers from an audio recording of the dial tones.")
parser.add_argument("-v", "--verbose", help="show a complete timeline", action="store_true")
parser.add_argument("-l", "--left", help="left channel only (if the sound is stereo)", action="store_true")
parser.add_argument("-r", "--right", help="right channel only (if the sound is stereo)", action="store_true")
parser.add_argument("-d", "--debug", help="show graphs to debug", action="store_true")
parser.add_argument("-t", type=int, metavar="F", help="acceptable frequency error (in hertz, 20 by default)", default=20)
parser.add_argument("-i", type=float, metavar='T', help="process by T seconds intervals (0.04 by default)", default=0.04)

parser.add_argument('file', type=argparse.FileType('r'))

args = parser.parse_args()


file = args.file.name
try:
    fps, data = wavfile.read(file)
except FileNotFoundError:
    print ("No such file:", file)
    exit()
except ValueError:
    print ("Impossible to read:", file)
    print("Please give a wav file.")
    exit()


if args.left and not args.right:
    if len(data.shape) == 2 and data.shape[1] == 2:
        data = np.array([i[0] for i in data])
    elif len(data.shape) == 1:
        print ("Warning: The sound is mono so the -l option was ignored.")
    else:
        print ("Warning: The sound is not mono and not stereo ("+str(data.shape[1])+" canals)... so the -l option was ignored.")


elif args.right and not args.left:
    if len(data.shape) == 2 and data.shape[1] == 2:
        data = np.array([i[1] for i in data])
    elif len(data.shape) == 1:
        print ("Warning: the sound is mono so the -r option was ignored.")
    else:
        print ("Warning: The sound is not mono and not stereo ("+str(data.shape[1])+" canals)... so the -r option was ignored.")

else:
    if len(data.shape) == 2: 
        data = data.sum(axis=1) # stereo

precision = args.i

duration = len(data)/fps

step = int(len(data)//(duration//precision))

debug = args.debug
verbose = args.verbose
c = ""

if debug:
    print("Warning:\nThe debug mode is very uncomfortable: you need to close each window to continue.\nFeel free to kill the process doing CTRL+C and then close the window.\n")

if verbose:
    print ("0:00 ", end='', flush=True)

try:
    for i in range(0, len(data)-step, step):
        signal = data[i:i+step]

        if debug:
            plt.subplot(311)
            plt.subplots_adjust(hspace=0.5)
            plt.title("audio (entire signal)")
            plt.plot(data)
            plt.xticks([])
            plt.yticks([])
            plt.axvline(x=i, linewidth=1, color='red')
            plt.axvline(x=i+step, linewidth=1, color='red')
            plt.subplot(312)
            plt.title("analysed frame")
            plt.plot(signal)
            plt.xticks([])
            plt.yticks([])
        
        
        frequencies = np.fft.fftfreq(signal.size, d=1/fps)
        amplitudes = np.fft.fft(signal)

        # Low
        # i_min = np.where(frequencies > 0)[0][0]
        # i_max = np.where(frequencies > 1050)[0][0]
        
        freq = frequencies[:]
        amp = abs(amplitudes.real[:])

        lf = freq[np.where(amp == max(amp))[0][0]]

        delta = args.t

        if debug:
            plt.subplot(313)
            plt.title("Fourier transform")
            plt.plot(freq, amp)
            ax = plt.gca()
            ax.set_ylim([0,200000])
            plt.yticks([])
            plt.annotate(str(int(lf))+"Hz", xy=(lf, max(amp)))

        if debug:
            plt.show()

    print()

except KeyboardInterrupt:
    print("\nCTRL+C detected: exiting...")