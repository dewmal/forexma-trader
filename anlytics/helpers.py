import numpy as np
from scipy.signal import argrelextrema


def peak_detection(prices, order=10, count=5):
    max_idx = list(argrelextrema(prices, np.greater, order=order)[0])
    min_idx = list(argrelextrema(prices, np.less, order=order)[0])

    idx = max_idx + min_idx + [len(prices) - 1]
    idx.sort()
    idx = idx[-count:]

    return idx, prices[idx]
