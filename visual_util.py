import os

# Project libraries
import config as CONFIG
import data_util

# Data libraries
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

# Returns True if image exists
def _stimulus_image_exists(stimulus_image_file_name):
    return os.path.exists(CONFIG.RELATIVE_STIMULUS_IMAGE_DIRECTORY + stimulus_image_file_name)

# Returns a 2D array with RGB values for each
# pixel in the specified file_name containing the
# stimulus image
def _import_stimulus_image(stimulus_image_file_name):
    return plt.imread(CONFIG.RELATIVE_STIMULUS_IMAGE_DIRECTORY + stimulus_image_file_name)

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


# Returns a figure containing a scatter plot of
# gaze path data as specified in data_frame
def _get_gaze_plot(data_frame, stimulus_file_name, show_axes, show_only_data_on_stimulus):
    # close previous plot
    plt.close('all')

    # create new scatter plot from data in data frame
    facet_grid_obj = sns.lmplot(CONFIG.X_GAZE_COL_TITLE,
                                 y = CONFIG.Y_GAZE_COL_TITLE,
                                 data = data_frame,
                                 hue = 'participant_identifier',
                                 fit_reg = False,
                                 height = CONFIG.PLOT_HEIGHT,
                                 legend = False)

    # add title to graph
    # facet_grid_obj.fig.suptitle(CONFIG.GAZE_SCATTER_PLOT_TITLE)

    # legend inspection -- remove later
    # print(len(dir(facet_grid_obj._legend)))
    # for attr in dir(facet_grid_obj._legend):
    #     print(str(type(getattr(facet_grid_obj._legend, attr))) + ": " + attr)

    # manage legend for scatterplot
    # axes = facet_grid_obj.axes
    # ax = axes[0, 0]
    # ax.set_position([ax.get_position().x0, ax.get_position().y0 +\
    #                 ax.get_position().height * 0.2, ax.get_position().width,
    #                 ax.get_position().height * 0.8])
    # handles, labels = ax.get_legend_handles_labels()
    # ax.legend(handles=handles[1:], labels=labels[1:])
    # ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2), fancybox=True, shadow=True)

    # plot_legend = facet_grid_obj._legend
    # plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), fancybox=True, shadow=True)
    # plot_legend.set_bbox_to_anchor([0.5, -0.15])
    # plot_legend._loc = 2

    # custom legend configuration for 800 x 600 px display
    # ax = plt.gca()
    # ax.set_position([ax.get_position().x0, ax.get_position().y0 +\
    #                 ax.get_position().height * 0.2, ax.get_position().width,
    #                 ax.get_position().height * 0.8])
    # handles, labels = ax.get_legend_handles_labels()
    # print(handles)
    # print(labels)
    # ax.legend(prop={'size':6})
    # ax.legend(handles=handles[1:], labels=labels[1:])
    # ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), fancybox=True, shadow=True)

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


    if (show_only_data_on_stimulus):
        plt.axis(stimulus_extent)
    else:
        plt.axis([data_util._get_lower_lim(data_frame, CONFIG.X_GAZE_COL_TITLE, stimulus_extent),
                  data_util._get_upper_lim(data_frame, CONFIG.X_GAZE_COL_TITLE, stimulus_extent),
                  data_util._get_lower_lim(data_frame, CONFIG.Y_GAZE_COL_TITLE, stimulus_extent),
                  data_util._get_upper_lim(data_frame, CONFIG.Y_GAZE_COL_TITLE, stimulus_extent)])

    if (show_axes):
        plt.axis('on')
    else:
        plt.axis('off')

    plt.imshow(stimulus_image, extent = stimulus_extent)

    return plt.gcf()
