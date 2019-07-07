# Project libraries
import config as CONFIG
import data_util

# Data libraries
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

# Returns a 2D array with RGB values for each
# pixel in the specified file_name containing the
# stimulus image
def _import_stimulus_image(file_name):
    return plt.imread(file_name)

# Returns a blank plot
def _get_blank_plot():
    data_frame = pd.DataFrame(columns=['X', 'Y'])
    x_title = 'X'
    y_title = 'Y'
    sns.lmplot(x_title, y_title, data_frame, height = CONFIG.PLOT_HEIGHT)
    plt.axis('off')
    return plt.gcf()

def _get_data_frame_for_stimulus(data_frame, stimulus_file_name):

    # Find index of stimulus_file_name
    stimulus_series = data_frame[CONFIG.STIMULUS_COL_TITLE]
    data_frame_num_rows = data_frame.shape[0]
    for row_index in range(data_frame_num_rows):
        if (str(stimulus_series[row_index]) not in CONFIG.EXCLUDE_STIMULI_LIST):
            data_frame_start_index = row_index + 1

    # Find end index of data related to this stimulus
    data_frame_num_rows = data_frame.shape[0]
    for row_index in range(data_frame_start_index, data_frame_num_rows):
        if (str(stimulus_series[row_index]) not in CONFIG.EXCLUDE_STIMULI_LIST):
            data_frame_end_index = row_index - 1
        elif (row_index == data_frame_num_rows - 1):
            data_frame_end_index = row_index

    data_frame_for_stimulus = data_util._filter_data(data_frame,
                                                    [CONFIG.X_GAZE_COL_TITLE,
                                                     CONFIG.Y_GAZE_COL_TITLE])
    return data_frame_for_stimulus[data_frame_start_index : data_frame_end_index + 1]



# Returns a facet grid object containing a figure plotting
# gaze path data given a data frame
def _get_gaze_plot(data_frame, stimulus_file_name, show_axes,
                   show_only_data_on_stimulus):
    # close previous plot
    plt.close('all')

    data_frame_for_stimulus = _get_data_frame_for_stimulus(data_frame, stimulus_file_name)

    # create new scatter plot from data in data frame
    sns.lmplot(CONFIG.X_GAZE_COL_TITLE, CONFIG.Y_GAZE_COL_TITLE,
               data = data_frame_for_stimulus, fit_reg = False, height = CONFIG.PLOT_HEIGHT,
               scatter_kws = {"s": 0.01})

    # load in stimulus image
    stimulus_image = _import_stimulus_image(stimulus_file_name)

    # defining stimulus image extent in plot
    stimulus_image_x_max = len(stimulus_image[0])
    stimulus_image_y_max = len(stimulus_image)
    stimulus_image_x_shift = 171
    stimulus_image_y_shift = 0
    # stimulus_image_x_shift = _get_stimulus_image_x_shift()
    # stimulus_image_y_shift = _get_stimulus_image_y_shift()
    stimulus_extent = [0 + stimulus_image_x_shift,
                       stimulus_image_x_max + stimulus_image_x_shift,
                       0 + stimulus_image_y_shift,
                       stimulus_image_y_max + stimulus_image_y_shift]


    if (show_only_data_on_stimulus):
        plt.axis(stimulus_extent)
    else:
        plt.axis([data_util._get_lower_lim(data_frame_for_stimulus, CONFIG.X_GAZE_COL_TITLE, stimulus_extent),
                  data_util._get_upper_lim(data_frame_for_stimulus, CONFIG.X_GAZE_COL_TITLE, stimulus_extent),
                  data_util._get_lower_lim(data_frame_for_stimulus, CONFIG.Y_GAZE_COL_TITLE, stimulus_extent),
                  data_util._get_upper_lim(data_frame_for_stimulus, CONFIG.Y_GAZE_COL_TITLE, stimulus_extent)])

    if (show_axes):
        plt.axis('on')
    else:
        plt.axis('off')

    plt.imshow(stimulus_image, extent = stimulus_extent)

  # facet_grid.set(xlim=[0+171,1023+171], ylim=[0,768])
  # facet_grid.set(xlim=(get_lower_lim(data_frame, CONFIG.X_GAZE_COL_TITLE),
                       # get_upper_lim(data_frame, CONFIG.X_GAZE_COL_TITLE)))
  # facet_grid.set(ylim=(get_lower_lim(data_frame, CONFIG.Y_GAZE_COL_TITLE),
                       # get_upper_lim(data_frame, CONFIG.Y_GAZE_COL_TITLE)))
    return plt.gcf()
