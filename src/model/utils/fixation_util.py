import math

# Data libraries
import pandas as pd

# import project libraries
import src.main.config as config


def get_fixation_size_array(data_frame):
    sizes = []

    analyzing_fixation = False
    current_fixation_x_coordinate = -1
    current_fixation_y_coordinate = -1
    prev_fixation_timestamp = 0
    fixation_duration = 0
    prev_participant_identifier = ''

    for index in range(len(data_frame.index)):
        x_fixation_column = pd.Series(data_frame[config.X_FIXATION_COL_TITLE])
        y_fixation_column = pd.Series(data_frame[config.Y_FIXATION_COL_TITLE])
        timestamp_column = pd.Series(data_frame[config.TIMESTAMP_COL_TITLE])
        participant_identifier_column = pd.Series(data_frame['participant_identifier'])

        print("col type: " + str(type(participant_identifier_column)))
        print(participant_identifier_column[index])

        if analyzing_fixation:
            if (float(x_fixation_column[index]) == current_fixation_x_coordinate and
                    float(y_fixation_column[index]) == current_fixation_y_coordinate and
                    participant_identifier_column[index] == prev_participant_identifier):
                fixation_duration += timestamp_column[index] - prev_fixation_timestamp
            else:
                if fixation_duration > 0:
                    sizes.append(fixation_duration)
                if (not math.isnan(float(x_fixation_column[index])) and
                        not math.isnan(float(y_fixation_column[index]))):
                    fixation_duration = 0

                    current_fixation_x_coordinate = float(x_fixation_column[index])
                    current_fixation_y_coordinate = float(y_fixation_column[index])
                else:
                    analyzing_fixation = False
        else:
            # print(x_fixation_column)
            # print(float(x_fixation_column[index]))
            # print(math.isnan(float(x_fixation_column[index])))

            if (not math.isnan(float(x_fixation_column[index])) and
                    not math.isnan(float(y_fixation_column[index]))):
                analyzing_fixation = True
                fixation_duration = 0

                current_fixation_x_coordinate = float(x_fixation_column[index])
                current_fixation_y_coordinate = float(y_fixation_column[index])

        prev_fixation_timestamp = timestamp_column[index]
        prev_participant_identifier = participant_identifier_column[index]

    maximum_size = max(sizes)
    print(sizes)
    for i in range(len(sizes)):
        sizes[i] = (float(sizes[i]) / float(maximum_size)) * config.MAX_FIXATION_POINT_SIZE

    return sizes
