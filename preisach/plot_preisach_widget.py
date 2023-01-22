"""One input widget"""

import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np

from matplotlib.widgets import Slider, Button
from palettable.colorbrewer.sequential import YlGnBu_9

from .preisach_python import preisach_single_value
from .weights import weights


# number of hysterons on each side of the triangle
hys_per_side = 101

# create meshgrid with location of hysterons
beta_values = np.around(np.linspace(0, 1, hys_per_side), 2)
alpha_values = np.around(np.linspace(1, 0, hys_per_side), 2)
beta_grid, alpha_grid = np.meshgrid(beta_values, alpha_values)

# create array showing whether hysterons on/off
# inital values: all hysterons set to 0 (negative saturation) and
# values outside of preisach triangle set to np.nan
preisach_triangle = np.where(alpha_grid >= beta_grid, 0, np.nan)

# assign weights: "uniform", "linear", "bottom_heavy", "top_heavy",
# "left_heavy", "right_heavy" "center_light_alpha", "center_light_beta",
# "center_heavy_alpha", "center_heavy_beta"
mu = weights("irreversible", beta_grid, alpha_grid)
mass = np.nansum(mu)
mu = mu / mass


# initial state of system
initial_input = 0
inputs = np.array([initial_input])
outputs = np.array([np.nansum(preisach_triangle)])


# Begin plotting
plt.ion()
plt.clf()

fig = plt.figure(1)
gs = gridspec.GridSpec(2, 2, width_ratios=[2, 1], height_ratios=[1, 1])
gs.update(left=0.1, right=0.95, bottom=0.25, top=0.9, wspace=0.3)


ax1 = plt.subplot(gs[:, 0])  # Input/output
ax2 = plt.subplot(gs[0, 1])  # Preisach plane
ax3 = plt.subplot(gs[1, 1])  # Weights

(plot1,) = ax1.plot(inputs[0], 1 - outputs[0], color="red")
plot2 = ax2.pcolormesh(
    beta_grid, alpha_grid, preisach_triangle, cmap=YlGnBu_9.mpl_colormap
)
plot3 = ax3.scatter(beta_grid, alpha_grid, c=mu, cmap=YlGnBu_9.mpl_colormap, s=0.2)


# axis limits
ax1.set_xlim([-0.05, 1.05])
ax1.set_ylim([-0.05, 1.05])
ax2.set_xlim([-0.05, 1.05])
ax2.set_ylim([-0.05, 1.05])

# add slider (rect = [left, bottom, width, height])
axcolor = "lightgoldenrodyellow"
axinputs = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
sinputs = Slider(axinputs, "input", valmin=0, valmax=1, valinit=0.0)

# function to update plots based on slider input
def update(val):
    global inputs, outputs, preisach_triangle
    inputs = np.concatenate((inputs, np.array([sinputs.val])))
    outputs, preisach_triangle = preisach_single_value(
        inputs, alpha_grid, beta_grid, mu, preisach_triangle, outputs
    )
    plot1.set_ydata(outputs)
    plot1.set_xdata(inputs)
    ax2.pcolormesh(beta_grid, alpha_grid, preisach_triangle)
    fig.canvas.draw_idle()


# for the slider to remain responsive you must maintain a reference to it.
# Call on_changed() to connect to the slider event.
sinputs.on_changed(update)
