"""Functions used for calculating preisach output based on given input"""

import numpy as np

def preisach_single_value(inputs, alpha_grid, beta_grid, mu, preisach_triangle, outputs):
    """Preisach function with single input"""

    # compare new input to previous input value and change hysteron values accordingly
    if inputs[-1] > inputs[-2]: # if input increases
        preisach_triangle = np.where(inputs[-1]>alpha_grid, 1, preisach_triangle)
    elif inputs[-1] < inputs[-2]: # if input increases
        preisach_triangle = np.where(inputs[-1]<beta_grid, 0, preisach_triangle)

    # values outside the presiach half-plane are set to nan
    preisach_triangle = np.where(alpha_grid>=beta_grid, preisach_triangle, np.nan)

    # calculate weighted presiach triangle
    weighted_preisach = preisach_triangle*mu

    # new output value
    f = np.nansum(weighted_preisach)
    outputs = np.concatenate((outputs, np.array([f])))
    return outputs, preisach_triangle

def preisach_array(inputs, alpha_grid, beta_grid, mu, starting_value):
    """Preisach function for array of input values"""

    preisach_triangle = np.where(alpha_grid>=beta_grid, starting_value, np.nan)
    outputs = np.array([np.nansum(preisach_triangle*mu)])

    for ii in range(len(inputs)-1):
        new_input = inputs[ii+1]
        old_input = inputs[ii]
        if new_input > old_input: # if input increases
            preisach_triangle = np.where(new_input>alpha_grid, 1, preisach_triangle)
        elif new_input < old_input: # if input increases
            preisach_triangle = np.where(new_input<beta_grid, 0, preisach_triangle)

        preisach_triangle = np.where(alpha_grid>=beta_grid, preisach_triangle, np.nan)
        weighted_preisach = preisach_triangle*mu
        f = np.nansum(weighted_preisach)
        outputs = np.concatenate((outputs, np.array([f])))

    return outputs, preisach_triangle
