import os
from pathlib import Path
import numpy as np
import math
from heatmap_image import Heatmap_Image
from PIL import Image
from matplotlib import image

# Project libraries
import config as CONFIG
import data_util

# Data libraries
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

# Returns True if image exists
def _stimulus_image_exists(stimulus_image_file_name):
    return os.path.exists(str(Path.cwd() / CONFIG.RELATIVE_STIMULUS_IMAGE_DIRECTORY / stimulus_image_file_name))

# Returns a 2D array with RGB values for each
# pixel in the specified file_name containing the
# stimulus image
def _import_stimulus_image(stimulus_image_file_name):
    return plt.imread(str(Path.cwd() / CONFIG.RELATIVE_STIMULUS_IMAGE_DIRECTORY / stimulus_image_file_name))

# Returns a blank plot
def _get_blank_plot():
    data_frame = pd.DataFrame(columns=['X', 'Y'])
    x_title = 'X'
    y_title = 'Y'
    sns.lmplot(x = x_title, y = y_title, data = data_frame,
               fit_reg = False, height = CONFIG.PLOT_HEIGHT,
               legend = False)
    plt.axis('off')
    return plt.gcf()

def _cluster_range_query(data_frame_cluster, index_list_of_all_points, index_of_center_point, max_dist_btw_center_point_and_potential_neighbor, X_COL_TITLE, Y_COL_TITLE):
    neighbor_point_index_list = []
    for index_of_potential_neighbor in index_list_of_all_points:
        x1 = data_frame_cluster.loc[index_of_center_point, X_COL_TITLE]
        x2 = data_frame_cluster.loc[index_of_potential_neighbor, X_COL_TITLE]
        y1 = data_frame_cluster.loc[index_of_center_point, Y_COL_TITLE]
        y2 = data_frame_cluster.loc[index_of_potential_neighbor, Y_COL_TITLE]
        dist_btw_center_point_and_potential_neighbor = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        if dist_btw_center_point_and_potential_neighbor <= max_dist_btw_center_point_and_potential_neighbor:
            neighbor_point_index_list.append(index_of_potential_neighbor)
    return neighbor_point_index_list


def _cluster_range_query_gaze(data_frame_cluster, index_list_of_all_points, index_of_center_point,
                              max_dist_btw_center_point_and_potential_neighbor):
    return _cluster_range_query(data_frame_cluster, index_list_of_all_points, index_of_center_point,
                                max_dist_btw_center_point_and_potential_neighbor, CONFIG.X_GAZE_COL_TITLE,
                                CONFIG.Y_GAZE_COL_TITLE)

def _cluster_range_query_fixation(data_frame_cluster, index_list_of_all_points, index_of_center_point,
                                  max_dist_btw_center_point_and_potential_neighbor):
    return _cluster_range_query(data_frame_cluster, index_list_of_all_points, index_of_center_point,
                         max_dist_btw_center_point_and_potential_neighbor, CONFIG.X_FIXATION_COL_TITLE,
                         CONFIG.Y_FIXATION_COL_TITLE)

