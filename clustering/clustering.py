
from datetime import datetime
from pandas import DataFrame
from numpy import unique
from numpy import where
import numpy as np
from sklearn.datasets import make_classification
from sklearn.cluster import AgglomerativeClustering
from matplotlib import pyplot
from preprocessing.clean_data import sum_up_to_days
import seaborn as sns

from visualizing.visualize_clustering import visualize_agglomerative_clustering, visualize_optimal_cluster


def cluster(df1: DataFrame):
    print("Running clustering...")
    # extract year 2005 from dataframe  
    df1 = df1.loc[df1.index.year == 2005]
    _optimal_seasonal_clustering(df1)
    _agglomerative_clustering(df1)


def _optimal_seasonal_clustering(df1: DataFrame):
    # get months march, april and may from df1
    spring = df1.loc[(df1.index.month == 3) | (
        df1.index.month == 4) | (df1.index.month == 5)]
    summer = df1.loc[(df1.index.month == 6) | (
        df1.index.month == 7) | (df1.index.month == 8)]
    autumn = df1.loc[(df1.index.month == 9) | (
        df1.index.month == 10) | (df1.index.month == 11)]
    winter = df1.loc[(df1.index.month == 12) | (
        df1.index.month == 1) | (df1.index.month == 2)]
    visualize_optimal_cluster(spring, summer, autumn, winter, df1.index.name)


def _agglomerative_clustering(df1: DataFrame):
    model = AgglomerativeClustering(n_clusters=4)

    df1 = sum_up_to_days(df1)
    # print(df1.head())
    print("Running agglomerative clustering...")
    precip = df1['R1'].values
    date = df1.index.values
    precip = precip.reshape((len(precip), 1))
    date = date.reshape((len(date), 1))
    # convert date to float
    # print type of ndarray
    date = (date - np.datetime64('1970-01-01T00:00:00Z')) / np.timedelta64(1, 's')
    # concat two np arrays
    data = np.concatenate((precip, date), axis=1)
    yhat = model.fit_predict(data)
    visualize_agglomerative_clustering(data, yhat, df1.index.name)
