"""
Contains the class ModelPlot

MODULAR INTERNAL IMPORTS ARE AT THE BOTTOM OF THE FILE. THIS IS AN
INTENTIONAL DESIGN CHOICE. IT HELPS AVOID CIRCULAR IMPORT ISSUES.
IT IS ALSO OKAY TO AVOID THEM IN THIS MANNER BECAUSE THIS IS A
HIGHLY MODULAR PROGRAM.
"""

import base64
import os.path
import numba
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image, ImageOps
from numba.core.errors import NumbaWarning, NumbaDeprecationWarning, NumbaPendingDeprecationWarning
import warnings
from sklearn.cluster import DBSCAN

from src.main.config import MAX_FIXATION_PT_SIZE, DEFAULT_EPS_VALUE, DEFAULT_MIN_SAMPLES_VALUE, MAKE_IMG_GRAYSCALE
from src.main.config import STIMULUS_COL_TITLE
from src.main.config import PARTICIPANT_FILENAME_COL_TITLE
from src.main.config import PARTICIPANT_NAME_COL_TITLE
from src.main.config import RELATIVE_STIMULUS_IMAGE_DIR
from src.main.config import STIMULUS_X_DISPLACEMENT_COL_TITLE
from src.main.config import STIMULUS_Y_DISPLACEMENT_COL_TITLE
from src.main.config import TIMESTAMP_COL_TITLE
from src.main.config import X_FIXATION_COL_TITLE
from src.main.config import X_GAZE_COL_TITLE
from src.main.config import Y_FIXATION_COL_TITLE
from src.main.config import Y_GAZE_COL_TITLE


