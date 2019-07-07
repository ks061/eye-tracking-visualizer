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


# Returns a facet grid object containing a figure plotting
# gaze path data given a data frame
def _get_gaze_plot(data_frame, stimulus_file_name, show_axes,
                   show_only_data_on_stimulus):
    # close previous plot
    plt.close('all')

    data_frame_for_stimulus = data_util._get_data_frame_for_stimulus(data_frame, stimulus_file_name)

    # create new scatter plot from data in data frame
    sns.lmplot(CONFIG.X_GAZE_COL_TITLE, CONFIG.Y_GAZE_COL_TITLE,
               data = data_frame_for_stimulus, fit_reg = False, height = CONFIG.PLOT_HEIGHT,
               scatter_kws = {"s": 0.01})

    # load in stimulus image
    stimulus_image = _import_stimulus_image(stimulus_file_name)

    # defining stimulus image extent in plot
    stimulus_image_x_max = len(stimulus_image[0])
    stimulus_image_y_max = len(stimulus_image)
    stimulus_image_x_shift = data_frame_for_stimulus[CONFIG.STIMULUS_X_DISPLACEMENT_COL_TITLE].iloc[0]
    stimulus_image_y_shift = data_frame_for_stimulus[CONFIG.STIMULUS_Y_DISPLACEMENT_COL_TITLE].iloc[0]

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

    return plt.gcf()
