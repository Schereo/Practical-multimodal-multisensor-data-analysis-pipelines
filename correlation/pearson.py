

from matplotlib import pyplot as plt
from pandas import DataFrame
from visualizing.visualize_correlation import  visualize_pearson_correlation, visualize_rolling_correlation

def correlation(df1: DataFrame, df2: DataFrame, df3: DataFrame):
    print('Calculating pearson correlation...')
    _pearson_correlation(df1, df2, df3)
    _rolling_pearson(df1, df2, df3)

def _pearson_correlation(df1: DataFrame, df2: DataFrame, df3: DataFrame):
    # compute pearson correlation between R1 columns
    df1_name = df1.index.name
    df2_name = df2.index.name
    df3_name = df3.index.name
    df1 = df1[['R1']]
    df2 = df2[['R1']]
    df3 = df3[['R1']]
    df1 = df1.rename(columns={'R1': f'{df1_name}'})
    df2 = df2.rename(columns={'R1': f'{df2_name}'})
    df3 = df3.rename(columns={'R1': f'{df3_name}'})
    df = df1.join(df2, how='outer')
    df = df.join(df3, how='outer')
    df = df.dropna()
    df = df.corr(method='pearson')
    df.to_csv('data/correlation/pearson.csv')
    visualize_pearson_correlation(df)

def _rolling_pearson(df1: DataFrame, df2: DataFrame, df3: DataFrame, window_size=30):
    rolling_r_df1_df2 = df1['R1'].rolling(window=window_size).corr(df2['R1'])
    rolling_r_df1_df3 = df1['R1'].rolling(window=window_size).corr(df3['R1'])
    rolling_r_df2_df3 = df2['R1'].rolling(window=window_size).corr(df3['R1'])
    rolling_r_df1_df2.rename(f'Correlation', inplace=True)
    rolling_r_df1_df3.rename(f'Correlation', inplace=True)
    rolling_r_df2_df3.rename(f'Correlation', inplace=True)
    rolling_r_df1_df2.to_csv(f'data/correlation/rolling_pearson_{df1.index.name}_{df2.index.name}.csv')
    rolling_r_df1_df3.to_csv(f'data/correlation/rolling_pearson_{df1.index.name}_{df3.index.name}.csv')
    rolling_r_df2_df3.to_csv(f'data/correlation/rolling_pearson_{df2.index.name}_{df3.index.name}.csv')
    visualize_rolling_correlation(rolling_r_df1_df2, rolling_r_df1_df3, rolling_r_df2_df3, window_size, df1.index.name, df2.index.name, df3.index.name)

    
