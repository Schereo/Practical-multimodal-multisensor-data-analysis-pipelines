import calendar
from pathlib import Path
from matplotlib import pyplot as plt, ticker
import seaborn as sns
import pandas as pd


def print_stats(name, df):
    print()
    print(name)
    print(df.info())
    print(df['R1'].describe())


def visualize_data(df1, df2, df3, show=False):
    print('Visualizing data...')
    _precipitation_distribution(df1, df2, df3)
    _monthly_summed_precipitation(df1, df2, df3)
    _visualize_full_data(df1)
    _visualize_full_data(df2)
    _visualize_full_data(df3)
    _visualize_data_years_seperated(df1)
    _visualize_data_years_seperated(df2)
    _visualize_data_years_seperated(df3)
    _visualize_combined_data(df1, df2, df3)
    _yearly_summed_percipitation(df1, df2, df3)
    


def _visualize_full_data(df, show=False):
    plt.xlabel('Date')
    plt.ylabel('Precipitation in mm')
    plt.title(f'Precipitation in mm in {df.index.name}')
    plt.plot(df.index, df['R1'])
    if show:
        plt.show()
    plt.savefig(f'visualizations/{df.index.name}/percipitation_full.png')
    plt.clf()


def _visualize_data_years_seperated(df, show=False):
    # get the first and last row of the dataframe
    first_year = df.iloc[0].index
    print('index', first_year)
    last_year = df.iloc[-1].index.year
    min_year, max_year = _get_year_with_least_and_most_precipitation(df)
    for year in range(first_year, last_year):
        plt.xlabel('Date')
        plt.ylabel('Precipitation in mm')
        plt.title(f'Precipitation in mm in {df.index.name} in {year}')
        plt.plot(df[df.index.year == year]['MESS_DATUM'],
                 df[df.index.year == year]['R1'])
        if show:
            plt.show()
        if (year == min_year):
            plt.savefig(
                f'visualizations/{df.index.name}/percipitation_{year}_min.png')
        if (year == max_year):
            plt.savefig(
                f'visualizations/{df.index.name}/percipitation_{year}_max.png')

        plt.clf()
    _overlay_year_with_least_and_most_percipitation(df, min_year, max_year)


def _overlay_year_with_least_and_most_percipitation(df1, least_year, most_year):
    plt.xlabel('Date')
    plt.ylabel('Precipitation in mm')
    plt.title(f'Precipitation in mm in {df1.index.name}')
    plt.plot(df1[df1.index.year == least_year]['MESS_DATUM'].dt.dayofyear,
             df1[df1.index.year == least_year]['R1'], label=f'{least_year} with least percipitation')
    plt.plot(df1[df1.index.year == most_year]['MESS_DATUM'].dt.dayofyear,
             df1[df1.index.year == most_year]['R1'], label=f'{most_year} with most percipitation')
    plt.legend()
    plt.savefig(
        f'visualizations/{df1.index.name}/percipitation_max_and_min.png')
    plt.clf()


def _get_year_with_least_and_most_precipitation(df):
    # get the first and last row of the dataframe
    fist_year = df.iloc[0]['MESS_DATUM'].year
    last_year = df.iloc[-1]['MESS_DATUM'].year
    min_year = fist_year
    max_year = fist_year
    min_year_r1 = df[df['MESS_DATUM'].dt.year == fist_year]['R1'].sum()
    max_year_r1 = df[df['MESS_DATUM'].dt.year == fist_year]['R1'].sum()
    for year in range(fist_year, last_year):
        r1_sum = df[df['MESS_DATUM'].dt.year == year]['R1'].sum()
        if r1_sum < min_year_r1:
            min_year = year
            min_year_r1 = r1_sum
        if r1_sum > max_year_r1:
            max_year = year
            max_year_r1 = r1_sum
    # Ignore first year because it is not a full year
    return min_year + 1, max_year


def _visualize_combined_data(df1, df2, df3, show=False):
    plt.xlabel('Year')
    plt.ylabel('Precipitation (mm)')
    plt.title(
        f'Overall precipitation')
    plt.plot(df1['MESS_DATUM'], df1['R1'], label=df1.index.name, markersize=0.4)
    plt.plot(df2['MESS_DATUM'], df2['R1'], label=df2.index.name, markersize=0.4)
    plt.plot(df3['MESS_DATUM'], df3['R1'], label=df3.index.name, markersize=0.4)
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'visualizations/combined/overall_percipitation.png')
    plt.clf()


def _precipitation_distribution(df1, df2, df3):
    fig, axs = plt.subplots(2, 2, figsize=(7, 7))
    histo1 = sns.histplot(df1['R1'], color='blue',
                          stat='percent', ax=axs[0, 0], legend=True)
    histo1.legend([df1.index.name])
    histo1.set_yscale('log')
    histo1.set(xlabel='Precipitation (mm)')
    histo2 = sns.histplot(df2['R1'], color='red', stat='percent', ax=axs[0, 1])
    histo2.legend([df2.index.name])
    histo2.set_yscale('log')
    histo2.set(xlabel='Precipitation (mm)')
    histo3 = sns.histplot(df3['R1'], color='green',
                          stat='percent', ax=axs[1, 0])
    histo3.legend([df3.index.name])
    histo3.set_yscale('log')
    histo3.set(xlabel='Precipitation (mm)')

    concat_df = pd.concat([df1['R1'].rename(df1.index.name), df2['R1'].rename(
        df2.index.name), df3['R1'].rename(df3.index.name)], axis=1).reset_index()
    histo4 = sns.histplot((concat_df['Oldenburg'], concat_df['Munich'],
                          concat_df['Berlin']), stat='percent', ax=axs[1, 1], legend=True)
    histo4.set_yscale('log')
    histo4.set(xlabel='Precipitation (mm)')
    fig.suptitle('Distribution of precipitation')
    fig.tight_layout()
    plt.savefig(f'visualizations/combined/precipitation_distribution.png')
    plt.clf()


