import player
from audiovariants import change_sampling_rate, quantize, a_law_compress, u_law_compress, adpcm_compress
from audiovariants import QUANTIZATION_VARIANTS, SAMPLING_RATE_VARIANTS
from matplotlib.figure import Figure
from tkinter import *
from tkinter.ttk import Separator
import wave
import os
import numpy as np
import matplotlib.pyplot as plt
from glob import glob
from audiomeasures import peak_signal_to_noise_ratio

SAMPLES_PATH = os.path.join(os.path.dirname(__file__), 'samples')
BASE_SAMPLING_RATE = 44100

root = Tk()


def main():
    root.title('Perceptual audio quality assessment')

    samples = glob(os.path.join(SAMPLES_PATH, '*.wav'))
    loaded_samples = [load_wav(sample) for sample in samples]

    if len(samples) == 0:
        print('No samples found')
        exit(1)

    samplesListBox = Listbox(root)
    samplesListBox.insert(0, *samples)
    samplesListBox.select_set(0)
    samplesListBox.pack(fill='both', expand=True, padx=10, pady=10)

    def selected_sample_name():
        return os.path.splitext(os.path.split(samples[samplesListBox.curselection()[0]])[-1])[0]

    def selected_sample_np_array():
        return loaded_samples[samplesListBox.curselection()[0]]

    Button(root, text='Stop playing', highlightbackground='green',
           command=player.stop).pack(fill='both', expand=True)

    Separator().pack(pady=5, fill='both')

    Button(root, text='Play and plot original (16-bit, 44.1 kHz)', command=lambda: show_plot_and_play(
        selected_sample_np_array(), BASE_SAMPLING_RATE)).pack(fill='both', expand=True)

    Separator().pack(pady=5, fill='both')

    for num_bits in QUANTIZATION_VARIANTS:
        button_with_score(root, text=f'Play and plot quantized to {num_bits}-bit', command=lambda num_bits=num_bits: show_plot_and_play(
            quantize(selected_sample_np_array(), num_bits), BASE_SAMPLING_RATE, selected_sample_np_array()))

    Separator().pack(pady=5, fill='both')

    for sampling_rate in SAMPLING_RATE_VARIANTS:
        button_with_score(root, text=f'Play and plot interpolated to {round(sampling_rate/1000)} kHz', command=lambda sampling_rate=sampling_rate: show_plot_and_play(
            change_sampling_rate(selected_sample_np_array(), BASE_SAMPLING_RATE, sampling_rate), sampling_rate, selected_sample_np_array()))

    Separator().pack(pady=5, fill='both')

    button_with_score(root, text='Play and plot after A-law compression', command=lambda: show_plot_and_play(
        a_law_compress(selected_sample_np_array(), 2), BASE_SAMPLING_RATE, selected_sample_np_array()))

    button_with_score(root, text='Play and plot after μ-law compression', command=lambda: show_plot_and_play(
        u_law_compress(selected_sample_np_array(), 2), BASE_SAMPLING_RATE, selected_sample_np_array()))

    button_with_score(root, text='Play and plot after ADPCM compression', command=lambda: show_plot_and_play(
        adpcm_compress(selected_sample_np_array(), 2), BASE_SAMPLING_RATE, selected_sample_np_array()))

    Separator().pack(pady=5, fill='both')

    Button(root, text='Save perceptual score for selected file', command=lambda: print(f'Will save to scores/{selected_sample_name()}.json'),
           highlightbackground='cyan').pack(fill='both', expand=True)

    root.mainloop()
    player.stop()


def load_wav(sample_file):
    with wave.open(sample_file, 'rb') as wf:
        if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() != BASE_SAMPLING_RATE:
            raise AssertionError(
                'Only 16-bit PCM mono 44 kHz WAVE files are supported')
        return np.frombuffer(wf.readframes(-1), dtype=np.int16)


def button_with_score(master, **button_kwargs):
    scores = [1, 2, 3, 4, 5]
    f = Frame(master)
    Button(f, **button_kwargs).pack(side='left', fill='both', expand=True)
    variable = StringVar()
    variable.set(scores[0])
    o = OptionMenu(f, variable, *scores)
    o.configure(width=5, bg='cyan')
    o.pack(side='right')
    f.pack(fill='both', expand=True)
    return variable


def show_plot_and_play(np_array, frequency, np_array_orig=None):
    player.stop()
    show_plot(np_array, np_array_orig if np_array_orig is not None else np_array)
    root.after(500, lambda: player.play(np_array, frequency))


def show_plot(current, original):
    plt.figure('Signal in time')
    plt.clf()
    plt.subplot(2, 1, 1)
    plt.plot(current, 'm')
    plt.title(
        f'Current | PSNR={round(peak_signal_to_noise_ratio(original, current), 2)}')
    plt.grid()
    plt.tight_layout()
    plt.subplot(2, 1, 2)
    if original is not None:
        plt.plot(original, 'c')
    plt.title('Original')
    plt.grid()
    plt.tight_layout()
    plt.draw()
    plt.show(block=False)


if __name__ == '__main__':
    main()
