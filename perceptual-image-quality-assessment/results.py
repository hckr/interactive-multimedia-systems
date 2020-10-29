import os
import json
import sys
import math

import cv2
import matplotlib.pyplot as plt
import numpy as np

from helpers import first, second, unzip
from imagevariants import generate_jpeg_variants
from imagemeasures import mean_squared_error, root_mean_square_deviation, peak_signal_to_noise_ratio


def main():
    labels, assessments = load_results('survey-results.json')
    # plot_raw_results(labels, assessments)
    moses = list(mean_opinion_scores(assessments))

    original_image = cv2.imread(os.path.join(
        sys.path[0], 'image-grayscale.png'), cv2.IMREAD_UNCHANGED)
    image_variants = generate_jpeg_variants(original_image)

    mses = [mean_squared_error(original_image, image)
            for (_, image) in image_variants]

    pstnrs = [peak_signal_to_noise_ratio(original_image, image)
              for (_, image) in image_variants]

    rmsds = [root_mean_square_deviation(original_image, image)
             for (_, image) in image_variants]

    plt.figure()

    plt.plot(labels, mses, label='mean squared error')
    plt.plot(labels, pstnrs, label='peak signal to noise ratio')
    plt.plot(labels, rmsds, label='root mean square deviation')

    plt.title('Simple image quality measures')
    plt.legend()
    plt.yticks(range(math.floor(min(*mses, *pstnrs, *rmsds)),
                     math.ceil(max(*mses, *pstnrs, *rmsds)) + 1, 3))
    plt.xticks(labels)
    plt.grid()

    plt.figure()

    plt.plot(labels, moses, '-c')
    plt.plot(labels, moses, '*m')

    for xy in zip(labels, moses):
        plt.annotate(second(xy), xy=(first(xy) - 0.02, second(xy) + 0.1), textcoords='data')

    plt.title('Mean opinion score')
    plt.yticks([1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5])
    plt.xticks(labels)
    plt.grid()

    plt.show()


def load_results(filename):
    with open(filename) as f:
        data = json.load(f)
        results = list(map(lambda xy_tuples: list(
            unzip(sorted(xy_tuples))), data))
        labels = first(results[0])
        assessments = list(map(second, results))
        return labels, assessments


def mean_opinion_scores(assessments):
    return map(np.mean, zip(*assessments))


def plot_raw_results(labels, assessments):
    for a in assessments:
        plt.plot(labels, a, '-*')
    plt.xticks(labels)
    plt.yticks([1, 2, 3, 4, 5])
    plt.show()


if __name__ == "__main__":
    main()