def _yearly_summed_percipitation(df1, df2, df3):
    fig, axs = plt.subplots(2, 2, figsize=(7, 7))
    # divide summed yearly percipitation by number of entries to get average
    yearly_sum1 = df1.groupby(df1['MESS_DATUM'].dt.year).sum(
    )['R1'] / df1.groupby(df1['MESS_DATUM'].dt.year).count()['R1']
    histo1 = sns.histplot(yearly_sum1, color='blue',
                          stat='percent', ax=axs[0, 0], legend=True)
    histo1.legend([df1.index.name])
    histo1.set(xlabel='Precipitation (mm/day)')
    yearly_sum2 = df2.groupby(df2['MESS_DATUM'].dt.year).sum(
    )['R1'] / df2.groupby(df2['MESS_DATUM'].dt.year).count()['R1']
    histo2 = sns.histplot(yearly_sum2, color='red',
                          stat='percent', ax=axs[0, 1])
    histo2.legend([df2.index.name])
    histo2.set(xlabel='Precipitation (mm/day)')
    yearly_sum3 = df3.groupby(df3['MESS_DATUM'].dt.year).sum(
    )['R1'] / df3.groupby(df3['MESS_DATUM'].dt.year).count()['R1']
    histo3 = sns.histplot(yearly_sum3, color='green', stat='percent', ax=axs[1, 0])
    histo3.legend([df3.index.name])
    histo3.set(xlabel='Precipitation (mm/day)')
    concat_df = pd.concat([df1.groupby(df1['MESS_DATUM'].dt.year)['R1'].sum().rename(df1.index.name), df2.groupby(df2['MESS_DATUM'].dt.year)[
                          'R1'].sum().rename(df2.index.name), df3.groupby(df3['MESS_DATUM'].dt.year)['R1'].sum().rename(df3.index.name)], axis=1).reset_index()

    histo4 = sns.histplot((concat_df['Oldenburg'], concat_df['Munich'],
                          concat_df['Berlin']), stat='percent', ax=axs[1, 1], legend=True)
    histo4.set(xlabel='Precipitation (mm/day)')

    fig.suptitle('Average daily precipitation')
    fig.tight_layout()
    plt.savefig(f'visualizations/combined/daily_avg_percipitation.png')
    plt.clf()

def _monthly_summed_precipitation(df1, df2, df3):
    fig, axs = plt.subplots(2, 2, figsize=(7, 7))
    # divide summed yearly percipitation by number of entries to get average
    monthly_sum1 = df1.groupby(df1.index.month).sum(
    )['R1'] / df1.groupby(df1.index.month).count()['R1']
    histo1 = sns.lineplot(monthly_sum1, color='blue', ax=axs[0, 0], legend=True, label='Test')
    histo1.legend([df1.index.name])
    histo1.xaxis.set_major_locator(ticker.MultipleLocator(1))
    histo1.set(xlabel=None)
    histo1.set(ylabel='Precipitation (mm)')
    
    monthly_sum2 = df2.groupby(df2.index.month).sum(
    )['R1'] / df2.groupby(df2.index.month).count()['R1']
    histo2 = sns.lineplot(monthly_sum2, color='red', ax=axs[0, 1])
    histo2.legend([df2.index.name])
    histo2.xaxis.set_major_locator(ticker.MultipleLocator(1))
    histo2.set(xlabel=None)
    histo2.set(ylabel='Precipitation (mm)')

    

    monthly_sum3 = df3.groupby(df3.index.month).sum(
    )['R1'] / df3.groupby(df3.index.month).count()['R1']
    histo3 = sns.lineplot(monthly_sum3, color='green', ax=axs[1, 0])
    histo3.legend([df3.index.name])
    histo3.xaxis.set_major_locator(ticker.MultipleLocator(1))
    histo3.set(xlabel=None)
    histo3.set(ylabel='Precipitation (mm)')
    concat_df = pd.concat([monthly_sum1.rename(df1.index.name), monthly_sum2.rename(df2.index.name), monthly_sum3.rename(df3.index.name)], axis=1)

    histo4 = sns.lineplot((concat_df['Oldenburg'], concat_df['Munich'],
                          concat_df['Berlin']), ax=axs[1, 1], legend=True)
    histo4.xaxis.set_major_locator(ticker.MultipleLocator(1))
    histo4.set(xlabel=None)
    histo4.set(ylabel='Precipitation (mm)')
    for i in range(1, 13):
        histo1.axvline(x=i, color='black', linestyle='--', alpha=0.3)
        histo2.axvline(x=i, color='black', linestyle='--', alpha=0.3)
        histo3.axvline(x=i, color='black', linestyle='--', alpha=0.3)
        histo4.axvline(x=i, color='black', linestyle='--', alpha=0.3)

    fig.suptitle('Average monthly precipitation')
    fig.tight_layout()
    plt.savefig(f'visualizations/combined/monthly_avg_percipitation.png')
    plt.clf()



