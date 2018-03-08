'''
Script to mix two testing samples
'''
import librosa
import numpy as np

SAMPLE_RATE = 8000

speech1 = '/home/eric/deep-clustering/db/original/test/hillary_clinton/01_clinton.wav'
speech2 = '/home/eric/deep-clustering/db/original/test/barack_obama/02_obama.wav'


# generating partial overlap mixtures

data1, _ = librosa.load(speech1, sr=SAMPLE_RATE)

empty_third = np.zeros(len(data1)/3)

two_thirds = data1[0:-len(data1)/3]

data1 = np.array(list(empty_third) + list(two_thirds))

data2, _ = librosa.load(speech2, sr=SAMPLE_RATE)

empty_third = np.zeros(len(data2)/3)

two_thirds = data2[0:-len(data2)/3]

data2 = np.array(list(two_thirds) + list(empty_third))

mix = data1[:len(data2)] + data2[:len(data1)]

librosa.output.write_wav('mix.wav', mix, 8000)
librosa.output.write_wav('spkr1.wav', data1, 8000)
librosa.output.write_wav('spkr2.wav', data2, 8000)