def _get_fixation_cluster_plot(data_frame, color_palette, stimulus_file_name, show_axes, show_only_data_on_stimulus):
    # close previous plot
    plt.close('all')

    # font size
    plt.rcParams.update({'font.size': 5})

    data_frame_cluster = data_frame.copy(deep=True)
    data_frame_cluster.reset_index(drop=True, inplace=True)
    C = 0
    num_rows = data_frame_cluster.shape[0]
    data_frame_cluster['cluster_identifier'] = pd.Series(["-1" for i in range(0, num_rows)], index=data_frame_cluster.index)
    data_frame_index_list = [i for i in range(0, num_rows)]
    max_neighbor_distance_for_cluster = 20
    min_points_in_cluster = 15
    for index in data_frame_index_list:
        if data_frame_cluster.loc[index, 'cluster_identifier'] != "-1":
            continue
        neighbors = _cluster_range_query_fixation(data_frame_cluster, data_frame_index_list, index,
                                                  max_neighbor_distance_for_cluster)
        if len(neighbors) < min_points_in_cluster:
            data_frame_cluster.loc[index, 'cluster_identifier'] = "Noise"
            continue
        C += 1
        data_frame_cluster.loc[index, 'cluster_identifier'] = str(C)
        seed = neighbors.copy()
        seed.remove(index)
        for index_seed in seed:
            if data_frame_cluster.loc[index_seed, 'cluster_identifier'] == "Noise":
                data_frame_cluster.loc[index_seed, 'cluster_identifier'] = str(C)
            if data_frame_cluster.loc[index_seed, 'cluster_identifier'] != "-1":
                continue
            data_frame_cluster.loc[index_seed, 'cluster_identifier'] = str(C)
            neighbors = _cluster_range_query_fixation(data_frame_cluster, data_frame_index_list, index_seed,
                                                      max_neighbor_distance_for_cluster)
            if len(neighbors) >= min_points_in_cluster:
                seed.extend(neighbors)

    cluster_color_palette = sns.color_palette("gist_rainbow", C)

    # create new scatter plot from data in data frame
    facet_grid_obj = sns.lmplot(x=CONFIG.X_FIXATION_COL_TITLE,
                                y=CONFIG.Y_FIXATION_COL_TITLE,
                                data=data_frame_cluster,
                                hue='cluster_identifier',
                                palette=cluster_color_palette,
                                fit_reg=False,
                                height=CONFIG.PLOT_HEIGHT,
                                legend=False,
                                scatter_kws={"s": 1})

    # load in stimulus image
    stimulus_image = _import_stimulus_image(stimulus_file_name)

    # defining stimulus image extent in plot
    stimulus_image_x_max = len(stimulus_image[0])
    stimulus_image_y_max = len(stimulus_image)
    stimulus_image_x_shift = data_frame[CONFIG.STIMULUS_X_DISPLACEMENT_COL_TITLE].iloc[0]
    stimulus_image_y_shift = data_frame[CONFIG.STIMULUS_Y_DISPLACEMENT_COL_TITLE].iloc[0]

    stimulus_extent = [0 + stimulus_image_x_shift,
                       stimulus_image_x_max + stimulus_image_x_shift,
                       0 + stimulus_image_y_shift,
                       stimulus_image_y_max + stimulus_image_y_shift]

    data_frame.to_csv("output.csv")

    if show_only_data_on_stimulus:
        plt.axis(stimulus_extent)
    else:
        plt.axis([data_util._get_lower_lim(data_frame, CONFIG.X_FIXATION_COL_TITLE, stimulus_extent),
                  data_util._get_upper_lim(data_frame, CONFIG.X_FIXATION_COL_TITLE, stimulus_extent),
                  data_util._get_lower_lim(data_frame, CONFIG.Y_FIXATION_COL_TITLE, stimulus_extent),
                  data_util._get_upper_lim(data_frame, CONFIG.Y_FIXATION_COL_TITLE, stimulus_extent)])

    if show_axes:
        plt.axis('on')
    else:
        plt.axis('off')

    plt.imshow(stimulus_image, extent = stimulus_extent)

    return plt.gcf()

