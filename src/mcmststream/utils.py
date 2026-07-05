"""Utility helpers for the mcmststream package."""

import numpy as np
from importlib.resources import files


def load_exclastar():
    """Load the bundled ExclaStar benchmark dataset.

    Returns
    -------
    X : ndarray of shape (n_samples, 2)
        Feature matrix.
    y_true : ndarray of shape (n_samples,)
        Ground-truth cluster labels.
    """
    data_path = files("mcmststream").joinpath("data/ExclaStar.txt")
    dataset = np.loadtxt(data_path, delimiter=",", dtype=float)
    X = dataset[:, 1:3]
    y_true = dataset[:, 3]
    return X, y_true
