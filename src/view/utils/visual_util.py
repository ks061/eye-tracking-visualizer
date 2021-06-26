import os
from pathlib import Path
import numpy as np
import math

from PIL import ImageDraw
from PIL import Image
from PyQt5 import QtGui
from matplotlib import image

# Data libraries
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

# import project libraries
import src.main.config as config
import src.model.utils.data_util as data_util
import src.view.utils.heatmap_image as heatmapimage
import src.controller.delegator as delegator

WHITE_DOT_IMAGE_PATH = str(Path.cwd() / '../../_images/white_dot.png')
COLORED_DOT_IMAGE_PATH_PREFIX = str(Path.cwd() / '../../_images/colored_dots/colored_dot_')
DOT_SIZE = 19
DOT_PERCENT_INWARDS = 20
DOT_MARGIN_ADJUSTMENT = (DOT_PERCENT_INWARDS / 100.0) * DOT_SIZE


# Returns True if image exists
def _stimulus_image_exists(stimulus_image_file_name):
    return os.path.exists(str(Path.cwd() / config.RELATIVE_STIMULUS_IMAGE_DIRECTORY / stimulus_image_file_name))


# Returns a 2D array with RGB values for each
# pixel in the specified file_name containing the
# stimulus image
def import_stimulus_image(stimulus_image_file_name):
    return plt.imread(str(Path.cwd() / config.RELATIVE_STIMULUS_IMAGE_DIRECTORY / stimulus_image_file_name))


def get_fixation_size_array(data_frame):
    sizes = []

    analyzing_fixation = False
    current_fixation_x_coordinate = -1
    current_fixation_y_coordinate = -1
    prev_fixation_timestamp = 0
    fixation_duration = 0
    prev_participant_identifier = ''

    for index in range(len(data_frame.index)):
        x_fixation_column = pd.Series(data_frame[config.X_FIXATION_COL_TITLE])
        y_fixation_column = pd.Series(data_frame[config.Y_FIXATION_COL_TITLE])
        timestamp_column = pd.Series(data_frame[config.TIMESTAMP_COL_TITLE])
        participant_identifier_column = pd.Series(data_frame['participant_identifier'])

        print("col type: " + str(type(participant_identifier_column)))
        print(participant_identifier_column[index])

        if analyzing_fixation:
            if (float(x_fixation_column[index]) == current_fixation_x_coordinate and
                    float(y_fixation_column[index]) == current_fixation_y_coordinate and
                    participant_identifier_column[index] == prev_participant_identifier):
                fixation_duration += timestamp_column[index] - prev_fixation_timestamp
            else:
                if fixation_duration > 0:
                    sizes.append(fixation_duration)
                if (not math.isnan(float(x_fixation_column[index])) and
                        not math.isnan(float(y_fixation_column[index]))):
                    fixation_duration = 0

                    current_fixation_x_coordinate = float(x_fixation_column[index])
                    current_fixation_y_coordinate = float(y_fixation_column[index])
                else:
                    analyzing_fixation = False
        else:
            # print(x_fixation_column)
            # print(float(x_fixation_column[index]))
            # print(math.isnan(float(x_fixation_column[index])))

            if (not math.isnan(float(x_fixation_column[index])) and
                    not math.isnan(float(y_fixation_column[index]))):
                analyzing_fixation = True
                fixation_duration = 0

                current_fixation_x_coordinate = float(x_fixation_column[index])
                current_fixation_y_coordinate = float(y_fixation_column[index])

        prev_fixation_timestamp = timestamp_column[index]
        prev_participant_identifier = participant_identifier_column[index]

    maximum_size = max(sizes)
    print(sizes)
    for i in range(len(sizes)):
        sizes[i] = (float(sizes[i]) / float(maximum_size)) * config.MAX_FIXATION_POINT_SIZE

    return sizes


# Return a list of stimuli, where each stimulus corresponds to
# a trial on a participant, from a specified data frame
# and column title
def get_stimuli(selected_participant_check_box_list_text, data_directory_path, col_title=None):
    if col_title is None:
        col_title = config.STIMULUS_COL_TITLE
    data_frame = data_util.get_data_frame_multiple_participants(
        selected_participant_check_box_list_text,
        data_directory_path)
    return data_frame[col_title].unique()


# Returns a list of stimuli that whose corresponding images
# could be found in the stimuli images directory specified
# in the project configuration file
def get_found_stimuli(selected_participant_check_box_list_text, data_directory_path, col_title=None):
    if col_title is None:
        col_title = config.STIMULUS_COL_TITLE
    stimuli_list = get_stimuli(selected_participant_check_box_list_text, data_directory_path, col_title)
    for stimulus in stimuli_list:
        if str(stimulus) in config.EXCLUDE_STIMULI_LIST:
            stimuli_list = np.delete(stimuli_list, np.argwhere(stimulus))
        elif not _stimulus_image_exists(str(stimulus)):
            stimuli_list = np.delete(stimuli_list, np.argwhere(stimulus))
    return stimuli_list
