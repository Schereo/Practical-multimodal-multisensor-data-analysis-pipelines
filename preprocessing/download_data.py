
from urllib import request
import zipfile
import os
import pandas as pd


def get_data():
    # check if folder exists
    if not os.path.exists('./data/raw'):
        _download_data()
        _unzip_files()
    else:
        print('Data already downloaded')
    return _create_dataframes()

def _download_data():
    _download_file("https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/hourly/precipitation/historical/stundenwerte_RR_00399_19950901_20110801_hist.zip",
                   "oldenburg.zip")
    _download_file("https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/hourly/precipitation/historical/stundenwerte_RR_03379_19970707_20211231_hist.zip",
               "munich.zip")
    _download_file("https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/hourly/precipitation/historical/stundenwerte_RR_03791_19980930_20121001_hist.zip",
               "berlin.zip")



def _download_file(url, file_name):
    request.urlretrieve(url, file_name)
    print('Downloaded', file_name)


def _unzip_files():
    # unzip oldenburg.zip to oldenburg folder
    with zipfile.ZipFile("oldenburg.zip", 'r') as zip_ref:
        zip_ref.extractall("./data/raw/oldenburg")
    os.remove("oldenburg.zip")

    with zipfile.ZipFile("munich.zip", 'r') as zip_ref:
        zip_ref.extractall("./data/raw/munich")
    os.remove("munich.zip")

    with zipfile.ZipFile("berlin.zip", 'r') as zip_ref:
        zip_ref.extractall("./data/raw/berlin")
    os.remove("berlin.zip")

def _create_dataframes():
    # create dataframes
    oldenburg_df = pd.read_csv('./data/raw/oldenburg/produkt_rr_stunde_19950901_20110801_00399.txt', sep=';')
    munich_df = pd.read_csv('./data/raw/munich/produkt_rr_stunde_19970707_20211231_03379.txt', sep=';')
    berlin_df = pd.read_csv('./data/raw/berlin/produkt_rr_stunde_19980930_20121001_03791.txt', sep=';')
    # remove whitespace from df column names
    oldenburg_df.columns = oldenburg_df.columns.str.strip()
    munich_df.columns = munich_df.columns.str.strip()
    berlin_df.columns = berlin_df.columns.str.strip()
    oldenburg_df.index.name = 'Oldenburg'
    munich_df.index.name = 'Munich'
    berlin_df.index.name = 'Berlin'
    return oldenburg_df, munich_df, berlin_df