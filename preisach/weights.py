"""function for creating different weight functions"""
import numpy as np

from numpy import where, nan, nansum


def weights(method, beta, alpha):
    distance = (alpha - beta) / np.sqrt(2)
    mu = {
        "uniform": where(alpha >= beta, 1, nan),
        "linear": where(alpha == beta, 1, nan),
        "top_heavy": where(alpha >= beta, alpha, nan),
        "bottom_heavy": where(alpha >= beta, 1 - alpha, nan),
        "right_heavy": where(alpha >= beta, beta, nan),
        "left_heavy": where(alpha >= beta, 1 - beta, nan),
        "center_light_alpha": where(alpha >= beta, np.abs(0.5 - alpha), nan),
        "center_light_beta": where(alpha >= beta, np.abs(0.5 - beta), nan),
        "single_line": where(np.logical_and(0.3 < beta, beta < 0.5), 1, 0),
        "upper_left": where(np.logical_and(0.6 > beta, alpha > 0.90), 1, 0),
        "near_diagonal": where((alpha - beta) < 0.2, 1, 0),
        "far_diagonal": where((alpha - beta) < 0.5, 0, 1),
        "dirac_detal": where(np.logical_and(0.5 == beta, alpha == 0.5), 1, 0),
        "irreversible": where(alpha >= beta, distance, 0),
        "reversible": where(alpha >= beta, (1 - distance) ** 4, 0),
        "set_1": where(alpha >= beta, (1 - distance), nan),
        "set_2": where(alpha >= beta, (1 - distance) ** 2, nan),
        "set_3": where(alpha >= beta, (1 - distance) ** 4, nan),
        "mcneal": where(
            np.logical_and(
                np.logical_or(0.3 > beta, 0.8 < beta),
                alpha > 0.8
            ),
            1,
            0
        ),
    }[method]
    mu = where(alpha >= beta, mu, nan)
    mass = nansum(mu)
    mu = mu / mass
    return mu
