'''
Script to mix two testing samples
'''
import librosa
import numpy as np


# provide the wav name and mix
# speech1 = '/media/nca/data/raw_data/speech_train_r/FCMM0/TRAIN_DR2_FCMM0_SI1957.WAV'
# speech2 = '/media/nca/data/raw_data/speech_train_r/FKLC0/TRAIN_DR4_FKLC0_SX355.WAV'

# FROM TRAINING SET
#speech1 = '/home/eric/deep-clustering/db/train/ange_ansour/ange_ansour-0000120000-0000176000.wav'
#speech2 = '/home/eric/deep-clustering/db/train/bernard_werber/bernard_werber-0000176000-0000232000.wav'

# FROM TEST SET
speech1 = '/home/eric/deep-clustering/db/original/test/barack_obama/02_obama.wav'
speech2 = '/home/eric/deep-clustering/db/original/test/hillary_clinton/02_clinton.wav'

data1, _ = librosa.load(speech1, sr=8000)
data2, _ = librosa.load(speech2, sr=8000)
mix = data1[:len(data2)] + data2[:len(data1)]
librosa.output.write_wav('mix.wav', mix, 8000)
