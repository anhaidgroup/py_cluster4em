
import pandas as pd

def contains_columns(matches_df, l_id, r_id, score) :
    """
    Validates whether the dataframe contains all the columns specified by user.

    Args:
        matches_df (DataFrame): the matches dataframe
        l_id (str): column name representing left id
        r_id (str): column name representing right id
        score (str): column name representing the match score between l_id and r_id

    Returns:
        True, if all column names are valid
        NameError exception, if the column is not present

    Notes:
        This is an exposed helper function that is used by the implemented clustering approaches.
        This can also be used for a custom clustering implementation at user's will.
    """
    if l_id not in matches_df:
        raise NameError('{error_text} Detail: {error_details}'.format(
            error_text=repr(l_id), error_details=repr(l_id + ' is not present in Dataframe')))
    elif r_id not in matches_df:
        raise NameError('{error_text} Detail: {error_details}'.format(
            error_text=repr(r_id), error_details=repr(r_id + ' is not present in Dataframe')))
    elif score not in matches_df:
        raise NameError('{error_text} Detail: {error_details}'.format(
            error_text=repr(score), error_details=repr(score + ' is not present in Dataframe')))
    else:
        return True
    return False

def is_dataframe(matches_df):
    """
    Checks if the structure being used is a dataframe.

    Args:
        matches_df (DataFrame): the matches dataframe

    Returns:
        True, if it is a Pandas DataFrame.
        TypeError exception, if not.

    Notes:
        This is an exposed helper function that is used by the implemented clustering approaches.
        This can also be used for a custom clustering implementation at user's will.
    """
    if isinstance(matches_df, pd.DataFrame):
        return True
    else:
        raise TypeError('{error_text} Detail: {error_details}'.format(
            error_text=repr(matches_df), error_details=repr(matches_df + ' is not a Pandas Dataframe')))
    return False