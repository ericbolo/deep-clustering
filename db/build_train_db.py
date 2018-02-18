'''
Builds a training audio db from mp3: trimming, converting to wav, splitting into chunks
'''

import os
import subprocess
from train_file_index import files

CHUNK_LENGTH = 3  # in seconds
DB_PATH = '/home/eric/deep-clustering/db'
WAV_PATH = os.path.join(DB_PATH, 'wav')
TRAIN_DB_PATH = os.path.join(DB_PATH, 'train')

SAMPLE_RATE = 8000

# converting to wav
try:
    os.makedirs(WAV_PATH)
except FileExistsError:
    pass

def get_wave_name(mp3_path):
    return mp3_path.split('/')[-1].split('.')[0]+'.wav'

for speaker in files:
    speaker_dir = os.path.join(WAV_PATH, speaker)
    try:
        os.makedirs(speaker_dir)
    except FileExistsError:
        pass

    for file in files[speaker]:
        wave_name = get_wave_name(file['path'])
        wave_file_path = os.path.join(speaker_dir,
                                      wave_name)
        command = "ffmpeg -i {}  -ac 1 -ar {} {}".format(
            file['path'],
            SAMPLE_RATE,
            wave_file_path
        )
        output = subprocess.check_output(['bash','-c', command])

# splitting audio into chunks of CHUNK_LENGTH seconds
for speaker in files:
    speaker_dir = os.path.join(TRAIN_DB_PATH, speaker)
    try:
        os.makedirs(speaker_dir)
    except FileExistsError:
        pass

    for file in files[speaker]:
        wave_name = get_wave_name(file['path'])
        wave_file_path = os.path.join(WAV_PATH, speaker, wave_name)

        # python ../audiocut/audiocut.py -v foo.wav 0:0:15:0 0:10:0:0 0:0:7:0
        command = "python ../audiocut/audiocut.py -d {} -v {} {}:0 {}:0 0:0:{}:0".format(
                                                                                   speaker_dir,
                                                                                   wave_file_path,
                                                                                   file['start'],
                                                                                   file['end'],
                                                                                   CHUNK_LENGTH)
        output = subprocess.check_output(['bash','-c', command])




