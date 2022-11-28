from matplotlib import pyplot as plt
from pandas import DataFrame, Series
import seaborn as sns


def visualize_pearson_correlation(df1: DataFrame):
    sns.heatmap(df1)
    plt.savefig(
        f'visualizations/correlation/pearson_correlation.png')
    plt.clf()

def visualize_rolling_correlation(df1_df2_rolling_corr: Series, df1_df3_rolling_corr: Series, df2_df3_rolling_corr: Series, window_size: int, df1_name: str, df2_name: str, df3_name: str):
    f,ax=plt.subplots(3,1,figsize=(14,9),sharex=True, sharey=True)
    ax[0].set(xlabel='Year',ylabel=f'Corr. over {window_size}h')
    df1_df2_rolling_corr.plot(ax=ax[0],title=f'Rolling correlation between {df1_name} and {df2_name}')
    ax[1].set(xlabel='Year',ylabel=f'Corr. over {window_size}h')
    df1_df3_rolling_corr.plot(ax=ax[1],title=f'Rolling correlation between {df1_name} and {df3_name}')
    ax[2].set(xlabel='Year',ylabel=f'Corr. over {window_size}h')
    df2_df3_rolling_corr.plot(ax=ax[2],title=f'Rolling correlation between {df2_name} and {df3_name}')
    plt.suptitle("Rolling window correlation")
    plt.xlabel('Year')
    plt.savefig(
        f'visualizations/correlation/rolling_pearson_correlation.png')
    plt.clf()
