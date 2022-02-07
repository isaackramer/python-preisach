"""function for creating different weight functions"""
import numpy as np

def weights(method, beta_grid, alpha_grid):
    distance = (alpha_grid - beta_grid)/np.sqrt(2)
    mu =  {
           'uniform': np.where(alpha_grid>=beta_grid, 1, np.nan),
           'linear': np.where(alpha_grid==beta_grid, 1, np.nan),
           'top_heavy': np.where(alpha_grid>=beta_grid, alpha_grid, np.nan),
           'bottom_heavy': np.where(alpha_grid>=beta_grid, 1-alpha_grid, np.nan),
           'right_heavy': np.where(alpha_grid>=beta_grid, beta_grid, np.nan),
           'left_heavy': np.where(alpha_grid>=beta_grid, 1-beta_grid, np.nan),
           'center_light_alpha': np.where(alpha_grid>=beta_grid, np.abs(0.5-alpha_grid), np.nan),
           'center_light_beta': np.where(alpha_grid>=beta_grid, np.abs(0.5-beta_grid), np.nan),
           'single_line': np.where(np.logical_and(0.3<beta_grid, beta_grid<0.5), 1, 0),
           'upper_left': np.where(np.logical_and(0.6>beta_grid, alpha_grid>0.90), 1, 0),
           'near_diagonal': np.where((alpha_grid-beta_grid)<0.2, 1, 0),
           'far_diagonal': np.where((alpha_grid-beta_grid)<0.5, 0, 1),
           'dirac_detal': np.where(np.logical_and(0.5 == beta_grid, alpha_grid == 0.5), 1, 0),
           'irreversible': np.where(alpha_grid>=beta_grid, distance, 0),
           'reversible': np.where(alpha_grid>=beta_grid, (1-distance)**4, 0),
           'set_1': np.where(alpha_grid>=beta_grid, (1-distance), np.nan),
           'set_2': np.where(alpha_grid>=beta_grid, (1-distance)**2, np.nan),
           'set_3': np.where(alpha_grid>=beta_grid, (1-distance)**4, np.nan),
           'mcneal': np.where(np.logical_and(np.logical_or(0.3>beta_grid, 0.8<beta_grid), alpha_grid>0.8), 1, 0),
           }[method]
    mu = np.where(alpha_grid>=beta_grid, mu, np.nan)
    mass = np.nansum(mu)
    mu = mu/mass
    return mu
