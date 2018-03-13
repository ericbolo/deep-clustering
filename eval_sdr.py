import subprocess
import scipy.io.wavfile
import scipy.signal
import numpy as np
import mir_eval


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

    clinton_original = original_signal
    clinton_computed = computed_signal

    reference_sources = np.array(
        [original_signal]
    )

    estimated_sources = np.array(
        [computed_signal]
    )

    metrics = mir_eval.separation.bss_eval_sources(reference_sources, estimated_sources, compute_permutation=True)

    print("metrics: ", metrics)

    print("original: clinton; computed:obama")

    original_signal, computed_signal = collect_signals(
        original='/home/eric/deep-clustering/tests/03_experiment/02_test_partial_overlap_mixtures/02/spkr1.wav',
        computed='/home/eric/deep-clustering/tests/03_experiment/02_test_partial_overlap_mixtures/02/out_32.wav'
    )

    reference_sources = np.array(
        [original_signal]
    )

    estimated_sources = np.array(
        [computed_signal]
    )

    metrics = mir_eval.separation.bss_eval_sources(reference_sources, estimated_sources, compute_permutation=True)

    print("metrics: ", metrics)

    print("original: obama; computed:obama")

    original_signal, computed_signal = collect_signals(
        original='/home/eric/deep-clustering/tests/03_experiment/02_test_partial_overlap_mixtures/02/spkr2.wav',
        computed='/home/eric/deep-clustering/tests/03_experiment/02_test_partial_overlap_mixtures/02/out_32.wav'
    )

    reference_sources = np.array(
        [original_signal]
    )

    estimated_sources = np.array(
        [computed_signal]
    )

    metrics = mir_eval.separation.bss_eval_sources(reference_sources, estimated_sources, compute_permutation=True)


    obama_original = original_signal
    obama_computed = computed_signal

    print("metrics: ", metrics)

    print("original: obama; computed:clinton")

    original_signal, computed_signal = collect_signals(
        original='/home/eric/deep-clustering/tests/03_experiment/02_test_partial_overlap_mixtures/02/spkr2.wav',
        computed='/home/eric/deep-clustering/tests/03_experiment/02_test_partial_overlap_mixtures/02/out_31.wav'
    )

    reference_sources = np.array(
        [original_signal]
    )

    estimated_sources = np.array(
        [computed_signal]
    )

    metrics = mir_eval.separation.bss_eval_sources(reference_sources, estimated_sources, compute_permutation=True)

    print("metrics: ", metrics)



    def generate_sine(max_amp=100, noise_amp=0, duration=2.0, sample_rate=8000):
        """
        Generates a sinewave
        :param max_amp: max amplitude of the sinusoid
        :type max_amp: int
        :param noise_amp: max amplitude of the added noise
        :type noise_amp: int
        :param duration: duration of the signal in seconds
        :type duration: float
        :param sample_rate: sampling rate of the generated digital signal
        :type sample_rate: int
        :return: signal
        :rtype: numpy.ndarray, dtype: int
        """
        pitch = 200
        time = np.linspace(0, duration, int(duration * sample_rate), endpoint=False)
        signal = max_amp * np.sin(2 * np.pi * pitch * time)
        signal = signal.astype(int)
        noise = np.random.normal(0, noise_amp, len(signal))
        signal += noise.astype(int)
        return signal


    noisy_sine = generate_sine()


    print("trying with permutations")

    reference_sources = np.array(
        [clinton_original,
         obama_original]
    )

    estimated_sources = np.array(
        [obama_computed,
         clinton_computed]
    )

    metrics = mir_eval.separation.bss_eval_sources(reference_sources, estimated_sources, compute_permutation=True)

    print("metrics: ", metrics)



