import os
from pathlib import Path

# Project libraries
import config as CONFIG

# Data libraries
import pandas as pd
import seaborn as sns

# Returns a lower limit for a particular axis from the
# minimum value in the specified
# column in the specified data frame or
# minimum value of the stimulus image in that axis,
# whichever is lower, and an additional percentage of this value
# See EXTREMA_BUFFER_PCT constant in config.py.
def _get_lower_lim(data_frame, col_name, stimulus_extent):
    if (col_name == CONFIG.X_GAZE_COL_TITLE):
        min_value = min(data_frame[col_name].min(), stimulus_extent[0])
    elif (col_name == CONFIG.Y_GAZE_COL_TITLE):
        min_value = min(data_frame[col_name].min(), stimulus_extent[2])
    if (min_value >= 0): return min_value * (1-CONFIG.EXTREMA_BUFFER_PCT)
    else: return min_value * (1+CONFIG.EXTREMA_BUFFER_PCT)

# Returns an upper limit for a particular axis from the
# maximum value in the specified
# column in the specified data frame or
# maximum value of the stimulus image in that axis,
# whichever is greater, and an additional percentage of this value
# See EXTREMA_BUFFER_PCT constant in config.py.
def _get_upper_lim(data_frame, col_name, stimulus_extent):
    if (col_name == CONFIG.X_GAZE_COL_TITLE):
        max_value = max(data_frame[col_name].max(), stimulus_extent[1])
    elif (col_name == CONFIG.Y_GAZE_COL_TITLE):
        max_value = max(data_frame[col_name].max(), stimulus_extent[3])
    if (max_value >= 0): return max_value * (1+CONFIG.EXTREMA_BUFFER_PCT)
    else: return max_value * (1-CONFIG.EXTREMA_BUFFER_PCT)

# Return a data frame based on data for a particular participant
# from a specified .tsv file
def _get_data_frame_one_participant(selected_participant_file_path):
    return pd.read_csv(selected_participant_file_path, sep='\t')

# Isolate data for a particular stimulus from the data frame
def _get_data_frame_one_participant_one_stimulus(selected_participant_file_path, stimulus_file_name):
    data_frame_one_participant = _get_data_frame_one_participant(selected_participant_file_path)
    data_frame_one_participant_one_stimulus = data_frame_one_participant.loc[\
                                              data_frame_one_participant[CONFIG.STIMULUS_COL_TITLE]\
                                              == stimulus_file_name]
    data_frame_one_participant_one_stimulus = _filter_data(data_frame_one_participant_one_stimulus,
                                              [CONFIG.X_GAZE_COL_TITLE,
                                               CONFIG.Y_GAZE_COL_TITLE])
    return data_frame_one_participant_one_stimulus

# Return a data frame based on data for multiple participants
# from multiple specified .tsv files within the
# selected_participant_file_name_list array. Optional parameter
# stimulus_file_name to filter by a particular stimulus.
def _get_data_frame_multiple_participants(selected_participant_file_name_list, data_directory_path, stimulus_file_name=None):
    for i in range(len(selected_participant_file_name_list)):
        selected_participant_file_name = selected_participant_file_name_list[i]
        if (stimulus_file_name == None):
            data_frame_one_participant = _get_data_frame_one_participant(
                                        str(Path(data_directory_path) / selected_participant_file_name)
                                        )
        else:
            data_frame_one_participant = _get_data_frame_one_participant_one_stimulus(
                                        str(Path(data_directory_path) / selected_participant_file_name),
                                        stimulus_file_name
                                        )
        data_frame_one_participant = data_frame_one_participant.assign(participant_identifier = selected_participant_file_name)
        if (i == 0): data_frame_multiple_participants = data_frame_one_participant
        else: data_frame_multiple_participants = pd.concat(\
                                                [data_frame_multiple_participants,
                                                 data_frame_one_participant])
    return data_frame_multiple_participants

# Filter out rows with empty values in any of the columns specified.
def _filter_data(data_frame, arr_col_titles):
    for col_title in arr_col_titles:
        data_frame = data_frame[(data_frame[col_title].notnull()) == True]
    return data_frame