def _get_gaze_cluster_plot(data_frame, color_palette, stimulus_file_name, show_axes, show_only_data_on_stimulus):
    # close previous plot
    plt.close('all')

    # font size
    plt.rcParams.update({'font.size': 5})

    data_frame_cluster = data_frame.copy(deep=True)
    data_frame_cluster.reset_index(drop=True, inplace=True)
    C = 0
    num_rows = data_frame_cluster.shape[0]
    data_frame_cluster['cluster_identifier']=pd.Series(["-1" for i in range(0, num_rows)], index=data_frame_cluster.index)
    data_frame_index_list = [i for i in range(0, num_rows)]
    max_neighbor_distance_for_cluster = 20
    min_points_in_cluster = 15
    for index in data_frame_index_list:
        if data_frame_cluster.loc[index, 'cluster_identifier'] != "-1":
            continue
        neighbors = _cluster_range_query_gaze(data_frame_cluster, data_frame_index_list, index, max_neighbor_distance_for_cluster)
        if len(neighbors) < min_points_in_cluster:
            data_frame_cluster.loc[index, 'cluster_identifier'] = "Noise"
            continue
        C += 1
        data_frame_cluster.loc[index, 'cluster_identifier'] = str(C)
        seed = neighbors.copy()
        seed.remove(index)
        for index_seed in seed:
            if data_frame_cluster.loc[index_seed, 'cluster_identifier'] == "Noise":
                data_frame_cluster.loc[index_seed, 'cluster_identifier'] = str(C)
            if data_frame_cluster.loc[index_seed, 'cluster_identifier'] != "-1":
                continue
            data_frame_cluster.loc[index_seed,'cluster_identifier'] = str(C)
            neighbors = _cluster_range_query_gaze(data_frame_cluster, data_frame_index_list, index_seed, max_neighbor_distance_for_cluster)
            if len(neighbors) >= min_points_in_cluster:
                seed.extend(neighbors)

    print("C: " + str(C))
    cluster_color_palette = sns.color_palette("gist_rainbow", C)

    # create new scatter plot from data in data frame
    facet_grid_obj = sns.lmplot(x=CONFIG.X_GAZE_COL_TITLE,
                                y=CONFIG.Y_GAZE_COL_TITLE,
                                data=data_frame_cluster,
                                hue='cluster_identifier',
                                palette=cluster_color_palette,
                                fit_reg=False,
                                height=CONFIG.PLOT_HEIGHT,
                                legend=False,
                                scatter_kws={"s": 1})

    # load in stimulus image
    stimulus_image = _import_stimulus_image(stimulus_file_name)

    # defining stimulus image extent in plot
    stimulus_image_x_max = len(stimulus_image[0])
    stimulus_image_y_max = len(stimulus_image)
    stimulus_image_x_shift = data_frame[CONFIG.STIMULUS_X_DISPLACEMENT_COL_TITLE].iloc[0]
    stimulus_image_y_shift = data_frame[CONFIG.STIMULUS_Y_DISPLACEMENT_COL_TITLE].iloc[0]

    stimulus_extent = [0 + stimulus_image_x_shift,
                       stimulus_image_x_max + stimulus_image_x_shift,
                       0 + stimulus_image_y_shift,
                       stimulus_image_y_max + stimulus_image_y_shift]

    data_frame.to_csv("output.csv")

    if show_only_data_on_stimulus:
        plt.axis(stimulus_extent)
    else:
        plt.axis([data_util._get_lower_lim(data_frame, CONFIG.X_GAZE_COL_TITLE, stimulus_extent),
                  data_util._get_upper_lim(data_frame, CONFIG.X_GAZE_COL_TITLE, stimulus_extent),
                  data_util._get_lower_lim(data_frame, CONFIG.Y_GAZE_COL_TITLE, stimulus_extent),
                  data_util._get_upper_lim(data_frame, CONFIG.Y_GAZE_COL_TITLE, stimulus_extent)])

    if show_axes:
        plt.axis('on')
    else:
        plt.axis('off')

    plt.imshow(stimulus_image, extent=stimulus_extent)

    return plt.gcf()

# Returns a figure containing a scatter plot of
# raw gaze data as specified in data_frame
def _get_gaze_scatter_plot(data_frame, color_palette, stimulus_file_name, show_axes, show_only_data_on_stimulus):
    # close previous plot
    plt.close('all')

    # font size
    plt.rcParams.update({'font.size': 5})

    # create new scatter plot from data in data frame
    facet_grid_obj = sns.lmplot(x = CONFIG.X_GAZE_COL_TITLE,
                                y = CONFIG.Y_GAZE_COL_TITLE,
                                data = data_frame,
                                hue = 'participant_identifier',
                                palette = color_palette,
                                fit_reg = False,
                                height = CONFIG.PLOT_HEIGHT,
                                legend = False,
                                scatter_kws = {"s": 1})

    # load in stimulus image
    stimulus_image = _import_stimulus_image(stimulus_file_name)

    # defining stimulus image extent in plot
    stimulus_image_x_max = len(stimulus_image[0])
    stimulus_image_y_max = len(stimulus_image)
    stimulus_image_x_shift = data_frame[CONFIG.STIMULUS_X_DISPLACEMENT_COL_TITLE].iloc[0]
    stimulus_image_y_shift = data_frame[CONFIG.STIMULUS_Y_DISPLACEMENT_COL_TITLE].iloc[0]

    stimulus_extent = [0 + stimulus_image_x_shift,
                       stimulus_image_x_max + stimulus_image_x_shift,
                       0 + stimulus_image_y_shift,
                       stimulus_image_y_max + stimulus_image_y_shift]

    data_frame.to_csv("output.csv")

    if show_only_data_on_stimulus:
        plt.axis(stimulus_extent)
    else:
        plt.axis([data_util._get_lower_lim(data_frame, CONFIG.X_GAZE_COL_TITLE, stimulus_extent),
                  data_util._get_upper_lim(data_frame, CONFIG.X_GAZE_COL_TITLE, stimulus_extent),
                  data_util._get_lower_lim(data_frame, CONFIG.Y_GAZE_COL_TITLE, stimulus_extent),
                  data_util._get_upper_lim(data_frame, CONFIG.Y_GAZE_COL_TITLE, stimulus_extent)])

    if show_axes:
        plt.axis('on')
    else:
        plt.axis('off')

    plt.imshow(stimulus_image, extent = stimulus_extent)

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
        x_fixation_column = pd.Series(data_frame[CONFIG.X_FIXATION_COL_TITLE])
        y_fixation_column = pd.Series(data_frame[CONFIG.Y_FIXATION_COL_TITLE])
        timestamp_column = pd.Series(data_frame[CONFIG.TIMESTAMP_COL_TITLE])
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
        sizes[i] = (float(sizes[i])/float(maximum_size)) * CONFIG.MAX_FIXATION_POINT_SIZE

    return sizes

