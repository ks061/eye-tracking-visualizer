from pathlib import Path
from PIL import Image
import plotly.express as px

import src.main.config as config
from src.model.model_analysis_type_selection import ModelAnalysisTypeSelection
from src.model.model_data_type_selection import ModelDataTypeSelection
from src.model.model_stimulus_selection import ModelStimulusSelection
from src.model.model_main import ModelMain
import src.view.utils.visual_util as visual_util


class ModelPlot:
    __instance = None

    fig = None

    def __init__(self):
        super().__init__()
        if ModelPlot.__instance is not None:
            raise Exception("ModelPlot should be treated as a singleton class.")
        else:
            ModelPlot.__instance = self

    @staticmethod
    def get_instance():
        """
        Static method to access the one instance currently
        implemented for the variable.
        :return: the single instance of ModelPlot
        """
        if ModelPlot.__instance is None:
            ModelPlot()
        return ModelPlot.__instance

    def update_fig(self):
        data_type_selection = ModelDataTypeSelection.get_instance().get_selection()

        if data_type_selection == "Gaze Data":
            x = config.X_GAZE_COL_TITLE
            y = config.Y_GAZE_COL_TITLE
        if data_type_selection == "Fixation Data":
            x = config.X_FIXATION_COL_TITLE
            y = config.Y_FIXATION_COL_TITLE

        analysis_type_selection = ModelAnalysisTypeSelection.get_instance().get_selection()

        if analysis_type_selection == "Scatter Plot":
            self.fig = px.scatter(
                ModelMain.get_instance().df,
                x=x,
                y=y,
                color="ParticipantName"
            )
        if analysis_type_selection == "Line Plot":
            self.fig = px.line(
                ModelMain.get_instance().df,
                x=x,
                y=y,
                color="ParticipantName"
            )
        if analysis_type_selection == "Heat Map":
            self.fig = px.density_heatmap(
                ModelMain.get_instance().df,
                x=x,
                y=y
            )
        # "Cluster":

        stimulus_file_name = ModelStimulusSelection.get_instance().get_selection()
        df = ModelMain.get_instance().get_df()

        stimulus_image = visual_util.import_stimulus_image(stimulus_file_name)
        # defining stimulus image extent in plot
        x_len = len(stimulus_image[0])
        y_len = len(stimulus_image)
        x_shift = df[config.STIMULUS_X_DISPLACEMENT_COL_TITLE].iloc[0]
        y_shift = df[config.STIMULUS_Y_DISPLACEMENT_COL_TITLE].iloc[0]
        img_path = str(Path.cwd() / config.STIMULUS_DIR_PATH_RELATIVE_TO_MODEL_PLOT / stimulus_file_name)
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
        self.update_fig()
        return self.fig

    def clear(self):
        self.fig = None
