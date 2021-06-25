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


# Returns a figure containing a scatter plot of
# raw gaze data as specified in data_frame
def get_gaze_scatter_plot(data_frame, color_palette, stimulus_file_name, show_axes, show_only_data_on_stimulus):
    # close previous plot
    plt.close('all')

    # font size
    plt.rcParams.update({'font.size': 5})

    # create new scatter plot from data in data frame
    sns.lmplot(x=config.X_GAZE_COL_TITLE,
               y=config.Y_GAZE_COL_TITLE,
               data=data_frame,
               hue='participant_identifier',
               palette=color_palette,
               fit_reg=False,
               height=config.PLOT_HEIGHT,
               legend=False,
               scatter_kws={"s": 1})

    # load in stimulus image
    stimulus_image = import_stimulus_image(stimulus_file_name)

    # defining stimulus image extent in plot
    stimulus_image_x_max = len(stimulus_image[0])
    stimulus_image_y_max = len(stimulus_image)
    stimulus_image_x_shift = data_frame[config.STIMULUS_X_DISPLACEMENT_COL_TITLE].iloc[0]
    stimulus_image_y_shift = data_frame[config.STIMULUS_Y_DISPLACEMENT_COL_TITLE].iloc[0]

    stimulus_extent = [0 + stimulus_image_x_shift,
                       stimulus_image_x_max + stimulus_image_x_shift,
                       0 + stimulus_image_y_shift,
                       stimulus_image_y_max + stimulus_image_y_shift]

    data_frame.to_csv("output.csv")

    if show_only_data_on_stimulus:
        plt.axis(stimulus_extent)
    else:
        plt.axis([data_util.get_lower_lim(data_frame, config.X_GAZE_COL_TITLE, stimulus_extent),
                  data_util.get_upper_lim(data_frame, config.X_GAZE_COL_TITLE, stimulus_extent),
                  data_util.get_lower_lim(data_frame, config.Y_GAZE_COL_TITLE, stimulus_extent),
                  data_util.get_upper_lim(data_frame, config.Y_GAZE_COL_TITLE, stimulus_extent)])

    if show_axes:
        plt.axis('on')
    else:
        plt.axis('off')

    plt.imshow(stimulus_image, extent=stimulus_extent)

    return plt.gcf()


def _get_fixation_size_array(data_frame):
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


# Returns a figure containing a scatter plot of
# fixation data as specified in data_frame
def get_fixation_scatter_plot(data_frame, color_palette, stimulus_file_name, show_axes, show_only_data_on_stimulus):
    # close previous plot
    plt.close('all')

    # font size
    plt.rcParams.update({'font.size': 5})

    # Getting relative size for each fixation point
    sizes = _get_fixation_size_array(data_frame)

    print(sizes)

    # create new scatter plot from data in data frame
    sns.lmplot(x=config.X_FIXATION_COL_TITLE,
               y=config.Y_FIXATION_COL_TITLE,
               data=data_frame,
               hue='participant_identifier',
               palette=color_palette,
               fit_reg=False,
               height=config.PLOT_HEIGHT,
               legend=False,
               scatter_kws={"s": sizes})

    # load in stimulus image
    stimulus_image = import_stimulus_image(stimulus_file_name)

    # defining stimulus image extent in plot
    stimulus_image_x_max = len(stimulus_image[0])
    stimulus_image_y_max = len(stimulus_image)
    stimulus_image_x_shift = data_frame[config.STIMULUS_X_DISPLACEMENT_COL_TITLE].iloc[0]
    stimulus_image_y_shift = data_frame[config.STIMULUS_Y_DISPLACEMENT_COL_TITLE].iloc[0]

    stimulus_extent = [0 + stimulus_image_x_shift,
                       stimulus_image_x_max + stimulus_image_x_shift,
                       0 + stimulus_image_y_shift,
                       stimulus_image_y_max + stimulus_image_y_shift]

    data_frame.to_csv("output.csv")

    if show_only_data_on_stimulus:
        plt.axis(stimulus_extent)
    else:
        plt.axis([data_util.get_lower_lim(data_frame, config.X_FIXATION_COL_TITLE, stimulus_extent),
                  data_util.get_upper_lim(data_frame, config.X_FIXATION_COL_TITLE, stimulus_extent),
                  data_util.get_lower_lim(data_frame, config.Y_FIXATION_COL_TITLE, stimulus_extent),
                  data_util.get_upper_lim(data_frame, config.Y_FIXATION_COL_TITLE, stimulus_extent)])

    if show_axes:
        plt.axis('on')
    else:
        plt.axis('off')

    plt.imshow(stimulus_image, extent=stimulus_extent)

    return plt.gcf()


