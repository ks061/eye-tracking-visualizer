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

    def update_fig(self):
        """
        Updates the underlying figure based upon
        user's selections
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

        if analysis_type_selection == "Scatter Plot":
            if data_type_selection == "Fixation Data":
                self.set_fixation_points_sizes_and_colors(
                    df=ModelData.get_instance().get_df()
                )
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
        print(self.fig.data)
        print(self.fig.layout)
        print(self.fig.layout.template)
        stimulus_file_name = ModelStimulusSelection.get_instance().get_selection()
        df = ModelData.get_instance().get_df()

        stimulus_image = ModelStimulusSelection.get_instance().import_stimulus_image(stimulus_file_name)
        # defining stimulus image extent in plot
        x_len = len(stimulus_image[0])
        y_len = len(stimulus_image)
        x_shift = \
        df[config.STIMULUS_X_DISPLACEMENT_COL_TITLE][df[config.STIMULUS_X_DISPLACEMENT_COL_TITLE].notnull()].iloc[0]
        y_shift = \
        df[config.STIMULUS_Y_DISPLACEMENT_COL_TITLE][df[config.STIMULUS_Y_DISPLACEMENT_COL_TITLE].notnull()].iloc[0]
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
                x=x_shift,
                y=y_shift + y_len,
                sizex=x_len,
                sizey=y_len,
                sizing="stretch",
                opacity=1,
                layer="below"
            )
        )
        self.fig.update_xaxes(
            showgrid=False,
            zeroline=False,
            range=[x_shift - (x_len * 0.10), x_shift + x_len + (x_len * 0.10)]
        )
        self.fig.update_yaxes(
            showgrid=False,
            zeroline=False,
            range=[y_shift - (y_len * 0.10), y_shift + y_len + (y_len * 0.10)],
            scaleanchor="x",
            scaleratio=1
        )

    def get_fig(self):
        """
        Returns the underlying figure
        :return: underlying figure
        :rtype: plotly.graph_objects.Figure
        """
        self.update_fig()
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
        x_coord_fixation_col = pd.Series(df[config.X_FIXATION_COL_TITLE])
        y_coord_fixation_col = pd.Series(df[config.Y_FIXATION_COL_TITLE])
        timestamp_col = pd.Series(df[config.TIMESTAMP_COL_TITLE])
        participant_identifier_col = pd.Series(df['participant_identifier'])

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

        self.set_x(fixation_x_coords)
        self.set_y(fixation_y_coords)
        self.set_color(fixation_participant_identifiers)
        self.set_size(fixation_point_sizes)

    def clear(self):
        """
        Clears the underlying figure stored in the model
        """
        self.fig = None
