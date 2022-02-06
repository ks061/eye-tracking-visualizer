"""
Utility to handle image-related tasks, i.e., those dealing with stimulus images
"""
import os

import numpy as np
from matplotlib import pyplot as plt

from src.main.config import RELATIVE_STIMULUS_IMAGE_DIR


def import_img_2d_rgb_arr(img_filename,
                          img_relative_dir=RELATIVE_STIMULUS_IMAGE_DIR) -> np.array:
    """
        Returns a 2D array with RGB values for
        the specified stimulus in the specified
        directory containing the stimulus

        :param img_filename: filename of the stimulus
        :type img_filename: str
        :param img_relative_dir: directory containing the stimulus
        :type img_relative_dir: str
        :return: 2D array of RGB values of stimulus
        :rtype: np.array
        """
    return plt.imread(
        str(img_relative_dir + "/" + \
            img_filename)
    )


def img_exists(img_filename: str,
               img_relative_dir: str = RELATIVE_STIMULUS_IMAGE_DIR) -> bool:
    """
    Returns True if the specified filename exists
    in the img directory

    :param img_filename: filename of img (or stimuli)
    :type img_filename: str
    :param img_relative_dir: directory specified to contain
        the images
    :type img_relative_dir: str
    :return: True if specified filename exists in
        the relative image (or stimuli) directory
    :rtype: bool
    """
    return os.path.exists(
        str(os.path.dirname(os.path.realpath(__file__)) + \
            img_relative_dir + \
            img_filename)
    )