# Returns a figure containing a scatter plot of
# fixation data as specified in data_frame
def _get_fixation_scatter_plot(data_frame, color_palette, stimulus_file_name, show_axes, show_only_data_on_stimulus):
    # close previous plot
    plt.close('all')

    # font size
    plt.rcParams.update({'font.size': 5})

    # Getting relative size for each fixation point
    sizes = _get_fixation_size_array(data_frame)

    print(sizes)

    # create new scatter plot from data in data frame
    facet_grid_obj = sns.lmplot(x = CONFIG.X_FIXATION_COL_TITLE,
                                y = CONFIG.Y_FIXATION_COL_TITLE,
                                data = data_frame,
                                hue = 'participant_identifier',
                                palette = color_palette,
                                fit_reg = False,
                                height = CONFIG.PLOT_HEIGHT,
                                legend = False,
                                scatter_kws = {"s": sizes})

    # load in stimulus image
    stimulus_image = _import_stimulus_image(stimulus_file_name)

    # defining stimulus image extent in plot
    stimulus_image_x_max = len(stimulus_image[0])
    stimulus_image_y_max = len(stimulus_image)
    stimulus_image_x_shift = data_frame[CONFIG.STIMULUS_X_DISPLACEMENT_COL_TITLE].iloc[0]
    stimulus_image_y_shift = data_frame[CONFIG.STIMULUS_Y_DISPLACEMENT_COL_TITLE].iloc[0]

    stimulus_extent = [0 + stimulus_image_x_shift,
                       stimulus_image_x_max + stimulus_image_x_shift,
                       0 + stimulus_image_y_shift,
                       stimulus_image_y_max + stimulus_image_y_shift]

    data_frame.to_csv("output.csv")

    if show_only_data_on_stimulus:
        plt.axis(stimulus_extent)
    else:
        plt.axis([data_util._get_lower_lim(data_frame, CONFIG.X_FIXATION_COL_TITLE, stimulus_extent),
                  data_util._get_upper_lim(data_frame, CONFIG.X_FIXATION_COL_TITLE, stimulus_extent),
                  data_util._get_lower_lim(data_frame, CONFIG.Y_FIXATION_COL_TITLE, stimulus_extent),
                  data_util._get_upper_lim(data_frame, CONFIG.Y_FIXATION_COL_TITLE, stimulus_extent)])

    if show_axes:
        plt.axis('on')
    else:
        plt.axis('off')

    plt.imshow(stimulus_image, extent = stimulus_extent)

    return plt.gcf()

