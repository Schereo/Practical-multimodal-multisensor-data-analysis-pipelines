import pandas as pd

def remove_error_data(df):
    # Remove data with error
    df = df[df['R1'] != -999]
    return df

def convert_to_datetime(df):
    # Convert to datetime
    df['MESS_DATUM'] = pd.to_datetime(df['MESS_DATUM'], format='%Y%m%d%H')
    return df

def remove_unwanted_variables(df):
    # Remove unwanted variables
    df = df.drop(['STATIONS_ID', 'eor', 'WRTR'], axis=1)
    return df