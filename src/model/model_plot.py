"""
Contains the class ModelPlot

MODULAR INTERNAL IMPORTS ARE AT THE BOTTOM OF THE FILE. THIS IS AN
INTENTIONAL DESIGN CHOICE. IT HELPS AVOID CIRCULAR IMPORT ISSUES.
IT IS ALSO OKAY TO AVOID THEM IN THIS MANNER BECAUSE THIS IS A
HIGHLY MODULAR PROGRAM.
"""

import base64
import os.path
import time
import warnings
from collections import defaultdict

import _plotly_utils
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image, ImageOps
from numba.core.errors import NumbaWarning, NumbaDeprecationWarning, NumbaPendingDeprecationWarning
from sklearn.cluster import DBSCAN

from src.main.config import MAX_FIXATION_PT_SIZE, DEFAULT_EPS_VALUE, DEFAULT_MIN_SAMPLES_VALUE, MAKE_IMG_GRAYSCALE, \
    DEFAULT_SUPPORT_THRESHOLD, DEFAULT_FORWARD_CONFIDENCE_THRESHOLD, DEFAULT_BACKWARD_CONFIDENCE_THRESHOLD, \
    DEFAULT_NUM_MONTE_CARLO_TRIALS
from src.main.config import PARTICIPANT_FILENAME_COL_TITLE
from src.main.config import PARTICIPANT_NAME_COL_TITLE
from src.main.config import RELATIVE_STIMULUS_IMAGE_DIR
from src.main.config import STIMULUS_COL_TITLE
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

    filtered_df = None
    fig = None
    x = None
    y = None
    color = None
    size = None
    fixation_participant_identifiers = None
    num_fixations = None
    num_fixations_in_cluster = None
    cluster_centroids = None
    cluster_sequences = None
    ord_assoc_rule_count = None
    cluster_id_count = None
    support_vals = None
    forward_confidence_vals = None
    backward_confidence_vals = None
    sig_cluster_assoc_rule_arrows = None
    assoc_rule_p_values = None

    stimulus_image = None
    x_len = None
    y_len = None
    x_shift = None
    y_shift = None

    def clear(self) -> None:
        self.fig = None
        self.figure_widget = None

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
        if color_col is not None:
            self.color = pd.Categorical(color_col)
        elif df is not None:
            color_col_name = PARTICIPANT_NAME_COL_TITLE
            color_col = df[color_col_name].copy(deep=True)
            self.color = pd.Categorical(color_col)
        else:
            raise Exception("Parameters df and color_col cannot both be None.")

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

    def update_fig(self) -> go.FigureWidget:
        """
        Updates the underlying figure based upon
        user's selections

        """
        self.fig_params_clear()

        self.filtered_df = ModelData.get_instance().df
        selected_stimulus_filename = ViewStimulusSelection.get_instance().get_selected()

        self.filtered_df = self.filtered_df[self.filtered_df[STIMULUS_COL_TITLE] == selected_stimulus_filename]
        self.filtered_df = self.filtered_df[self.filtered_df[PARTICIPANT_FILENAME_COL_TITLE].isin(
            ModelParticipantSelection.get_instance().get_selected_participants()
        )]

        self.extract_and_set_stimulus_params(
            selected_stimulus_filename=selected_stimulus_filename, df=self.filtered_df
        )

        data_type_selection = ViewDataTypeSelection.get_instance().get_selected()
        analysis_type_selection = ViewAnalysisTypeSelection.get_instance().get_selected()

        if data_type_selection == "Fixation Data":
            self.filtered_df = model_utils.remove_incomplete_observations(
                self.filtered_df,
                [TIMESTAMP_COL_TITLE, X_FIXATION_COL_TITLE, Y_FIXATION_COL_TITLE, PARTICIPANT_FILENAME_COL_TITLE]
            )
            self.set_fixation_params(df=self.filtered_df)
        else:
            self.filtered_df = model_utils.remove_incomplete_observations(
                self.filtered_df,
                [TIMESTAMP_COL_TITLE, X_GAZE_COL_TITLE, Y_GAZE_COL_TITLE, PARTICIPANT_FILENAME_COL_TITLE]
            )
            self.set_gaze_params(df=self.filtered_df)

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
            self.perform_dbscan_clustering()
            self.fig = px.scatter(
                x=self.x,
                y=self.y,
                color=self.color
            )
            self.add_cluster_labels()
            self.find_cluster_sequences(data_type_selection)
            self.add_arrow_cluster_seq_if_one_participant()  # runs if one participant
            self.ordinal_association_rule_mining()  # find num sequences each cluster and each association rule is in
            self.compute_support_vals()
            self.compute_confidence_vals()  # both forward and backward confidence vals
            self.add_arrows_sig_cluster_assoc_rules()  # runs if more than one participant
            # self.print_assoc_mining_data()
            self.fig.add_trace(go.Indicator(  # % Fixations in Cluster indicator
                domain={'x': [0.07, 0.15], 'y': [0.9, 0.95]},
                value=round((self.num_fixations_in_cluster / self.num_fixations) * 100, 2),
                number={"suffix": "%", "font": {"size": 10, "color": "black"}},
                mode="gauge+number",
                gauge={"axis": {"range": [None, 100], "showticklabels": False}},
                title={'text': "Fixations in Cluster", "font": {"size": 10, "color": "black"}}
            ))
            # self.run_monte_carlo_stimulation()
            # print(self.fig)

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

        if analysis_type_selection == "Cluster":
            for i in range(len(self.fig.data)):  # ensure outliers are deselected by default
                try:  # if inspecting a cluster of points within the figure object
                    if self.fig.data[i]['legendgroup'] == '-1':
                        self.fig.data[i]["visible"] = 'legendonly'
                except _plotly_utils.exceptions.PlotlyKeyError:  # like if trying to access plotly.graph_objs.Indicator
                    continue

        return self.fig

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
        # data being analyzed
        timestamps = df[TIMESTAMP_COL_TITLE].to_numpy()
        x_coord_fixation_points = df[X_FIXATION_COL_TITLE].to_numpy()
        y_coord_fixation_points = df[Y_FIXATION_COL_TITLE].to_numpy()
        participant_identifiers = df[PARTICIPANT_NAME_COL_TITLE].to_numpy()

        fixation_x_coords = np.empty(shape=x_coord_fixation_points.size, dtype=np.float)
        fixation_x_coords_curr_index = 0
        fixation_y_coords = np.empty(shape=y_coord_fixation_points.size, dtype=np.float)
        fixation_y_coords_curr_index = 0
        fixation_durations = np.empty(shape=timestamps.size, dtype=np.float)
        fixation_durations_curr_index = 0
        fixation_point_sizes = np.empty(shape=timestamps.size, dtype=np.float)
        # fixation_point_sizes_curr_index not needed; taken care of at end
        # when fixation durations are mapped to fixation point sizes
        fixation_participant_identifiers = np.empty(shape=participant_identifiers.size, dtype=object)
        fixation_participant_identifiers_curr_index = 0

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

        for fixation_index in range(len(df.index)):
            # assessing if fixation is currently being iterated through
            if is_analyzing_fixation:
                # defining conditions for continuing to iterate through fixation
                # that is being analyzed
                is_curr_x_coord_same_as_prev_x_coord = \
                    x_coord_fixation_points[fixation_index] == curr_fixation_x_coord
                is_curr_y_coord_same_as_prev_y_coord = \
                    y_coord_fixation_points[fixation_index] == curr_fixation_y_coord
                is_curr_participant_identifier_same_as_prev_participant_identifier = \
                    participant_identifiers[fixation_index] == prev_participant_identifier
                if (is_curr_x_coord_same_as_prev_x_coord and
                        is_curr_y_coord_same_as_prev_y_coord and
                        is_curr_participant_identifier_same_as_prev_participant_identifier):
                    curr_fixation_duration += timestamps[fixation_index] - prev_fixation_timestamp
                else:  # finished analyzing current fixation
                    # add size of fixation to resulting list
                    fixation_durations[fixation_durations_curr_index] = curr_fixation_duration
                    fixation_durations_curr_index += 1
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
                is_curr_x_coord_nan = np.isnan(float(x_coord_fixation_points[fixation_index]))
                is_curr_y_coord_nan = np.isnan(float(y_coord_fixation_points[fixation_index]))
                if (not is_curr_x_coord_nan and
                        not is_curr_y_coord_nan):
                    is_analyzing_fixation = True
                    curr_fixation_x_coord = float(x_coord_fixation_points[fixation_index])
                    curr_fixation_y_coord = float(y_coord_fixation_points[fixation_index])
                    curr_fixation_participant_identifier = participant_identifiers[fixation_index]

                    fixation_x_coords[fixation_x_coords_curr_index] = curr_fixation_x_coord
                    fixation_x_coords_curr_index += 1
                    fixation_y_coords[fixation_y_coords_curr_index] = curr_fixation_y_coord
                    fixation_y_coords_curr_index += 1
                    fixation_participant_identifiers[fixation_participant_identifiers_curr_index] = \
                        curr_fixation_participant_identifier
                    fixation_participant_identifiers_curr_index += 1

            prev_fixation_timestamp = timestamps[fixation_index]
            prev_participant_identifier = participant_identifiers[fixation_index]

        if is_analyzing_fixation:
            fixation_durations[fixation_durations_curr_index] = curr_fixation_duration
            fixation_durations_curr_index += 1

        # scaling for maximum size
        max_fixation_duration = np.amax(fixation_durations)
        for i in range(fixation_durations.size):
            fixation_point_sizes[i] = (float(fixation_durations[i]) / float(max_fixation_duration)) * max_point_size

        xy = pd.concat(
            [
                pd.DataFrame(fixation_x_coords),
                pd.DataFrame(fixation_y_coords)
            ],
            axis=1,
            copy=False
        )
        xy.dropna(inplace=True)

        fixation_x_coords = xy.iloc[:, 0].to_numpy()
        fixation_y_coords = xy.iloc[:, 1].to_numpy()

        for i in range(fixation_x_coords.size):
            fixation_x_coords[i] += self.x_shift

        for j in range(fixation_y_coords.size):
            fixation_y_coords[j] += self.y_shift

        fixation_x_coords = fixation_x_coords[:(fixation_x_coords_curr_index + 1)]
        fixation_y_coords = fixation_y_coords[:(fixation_y_coords_curr_index + 1)]
        fixation_participant_identifiers = fixation_participant_identifiers[
                                           :(fixation_participant_identifiers_curr_index + 1)
                                           ]
        fixation_point_sizes = fixation_point_sizes[:(fixation_durations_curr_index + 1)]

        # noinspection PyTypeChecker
        self.set_x(df=df, x_col=pd.Series(fixation_x_coords))
        # noinspection PyTypeChecker
        self.set_y(df=df, y_col=pd.Series(fixation_y_coords))
        # noinspection PyTypeChecker
        self.set_color(df=df, color_col=pd.Series(pd.Categorical(fixation_participant_identifiers)))
        # noinspection PyTypeChecker
        self.set_size(size_col=pd.Series(fixation_point_sizes))
        self.fixation_participant_identifiers = pd.Series(fixation_participant_identifiers)

    @staticmethod
    def get_eps_value() -> int:
        try:
            eps_value = ViewPlot.get_instance().eps_curr_input.value()
        except ValueError:
            eps_value = 0
        if eps_value == 0:
            ViewPlot.get_instance().eps_input_min.setValue(int(DEFAULT_EPS_VALUE - DEFAULT_EPS_VALUE * .5))
            ViewPlot.get_instance().eps_curr_input.setValue(int(DEFAULT_EPS_VALUE))
            ViewPlot.get_instance().eps_input_max.setValue(int(DEFAULT_EPS_VALUE + DEFAULT_EPS_VALUE * .5))

            src.controller.controller_plot.ControllerPlot.get_instance().process_eps_input_min_entered()
            src.controller.controller_plot.ControllerPlot.get_instance().process_eps_input_curr_entered()
            src.controller.controller_plot.ControllerPlot.get_instance().process_eps_input_max_entered()

            eps_value = ViewPlot.get_instance().eps_curr_input.value()
        return eps_value

    @staticmethod
    def get_min_samples_value() -> int:
        try:
            min_samples_value = ViewPlot.get_instance().min_samples_curr_input.value()
        except ValueError:
            min_samples_value = 0
        if min_samples_value == 0:
            ViewPlot.get_instance().min_samples_input_min.setValue(
                int(DEFAULT_MIN_SAMPLES_VALUE - DEFAULT_MIN_SAMPLES_VALUE * .5)
            )
            ViewPlot.get_instance().min_samples_curr_input.setValue(int(DEFAULT_MIN_SAMPLES_VALUE))
            ViewPlot.get_instance().min_samples_input_max.setValue(
                int(DEFAULT_MIN_SAMPLES_VALUE + DEFAULT_MIN_SAMPLES_VALUE * .5)
            )

            src.controller.controller_plot.ControllerPlot.get_instance().process_min_samples_input_min_entered()
            src.controller.controller_plot.ControllerPlot.get_instance().process_min_samples_input_curr_entered()
            src.controller.controller_plot.ControllerPlot.get_instance().process_min_samples_input_max_entered()

            min_samples_value = ViewPlot.get_instance().min_samples_curr_input.value()
        return min_samples_value

    def perform_dbscan_clustering(self) -> None:
        """
        Performs clustering on the x and y attributes,
        removing any x, y pairs that have either value
        missing from their respective attributes, and
        sets the color of the points based upon
        the cluster in which OPTICS assigns them to
        """

        xy = pd.concat([self.x, self.y], axis=1)
        xy = xy.dropna()

        optics_clustering = DBSCAN(eps=ModelPlot.get_eps_value(),
                                   min_samples=ModelPlot.get_min_samples_value(),
                                   n_jobs=-1).fit(xy)
        labels = optics_clustering.labels_
        self.num_fixations = labels.size
        self.num_fixations_in_cluster = np.count_nonzero(labels != -1)

        # df=None will be ignored
        self.set_x(x_col=xy.iloc[:, 0].tolist())
        self.set_y(y_col=xy.iloc[:, 1].tolist())
        self.set_color(color_col=labels)

    def add_cluster_labels(self) -> None:
        cluster_data = {'x': self.x, 'y': self.y, 'color': self.color}
        cluster_df = pd.DataFrame(data=cluster_data)
        self.cluster_centroids = cluster_df.groupby('color')[['x', 'y']].mean()
        for index, centroid in self.cluster_centroids.iterrows():
            if index != -1:
                self.fig.add_annotation(
                    x=centroid['x'],
                    y=centroid['y'],
                    xref="x",
                    yref="y",
                    text=str(index),
                    font=dict(
                        family="Courier New, monospace",
                        size=28,
                        color="#ffffff"
                    ),
                    bgcolor="#EE4B2B",
                    opacity=0.5,
                    xanchor='center',
                    showarrow=False
                )

    def find_cluster_sequences(self, data_type_selection: str) -> None:
        self.cluster_sequences = defaultdict(list)

        cluster_df = pd.DataFrame(data={'x': self.x, 'y': self.y, 'color': self.color})

        df_all: pd.DataFrame = None
        if data_type_selection == "Fixation Data":
            df_all = pd.DataFrame({
                'x': self.x,
                'y': self.y,
                'participant': self.fixation_participant_identifiers
            })
        else:
            df_all = pd.DataFrame({
                'x': self.filtered_df[X_GAZE_COL_TITLE],
                'y': self.filtered_df[Y_GAZE_COL_TITLE],
                'participant': self.filtered_df['participant_filename']
            })

        participants = df_all['participant'].unique()
        for participant in participants:
            df_participant = df_all[df_all['participant'] == participant]
            for index, point in df_participant.iterrows():
                point_label = int(
                    cluster_df[(cluster_df['x'] == point['x']) & (cluster_df['y'] == point['y'])].iloc[0]['color']
                )
                if point_label == -1:
                    continue
                elif len(self.cluster_sequences[participant]) == 0:  # self.cluster_sequences[participant]
                    # is the cluster sequence of a given participant
                    self.cluster_sequences[participant].append(point_label)
                elif self.cluster_sequences[participant][-1] != point_label:
                    self.cluster_sequences[participant].append(point_label)

    def add_arrow_cluster_seq_if_one_participant(self) -> None:
        '''
        Adopted from https://stackoverflow.com/questions/58095322/draw-multiple-arrows-using-plotly-python
        '''
        if len(self.cluster_sequences) != 1:
            return

        participant = list(self.cluster_sequences.keys())[0]
        seq = self.cluster_sequences[participant]
        for i in range(len(seq)):
            if i > 0:
                self.fig.add_annotation(
                    x=self.cluster_centroids['x'].loc[seq[i]],
                    y=self.cluster_centroids['y'].loc[seq[i]],
                    xref="x", yref="y",
                    text="",
                    showarrow=True,
                    axref="x", ayref='y',
                    ax=self.cluster_centroids['x'].loc[seq[i - 1]],
                    ay=self.cluster_centroids['y'].loc[seq[i - 1]],
                    arrowhead=3,
                    arrowwidth=1.5,
                    arrowcolor='#EE4B2B'
                )

    def print_assoc_mining_data(self) -> None:
        """
        Helper function adopted from
        https://stackoverflow.com/questions/20181899/how-to-make-each-key-value-of-a-dictionary-print-on-a-new-line
        :return: None
        """
        dict_names: list[str] = [
            'ord_assoc_rule_count',
            'cluster_id_count',
            'support_vals',
            'forward_confidence_vals',
            'backward_confidence_vals'
        ]
        for d_name in dict_names:
            print("**" + d_name + "**")
            print("{" + "\n".join("{!r}: {!r},".format(k, v) for k, v in getattr(self, d_name).items()) + "}")

    def run_monte_carlo_stimulation(self) -> None:
        num_monte_carlo_trials = DEFAULT_NUM_MONTE_CARLO_TRIALS
        if ViewPlot.get_instance().num_trials_monte_carlo_input.value() != 0:
            num_monte_carlo_trials = ViewPlot.get_instance().num_trials_monte_carlo_input.value()
        else:
            ViewPlot.get_instance().num_trials_monte_carlo_input.setValue(DEFAULT_NUM_MONTE_CARLO_TRIALS)

        self.assoc_rule_p_values = defaultdict(float)
        num_trials_where_assoc_rule_support_value_met = defaultdict(
            int)  # the number of trials in which the support value of
        # association rule in a trial is at least the same, if not greater than, that calculated in the actual data.
        # used to calculate the p values for each association rule (count / DEFAULT_NUM_MONTE_CARLO_TRIALS)

        # initializing randomness
        cluster_ids = self.color.unique().to_numpy(dtype=int)
        cluster_id_freq = self.color.value_counts() / self.color.size
        # np.random.choice parameters
        a = cluster_ids
        # size will be number of cluster_ids to generate for a particular sample cluster sequence
        p = [cluster_id_freq[cluster_id] for cluster_id in cluster_ids]

        num_participants = len(self.cluster_sequences.values())
        participant_seq_lengths = np.array(
            [len(cluster_sequence) for cluster_sequence in self.cluster_sequences.values()],
            dtype=int)

        trial_sequence_set = np.empty(shape=num_participants, dtype=object)
        total_time: int
        seconds_left: int
        ViewPlot.get_instance().monte_carlo_progress_bar.setMinimum(0)
        ViewPlot.get_instance().monte_carlo_progress_bar.setMaximum(num_monte_carlo_trials)
        for trial_num in range(num_monte_carlo_trials):
            if trial_num == 0:
                start_time = time.time()
            if trial_num == 100:
                total_time = round(
                    (time.time() - start_time) * (num_monte_carlo_trials/100)
                )
            if trial_num % 100 == 0 and trial_num != 0:
                # adopted from https://stackoverflow.com/questions/775049/how-do-i-convert-seconds-to-hours-minutes
                # -and-seconds
                ViewPlot.get_instance().monte_carlo_progress_bar.setValue(trial_num)
                seconds_left = round(
                    total_time*(1-(trial_num/num_monte_carlo_trials))
                )
                m, s = divmod(seconds_left, 60)
                h, m = divmod(m, 60)
                ViewPlot.get_instance().time_left_monte_carlo.setText('ET: {:d}:{:02d}:{:02d} (h:m:s)'.format(h, m, s))
            for i in range(trial_sequence_set.size):
                trial_sequence_set[i] = np.random.choice(a=a, size=participant_seq_lengths[i], p=p)
            trial_ord_assoc_rule_count = defaultdict(int)
            trial_cluster_id_count = defaultdict(int)
            for sequence in trial_sequence_set:
                assoc_rules_for_seq = []
                cluster_ids = []
                for index_first in range(len(sequence)):
                    if sequence[index_first] == -1:
                        continue
                    for index_last in range(index_first + 1, len(sequence), 1):
                        if sequence[index_last] == -1:
                            continue
                        if (index_first, index_last) not in assoc_rules_for_seq:
                            assoc_rules_for_seq.append((sequence[index_first], sequence[index_last]))
                for assoc_rule in assoc_rules_for_seq:
                    trial_ord_assoc_rule_count[assoc_rule] += 1
                for cluster_id in sequence:
                    if cluster_id not in cluster_ids:
                        cluster_ids.append(cluster_id)
                for cluster_id in cluster_ids:
                    trial_cluster_id_count[cluster_id] += 1
            for assoc_rule, count in trial_ord_assoc_rule_count.items():
                trial_assoc_rule_support_val = count / num_monte_carlo_trials
                if trial_assoc_rule_support_val >= self.support_vals[assoc_rule]:
                    num_trials_where_assoc_rule_support_value_met[assoc_rule] += 1

        for assoc_rule, count in num_trials_where_assoc_rule_support_value_met.items():
            self.assoc_rule_p_values[assoc_rule] = count / num_monte_carlo_trials
        ViewPlot.get_instance().time_left_monte_carlo.setText("")
        ViewPlot.get_instance().monte_carlo_progress_bar.setValue(0)

    def ordinal_association_rule_mining(self) -> None:
        self.ord_assoc_rule_count = defaultdict(int)
        self.cluster_id_count = defaultdict(int)
        # print(self.cluster_sequences.values())
        for sequence in self.cluster_sequences.values():
            assoc_rules_for_seq = []
            cluster_ids = []
            for index_first in range(len(sequence)):
                if sequence[index_first] == -1:
                    continue
                for index_last in range(index_first + 1, len(sequence), 1):
                    if sequence[index_last] == -1:
                        continue
                    if (index_first, index_last) not in assoc_rules_for_seq:
                        assoc_rules_for_seq.append((sequence[index_first], sequence[index_last]))
            for assoc_rule in assoc_rules_for_seq:
                self.ord_assoc_rule_count[assoc_rule] += 1
            for cluster_id in sequence:
                if cluster_id not in cluster_ids:
                    cluster_ids.append(cluster_id)
            for cluster_id in cluster_ids:
                self.cluster_id_count[cluster_id] += 1

    def compute_support_vals(self) -> None:
        self.support_vals = defaultdict(float)
        for assoc_rule, count in self.ord_assoc_rule_count.items():
            self.support_vals[assoc_rule] = count / len(self.ord_assoc_rule_count)

    def compute_confidence_vals(self) -> None:
        self.forward_confidence_vals = defaultdict(float)
        for assoc_rule, count in self.ord_assoc_rule_count.items():
            self.forward_confidence_vals[assoc_rule] = count / self.cluster_id_count[assoc_rule[0]]
        self.backward_confidence_vals = defaultdict(float)
        for assoc_rule, count in self.ord_assoc_rule_count.items():
            self.backward_confidence_vals[assoc_rule] = count / self.cluster_id_count[assoc_rule[1]]

    def add_arrows_sig_cluster_assoc_rules(self) -> None:
        '''
        Adapted https://stackoverflow.com/questions/58095322/draw-multiple-arrows-using-plotly-python
        '''
        if len(self.cluster_sequences) == 1:
            return

        self.sig_cluster_assoc_rule_arrows = {}
        assoc_rules = self.ord_assoc_rule_count.keys()
        if ViewPlot.get_instance().support_input.value() == 0:
            ViewPlot.get_instance().support_input.setValue(DEFAULT_SUPPORT_THRESHOLD)
        if ViewPlot.get_instance().forward_confidence_input.value() == 0:
            ViewPlot.get_instance().forward_confidence_input.setValue(DEFAULT_FORWARD_CONFIDENCE_THRESHOLD)
        if ViewPlot.get_instance().backward_confidence_input.value() == 0:
            ViewPlot.get_instance().backward_confidence_input.setValue(DEFAULT_BACKWARD_CONFIDENCE_THRESHOLD)
        for assoc_rule in assoc_rules:
            visible = True  # only show annotation if meets all metrics below
            # div by 100 b/c inputs are percentages
            if self.support_vals[assoc_rule] < (ViewPlot.get_instance().support_input.value() / 100):
                visible = False
            elif self.forward_confidence_vals[assoc_rule] < (
                    ViewPlot.get_instance().forward_confidence_input.value() / 100):
                visible = False
            elif self.backward_confidence_vals[assoc_rule] < (
                    ViewPlot.get_instance().backward_confidence_input.value() / 100):
                visible = False
            x = self.cluster_centroids['x'].loc[assoc_rule[1]]
            y = self.cluster_centroids['y'].loc[assoc_rule[1]]
            ax = self.cluster_centroids['x'].loc[assoc_rule[0]]
            ay = self.cluster_centroids['y'].loc[assoc_rule[0]]
            do_add = visible
            if do_add:
                self.fig.add_annotation(
                    x=x,
                    y=y,
                    xref="x", yref="y",
                    text="",
                    showarrow=True,
                    axref="x", ayref='y',
                    ax=ax,
                    ay=ay,
                    arrowhead=3,
                    arrowwidth=1.5,
                    arrowcolor='#000000',
                    visible=visible
                )
            self.sig_cluster_assoc_rule_arrows[assoc_rule] = {"x": x, "y": y, "ax": ax, "ay": ay, "visible": visible,
                                                              "added": do_add}

    def filter_sig_cluster_assoc_rule_arrows(self) -> None:
        assoc_rules = self.ord_assoc_rule_count.keys()
        annotations = self.fig['layout']['annotations']
        for assoc_rule in assoc_rules:
            should_be_visible = True
            if self.support_vals[assoc_rule] < (ViewPlot.get_instance().support_input.value() / 100):
                should_be_visible = False
            elif self.forward_confidence_vals[assoc_rule] < (
                    ViewPlot.get_instance().forward_confidence_input.value() / 100):
                should_be_visible = False
            elif self.backward_confidence_vals[assoc_rule] < (
                    ViewPlot.get_instance().backward_confidence_input.value() / 100):
                should_be_visible = False
            if should_be_visible and not self.sig_cluster_assoc_rule_arrows[assoc_rule]["added"]:
                x = self.cluster_centroids['x'].loc[assoc_rule[1]]
                y = self.cluster_centroids['y'].loc[assoc_rule[1]]
                ax = self.cluster_centroids['x'].loc[assoc_rule[0]]
                ay = self.cluster_centroids['y'].loc[assoc_rule[0]]
                self.fig.add_annotation(
                    x=x,
                    y=y,
                    xref="x", yref="y",
                    text="",
                    showarrow=True,
                    axref="x", ayref='y',
                    ax=ax,
                    ay=ay,
                    arrowhead=3,
                    arrowwidth=1.5,
                    arrowcolor='#000000',
                    visible=should_be_visible
                )
                self.sig_cluster_assoc_rule_arrows[assoc_rule]["added"] = True
                self.sig_cluster_assoc_rule_arrows[assoc_rule]["visible"] = should_be_visible
                continue
            if should_be_visible == self.sig_cluster_assoc_rule_arrows[assoc_rule]["visible"]:
                continue
            for annotation in annotations:
                if not hasattr(annotation, "x"):
                    continue
                elif annotation.x != self.sig_cluster_assoc_rule_arrows[assoc_rule]["x"]:
                    continue
                elif not hasattr(annotation, "y"):
                    continue
                elif annotation.y != self.sig_cluster_assoc_rule_arrows[assoc_rule]["y"]:
                    continue
                elif not hasattr(annotation, "ax"):
                    continue
                elif annotation.ax != self.sig_cluster_assoc_rule_arrows[assoc_rule]["ax"]:
                    continue
                elif not hasattr(annotation, "ay"):
                    continue
                elif annotation.ay != self.sig_cluster_assoc_rule_arrows[assoc_rule]["ay"]:
                    continue
                else:
                    annotation.visible = should_be_visible
                    self.sig_cluster_assoc_rule_arrows[assoc_rule]["visible"] = should_be_visible

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


import src.controller.controller_plot
import src.model.utils.img_utils as imgutils
from src.model.model_data import ModelData
from src.model.model_participant_selection import ModelParticipantSelection
from src.model.utils import model_utils
from src.view.view_analysis_type_selection import ViewAnalysisTypeSelection
from src.view.view_data_type_selection import ViewDataTypeSelection
from src.view.view_plot import ViewPlot
from src.view.view_stimulus_selection import ViewStimulusSelection