def get_gaze_line_plot(data_frame, color_palette, stimulus_file_name, show_axes, show_only_data_on_stimulus):
    # close previous plot
    plt.close('all')

    # font size
    plt.rcParams.update({'font.size': 5})

    # create new scatter plot from data in data frame
    sns.lineplot(x=config.X_GAZE_COL_TITLE,
                 y=config.Y_GAZE_COL_TITLE,
                 data=data_frame,
                 hue='participant_identifier',
                 palette=color_palette,
                 legend=False,
                 sort=False,
                 ci=None)

    # load in stimulus image
    stimulus_image = import_stimulus_image(stimulus_file_name)

    # defining stimulus image extent in plot
    stimulus_image_x_max = len(stimulus_image[0])
    stimulus_image_y_max = len(stimulus_image)
    stimulus_image_x_shift = data_frame[config.STIMULUS_X_DISPLACEMENT_COL_TITLE].iloc[0]
    stimulus_image_y_shift = data_frame[config.STIMULUS_Y_DISPLACEMENT_COL_TITLE].iloc[0]

    stimulus_extent = [0 + stimulus_image_x_shift,
                       stimulus_image_x_max + stimulus_image_x_shift,
                       0 + stimulus_image_y_shift,
                       stimulus_image_y_max + stimulus_image_y_shift]

    data_frame.to_csv("output.csv")

    if show_only_data_on_stimulus:
        plt.axis(stimulus_extent)
    else:
        plt.axis([data_util.get_lower_lim(data_frame, config.X_GAZE_COL_TITLE, stimulus_extent),
                  data_util.get_upper_lim(data_frame, config.X_GAZE_COL_TITLE, stimulus_extent),
                  data_util.get_lower_lim(data_frame, config.Y_GAZE_COL_TITLE, stimulus_extent),
                  data_util.get_upper_lim(data_frame, config.Y_GAZE_COL_TITLE, stimulus_extent)])

    if show_axes:
        plt.axis('on')
    else:
        plt.axis('off')

    plt.imshow(stimulus_image, extent=stimulus_extent)

    return plt.gcf()


def get_fixation_line_plot(data_frame, color_palette, stimulus_file_name, show_axes, show_only_data_on_stimulus):
    # close previous plot
    plt.close('all')

    # font size
    plt.rcParams.update({'font.size': 5})

    # create new scatter plot from data in data frame
    sns.lineplot(x=config.X_FIXATION_COL_TITLE,
                 y=config.Y_FIXATION_COL_TITLE,
                 data=data_frame,
                 hue='participant_identifier',
                 palette=color_palette,
                 legend=False,
                 sort=False,
                 ci=None)

    # load in stimulus image
    stimulus_image = import_stimulus_image(stimulus_file_name)

    # defining stimulus image extent in plot
    stimulus_image_x_max = len(stimulus_image[0])
    stimulus_image_y_max = len(stimulus_image)
    stimulus_image_x_shift = data_frame[config.STIMULUS_X_DISPLACEMENT_COL_TITLE].iloc[0]
    stimulus_image_y_shift = data_frame[config.STIMULUS_Y_DISPLACEMENT_COL_TITLE].iloc[0]

    stimulus_extent = [0 + stimulus_image_x_shift,
                       stimulus_image_x_max + stimulus_image_x_shift,
                       0 + stimulus_image_y_shift,
                       stimulus_image_y_max + stimulus_image_y_shift]

    data_frame.to_csv("output.csv")

    if show_only_data_on_stimulus:
        plt.axis(stimulus_extent)
    else:
        plt.axis([data_util.get_lower_lim(data_frame, config.X_FIXATION_COL_TITLE, stimulus_extent),
                  data_util.get_upper_lim(data_frame, config.X_FIXATION_COL_TITLE, stimulus_extent),
                  data_util.get_lower_lim(data_frame, config.Y_FIXATION_COL_TITLE, stimulus_extent),
                  data_util.get_upper_lim(data_frame, config.Y_FIXATION_COL_TITLE, stimulus_extent)])

    if show_axes:
        plt.axis('on')
    else:
        plt.axis('off')

    plt.imshow(stimulus_image, extent=stimulus_extent)

    return plt.gcf()


