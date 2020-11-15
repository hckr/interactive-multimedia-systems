import os
import json
import sys
import operator
from functools import reduce

import cv2
import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model
import scipy.signal as sig

from helpers import first, second, unzip
from imagevariants import generate_jpeg_variants
from imagemeasures import mean_squared_error, normalized_root_mean_square_deviation, peak_signal_to_noise_ratio


def main():
    labels, assessments = load_results('survey-results.json')
    # plot_raw_results(labels, assessments)
    mean_moses = list(mean_opinion_scores(assessments))

    original_image = cv2.imread(os.path.join(
        sys.path[0], 'image-grayscale.png'), cv2.IMREAD_UNCHANGED)
    image_variants = generate_jpeg_variants(original_image)

    mses = [mean_squared_error(original_image, image)
            for (_, image) in image_variants]

    pstnrs = [peak_signal_to_noise_ratio(original_image, image)
              for (_, image) in image_variants]

    nrmsds = [normalized_root_mean_square_deviation(original_image, image)
             for (_, image) in image_variants]

    plt.figure()
    
    plt.subplot(3, 1, 1)
    plt.plot(labels, mses)
    plt.title('mean squared error')
    plt.xticks(labels)
    plt.grid()

    plt.subplot(3, 1, 2)
    plt.plot(labels, pstnrs)
    plt.title('peak signal to noise ratio')
    plt.xticks(labels)
    plt.grid()
    
    plt.subplot(3, 1, 3)
    plt.plot(labels, nrmsds)
    plt.xticks(labels)
    plt.grid()
    plt.title('normalized root mean square deviation')

    plt.suptitle('Simple image quality measures')

    plt.figure()
    for i, assessment in enumerate(assessments):
        plt.plot(labels, assessment, '*-', label=f'{i}')
    plt.title('Opinion scores')
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.yticks([1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5])
    plt.xticks(labels)
    plt.grid()

    plt.figure()

    regr = linear_model.LinearRegression()
    regr.fit(np.array(labels).reshape(-1, 1), mean_moses)
    x_pred = np.linspace(0, 1, 101)
    regr_pred = regr.predict(x_pred.reshape(-1, 1))

    plt.plot(x_pred, regr_pred, '-c',
             label=f'Linear regression model: {round(regr.coef_[0], 2)}x + {round(regr.intercept_, 2)}')
    plt.plot(labels, mean_moses, '*m')

    for xy in zip(labels, mean_moses):
        plt.annotate(second(xy), xy=(first(xy) - 0.02,
                                     second(xy) + 0.1), textcoords='data')

    plt.title('Mean opinion score')
    plt.legend()
    plt.yticks([1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5])
    plt.xticks(labels)
    plt.grid()

    plt.figure()
    plot_correlation(mean_moses, mses, '`Mean MOS-es and mean squared errors correlation')

    plt.figure()
    plot_correlation(
        mean_moses, pstnrs, 'Mean MOSes and peak signal to noise ratios correlation')

    plt.figure()
    plot_correlation(
        mean_moses, nrmsds, 'Mean MOSes and normalized root mean square deviations correlation')

    plt.figure()
    plot_linreg(reduce(operator.concat, assessments), list(mses) * len(assessments), 'MOS', 'mean squared error')

    plt.figure()
    plot_linreg(reduce(operator.concat, assessments), list(pstnrs) * len(assessments), 'MOS', 'peak signal to noise ratio')

    plt.figure()
    plot_linreg(reduce(operator.concat, assessments), list(nrmsds) * len(assessments), 'MOS', 'normalized root mean square deviation')

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


def plot_correlation(a, b, title):
    c = sig.correlate(a, b)
    plt.plot(np.arange(len(c)) - (len(b) - 1), c, '*-')
    plt.axvline(0, lw=1, c='k')
    plt.xlabel('delay')
    plt.ylabel('correlation')
    plt.title(title)
    plt.grid()


def plot_linreg(a, b, a_label, b_label):
    regr = linear_model.LinearRegression()
    regr.fit(np.array(a).reshape(-1, 1), b)
    regr_pred = regr.predict(np.array(a).reshape(-1, 1))

    plt.plot(a, regr_pred, '-c',
             label=f'{round(regr.coef_[0], 2)}x + {round(regr.intercept_, 2)}')
    plt.plot(a, b, '*m')
    plt.legend()
    plt.xlabel(a_label)
    plt.ylabel(b_label)
    plt.title(f'{a_label} to {b_label} linear regression')
    plt.grid()


if __name__ == "__main__":
    main()