def _get_gaze_line_plot(data_frame, color_palette, stimulus_file_name, show_axes, show_only_data_on_stimulus):
    # close previous plot
    plt.close('all')

    # font size
    plt.rcParams.update({'font.size': 5})

    # create new scatter plot from data in data frame
    facet_grid_obj = sns.lineplot(x = CONFIG.X_GAZE_COL_TITLE,
                                  y = CONFIG.Y_GAZE_COL_TITLE,
                                  data = data_frame,
                                  hue = 'participant_identifier',
                                  palette = color_palette,
                                  legend = False,
                                  sort = False,
                                  ci = None)

    # load in stimulus image
    stimulus_image = _import_stimulus_image(stimulus_file_name)

    # defining stimulus image extent in plot
    stimulus_image_x_max = len(stimulus_image[0])
    stimulus_image_y_max = len(stimulus_image)
    stimulus_image_x_shift = data_frame[CONFIG.STIMULUS_X_DISPLACEMENT_COL_TITLE].iloc[0]
    stimulus_image_y_shift = data_frame[CONFIG.STIMULUS_Y_DISPLACEMENT_COL_TITLE].iloc[0]

    stimulus_extent = [0 + stimulus_image_x_shift,
                       stimulus_image_x_max + stimulus_image_x_shift,
                       0 + stimulus_image_y_shift,
                       stimulus_image_y_max + stimulus_image_y_shift]

    data_frame.to_csv("output.csv")

    if show_only_data_on_stimulus:
        plt.axis(stimulus_extent)
    else:
        plt.axis([data_util._get_lower_lim(data_frame, CONFIG.X_GAZE_COL_TITLE, stimulus_extent),
                  data_util._get_upper_lim(data_frame, CONFIG.X_GAZE_COL_TITLE, stimulus_extent),
                  data_util._get_lower_lim(data_frame, CONFIG.Y_GAZE_COL_TITLE, stimulus_extent),
                  data_util._get_upper_lim(data_frame, CONFIG.Y_GAZE_COL_TITLE, stimulus_extent)])

    if show_axes:
        plt.axis('on')
    else:
        plt.axis('off')

    plt.imshow(stimulus_image, extent = stimulus_extent)

    return plt.gcf()

def _get_fixation_line_plot(data_frame, color_palette, stimulus_file_name, show_axes, show_only_data_on_stimulus):
    # close previous plot
    plt.close('all')

    # font size
    plt.rcParams.update({'font.size': 5})

    # create new scatter plot from data in data frame
    facet_grid_obj = sns.lineplot(x = CONFIG.X_FIXATION_COL_TITLE,
                                  y = CONFIG.Y_FIXATION_COL_TITLE,
                                  data = data_frame,
                                  hue = 'participant_identifier',
                                  palette = color_palette,
                                  legend = False,
                                  sort = False,
                                  ci = None)

    # load in stimulus image
    stimulus_image = _import_stimulus_image(stimulus_file_name)

    # defining stimulus image extent in plot
    stimulus_image_x_max = len(stimulus_image[0])
    stimulus_image_y_max = len(stimulus_image)
    stimulus_image_x_shift = data_frame[CONFIG.STIMULUS_X_DISPLACEMENT_COL_TITLE].iloc[0]
    stimulus_image_y_shift = data_frame[CONFIG.STIMULUS_Y_DISPLACEMENT_COL_TITLE].iloc[0]

    stimulus_extent = [0 + stimulus_image_x_shift,
                       stimulus_image_x_max + stimulus_image_x_shift,
                       0 + stimulus_image_y_shift,
                       stimulus_image_y_max + stimulus_image_y_shift]

    data_frame.to_csv("output.csv")

    if show_only_data_on_stimulus:
        plt.axis(stimulus_extent)
    else:
        plt.axis([data_util._get_lower_lim(data_frame, CONFIG.X_FIXATION_COL_TITLE, stimulus_extent),
                  data_util._get_upper_lim(data_frame, CONFIG.X_FIXATION_COL_TITLE, stimulus_extent),
                  data_util._get_lower_lim(data_frame, CONFIG.Y_FIXATION_COL_TITLE, stimulus_extent),
                  data_util._get_upper_lim(data_frame, CONFIG.Y_FIXATION_COL_TITLE, stimulus_extent)])

    if show_axes:
        plt.axis('on')
    else:
        plt.axis('off')

    plt.imshow(stimulus_image, extent = stimulus_extent)

    return plt.gcf()

