import numpy as np
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
    df1, df2, df3 = _trim_data_to_same_time(df1, df2, df3)
    df1 = _interpolate_missing_hours(df1)
    df2 = _interpolate_missing_hours(df2)
    df3 = _interpolate_missing_hours(df3)
    df1.index.name = 'Oldenburg'
    df2.index.name = 'Berlin'
    df3.index.name = 'Munich'
    _save_data(df1, df2, df3)
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


def _trim_data_to_same_time(df1, df2, df3):
    # Trim whole df to only have data from 1998-09-30 12:00:00 to 2011-07-31 23:00:00
    df1 = df1[(df1['MESS_DATUM'] >= '1998-09-30 12:00:00') &
              (df1['MESS_DATUM'] <= '2011-07-31 23:00:00')]
    df2 = df2[(df2['MESS_DATUM'] >= '1998-09-30 12:00:00') &
              (df2['MESS_DATUM'] <= '2011-07-31 23:00:00')]
    df3 = df3[(df3['MESS_DATUM'] >= '1998-09-30 12:00:00') &
              (df3['MESS_DATUM'] <= '2011-07-31 23:00:00')]
    return df1, df2, df3

def _interpolate_missing_hours(df1):
    df1 = df1[['MESS_DATUM', 'R1']]
    df1.index = df1['MESS_DATUM']
    df1.index = pd.to_datetime(df1.index)
    del df1['MESS_DATUM']
    df1 = df1.resample('H').mean()
    df1['R1'] = df1['R1'].interpolate() # interpolate missing values linearly
    return df1

def sum_up_to_days(df1):
    df1 = df1.resample('D').sum()
    return df1

def _save_data(oldenburg_df, berlin_df, munich_df):
    oldenburg_df.to_csv('data/processed/oldenburg.csv')
    berlin_df.to_csv('data/processed/berlin.csv')
    munich_df.to_csv('data/processed/munich.csv')