import os
import json
from glob import glob
from loader import load_wav, SAMPLES_PATH
from audiovariants import generate_quantization_variants, generate_sampling_rate_variants, generate_compression_variants
from audiomeasures import peak_signal_to_noise_ratio
import matplotlib.pyplot as plt
import scipy.signal as sig
import numpy as np
from sklearn import linear_model

SCORES_PATH = os.path.join(os.path.dirname(
    os.path.relpath(__file__)), 'scores')


def main():
    for file_path in glob(os.path.join(SCORES_PATH, '*.json')):
        sample_name = os.path.splitext(os.path.split(file_path)[-1])[0]
        sample_array = load_wav(os.path.join(
            SAMPLES_PATH, f'{sample_name}.wav'))
        scores = load_scores(file_path)

        ###

        quantization_psnrs = [(num_bits, peak_signal_to_noise_ratio(sample_array, np_array))
                              for (num_bits, np_array)
                              in generate_quantization_variants(sample_array)]

        plt.figure()
        _xs, quantization_psnr_vals = zip(*sorted(quantization_psnrs))
        _xs, quantization_scores = zip(*sorted(scores['quantization']))
        plot_correlation(quantization_psnr_vals, quantization_scores,
                         f'{sample_name} | Quantization MOSes and peak signal to noise ratios correlation')

        ###

        sampling_rate_psnrs = [(sampling_rate, peak_signal_to_noise_ratio(sample_array, np_array))
                               for (sampling_rate, np_array)
                               in generate_sampling_rate_variants(sample_array)]

        plt.figure()
        _xs, sampling_rate_psnr_vals = zip(*sorted(sampling_rate_psnrs))
        _xs, sampling_rate_scores = zip(*sorted(scores['sampling_rate']))
        plot_correlation(sampling_rate_psnr_vals, sampling_rate_scores,
                         f'{sample_name} | Sampling rate MOSes and peak signal to noise ratios correlation')

        compression_psnrs = [(compression_name, peak_signal_to_noise_ratio(sample_array, np_array))
                             for (compression_name, np_array)
                             in generate_compression_variants(sample_array, 2)]

        ###

        plt.figure()
        _xs, compression_psnr_vals = zip(*sorted(compression_psnrs))
        _xs, compression_scores = zip(*sorted(scores['compression']))
        plot_correlation(compression_psnr_vals, compression_scores,
                         f'{sample_name} | Compression MOSes and peak signal to noise ratios correlation')

        plt.figure()
        plot_linreg(quantization_scores, quantization_psnr_vals, 'MOS',
                    'peak signal to noise ratio', f'{sample_name} | Quantization | ')

        plt.figure()
        plot_linreg(sampling_rate_scores, sampling_rate_psnr_vals, 'MOS',
                    'peak signal to noise ratio', f'{sample_name} | Sampling rate | ')

        plt.figure()
        plot_linreg(compression_scores, compression_psnr_vals, 'MOS',
                    'peak signal to noise ratio', f'{sample_name} | Compression | ')
    
    plt.show()


def load_scores(file_path):
    with open(file_path) as f:
        return json.load(f)


def plot_correlation(a, b, title):
    c = sig.correlate(a, b)
    plt.plot(np.arange(len(c)) - (len(b) - 1), c, '*-')
    plt.axvline(0, lw=1, c='k')
    plt.xlabel('delay')
    plt.ylabel('correlation')
    plt.title(title)
    plt.grid()


def plot_linreg(a, b, a_label, b_label, title_prefix=''):
    regr = linear_model.LinearRegression()
    regr.fit(np.array(a).reshape(-1, 1), b)
    regr_pred = regr.predict(np.array(a).reshape(-1, 1))

    plt.plot(a, regr_pred, '-c',
             label=f'{round(regr.coef_[0], 2)}x + {round(regr.intercept_, 2)}')
    plt.plot(a, b, '*m')
    plt.legend()
    plt.xlabel(a_label)
    plt.ylabel(b_label)
    plt.title(f'{title_prefix}{a_label} to {b_label} linear regression')
    plt.grid()


if __name__ == "__main__":
    main()
