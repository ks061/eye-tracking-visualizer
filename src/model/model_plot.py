"""
Contains the class ModelPlot
"""

# External imports
import base64
import os.path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
# Internal imports
from PIL import Image
from sklearn.cluster import OPTICS

import src.main.config as config
from src.model.model_analysis_type_selection import ModelAnalysisTypeSelection
from src.model.model_data import ModelData
from src.model.model_data_type_selection import ModelDataTypeSelection
from src.model.model_stimulus_selection import ModelStimulusSelection


class ModelPlot:
    """
    Model for the plot
    """
    __instance = None

    fig = None
    x = None
    y = None
    color = None
    size = None

    stimulus_image = None
    x_len = None
    y_len = None
    x_shift = None
    y_shift = None

    def __init__(self):
        if ModelPlot.__instance is not None:
            raise Exception("ModelPlot should be treated as a singleton class.")
        else:
            ModelPlot.__instance = self

    @staticmethod
    def get_instance():
        """
        Static method to access the singleton
        instance for this class

        :return: the singleton instance
        :rtype: ModelPlot
        """
        if ModelPlot.__instance is None:
            ModelPlot()
        return ModelPlot.__instance

    # noinspection DuplicatedCode
    def set_x(self, x_col=None):
        """
        Extracts the x column from the model DataFrame
        and sets self.x from which to read the x coordinates
        of the plot from the pandas DataFrame in the data model
        :param x_col: None by default, or insert pandas DataFrame
        directly as the x column for this model
        :type x_col: list
        """
        if x_col is not None:
            self.x = x_col
            return

        data_type_selection = ModelDataTypeSelection.get_instance().get_selection()
        df = ModelData.get_instance().df
        x_col_name = None

        if data_type_selection == "Gaze Data":
            x_col_name = config.X_GAZE_COL_TITLE
        if data_type_selection == "Fixation Data":
            x_col_name = config.X_FIXATION_COL_TITLE

        self.x = df[x_col_name].copy(deep=True)

    # noinspection DuplicatedCode
    def set_y(self, y_col=None):
        """
        Extracts the y column from the model DataFrame
        and sets self.y from which to read the y coordinates
        of the plot from the pandas DataFrame in the data model
        :param y_col: None by default, or insert pandas DataFrame
        directly as the y column for this model
        :type y_col: list
        """
        if y_col is not None:
            self.y = y_col
            return

        data_type_selection = ModelDataTypeSelection.get_instance().get_selection()
        df = ModelData.get_instance().df
        y_col_name = None

        if data_type_selection == "Gaze Data":
            y_col_name = config.Y_GAZE_COL_TITLE
        if data_type_selection == "Fixation Data":
            y_col_name = config.Y_FIXATION_COL_TITLE

        self.y = df[y_col_name].copy(deep=True)

    def set_color(self, color_col=None):
        """
        Extracts the color column from the model DataFrame
        and sets self.color from which to distinguish
        colors within the plot from the pandas DataFrame
        in the data model
        :param color_col: None by default, or insert pandas DataFrame
            directly as the color column for this model
        :type color_col: list
        """
        if color_col is None:
            df = ModelData.get_instance().df
            color_col_name = "ParticipantName"
            color_col = df[color_col_name].copy(deep=True)

        self.color = pd.Categorical(color_col)

    def set_size(self, size_col=None):
        """
        Extracts the size column from the model DataFrame
        and sets self.size from which to distinguish
        sizes within the plot from the pandas DataFrame
        in the data model
        :param size_col: None by default, or insert pandas DataFrame
            directly as the size column for this model
        :type size_col: list
        """
        if size_col is not None:
            self.size = size_col
            return

    def update_fig(self, min_samples):
        """
        Updates the underlying figure based upon
        user's selections
        :param min_samples:
        """
        # clear df column fields
        self.x = None
        self.y = None
        self.color = None
        self.size = None

        self.set_x()
        self.set_y()
        self.set_color()

        analysis_type_selection = ModelAnalysisTypeSelection.get_instance().get_selection()
        data_type_selection = ModelDataTypeSelection.get_instance().get_selection()
        stimulus_file_name = ModelStimulusSelection.get_instance().get_selection()
        df = ModelData.get_instance().get_df()

        self.extract_and_set_stimulus_info(stimulus_file_name=stimulus_file_name, df=df)

        if data_type_selection == "Fixation Data":
            self.set_fixation_points_sizes_and_colors(
                df=ModelData.get_instance().get_df()
            )

        if analysis_type_selection == "Scatter Plot":
            self.fig = px.scatter(
                x=self.x,
                y=self.y,
                color=self.color,
                size=self.size
            )
        if analysis_type_selection == "Line Plot":
            self.fig = px.line(
                x=self.x,
                y=self.y,
                color=self.color
            )
        if analysis_type_selection == "Heat Map":
            self.fig = go.Figure(
                go.Histogram2dContour(
                    x=self.x,
                    y=self.y,
                    contours=dict(coloring='heatmap',
                                  showlines=False),
                    line=dict(width=0),
                    opacity=0.8
                )
            )
            self.fig.update_traces(
                visible=False,
                selector=dict(type='contour')
            )
        # "Cluster":
        if analysis_type_selection == "Cluster":
            self.perform_clustering(min_samples)
            self.fig = px.scatter(
                x=self.x,
                y=self.y,
                color=self.color
            )

        dir_path = os.path.dirname(os.path.realpath(__file__))
        img_path_str = dir_path + "/" + config.RELATIVE_STIMULUS_IMAGE_DIRECTORY + "/" + stimulus_file_name

        img_bmp = Image.open(os.path.abspath(img_path_str))
        img_bmp.save(os.path.abspath(
            img_path_str + ".png"
        ))
        enc_img = base64.b64encode(
            open(img_path_str + ".png", 'rb').read()
        )

        self.fig.add_layout_image(
            dict(
                source="data:image/png;base64,{}".format(enc_img.decode()),
                xref="x",
                yref="y",
                x=self.x_shift,
                y=self.y_shift + self.y_len,
                sizex=self.x_len,
                sizey=self.y_len,
                sizing="stretch",
                opacity=1,
                layer="below"
            )
        )
        self.fig.update_xaxes(
            showgrid=False,
            zeroline=False,
            range=[self.x_shift - (self.x_len * 0.10),
                   self.x_shift + self.x_len + (self.x_len * 0.10)]
        )
        self.fig.update_yaxes(
            showgrid=False,
            zeroline=False,
            range=[self.y_shift - (self.y_len * 0.10),
                   self.y_shift + self.y_len + (self.y_len * 0.10)],
            scaleanchor="x",
            scaleratio=1
        )

    def get_fig(self, min_samples):
        """
        Returns the underlying figure
        :return: underlying figure
        :rtype: plotly.graph_objects.Figure
        """
        self.update_fig(min_samples)
        return self.fig

    def set_fixation_points_sizes_and_colors(self,
                                             df,
                                             max_point_size=config.MAX_FIXATION_POINT_SIZE):
        """
        Sets the fixation point coordinates and the corresponding
        fixation_durations of the fixations being plotted, which, in turn, are proportional to
        how long a fixation has been looked at (for a particular participant)

        :param df: DataFrame containing fixations within eye-tracking data
            currently being analyzed
        :type df: pd.DataFrame
        :param max_point_size: size of the longest fixation point in the plot
        :type max_point_size: int
        """
        fixation_x_coords = []
        fixation_y_coords = []
        fixation_durations = []
        fixation_point_sizes = []
        fixation_participant_identifiers = []

        # always rolling variables
        prev_participant_identifier = ''
        prev_fixation_timestamp = 0

        # per fixation variables
        is_analyzing_fixation = False
        fixation_duration = 0
        curr_fixation_x_coord = -1
        curr_fixation_y_coord = -1
        # noinspection PyUnusedLocal
        curr_fixation_participant_identifier = None

        # per fixation booleans
        # (determining whether to continue analysis of current fixation)
        # noinspection PyUnusedLocal
        is_curr_x_coord_same_as_prev_x_coord = False
        # noinspection PyUnusedLocal
        is_curr_y_coord_same_as_prev_y_coord = False
        # noinspection PyUnusedLocal
        is_curr_participant_identifier_same_as_prev_participant_identifier = False

        # per fixation booleans (not yet in analysis of current fixation)
        # noinspection PyUnusedLocal
        is_curr_x_coord_nan = False
        # noinspection PyUnusedLocal
        is_curr_y_coord_nan = False

        # columns being analyzed
        x_coord_fixation_col = df[config.X_FIXATION_COL_TITLE].values.tolist()
        y_coord_fixation_col = df[config.Y_FIXATION_COL_TITLE].values.tolist()
        timestamp_col = df[config.TIMESTAMP_COL_TITLE].values.tolist()
        participant_identifier_col = df['participant_identifier'].values.tolist()

        for index in range(len(df.index)):
            # assessing if fixation is currently being iterated through
            if is_analyzing_fixation:
                # defining conditions for continuing to iterate through fixation
                # that is being analyzed
                is_curr_x_coord_same_as_prev_x_coord = \
                    x_coord_fixation_col[index] == curr_fixation_x_coord
                is_curr_y_coord_same_as_prev_y_coord = \
                    y_coord_fixation_col[index] == curr_fixation_y_coord
                is_curr_participant_identifier_same_as_prev_participant_identifier = \
                    participant_identifier_col[index] == prev_participant_identifier
                if (is_curr_x_coord_same_as_prev_x_coord and
                        is_curr_y_coord_same_as_prev_y_coord and
                        is_curr_participant_identifier_same_as_prev_participant_identifier):
                    fixation_duration += timestamp_col[index] - prev_fixation_timestamp
                else:  # finished analyzing current fixation
                    # add size of fixation to resulting list
                    fixation_durations.append(fixation_duration)
                    # reset variables related to
                    # analysis of the current fixation
                    fixation_duration = 0
                    curr_fixation_x_coord = -1
                    curr_fixation_y_coord = -1
                    is_analyzing_fixation = False
            else:
                # if not currently analyzing fixation and if
                # the fixation coordinates in the current row
                # are not nan, then start a new iterative fixation
                # size calculation
                is_curr_x_coord_nan = np.isnan(float(x_coord_fixation_col[index]))
                is_curr_y_coord_nan = np.isnan(float(x_coord_fixation_col[index]))
                if (not is_curr_x_coord_nan and
                        not is_curr_y_coord_nan):
                    is_analyzing_fixation = True
                    curr_fixation_x_coord = float(x_coord_fixation_col[index])
                    curr_fixation_y_coord = float(y_coord_fixation_col[index])
                    curr_fixation_participant_identifier = participant_identifier_col[index]

                    fixation_x_coords.append(curr_fixation_x_coord)
                    fixation_y_coords.append(curr_fixation_y_coord)
                    fixation_participant_identifiers.append(curr_fixation_participant_identifier)

            prev_fixation_timestamp = timestamp_col[index]
            prev_participant_identifier = participant_identifier_col[index]

        # scaling for maximum size
        max_fixation_duration = max(fixation_durations)
        for i in range(len(fixation_durations)):
            fixation_point_sizes.append(
                (float(fixation_durations[i]) / float(max_fixation_duration)) * max_point_size
            )

        xy = pd.concat(
            [
                pd.DataFrame(fixation_x_coords),
                pd.DataFrame(fixation_y_coords)
            ],
            axis=1
        )
        xy = xy.dropna()

        fixation_x_coords = xy.iloc[:, 0].tolist()
        fixation_y_coords = xy.iloc[:, 1].tolist()

        for i in range(len(fixation_x_coords)):
            fixation_x_coords[i] += self.x_shift

        for j in range(len(fixation_y_coords)):
            fixation_y_coords[j] += self.y_shift

        # noinspection PyTypeChecker
        self.set_x(pd.DataFrame(fixation_x_coords))
        # noinspection PyTypeChecker
        self.set_y(pd.DataFrame(fixation_y_coords))
        # noinspection PyTypeChecker
        self.set_color(pd.DataFrame(pd.Categorical(fixation_participant_identifiers)))
        # noinspection PyTypeChecker
        self.set_size(pd.DataFrame(fixation_point_sizes))

    def perform_clustering(self, min_samples):
        """
        Performs clustering on the x and y attributes,
        removing any x, y pairs that have either value
        missing from their respective attributes, and
        sets the color of the points based upon
        the cluster in which OPTICS assigns them to
        :param min_samples:
        """

        xy = pd.concat([self.x, self.y], axis=1)
        xy = xy.dropna()

        print(min_samples)
        labels = OPTICS(min_samples=min_samples, n_jobs=-1).fit(xy).labels_

        self.set_x(xy.iloc[:, 0].tolist())
        self.set_y(xy.iloc[:, 1].tolist())
        self.set_color(labels)

    def clear(self):
        """
        Clears the underlying figure stored in the model
        """
        self.fig = None

    def extract_and_set_stimulus_info(self, stimulus_file_name, df):
        """
        Saves the information about the stimulus image, including the image itself,
        the dimensions of it, and the x and y shifts of the image on the plot
        :param stimulus_file_name: filename of the stimulus
        :type stimulus_file_name: str
        :param df: data
        :type df: pd.DataFrame
        """
        self.stimulus_image = ModelStimulusSelection.get_instance().import_stimulus_image(stimulus_file_name)
        # defining stimulus image extent in plot
        self.x_len = len(self.stimulus_image[0])
        self.y_len = len(self.stimulus_image)
        self.x_shift = \
            df[config.STIMULUS_X_DISPLACEMENT_COL_TITLE][df[config.STIMULUS_X_DISPLACEMENT_COL_TITLE].notnull()].iloc[0]
        self.y_shift = \
            df[config.STIMULUS_Y_DISPLACEMENT_COL_TITLE][df[config.STIMULUS_Y_DISPLACEMENT_COL_TITLE].notnull()].iloc[0]
        if self.x_shift is None:
            self.x_shift = 0
        if self.y_shift is None:
            self.y_shift = 0
