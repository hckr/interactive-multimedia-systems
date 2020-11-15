import math
import numpy as np
from scipy.ndimage import interpolation


def peak_signal_to_noise_ratio(original, modified):
    if len(original) != len(modified):
        modified = interpolation.zoom(modified, len(original) / len(modified))
    original = np.array(original, dtype=np.int64)
    modified = np.array(modified, dtype=np.int64)
    mse = mean_squared_error(original, modified)
    if mse == 0:
        return math.inf
    return 10 * np.log10(np.divide(
        np.square(np.max(original)),
        mse
    ))


def mean_squared_error(original, modified):
    return np.mean(np.square(np.subtract(original, modified)))
