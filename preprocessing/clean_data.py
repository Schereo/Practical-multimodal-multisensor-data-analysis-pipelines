def remove_error_data(df):
    # Remove data with error
    df = df[df['R1'] != -999]
    return df