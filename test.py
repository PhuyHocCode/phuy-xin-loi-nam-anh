
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.optimize import minimize


def f(x):
  return -x[0]**2 + x[1]**2  # Example function: f(x, y) = x^2 + y^2


def find_extrema(f):
  # ... (existing code for minimization)
  return max_result, min_result


def annotate_point(ax, x, y, z, text):
  """
  Adds annotation text at a point in the 3D plot.
  """
  ax.text(x, y, z, text, ha='center', va='center', fontsize=10, bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))


# Generate points for plotting
x = np.linspace(-5, 5, 100)
y = np.linspace(-5, 5, 100)
X, Y = np.meshgrid(x, y)
Z = f([X, Y])

# Find extrema
max_result, min_result = find_extrema(f)


def on_hover(event):
  """
  Function called when hovering over the plot.
  """
  if event.inaxes == ax:
    # Get data point under cursor
    x_data, y_data, z_data = event.artist.get_offsets()
    z = z_data[np.argmin(np.abs(x_data - event.x) + np.abs(y_data - event.y))]

    # Check if close to an extremum
    for result in [max_result, min_result]:
      if np.allclose(result.x, [event.x, event.y]):
        annotation_text = f"({result.x[0]:.2f}, {result.x[1]:.2f}) - f(x): {f(result.x):.2f}"
        annotate_point(ax, event.x, event.y, z, annotation_text)
        fig.canvas.draw_idle()
        return

    # No extremum found, hide annotation
    annotation_text = ""
    annotate_point(ax, event.x, event.y, z, annotation_text)
    fig.canvas.draw_idle()


# Plots
fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8)

# Scatter plot with hover event connection
scat = ax.scatter(
    [], [], [],  # Empty initial data (will be filled later)
    color='red',
    label='Extrema',
    picker=True,  # Enable hover events
)

# Connect hover event to the figure canvas
fig.canvas.mpl_connect('motion_notify_event', on_hover)

# Update scatter plot data with extrema locations
scat.set_offsets([[max_result.x[0], max_result.x[1]], [min_result.x[0], min_result.x[1]]])
scat.set_3d_collection(ax.scatter(max_result.x[0], max_result.x[1], f(max_result.x), color='red'))
scat.set_3d_collection(ax.scatter(min_result.x[0], min_result.x[1], f(min_result.x), color='green'))

# ... (remaining code for labels and legend)

plt.show()
