import pandas as pd


def preprocess(df1, df2, df3):
    df1 = _remove_unwanted_variables(df1)
    df2 = _remove_unwanted_variables(df2)
    df3 = _remove_unwanted_variables(df3)
    df1 = _remove_error_data(df1)
    df2 = _remove_error_data(df2)
    df3 = _remove_error_data(df3)
    df1 = _convert_to_datetime(df1)
    df2 = _convert_to_datetime(df2)
    df3 = _convert_to_datetime(df3)
    return df1, df2, df3
  

def _remove_error_data(df):
    # Remove data with error
    df = df[df['R1'] != -999]
    return df

def _convert_to_datetime(df):
    # Convert to datetime
    df['MESS_DATUM'] = pd.to_datetime(df['MESS_DATUM'], format='%Y%m%d%H')
    return df

def _remove_unwanted_variables(df):
    # Remove unwanted variables
    df = df.drop(['STATIONS_ID', 'eor', 'WRTR'], axis=1)
    return df