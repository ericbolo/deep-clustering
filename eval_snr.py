'''

Inspired by: https://dsp.stackexchange.com/questions/36626/snr-for-an-audio-wav-files-and-objective-measures-for-evaluating-filtering-tech

'''


import subprocess
import scipy.io.wavfile
import scipy.signal
import numpy as np


'''
Some files may have non-standard bit depths / precision,
converting to 16-bit.
'''
def adjust_bit_depth(wave_signal):
    adjusted_signal = "{0}_adjusted_bit_depth.wav".format(wave_signal.split('.')[0])

    command = "ffmpeg -loglevel panic -i {0} -y -sample_fmt s16 {1}".format(
        wave_signal, adjusted_signal
    )

    subprocess.check_output(['bash', '-c', command])

    return adjusted_signal


def compute_snr(computed_signal, 
                original_signal):

    np.seterr(divide='ignore')
    return 20 * np.log10(np.mean(np.square(computed_signal))/np.mean(np.square(computed_signal - original_signal)))


if __name__ == '__main__':

    '''
    spkr1, out_31: Clinton
    spkr2, out_32: Obama

    '''


    def collect_signals(original=None, computed=None):

        ORIGINAL_SIGNAL_WAVE = original
        COMPUTED_SIGNAL_WAVE = computed

        ORIGINAL_SIGNAL_WAVE = adjust_bit_depth(ORIGINAL_SIGNAL_WAVE)
        COMPUTED_SIGNAL_WAVE = adjust_bit_depth(COMPUTED_SIGNAL_WAVE)

        _, original_signal = scipy.io.wavfile.read(ORIGINAL_SIGNAL_WAVE)
        _, computed_signal = scipy.io.wavfile.read(COMPUTED_SIGNAL_WAVE)

        computed_signal = computed_signal[:len(original_signal)]

        return original_signal, computed_signal


    print("original: clinton; computed:clinton")
    original_signal, computed_signal = collect_signals(
        original='/home/eric/deep-clustering/tests/03_experiment/02_test_partial_overlap_mixtures/02/spkr1.wav',
        computed='/home/eric/deep-clustering/tests/03_experiment/02_test_partial_overlap_mixtures/02/out_31.wav'
    )

    snr = compute_snr(original_signal,
                      computed_signal)
    print("snr", snr)

    print("original: clinton; computed:obama")
    original_signal, computed_signal = collect_signals(
        original='/home/eric/deep-clustering/tests/03_experiment/02_test_partial_overlap_mixtures/02/spkr1.wav',
        computed='/home/eric/deep-clustering/tests/03_experiment/02_test_partial_overlap_mixtures/02/out_32.wav'
    )

    snr = compute_snr(original_signal,
                      computed_signal)
    print("snr", snr)

    print("original: obama; computed:obama")
    original_signal, computed_signal = collect_signals(
        original='/home/eric/deep-clustering/tests/03_experiment/02_test_partial_overlap_mixtures/02/spkr2.wav',
        computed='/home/eric/deep-clustering/tests/03_experiment/02_test_partial_overlap_mixtures/02/out_32.wav'
    )

    snr = compute_snr(original_signal,
                      computed_signal)
    print("snr", snr)

    print("original: obama; computed:clinton")
    original_signal, computed_signal = collect_signals(
        original='/home/eric/deep-clustering/tests/03_experiment/02_test_partial_overlap_mixtures/02/spkr2.wav',
        computed='/home/eric/deep-clustering/tests/03_experiment/02_test_partial_overlap_mixtures/02/out_31.wav'
    )

    snr = compute_snr(original_signal,
                      computed_signal)
    print("snr", snr)

    print("meme signaux")
    original_signal, computed_signal = collect_signals(
        original='/home/eric/deep-clustering/tests/03_experiment/02_test_partial_overlap_mixtures/02/spkr2.wav',
        computed='/home/eric/deep-clustering/tests/03_experiment/02_test_partial_overlap_mixtures/02/spkr2.wav'
    )

    snr = compute_snr(original_signal,
                      computed_signal)
    print("snr", snr)