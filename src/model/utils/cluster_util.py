import math

import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

if __name__ == '__main__':
    # import project libraries
    import src.main.config as config
    import src.model.utils.data_util as data_util
    import src.view.utils.visual_util as visual_util


def _cluster_range_query(data_frame_cluster, index_list_of_all_points, index_of_center_point,
                         max_dist_btw_center_point_and_potential_neighbor, x_col_title, y_col_title):
    neighbor_point_index_list = []
    for index_of_potential_neighbor in index_list_of_all_points:
        x1 = data_frame_cluster.loc[index_of_center_point, x_col_title]
        x2 = data_frame_cluster.loc[index_of_potential_neighbor, x_col_title]
        y1 = data_frame_cluster.loc[index_of_center_point, y_col_title]
        y2 = data_frame_cluster.loc[index_of_potential_neighbor, y_col_title]
        dist_btw_center_point_and_potential_neighbor = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        if dist_btw_center_point_and_potential_neighbor <= max_dist_btw_center_point_and_potential_neighbor:
            neighbor_point_index_list.append(index_of_potential_neighbor)
    return neighbor_point_index_list


def _cluster_range_query_gaze(data_frame_cluster, index_list_of_all_points, index_of_center_point,
                              max_dist_btw_center_point_and_potential_neighbor):
    return _cluster_range_query(data_frame_cluster, index_list_of_all_points, index_of_center_point,
                                max_dist_btw_center_point_and_potential_neighbor, config.X_GAZE_COL_TITLE,
                                config.Y_GAZE_COL_TITLE)


def _cluster_range_query_fixation(data_frame_cluster, index_list_of_all_points, index_of_center_point,
                                  max_dist_btw_center_point_and_potential_neighbor):
    return _cluster_range_query(data_frame_cluster, index_list_of_all_points, index_of_center_point,
                                max_dist_btw_center_point_and_potential_neighbor, config.X_FIXATION_COL_TITLE,
                                config.Y_FIXATION_COL_TITLE)


def get_fixation_cluster_plot(data_frame, stimulus_file_name, show_axes, show_only_data_on_stimulus):
    # close previous plot
    plt.close('all')

    # font size
    plt.rcParams.update({'font.size': 5})

    data_frame_cluster = data_frame.copy(deep=True)
    data_frame_cluster.reset_index(drop=True, inplace=True)
    c = 0
    num_rows = data_frame_cluster.shape[0]
    data_frame_cluster['cluster_identifier'] = pd.Series(["-1" for _ in range(0, num_rows)],
                                                         index=data_frame_cluster.index)
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
        c += 1
        data_frame_cluster.loc[index, 'cluster_identifier'] = str(c)
        seed = neighbors.copy()
        seed.remove(index)
        for index_seed in seed:
            if data_frame_cluster.loc[index_seed, 'cluster_identifier'] == "Noise":
                data_frame_cluster.loc[index_seed, 'cluster_identifier'] = str(c)
            if data_frame_cluster.loc[index_seed, 'cluster_identifier'] != "-1":
                continue
            data_frame_cluster.loc[index_seed, 'cluster_identifier'] = str(c)
            neighbors = _cluster_range_query_fixation(data_frame_cluster, data_frame_index_list, index_seed,
                                                      max_neighbor_distance_for_cluster)
            if len(neighbors) >= min_points_in_cluster:
                seed.extend(neighbors)

    cluster_color_palette = sns.color_palette("gist_rainbow", c)

    # create new scatter plot from data in data frame
    sns.lmplot(x=config.X_FIXATION_COL_TITLE,
               y=config.Y_FIXATION_COL_TITLE,
               data=data_frame_cluster,
               hue='cluster_identifier',
               palette=cluster_color_palette,
               fit_reg=False,
               height=config.PLOT_HEIGHT,
               legend=False,
               scatter_kws={"s": 1})

    # load in stimulus image
    stimulus_image = visual_util.import_stimulus_image(stimulus_file_name)

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


def get_gaze_cluster_plot(data_frame, stimulus_file_name, show_axes, show_only_data_on_stimulus):
    # close previous plot
    plt.close('all')

    # font size
    plt.rcParams.update({'font.size': 5})

    data_frame_cluster = data_frame.copy(deep=True)
    data_frame_cluster.reset_index(drop=True, inplace=True)
    c = 0
    num_rows = data_frame_cluster.shape[0]
    data_frame_cluster['cluster_identifier'] = pd.Series(["-1" for _ in range(0, num_rows)],
                                                         index=data_frame_cluster.index)
    data_frame_index_list = [i for i in range(0, num_rows)]
    max_neighbor_distance_for_cluster = 20
    min_points_in_cluster = 15
    for index in data_frame_index_list:
        if data_frame_cluster.loc[index, 'cluster_identifier'] != "-1":
            continue
        neighbors = _cluster_range_query_gaze(data_frame_cluster, data_frame_index_list, index,
                                              max_neighbor_distance_for_cluster)
        if len(neighbors) < min_points_in_cluster:
            data_frame_cluster.loc[index, 'cluster_identifier'] = "Noise"
            continue
        c += 1
        data_frame_cluster.loc[index, 'cluster_identifier'] = str(c)
        seed = neighbors.copy()
        seed.remove(index)
        for index_seed in seed:
            if data_frame_cluster.loc[index_seed, 'cluster_identifier'] == "Noise":
                data_frame_cluster.loc[index_seed, 'cluster_identifier'] = str(c)
            if data_frame_cluster.loc[index_seed, 'cluster_identifier'] != "-1":
                continue
            data_frame_cluster.loc[index_seed, 'cluster_identifier'] = str(c)
            neighbors = _cluster_range_query_gaze(data_frame_cluster, data_frame_index_list, index_seed,
                                                  max_neighbor_distance_for_cluster)
            if len(neighbors) >= min_points_in_cluster:
                seed.extend(neighbors)

    print("c: " + str(c))
    cluster_color_palette = sns.color_palette("gist_rainbow", c)

    # create new scatter plot from data in data frame
    sns.lmplot(x=config.X_GAZE_COL_TITLE,
               y=config.Y_GAZE_COL_TITLE,
               data=data_frame_cluster,
               hue='cluster_identifier',
               palette=cluster_color_palette,
               fit_reg=False,
               height=config.PLOT_HEIGHT,
               legend=False,
               scatter_kws={"s": 1})

    # load in stimulus image
    stimulus_image = visual_util.import_stimulus_image(stimulus_file_name)

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
