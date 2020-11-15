import player
from audiovariants import change_sampling_rate, quantize, a_law_compress, u_law_compress, adpcm_compress
from audiovariants import QUANTIZATION_VARIANTS, SAMPLING_RATE_VARIANTS
from matplotlib.figure import Figure
from tkinter import *
from tkinter.ttk import Separator
from tkinter.messagebox import showinfo
import os
import json
import matplotlib.pyplot as plt
from glob import glob
from audiomeasures import peak_signal_to_noise_ratio
from loader import load_wav, SAMPLES_PATH, BASE_SAMPLING_RATE

root = Tk()


def main():
    root.title('Perceptual audio quality assessment')

    samples = glob(os.path.join(SAMPLES_PATH, '*.wav'))
    loaded_samples = [load_wav(sample) for sample in samples]
    user_scores_variables = {
        # 'group': [
        #     'id': variable
        # ]
    }

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

    Button(root, text='Play and plot the original (16-bit, 44.1 kHz)', command=lambda: show_plot_and_play(
        selected_sample_np_array(), BASE_SAMPLING_RATE)).pack(fill='both', expand=True)

    Separator().pack(pady=5, fill='both')

    user_scores_variables['quantization'] = [
        (num_bits, button_with_score(root, text=f'Play and plot quantized to {num_bits}-bit', command=lambda num_bits=num_bits: show_plot_and_play(
            quantize(selected_sample_np_array(), num_bits), BASE_SAMPLING_RATE, selected_sample_np_array())))
        for num_bits in QUANTIZATION_VARIANTS
    ]

    Separator().pack(pady=5, fill='both')

    user_scores_variables['sampling_rate'] = [
        (sampling_rate, button_with_score(root, text=f'Play and plot interpolated to {round(sampling_rate/1000)} kHz', command=lambda sampling_rate=sampling_rate: show_plot_and_play(
            change_sampling_rate(selected_sample_np_array(), BASE_SAMPLING_RATE, sampling_rate), sampling_rate, selected_sample_np_array())))
        for sampling_rate in SAMPLING_RATE_VARIANTS
    ]

    Separator().pack(pady=5, fill='both')

    user_scores_variables['compression'] = [
        ('A-law', button_with_score(root, text='Play and plot after A-law compression', command=lambda: show_plot_and_play(
            a_law_compress(selected_sample_np_array(), 2), BASE_SAMPLING_RATE, selected_sample_np_array()))),

        ('u-law', button_with_score(root, text='Play and plot after μ-law compression', command=lambda: show_plot_and_play(
            u_law_compress(selected_sample_np_array(), 2), BASE_SAMPLING_RATE, selected_sample_np_array()))),

        ('ADPCM', button_with_score(root, text='Play and plot after ADPCM compression', command=lambda: show_plot_and_play(
            adpcm_compress(selected_sample_np_array(), 2), BASE_SAMPLING_RATE, selected_sample_np_array())))
    ]

    Separator().pack(pady=5, fill='both')

    Button(root, text='Save perceptual score for selected file', command=lambda: save_scores(selected_sample_name(), user_scores_variables),
           highlightbackground='cyan').pack(fill='both', expand=True)

    root.mainloop()
    player.stop()


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


def save_scores(sample_name, user_scores_variables):
    user_scores = {category: [[variant, int(variable.get())]
                              for (variant, variable) in scores_variables_list]
                   for (category, scores_variables_list) in user_scores_variables.items()}
    file_path = os.path.join('scores', f'{sample_name}.json')
    with open(file_path, 'w') as f:
        json.dump(user_scores, f, indent=2)
    showinfo('Saved', f'Scores saved to {file_path}')


if __name__ == '__main__':
    main()
