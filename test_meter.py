
import numpy as np
import sys

import pymongo
import collections
from nltk.tokenize import word_tokenize
import pronouncing
import unicodedata
import pywt
import random

signal = [1, 0, 0, 0] * 100
for i in range(len(signal)):
    if random.random() < 0.2:
        signal[i] = int(round(random.random()))
        
c_a, c_d = pywt.dwt(signal, 'haar')
for i, j in enumerate(signal):
    print(i, j)
print('')
# for i in c_a:
#     print i
# print ''
# for i in c_d:
#     print i
# print ''
ps = np.abs(np.fft.fft(signal))**2
# for i, j in enumerate(ps):
#     print i, j
time_step = 1 / 1
freqs = np.fft.fftfreq(len(signal), time_step)
print(freqs, file=sys.stderr)
idx = np.argsort(freqs)

for x, y in zip(freqs[idx], ps[idx]):
    print(x, y)
