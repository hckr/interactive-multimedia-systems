import os
import wave
import numpy as np


SAMPLES_PATH = os.path.join(os.path.dirname(
    os.path.relpath(__file__)), 'samples')

BASE_SAMPLING_RATE = 44100


def load_wav(sample_file):
    with wave.open(sample_file, 'rb') as wf:
        if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() != BASE_SAMPLING_RATE:
            raise AssertionError(
                'Only 16-bit PCM mono 44 kHz WAVE files are supported')
        return np.frombuffer(wf.readframes(-1), dtype=np.int16)
