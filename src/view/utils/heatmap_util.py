import math
from pathlib import Path

from matplotlib import pyplot as plt, image

from src.view.utils.heatmap_image import HeatmapImage

if __name__ == 'main':
    # import project libraries
    import src.main.config as config
    import src.model.utils.data_util as data_util
    import src.view.utils.visual_util as visual_util


def get_fixation_heat_map(data_frame, stimulus_file_name, show_axes, show_only_data_on_stimulus):
    # close previous plot
    plt.close('all')

    # font size
    plt.rcParams.update({'font.size': 5})

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

    im = image.imread(str(Path.cwd() / config.RELATIVE_STIMULUS_IMAGE_DIRECTORY / stimulus_file_name))
    heatmap_image = HeatmapImage((len(im[0]), len(im)))

    path = []

    for index in range(len(data_frame)):
        x_coordinate = data_frame[config.X_FIXATION_COL_TITLE].iloc[index]
        if math.isnan(x_coordinate):
            continue
        else:
            x_coordinate = int(data_frame[config.X_FIXATION_COL_TITLE].iloc[index])

        y_coordinate = -data_frame[config.Y_FIXATION_COL_TITLE].iloc[index]
        if math.isnan(y_coordinate):
            continue
        else:
            y_coordinate = int(data_frame[config.Y_FIXATION_COL_TITLE].iloc[index])

        path.append((x_coordinate, y_coordinate))

    heatmap_image.update_heatmap_array_with_trial(path)
    heatmap_image.overlay_heatmap_on_axes(plt.gca())

    return plt.gcf()
