"""
Utility to handle image-related tasks, i.e., those dealing with
pandas DataFrame objects containing eye-tracking data
"""
import pandas as pd


def remove_incomplete_observations(df: pd.DataFrame,
                                   col_names: list) -> pd.DataFrame:
    """
    Removes any observations from the specified pandas
    DataFrame that have an unspecified
    value in any of the specified columns

    :param df: target DataFrame
    :type df: pd.DataFrame
    :param col_names: target columns in target DataFrame
    :type col_names: list
    :return: result DataFrame
    :rtype: pd.DataFrame
    """
    for col_name in col_names:
        df = df[df[col_name].notnull()]
    return df
