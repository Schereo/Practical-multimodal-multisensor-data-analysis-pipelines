

from matplotlib import pyplot as plt
from numpy import ndarray
from pandas import DataFrame
import numpy as np


def visualize_optimal_cluster(df1: DataFrame, data_name: str):
    for g in np.unique(df1['cluster']):
        i = np.where(df1['cluster'] == g)
        plt.scatter(df1.iloc[i].index, df1.iloc[i]['R1'], label=g)
    plt.xlabel('Year')
    plt.ylabel('Precipitation (mm)')
    plt.title(f'Optimal clustering in different seasons for {data_name}')
    plt.legend()
    plt.gcf().set_size_inches(14, 4)
    # set tight layout to avoid overlapping of labels
    plt.tight_layout()
    plt.savefig(
        f'visualizations/clustering/optimal_seasonal_clustering.png')
    plt.clf()

def visualize_agglomerative_clustering(data: ndarray, labels: ndarray, data_name: str):
    colors = ['red', 'blue', 'green', 'yellow']
    plt.scatter(data[:, 1].astype('datetime64'), data[:, 0], c=labels)
    plt.xlabel('Year')
    plt.ylabel('Precipitation (mm)')
    plt.title(f'Agglomerative clustering for {data_name}')
    plt.gcf().set_size_inches(14, 4)
    # set tight layout to avoid overlapping of labels
    plt.tight_layout()
    plt.savefig(
        f'visualizations/clustering/agglomerative_clustering.png')
    plt.clf()