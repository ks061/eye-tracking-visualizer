from matplotlib import cm
from matplotlib.axes import Axes
import numpy as np

class Heatmap_Image:
    def __init__(self, dim, cmap = cm.jet):
        """
        Create a new Heatmap_Image object
        :param dim: sequence of ints representing the dimensions (e.g. (1024,768) )
        :param cmap: colormap to use. Default is cm.jet
        """
        self._heatmap_image_array = np.zeros(dim)
        self._cmap = cmap
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

    def update_heatmap_array_with_trial(self, trial, radius = 3):
        """
        This function updates the heatmap image with data from a trial
        :param trial: Trial data to plot for the heatmap
        :param radius: the size of each point to be placed on the heatmap
        :return:
        """
        for point in trial:
            self._mark_heatmap_array(point, radius)

    def overlay_heatmap_on_Axes(self, ax: Axes, vmin = 0.5, vmax = 10, sigma = 5, alpha=0.6) -> None:
        """
        Overlay the heatmap on a specified set of Axes
        :param ax: Axes object to overlap heatmap on
        :param vmin: Minimum value in heatmap to map to the coolest color. To allow everything to be displayed, set to 0.5. Higher is more restrictive.
        :param vmax: Maximum value in heatmap to be the "hottest" color
        :param sigma: Value passed to ndimage.gaussian_filter to blur
        :param alpha: amount of alpha blending = default = 0.6
        """
        # Create a modified colormap
        self._cmap.set_under('k', alpha=0)
        img = ndimage.gaussian_filter(self._heatmap_image_array.transpose(),sigma=sigma)
        # Now overlay the heatmap
        ax.imshow(img, cmap=self._cmap,
                  vmin=vmin, vmax=vmax,
                  interpolation='bilinear',
                  alpha=alpha
                  )