import os
import sys

import cv2
import numpy as np

from imagevariants import generate_jpeg_variants


def mean_squared_error(original_grayscale_image, grayscale_image):
    return np.mean(np.square(np.subtract(original_grayscale_image, grayscale_image)))


def peak_signal_to_noise_ratio(original_grayscale_image, grayscale_image):
    return 10 * np.log10(np.divide(
        np.square(np.max(original_grayscale_image)),
        mean_squared_error(original_grayscale_image, grayscale_image)
    ))


def normalized_root_mean_square_deviation(original_grayscale_image, grayscale_image):
    return np.sqrt(mean_squared_error(original_grayscale_image, grayscale_image)) / 255


def main():
    original_image = cv2.imread(os.path.join(
        sys.path[0], 'image-grayscale.png'), cv2.IMREAD_UNCHANGED)
    image_variants = generate_jpeg_variants(original_image)

    mses = [(quality, normalized_root_mean_square_deviation(original_image, image))
            for (quality, image) in image_variants]

    pstnrs = [(quality, peak_signal_to_noise_ratio(original_image, image))
              for (quality, image) in image_variants]

    nrmsds = [(quality, normalized_root_mean_square_deviation(original_image, image))
             for (quality, image) in image_variants]

    print(mses)
    print(pstnrs)
    print(nrmsds)


if __name__ == "__main__":
    main()
