
# Assignment 2

## 3 data questions

1. Can one predict the future precipitation only from historical precipitation data?
    1. How accurate is the prediction?
    2. Does the accuracy differ between cities?
    3. How accurate are non-deep learning methods (e.g. regression) compared to deep learning methods?
2. Can the yearly precipitation be clustered in periods of more or less rain?
    1. How many clusters can be identified?
    2. Do the clusters differ between cities?
3. How related is the precipitation of Oldenburg, Munich and Berlin?

## Implemented approaches

1. Predicting the future precipitation
    - A linear regression over all years was used to possibly show a linear relationship between time and precipitation. A trend could not be found. The slope was minimal.  See [linear regression Oldenburg](../visualizations/forecasting/linear_regressionOldenburg_.png), [linear regression Munich](../visualizations/forecasting/linear_regressionMunich_.png) and [linear regression Berlin](../visualizations/forecasting/linear_regressionBerlin_.png)
    - A LSTM model was trained to predict the precipitation of the next day based on the precipitation of the last 10 days. The models seems to only predict the average precipitation. A future improvement could be to use the hourly precipitation data to predict the hourly precipitation of the next day. See [Prediction Oldenburg](../output/lstm_out.csv)
2. Clustering the yearly precipitation
    - First a optimal clusters for the seasons where identified manually (spring, summer, autumn, winter). Then the yearly precipitation was clustered into these seasons. The yearly precipitation was clustered into 4 clusters. Than the agglomerative clustering algorithm was used to cluster the same data. The identified clusters matched the manually identified clusters partially. The winter season could not be identified by the algorithm. See [optimal clustering](../visualizations/clustering/optimal_seasonal_clustering.png) and [agglomerative clustering](../visualizations/clustering/agglomerative_clustering.png).
3. Correlation between the precipitation of Oldenburg, Munich and Berlin
    - The global Pearson correlation between the precipitation of Oldenburg, Munich and Berlin was calculated. There seems to be no correlation between the precipitation of the cities. See [global correlation](../visualizations/correlation/pearson_correlation.png) and [rolling correlation](../visualizations/correlation/rolling_pearson_correlation.png).
