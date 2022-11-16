from pathlib import Path
from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd

def print_stats(name, df):
    print()
    print(name)
    print(df.info())
    print(df['R1'].describe())

def visualize_data(df1, df2, df3, show=False):
    print('Visualizing data...')
    Path("visualizations").mkdir(parents=True, exist_ok=True)
    Path("visualizations/Oldenburg").mkdir(parents=True, exist_ok=True)
    Path("visualizations/Munich").mkdir(parents=True, exist_ok=True)
    Path("visualizations/Berlin").mkdir(parents=True, exist_ok=True)
    Path("visualizations/combined").mkdir(parents=True, exist_ok=True)
    _histogram(df1, df2, df3)
    _visualize_full_data(df1)
    _visualize_full_data(df2)
    _visualize_full_data(df3)
    _visualize_data_years_seperated(df1)
    _visualize_data_years_seperated(df2)
    _visualize_data_years_seperated(df3)
    _visualize_combined_data(df1, df2, df3)


def _visualize_full_data(df, show=False):
    plt.xlabel('Date')
    plt.ylabel('Precipitation in mm')
    plt.title(f'Precipitation in mm in {df.index.name}')
    plt.plot(df['MESS_DATUM'], df['R1'])
    if show:
        plt.show()
    plt.savefig(f'visualizations/{df.index.name}/percipitation_full.png')
    plt.clf()

def _visualize_data_years_seperated(df, show=False):
    # get the first and last row of the dataframe
    fist_year = df.iloc[0]['MESS_DATUM'].year
    last_year = df.iloc[-1]['MESS_DATUM'].year
    min_year, max_year = _get_year_with_least_and_most_precipitation(df)
    for year in range(fist_year, last_year):
        plt.xlabel('Date')
        plt.ylabel('Precipitation in mm')
        plt.title(f'Precipitation in mm in {df.index.name} in {year}')
        plt.plot(df[df['MESS_DATUM'].dt.year == year]['MESS_DATUM'], df[df['MESS_DATUM'].dt.year == year]['R1'])
        if show:
            plt.show()
        if (year == min_year):
            plt.savefig(f'visualizations/{df.index.name}/percipitation_{year}_min.png')
        if (year == max_year):
            plt.savefig(f'visualizations/{df.index.name}/percipitation_{year}_max.png')
        else:
            plt.savefig(f'visualizations/{df.index.name}/percipitation_{year}.png')
        plt.clf()
    _overlay_year_with_leasst_and_most_percipitation(df, min_year, max_year)

def _overlay_year_with_leasst_and_most_percipitation(df1, least_year, most_year):
    plt.xlabel('Date')
    plt.ylabel('Precipitation in mm')
    plt.title(f'Precipitation in mm in {df1.index.name}')
    plt.plot(df1[df1['MESS_DATUM'].dt.year == least_year]['MESS_DATUM'].dt.dayofyear, df1[df1['MESS_DATUM'].dt.year == least_year]['R1'], label=f'{least_year} with least percipitation')
    plt.plot(df1[df1['MESS_DATUM'].dt.year == most_year]['MESS_DATUM'].dt.dayofyear, df1[df1['MESS_DATUM'].dt.year == most_year]['R1'], label=f'{most_year} with most percipitation')
    plt.legend()
    plt.savefig(f'visualizations/{df1.index.name}/percipitation_max_and_min.png')
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
    plt.xlabel('Date')
    plt.ylabel('Precipitation in mm')
    plt.title(f'Precipitation in mm in {df1.index.name}, {df2.index.name}, {df3.index.name}')
    plt.plot(df1['MESS_DATUM'], df1['R1'], label=df1.index.name)
    plt.plot(df2['MESS_DATUM'], df2['R1'], label=df2.index.name)
    plt.plot(df3['MESS_DATUM'], df3['R1'], label=df3.index.name)
    plt.legend()
    if show:
        plt.show()
    plt.savefig(f'visualizations/combined/percipitation.png')
    plt.clf()

def _histogram(df1, df2, df3):
    fig, axs = plt.subplots(2, 2, figsize=(7, 7))
    histo1 = sns.histplot(df1['R1'].rename(df1.index.name),color='blue', stat='percent', ax=axs[0, 0], legend=True, label='Test')
    histo2 = sns.histplot(df2['R1'].rename(df2.index.name),color='red', stat='percent', ax=axs[0, 1], label='Test' )
    histo3 = sns.histplot(df3['R1'].rename(df3.index.name),color='green', stat='percent', ax=axs[1, 0], label='Test')

    concat_df = pd.concat([df1['R1'].rename(df1.index.name), df2['R1'].rename(df2.index.name), df3['R1'].rename(df3.index.name)], axis=1).reset_index()
    print(concat_df.head())
    histo4 = sns.histplot((concat_df['Oldenburg'], concat_df['Munich'], concat_df['Berlin']), stat='percent', ax=axs[1, 1], legend=True)
    histo1.set_yscale('log')
    histo2.set_yscale('log')
    histo3.set_yscale('log')
    histo4.set_yscale('log')
    
    fig.suptitle('Precipitation in mm')
    fig.tight_layout()
    plt.savefig(f'visualizations/combined/histogram.png')
    plt.clf()