def get_gaze_heat_map(data_frame, stimulus_file_name, show_axes, show_only_data_on_stimulus):
    # close previous plot
    plt.close('all')

    # font size
    plt.rcParams.update({'font.size': 5})

    # im = Image.open(str(Path.cwd() / CONFIG.RELATIVE_STIMULUS_IMAGE_DIRECTORY / stimulus_file_name))
    # heatmap_image = Heatmap_Image(im.size)

    # create new scatter plot from data in data frame
    # facet_grid_obj = sns.heatmap(data = data_frame[[CONFIG.X_GAZE_COL_TITLE, CONFIG.Y_GAZE_COL_TITLE]])

    # load in stimulus image
    stimulus_image = import_stimulus_image(stimulus_file_name)

    # defining stimulus image extent in plot
    stimulus_image_x_max = len(stimulus_image[0])
    stimulus_image_y_max = len(stimulus_image)
    stimulus_image_x_shift = data_frame[config.STIMULUS_X_DISPLACEMENT_COL_TITLE].iloc[0]
    stimulus_image_y_shift = data_frame[config.STIMULUS_Y_DISPLACEMENT_COL_TITLE].iloc[0]

    stimulus_extent = [0 + stimulus_image_x_shift,
                       stimulus_image_x_max + stimulus_image_x_shift,
                       0 + stimulus_image_y_shift,
                       stimulus_image_y_max + stimulus_image_y_shift]

    data_frame.to_csv("output.csv")

    if show_only_data_on_stimulus:
        plt.axis(stimulus_extent)
    else:
        plt.axis([data_util.get_lower_lim(data_frame, config.X_GAZE_COL_TITLE, stimulus_extent),
                  data_util.get_upper_lim(data_frame, config.X_GAZE_COL_TITLE, stimulus_extent),
                  data_util.get_lower_lim(data_frame, config.Y_GAZE_COL_TITLE, stimulus_extent),
                  data_util.get_upper_lim(data_frame, config.Y_GAZE_COL_TITLE, stimulus_extent)])

    if show_axes:
        plt.axis('on')
    else:
        plt.axis('off')

    plt.imshow(stimulus_image, extent=stimulus_extent)

    im = image.imread(str(Path.cwd() / config.RELATIVE_STIMULUS_IMAGE_DIRECTORY / stimulus_file_name))
    heatmap_image = heatmapimage.HeatmapImage((len(im[0]), len(im)))

    path = []

    for index in range(len(data_frame)):
        x_coordinate = data_frame[config.X_GAZE_COL_TITLE].iloc[index]
        if not math.isnan(x_coordinate):
            x_coordinate = int(data_frame[config.X_GAZE_COL_TITLE].iloc[index])

        y_coordinate = data_frame[config.Y_GAZE_COL_TITLE].iloc[index]
        if not math.isnan(y_coordinate):
            y_coordinate = int(data_frame[config.Y_GAZE_COL_TITLE].iloc[index])

        path.append((x_coordinate, y_coordinate))

    heatmap_image.update_heatmap_array_with_trial(path)
    heatmap_image.overlay_heatmap_on_axes(plt.gca())

    return plt.gcf()


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
