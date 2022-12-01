

from matplotlib import pyplot as plt
from numpy import ndarray
from pandas import DataFrame


def visualize_optimal_cluster(spring: DataFrame, summer: DataFrame, autumn: DataFrame, winter: DataFrame, data_name: str):
    plt.scatter(spring.index, spring['R1'], label='spring')
    plt.scatter(summer.index, summer['R1'], label='summer')
    plt.scatter(autumn.index, autumn['R1'], label='autumn')
    plt.scatter(winter.index, winter['R1'], label='winter')
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