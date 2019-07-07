## Configuration document

import pandas as pd

## Data configurations

# Name of the column of the X coordinates of the gaze
# paths as specified in the .tsv files
X_GAZE_COL_TITLE = 'GazePointX (ADCSpx)'

# Name of the column of the Y coordinates of the gaze
# paths as specified in the .tsv files
Y_GAZE_COL_TITLE = 'GazePointY (ADCSpx)'

# Name of the column of the X displacement of stimulus image
STIMULUS_X_DISPLACEMENT_COL_TITLE = 'MediaPosX (ADCSpx)'

# Name of the column of the Y displacement of stimulus image
STIMULUS_Y_DISPLACEMENT_COL_TITLE = 'MediaPosY (ADCSpx)'

# Name of the column with the stimuli names
STIMULUS_COL_TITLE = 'MediaName'

# Name of stimuli to exclude from the stimuli
# that can be visualized.
EXCLUDE_STIMULI_LIST = ['nan', 'Instruction Element']

## Figure configurations

# Choose an integer value
# from 1 through 4 (inclusive)
# for the plot height. Higher
# numbers correspond to a larger
# plot height
PLOT_HEIGHT = 4

# Maximum and minimum values of each axis in a
# figure will be set beyond the extrema values within
# the data set along said axis; the buffer will
# be calculated as a percentage, namely
# EXTREMA_BUFFER_PCT, of extrema values.
EXTREMA_BUFFER_PCT = 0.05
