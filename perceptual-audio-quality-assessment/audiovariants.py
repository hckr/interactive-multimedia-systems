import audioop
import numpy as np
from scipy.ndimage import interpolation
from loader import BASE_SAMPLING_RATE

QUANTIZATION_VARIANTS = [8, 4, 2]
SAMPLING_RATE_VARIANTS = [22000, 11000, 8000, 4000, 2000]


def generate_quantization_variants(np_array):
    return [(num_bits, quantize(np_array, num_bits))
            for num_bits in QUANTIZATION_VARIANTS]


def generate_sampling_rate_variants(np_array):
    return [(sampling_rate,
             change_sampling_rate(np_array, BASE_SAMPLING_RATE, sampling_rate))
            for sampling_rate in SAMPLING_RATE_VARIANTS]


def generate_compression_variants(np_array, sample_width):
    return [
        ('A-law', a_law_compress(np_array, sample_width)),
        ('u-law', u_law_compress(np_array, sample_width)),
        ('ADPCM', adpcm_compress(np_array, sample_width))
    ]


def quantize(np_array, num_bits):
    shift = 16 - num_bits
    return np.left_shift(np.right_shift(np_array, shift), shift)


def change_sampling_rate(np_array, sampling_rate, target_sampling_rate):
    return interpolation.zoom(np_array, target_sampling_rate / sampling_rate)


def a_law_compress(np_array, sample_width):
    compressed = audioop.lin2alaw(np_array, sample_width)
    return np.frombuffer(audioop.alaw2lin(compressed, sample_width), dtype=np.int16)


def u_law_compress(np_array, sample_width):
    compressed = audioop.lin2ulaw(np_array, sample_width)
    return np.frombuffer(audioop.ulaw2lin(compressed, sample_width), dtype=np.int16)


def adpcm_compress(np_array, sample_width):
    compressed = audioop.lin2adpcm(np_array, sample_width, None)
    return np.frombuffer(audioop.adpcm2lin(compressed[0], sample_width, None)[0], dtype=np.int16)
