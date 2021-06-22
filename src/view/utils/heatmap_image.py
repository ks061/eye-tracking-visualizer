"""
Credits to Professor Brian R. King, Bucknell University
"""

from matplotlib.axes import Axes
import numpy as np
from scipy import ndimage


class HeatmapImage:
    def __init__(self, dim, colormap):
        """
        Create a new Heatmap_Image object
        :param dim: sequence of ints representing the dimensions (e.g. (1024,768) )
        :param colormap: colormap to use. Default is cm.jet
        """
        self._heatmap_image_array = np.zeros(dim)
        self._colormap = colormap

    def _mark_heatmap_array(self, point, radius=3) -> None:
        """
        Internal helper function to update the heatmap with a new point p.
        :param point: a point tuple with (x-coordinate, y-coordinate)
        :param radius: how far out do we go from the center of the point we are adding
        """
        for i in range(-radius, radius + 1):
            for j in range(-radius, radius + 1):
                if np.sqrt(i * i + j * j) >= radius:
                    continue
                x_mark = point[0] + i
                y_mark = point[1] + j
                if x_mark < 0 or x_mark >= self._heatmap_image_array.shape[0]:
                    continue
                if y_mark < 0 or y_mark >= self._heatmap_image_array.shape[1]:
                    continue
                # We're good!
                self._heatmap_image_array[x_mark, y_mark] = self._heatmap_image_array[x_mark, y_mark] + 1

    def update_heatmap_array_with_trial(self, trial, radius=3):
        """
        This function updates the heatmap image with data from a trial
        :param trial: Trial data to plot for the heatmap
        :param radius: the size of each point to be placed on the heatmap
        :return:
        """
        for point in trial:
            self._mark_heatmap_array(point, radius)

    def overlay_heatmap_on_axes(self, ax: Axes, min_color_val=0.5, max_color_val=10, sigma=5, alpha=0.6) -> None:
        """
        Overlay the heatmap on a specified set of Axes
        :param ax: Axes object to overlap heatmap on
        :param min_color_val: Minimum value in heatmap to map to the coolest color. To allow everything to be displayed, set to 0.5. Higher is more restrictive.
        :param max_color_val: Maximum value in heatmap to be the "hottest" color
        :param sigma: Value passed to ndimage.gaussian_filter to blur
        :param alpha: amount of alpha blending = default = 0.6
        """
        # Create a modified colormap
        self._colormap.set_under('k', alpha=0)
        img = ndimage.gaussian_filter(self._heatmap_image_array.transpose(), sigma=sigma)
        # Now overlay the heatmap
        ax.imshow(img, cmap=self._colormap,
                  vmin=min_color_val, vmax=max_color_val,
                  interpolation='bilinear',
                  alpha=alpha
                  )
