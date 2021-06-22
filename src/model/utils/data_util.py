from pathlib import Path

# Data libraries
import pandas as pd
import src.main.config as config


# Return a data frame based on data for a particular participant
# from a specified .tsv file
def get_data_frame_one_participant(selected_participant_file_path):
    return pd.read_csv(selected_participant_file_path, sep='\t')


# Isolate data for a particular stimulus from the data frame
def get_data_frame_one_participant_one_stimulus(
        selected_participant_file_path,
        stimulus_file_name):
    data_frame_one_participant = get_data_frame_one_participant(
        selected_participant_file_path
    )
    data_frame_one_participant_one_stimulus = data_frame_one_participant.loc[
        data_frame_one_participant[config.STIMULUS_COL_TITLE] == stimulus_file_name
        ]
    data_frame_one_participant_one_stimulus = remove_incomplete_observations(
        data_frame_one_participant_one_stimulus,
        [
            config.X_GAZE_COL_TITLE,
            config.Y_GAZE_COL_TITLE
        ]
    )
    return data_frame_one_participant_one_stimulus


# Return a data frame based on data for multiple participants
# from multiple specified .tsv files within the
# selected_participant_file_name_list array. Optional parameter
# stimulus_file_name to filter by a particular stimulus.
def get_data_frame_multiple_participants(
        selected_participant_file_name_list,
        data_directory_path,
        stimulus_file_name=None):
    data_frame_multiple_participants = None

    for i in range(len(selected_participant_file_name_list)):
        selected_participant_file_name = selected_participant_file_name_list[i]
        if stimulus_file_name is None:
            data_frame_one_participant = get_data_frame_one_participant(
                str(data_directory_path + "/" + selected_participant_file_name)
            )
        else:
            data_frame_one_participant = get_data_frame_one_participant_one_stimulus(
                str(data_directory_path + "/" + selected_participant_file_name), stimulus_file_name)
        data_frame_one_participant = data_frame_one_participant.assign(
            participant_identifier=selected_participant_file_name)
        if i == 0:
            data_frame_multiple_participants = data_frame_one_participant
        else:
            data_frame_multiple_participants = pd.concat([data_frame_multiple_participants, data_frame_one_participant])

    data_frame_multiple_participants.reset_index(inplace=True)
    return data_frame_multiple_participants


# Filter out rows with empty values in any of the columns specified.
def remove_incomplete_observations(data_frame, arr_col_titles):
    for col_title in arr_col_titles:
        data_frame = data_frame[data_frame[col_title].notnull() is True]
    return data_frame
