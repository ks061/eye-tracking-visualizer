"""
Contains the class ModelPlot
"""

# External imports
import os.path
from PIL import Image
import plotly.express as px
# Internal imports
import src.main.config as config
from src.model.model_analysis_type_selection import ModelAnalysisTypeSelection
from src.model.model_data_type_selection import ModelDataTypeSelection
from src.model.model_stimulus_selection import ModelStimulusSelection
from src.model.model_data import ModelData


class ModelPlot:
    """
    Model for the plot
    """
    __instance = None

    fig = None
    x = None
    y = None

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

    def set_x_col_name(self):
        """
        Sets the column name from which to read the x coordinates
        of the plot from the pandas DataFrame in the data model
        """
        data_type_selection = ModelDataTypeSelection.get_instance().get_selection()

        if data_type_selection is "Gaze Data":
            self.x = config.X_GAZE_COL_TITLE
        if data_type_selection is "Fixation Data":
            self.x = config.X_FIXATION_COL_TITLE

    def set_y_col_name(self):
        """
        Sets the column name from which to read the y coordinates
        of the plot from the pandas DataFrame in the data model
        """
        data_type_selection = ModelDataTypeSelection.get_instance().get_selection()

        if data_type_selection is "Gaze Data":
            self.y = config.Y_GAZE_COL_TITLE
        if data_type_selection is "Fixation Data":
            self.y = config.Y_FIXATION_COL_TITLE

    def update_fig(self):
        """
        Updates the underlying figure based upon
        user's selections
        """
        self.set_x_col_name()
        self.set_y_col_name()

        analysis_type_selection = ModelAnalysisTypeSelection.get_instance().get_selection()

        if analysis_type_selection == "Scatter Plot":
            self.fig = px.scatter(
                ModelData.get_instance().df,
                x=self.x,
                y=self.y,
                color="ParticipantName"
            )
        if analysis_type_selection == "Line Plot":
            self.fig = px.line(
                ModelData.get_instance().df,
                x=self.x,
                y=self.y,
                color="ParticipantName"
            )
        if analysis_type_selection == "Heat Map":
            self.fig = px.density_heatmap(
                ModelData.get_instance().df,
                x=self.x,
                y=self.y
            )
        # "Cluster":

        stimulus_file_name = ModelStimulusSelection.get_instance().get_selection()
        df = ModelData.get_instance().get_df()

        stimulus_image = ModelStimulusSelection.get_instance().import_stimulus_image(stimulus_file_name)
        # defining stimulus image extent in plot
        x_len = len(stimulus_image[0])
        y_len = len(stimulus_image)
        x_shift = df[config.STIMULUS_X_DISPLACEMENT_COL_TITLE].iloc[0]
        y_shift = df[config.STIMULUS_Y_DISPLACEMENT_COL_TITLE].iloc[0]
        dir_path = os.path.dirname(os.path.realpath(__file__))
        img_path = os.path.abspath(dir_path / config.STIMULUS_DIR_PATH_RELATIVE_TO_MODEL_PLOT / stimulus_file_name)
        img = Image.open(img_path)
        self.fig.add_layout_image(
            dict(
                source=img,
                xref="x",
                yref="y",
                x=x_shift,
                y=y_shift,
                sizex=x_len,
                sizey=y_len,
                sizing="stretch",
                opacity=0.5,
                xanchor='left',
                yanchor='bottom')
        )

    def get_fig(self):
        """
        Returns the underlying figure
        :return: underlying figure
        :rtype: plotly.graph_objects.Figure
        """
        self.update_fig()
        return self.fig

    def clear(self):
        """
        Clears the underlying figure stored in the model
        """
        self.fig = None