def _get_gaze_heat_map(data_frame, color_palette, stimulus_file_name, show_axes, show_only_data_on_stimulus):
    # close previous plot
    plt.close('all')

    # font size
    plt.rcParams.update({'font.size': 5})

    # im = Image.open(str(Path.cwd() / CONFIG.RELATIVE_STIMULUS_IMAGE_DIRECTORY / stimulus_file_name))
    # heatmap_image = Heatmap_Image(im.size)

    # create new scatter plot from data in data frame
    # facet_grid_obj = sns.heatmap(data = data_frame[[CONFIG.X_GAZE_COL_TITLE, CONFIG.Y_GAZE_COL_TITLE]])

    # load in stimulus image
    stimulus_image = _import_stimulus_image(stimulus_file_name)

    # defining stimulus image extent in plot
    stimulus_image_x_max = len(stimulus_image[0])
    stimulus_image_y_max = len(stimulus_image)
    stimulus_image_x_shift = data_frame[CONFIG.STIMULUS_X_DISPLACEMENT_COL_TITLE].iloc[0]
    stimulus_image_y_shift = data_frame[CONFIG.STIMULUS_Y_DISPLACEMENT_COL_TITLE].iloc[0]

    stimulus_extent = [0 + stimulus_image_x_shift,
                       stimulus_image_x_max + stimulus_image_x_shift,
                       0 + stimulus_image_y_shift,
                       stimulus_image_y_max + stimulus_image_y_shift]

    data_frame.to_csv("output.csv")

    if show_only_data_on_stimulus:
        plt.axis(stimulus_extent)
    else:
        plt.axis([data_util._get_lower_lim(data_frame, CONFIG.X_GAZE_COL_TITLE, stimulus_extent),
                  data_util._get_upper_lim(data_frame, CONFIG.X_GAZE_COL_TITLE, stimulus_extent),
                  data_util._get_lower_lim(data_frame, CONFIG.Y_GAZE_COL_TITLE, stimulus_extent),
                  data_util._get_upper_lim(data_frame, CONFIG.Y_GAZE_COL_TITLE, stimulus_extent)])

    if show_axes:
        plt.axis('on')
    else:
        plt.axis('off')

    plt.imshow(stimulus_image, extent = stimulus_extent)

    im = image.imread(str(Path.cwd() / CONFIG.RELATIVE_STIMULUS_IMAGE_DIRECTORY / stimulus_file_name))
    heatmap_image = Heatmap_Image((len(im[0]), len(im)))

    path = []

    for index in range(len(data_frame)):
        x_coordinate = data_frame[CONFIG.X_GAZE_COL_TITLE].iloc[index]
        if not math.isnan(x_coordinate):
            x_coordinate = int(data_frame[CONFIG.X_GAZE_COL_TITLE].iloc[index])

        y_coordinate = data_frame[CONFIG.Y_GAZE_COL_TITLE].iloc[index]
        if not math.isnan(y_coordinate):
            y_coordinate = int(data_frame[CONFIG.Y_GAZE_COL_TITLE].iloc[index])

        path.append((x_coordinate, y_coordinate))

    heatmap_image.update_heatmap_array_with_trial(path)
    heatmap_image.overlay_heatmap_on_Axes(plt.gca())

    return plt.gcf()

