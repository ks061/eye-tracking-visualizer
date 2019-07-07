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

# Return a data frame based on data from a specified .tsv file
def _import_data(tsv_filename):
    return pd.read_csv(tsv_filename, sep='\t')

# Isolate data for a particular stimulus from the data frame
def _get_data_frame_for_stimulus(data_frame, stimulus_file_name):

    # Find index of stimulus_file_name
    stimulus_series = data_frame[CONFIG.STIMULUS_COL_TITLE]
    data_frame_num_rows = data_frame.shape[0]
    for row_index in range(data_frame_num_rows):
        if (str(stimulus_series[row_index]) not in CONFIG.EXCLUDE_STIMULI_LIST):
            data_frame_start_index = row_index + 1

    # Find end index of data related to this stimulus
    data_frame_num_rows = data_frame.shape[0]
    for row_index in range(data_frame_start_index, data_frame_num_rows):
        if (str(stimulus_series[row_index]) not in CONFIG.EXCLUDE_STIMULI_LIST):
            data_frame_end_index = row_index - 1
        elif (row_index == data_frame_num_rows - 1):
            data_frame_end_index = row_index

    data_frame_for_stimulus = _filter_data(data_frame,
                                           [CONFIG.X_GAZE_COL_TITLE,
                                            CONFIG.Y_GAZE_COL_TITLE])
    return data_frame_for_stimulus[data_frame_start_index : data_frame_end_index + 1]

# Return a list of stimuli, where each stimulus corresponds to
# a trial on a participant, from a specified data frame
# and column title
def _get_stimuli(data_frame, col_title = CONFIG.STIMULUS_COL_TITLE):
    return data_frame[col_title].unique()

# Filter out rows with empty values in any of the columns specified.
def _filter_data(data_frame, arr_col_titles):
    for col_title in arr_col_titles:
        data_frame = data_frame[(data_frame[col_title].notnull()) == True]
    return data_frame