class ModelPlot(object):
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

    def clear(self) -> None:
        self.fig = None

    def __init__(self):
        if ModelPlot.__instance is not None:
            raise Exception("ModelPlot should be treated as a singleton class.")
        else:
            ModelPlot.__instance = self
        self._suppress_warnings()

    @staticmethod
    def _suppress_warnings() -> None:
        """
        Suppress numba warnings
        """
        warnings.simplefilter('ignore', category=NumbaWarning)
        warnings.simplefilter('ignore', category=NumbaDeprecationWarning)
        warnings.simplefilter('ignore', category=NumbaPendingDeprecationWarning)

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
    def set_x(self, df: pd.DataFrame = None, x_col: pd.Series = None) -> None:
        """
        Extracts the x column from the model DataFrame
        and sets self.x from which to read the x coordinates
        of the plot from the pandas DataFrame in the data model
        :param df: eye-tracking data
        :type df: pd.DataFrame
        :param x_col: None by default, or insert pandas DataFrame
        directly as the x column for this model
        :type x_col: pd.Series
        """
        if x_col is not None:
            self.x = x_col
            return
        elif df is not None:
            data_type_selection = ViewDataTypeSelection.get_instance().get_selected()
            x_col_name = None

            if data_type_selection == "Gaze Data":
                x_col_name = X_GAZE_COL_TITLE
            if data_type_selection == "Fixation Data":
                x_col_name = X_FIXATION_COL_TITLE

            self.x = df[x_col_name]
        else:
            raise Exception("Parameters df and x_col cannot both be None.")

    # noinspection DuplicatedCode
    def set_y(self, df: pd.DataFrame = None, y_col: pd.Series = None) -> None:
        """
        Extracts the y column from the model DataFrame
        and sets self.y from which to read the y coordinates
        of the plot from the pandas DataFrame in the data model
        :param df: eye-tracking data
        :type df: pd.DataFrame
        :param y_col: None by default, or insert pandas DataFrame
        directly as the y column for this model
        :type y_col: pd.Series
        """
        if y_col is not None:
            self.y = y_col
            return
        elif df is not None:
            data_type_selection = ViewDataTypeSelection.get_instance().get_selected()
            y_col_name = None

            if data_type_selection == "Gaze Data":
                y_col_name = Y_GAZE_COL_TITLE
            if data_type_selection == "Fixation Data":
                y_col_name = Y_FIXATION_COL_TITLE

            self.y = df[y_col_name]
        else:
            raise Exception("Parameters df and y_col cannot both be None.")

    def set_color(self, df: pd.DataFrame = None, color_col: list = None) -> None:
        """
        Extracts the color column from the model DataFrame
        and sets self.color from which to distinguish
        colors within the plot from the pandas DataFrame
        in the data model
        :param df: eye-tracking data
        :type df: pd.DataFrame
        :param color_col: None by default, or insert pandas DataFrame
            directly as the color column for this model
        :type color_col: list
        """
        if color_col is None and df is None:
            raise Exception("Parameters df and color_col cannot both be None.")

        if color_col is None:
            color_col_name = PARTICIPANT_NAME_COL_TITLE
            color_col = df[color_col_name].copy(deep=True)
        self.color = pd.Categorical(color_col)

    def set_size(self, size_col: list = None) -> None:
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

    def fig_params_clear(self) -> None:
        self.x, self.y, self.color, self.size = None, None, None, None

    def set_gaze_params(self, df: pd.DataFrame) -> None:
        self.set_x(df=df), self.set_y(df=df), self.set_color(df=df)

    @numba.jit
    def update_fig(self) -> go.Figure:
        """
        Updates the underlying figure based upon
        user's selections

        """
        self.fig_params_clear()

        df = ModelData.get_instance().df
        selected_stimulus_filename = ViewStimulusSelection.get_instance().get_selected()

        df = df[df[STIMULUS_COL_TITLE] == selected_stimulus_filename]
        df = df[df[PARTICIPANT_FILENAME_COL_TITLE].isin(
            ModelParticipantSelection.get_instance().get_selected_participants()
        )]

        self.extract_and_set_stimulus_params(
            selected_stimulus_filename=selected_stimulus_filename, df=df
        )

        data_type_selection = ViewDataTypeSelection.get_instance().get_selected()
        analysis_type_selection = ViewAnalysisTypeSelection.get_instance().get_selected()

        if data_type_selection == "Fixation Data":
            df = model_utils.remove_incomplete_observations(
                df,
                [TIMESTAMP_COL_TITLE, X_FIXATION_COL_TITLE, Y_FIXATION_COL_TITLE]
            )
            self.set_fixation_params(df=df)
        else:
            df = model_utils.remove_incomplete_observations(
                df,
                [TIMESTAMP_COL_TITLE, X_GAZE_COL_TITLE, Y_GAZE_COL_TITLE]
            )
            self.set_gaze_params(df=df)

        if analysis_type_selection == "Scatter Plot":
            self.fig = px.scatter(
                x=self.x,
                y=self.y,
                color=self.color,
                size=self.size,
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
            self.perform_optics_clustering()
            self.fig = px.scatter(
                x=self.x,
                y=self.y,
                color=self.color
            )
        self.fig.add_annotation(
            x=800,
            y=600,
            xref="x",
            yref="y",
            text="1",
            showarrow=True,
            font=dict(
                family="Courier New, monospace",
                size=36,
                color="#ffffff"
            ),
            align="center",
            # arrowhead=2,
            # arrowsize=1,
            # arrowwidth=2,
            # arrowcolor="#636363",
            # ax=20,
            # ay=-30,
            # bordercolor="#c7c7c7",
            borderwidth=2,
            borderpad=4,
            bgcolor="#EE4B2B",
            opacity=0.5
        )

        img_path_str = RELATIVE_STIMULUS_IMAGE_DIR + "/" + selected_stimulus_filename

        img_bmp = Image.open(os.path.abspath(img_path_str))
        img_bmp = ImageOps.grayscale(img_bmp) if MAKE_IMG_GRAYSCALE else img_bmp
        img_bmp.save(os.path.abspath(img_path_str + ".png"))
        enc_img = base64.b64encode(open(img_path_str + ".png", 'rb').read())

        self.fig.add_layout_image(
            dict(
                source="data:image/png;base64,{}".format(enc_img.decode()),
                xref="x",
                yref="y",
                x=self.x_shift,
                y=self.y_shift,
                sizex=self.x_len,
                sizey=self.y_len,
                sizing="stretch",
                opacity=0.4,
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
            scaleratio=1,
            autorange="reversed"
        )

        return self.fig

    @numba.jit
    def set_fixation_params(self,
                            df: pd.DataFrame,
                            max_point_size: int = MAX_FIXATION_PT_SIZE) -> None:
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
        curr_fixation_duration = 0
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
        # noinspection PyUnusedLocal
        is_curr_x_coord_nan = False
        # noinspection PyUnusedLocal
        is_curr_y_coord_nan = False

        # data being analyzed
        timestamps = df[TIMESTAMP_COL_TITLE].values.tolist()
        x_coord_fixation_points = df[X_FIXATION_COL_TITLE].values.tolist()
        y_coord_fixation_points = df[Y_FIXATION_COL_TITLE].values.tolist()
        participant_identifiers = df[PARTICIPANT_NAME_COL_TITLE].values.tolist()

        for index in range(len(df.index)):
            # assessing if fixation is currently being iterated through
            if is_analyzing_fixation:
                # defining conditions for continuing to iterate through fixation
                # that is being analyzed
                is_curr_x_coord_same_as_prev_x_coord = \
                    x_coord_fixation_points[index] == curr_fixation_x_coord
                is_curr_y_coord_same_as_prev_y_coord = \
                    y_coord_fixation_points[index] == curr_fixation_y_coord
                is_curr_participant_identifier_same_as_prev_participant_identifier = \
                    participant_identifiers[index] == prev_participant_identifier
                if (is_curr_x_coord_same_as_prev_x_coord and
                        is_curr_y_coord_same_as_prev_y_coord and
                        is_curr_participant_identifier_same_as_prev_participant_identifier):
                    curr_fixation_duration += timestamps[index] - prev_fixation_timestamp
                else:  # finished analyzing current fixation
                    # add size of fixation to resulting list
                    fixation_durations.append(curr_fixation_duration)
                    # reset variables related to
                    # analysis of the current fixation
                    curr_fixation_duration = 0
                    curr_fixation_x_coord = -1
                    curr_fixation_y_coord = -1
                    is_analyzing_fixation = False
            else:
                # if not currently analyzing fixation and if
                # the fixation coordinates in the current row
                # are not nan, then start a new iterative fixation
                # size calculation
                is_curr_x_coord_nan = np.isnan(float(x_coord_fixation_points[index]))
                is_curr_y_coord_nan = np.isnan(float(x_coord_fixation_points[index]))
                if (not is_curr_x_coord_nan and
                        not is_curr_y_coord_nan):
                    is_analyzing_fixation = True
                    curr_fixation_x_coord = float(x_coord_fixation_points[index])
                    curr_fixation_y_coord = float(y_coord_fixation_points[index])
                    curr_fixation_participant_identifier = participant_identifiers[index]

                    fixation_x_coords.append(curr_fixation_x_coord)
                    fixation_y_coords.append(curr_fixation_y_coord)
                    fixation_participant_identifiers.append(curr_fixation_participant_identifier)

            prev_fixation_timestamp = timestamps[index]
            prev_participant_identifier = participant_identifiers[index]

        if is_analyzing_fixation:
            fixation_durations.append(curr_fixation_duration)

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
        xy.dropna(inplace=True)

        fixation_x_coords = xy.iloc[:, 0].tolist()
        fixation_y_coords = xy.iloc[:, 1].tolist()

        for i in range(len(fixation_x_coords)):
            fixation_x_coords[i] += self.x_shift

        for j in range(len(fixation_y_coords)):
            fixation_y_coords[j] += self.y_shift

        # noinspection PyTypeChecker
        self.set_x(df=df, x_col=pd.Series(fixation_x_coords))
        # noinspection PyTypeChecker
        self.set_y(df=df, y_col=pd.Series(fixation_y_coords))
        # noinspection PyTypeChecker
        self.set_color(df=df, color_col=pd.Series(pd.Categorical(fixation_participant_identifiers)))
        # noinspection PyTypeChecker
        self.set_size(size_col=pd.Series(fixation_point_sizes))

    @staticmethod
    def get_eps_value():
        try:
            eps_value = int(ViewPlot.get_instance().eps_curr_value.text())
        except ValueError:
            eps_value = ""
        if eps_value == "":
            ViewPlot.get_instance().eps_input_min.setText(str(int(DEFAULT_EPS_VALUE - DEFAULT_EPS_VALUE*.5)))
            ViewPlot.get_instance().eps_input_min.returnPressed.emit()
            ViewPlot.get_instance().eps_input_max.setText(str(int(DEFAULT_EPS_VALUE + DEFAULT_EPS_VALUE*.5)))
            ViewPlot.get_instance().eps_input_max.returnPressed.emit()
            ViewPlot.get_instance().eps_slider.sliderMoved.emit(int(DEFAULT_EPS_VALUE))
            eps_value = int(ViewPlot.get_instance().eps_curr_value.text())
        return eps_value

    @staticmethod
    def get_min_samples_value():
        try:
            min_samples_value = int(ViewPlot.get_instance().min_samples_curr_value.text())
        except ValueError:
            min_samples_value = ""
        if min_samples_value == "":
            ViewPlot.get_instance().min_samples_input_min.setText(
                str(int(DEFAULT_MIN_SAMPLES_VALUE - DEFAULT_MIN_SAMPLES_VALUE*.5))
            )
            ViewPlot.get_instance().min_samples_input_min.returnPressed.emit()
            ViewPlot.get_instance().min_samples_input_max.setText(
                str(int(DEFAULT_MIN_SAMPLES_VALUE + DEFAULT_MIN_SAMPLES_VALUE*.5))
            )
            ViewPlot.get_instance().min_samples_input_max.returnPressed.emit()
            ViewPlot.get_instance().min_samples_slider.sliderMoved.emit(int(DEFAULT_MIN_SAMPLES_VALUE))
            min_samples_value = int(ViewPlot.get_instance().min_samples_curr_value.text())
        return min_samples_value

    @numba.jit
    def perform_optics_clustering(self) -> None:
        """
        Performs clustering on the x and y attributes,
        removing any x, y pairs that have either value
        missing from their respective attributes, and
        sets the color of the points based upon
        the cluster in which OPTICS assigns them to
        """

        xy = pd.concat([self.x, self.y], axis=1)
        xy = xy.dropna()

        labels = DBSCAN(eps=ModelPlot.get_eps_value(), min_samples=ModelPlot.get_min_samples_value(), n_jobs=-1).fit(
            xy).labels_

        # df=None will be ignored
        self.set_x(x_col=xy.iloc[:, 0].tolist())
        self.set_y(y_col=xy.iloc[:, 1].tolist())
        self.set_color(color_col=labels)

    def extract_and_set_stimulus_params(self,
                                        selected_stimulus_filename: str,
                                        df: pd.DataFrame) -> None:
        """
        Saves the information about the stimulus image, including the image itself,
        the dimensions of it, and the x and y shifts of the image on the plot
        :param selected_stimulus_filename: filename of the stimulus
        :type selected_stimulus_filename: str
        :param df: data
        :type df: pd.DataFrame
        """
        self.stimulus_image = imgutils.import_img_2d_rgb_arr(selected_stimulus_filename)
        # defining stimulus image extent in plot
        self.x_len = len(self.stimulus_image[0])
        self.y_len = len(self.stimulus_image)
        self.x_shift = \
            df[STIMULUS_X_DISPLACEMENT_COL_TITLE][df[STIMULUS_X_DISPLACEMENT_COL_TITLE].notnull()].iloc[0]
        self.y_shift = \
            df[STIMULUS_Y_DISPLACEMENT_COL_TITLE][df[STIMULUS_Y_DISPLACEMENT_COL_TITLE].notnull()].iloc[0]
        if self.x_shift is None:
            self.x_shift = 0
        if self.y_shift is None:
            self.y_shift = 0


import src.model.utils.img_utils as imgutils
from src.model.model_data import ModelData
from src.model.model_participant_selection import ModelParticipantSelection
from src.model.utils import model_utils
from src.view.view_analysis_type_selection import ViewAnalysisTypeSelection
from src.view.view_data_type_selection import ViewDataTypeSelection
from src.view.view_plot import ViewPlot
from src.view.view_stimulus_selection import ViewStimulusSelection