def _get_fixation_heat_map(data_frame, color_palette, stimulus_file_name, show_axes, show_only_data_on_stimulus):
    # close previous plot
    plt.close('all')

    # font size
    plt.rcParams.update({'font.size': 5})

    # load in stimulus image
    stimulus_image = _import_stimulus_image(stimulus_file_name)

    # defining stimulus image extent in plot
    stimulus_image_x_max = len(stimulus_image[0])
    stimulus_image_y_max = len(stimulus_image)
    stimulus_image_x_shift = data_frame[CONFIG.STIMULUS_X_DISPLACEMENT_COL_TITLE].iloc[0]
    stimulus_image_y_shift = data_frame[CONFIG.STIMULUS_Y_DISPLACEMENT_COL_TITLE].iloc[0]

    stimulus_extent = [0 + stimulus_image_x_shift,
                       stimulus_image_x_max + stimulus_image_x_shift,
                       0 + stimulus_image_y_shift,
                       stimulus_image_y_max + stimulus_image_y_shift]

    data_frame.to_csv("output.csv")

    if show_only_data_on_stimulus:
        plt.axis(stimulus_extent)
    else:
        plt.axis([data_util._get_lower_lim(data_frame, CONFIG.X_FIXATION_COL_TITLE, stimulus_extent),
                  data_util._get_upper_lim(data_frame, CONFIG.X_FIXATION_COL_TITLE, stimulus_extent),
                  data_util._get_lower_lim(data_frame, CONFIG.Y_FIXATION_COL_TITLE, stimulus_extent),
                  data_util._get_upper_lim(data_frame, CONFIG.Y_FIXATION_COL_TITLE, stimulus_extent)])

    if show_axes:
        plt.axis('on')
    else:
        plt.axis('off')

    plt.imshow(stimulus_image, extent = stimulus_extent)

    im = image.imread(str(Path.cwd() / CONFIG.RELATIVE_STIMULUS_IMAGE_DIRECTORY / stimulus_file_name))
    heatmap_image = Heatmap_Image((len(im[0]), len(im)))

    path = []

    for index in range(len(data_frame)):
        x_coordinate = data_frame[CONFIG.X_FIXATION_COL_TITLE].iloc[index]
        if math.isnan(x_coordinate):
            continue
        else:
            x_coordinate = int(data_frame[CONFIG.X_FIXATION_COL_TITLE].iloc[index])

        y_coordinate = -data_frame[CONFIG.Y_FIXATION_COL_TITLE].iloc[index]
        if math.isnan(y_coordinate):
            continue
        else:
            y_coordinate = int(data_frame[CONFIG.Y_FIXATION_COL_TITLE].iloc[index])

        path.append((x_coordinate, y_coordinate))

    heatmap_image.update_heatmap_array_with_trial(path)
    heatmap_image.overlay_heatmap_on_Axes(plt.gca())

    return plt.gcf()

    # create new scatter plot from data in data frame
    # facet_grid_obj = sns.heatmap(data=data_frame[[CONFIG.X_FIXATION_COL_TITLE, CONFIG.Y_FIXATION_COL_TITLE]])

    # # load in stimulus image
    # stimulus_image = _import_stimulus_image(stimulus_file_name)
    #
    # # defining stimulus image extent in plot
    # stimulus_image_x_max = len(stimulus_image[0])
    # stimulus_image_y_max = len(stimulus_image)
    # stimulus_image_x_shift = data_frame[CONFIG.STIMULUS_X_DISPLACEMENT_COL_TITLE].iloc[0]
    # stimulus_image_y_shift = data_frame[CONFIG.STIMULUS_Y_DISPLACEMENT_COL_TITLE].iloc[0]
    #
    # stimulus_extent = [0 + stimulus_image_x_shift,
    #                    stimulus_image_x_max + stimulus_image_x_shift,
    #                    0 + stimulus_image_y_shift,
    #                    stimulus_image_y_max + stimulus_image_y_shift]
    #
    # data_frame.to_csv("output.csv")
    #
    # if show_only_data_on_stimulus:
    #     plt.axis(stimulus_extent)
    # else:
    #     plt.axis([data_util._get_lower_lim(data_frame, CONFIG.X_FIXATION_COL_TITLE, stimulus_extent),
    #               data_util._get_upper_lim(data_frame, CONFIG.X_FIXATION_COL_TITLE, stimulus_extent),
    #               data_util._get_lower_lim(data_frame, CONFIG.Y_FIXATION_COL_TITLE, stimulus_extent),
    #               data_util._get_upper_lim(data_frame, CONFIG.Y_FIXATION_COL_TITLE, stimulus_extent)])
    #
    # if show_axes:
    #     plt.axis('on')
    # else:
    #     plt.axis('off')
    #
    # plt.imshow(stimulus_image, extent = stimulus_extent)

# Round the RGB values in the palette
def _scale_palette(color_palette):
    rounded_color_palette = []
    for color in color_palette:
        rounded_red_value = round(color[0] * 255)
        rounded_green_value = round(color[1] * 255)
        rounded_blue_value = round(color[2] * 255)
        rounded_color = (rounded_red_value,
                         rounded_green_value,
                         rounded_blue_value)
        rounded_color_palette.append(rounded_color)
    return rounded_color_palette

def _get_check_box_text(check_box):
    return check_box.text()

# Return a list of stimuli, where each stimulus corresponds to
# a trial on a participant, from a specified data frame
# and column title
def _get_stimuli(selected_participant_check_box_list, data_directory_path, col_title = CONFIG.STIMULUS_COL_TITLE):
    data_frame = data_util._get_data_frame_multiple_participants(list(map(_get_check_box_text, selected_participant_check_box_list)), data_directory_path)
    return data_frame[col_title].unique()

# Returns a list of stimuli that whose corresponding images
# could be found in the stimuli images directory specified
# in the project configuration file
def _get_found_stimuli(selected_participant_check_box_list, data_directory_path, col_title = CONFIG.STIMULUS_COL_TITLE):
    stimuli_list = _get_stimuli(selected_participant_check_box_list, data_directory_path, col_title)
    for stimulus in stimuli_list:
        if str(stimulus) in CONFIG.EXCLUDE_STIMULI_LIST:
            stimuli_list = np.delete(stimuli_list, np.argwhere(stimulus))
        elif not _stimulus_image_exists(str(stimulus)):
            stimuli_list = np.delete(stimuli_list, np.argwhere(stimulus))
    return stimuli_list
