from correlation.pearson import correlation
from forecasting.arma import arma
from forecasting.dl.train import lstm
from forecasting.linear_regression import linear_regression
from preprocessing.download_data import get_data
from preprocessing.clean_data import preprocess
from visualizing.visualization import print_stats, visualize_data

debug = False

oldenburg_df, berlin_df, munich_df = get_data()

if debug:
    print_stats('Oldenburg (uncleaned)', oldenburg_df)
    print_stats('Berlin (uncleaned)', berlin_df)
    print_stats('Munich (uncleaned)', munich_df)

oldenburg_df, berlin_df, munich_df = preprocess(oldenburg_df, berlin_df, munich_df)
 
if debug:
    print_stats('Oldenburg (err removed)', oldenburg_df)
    print_stats('Berlin (err removed)', berlin_df)
    print_stats('Munich (err removed)', munich_df)


# lstm(oldenburg_df)
# arma(oldenburg_df)
# linear_regression(oldenburg_df, berlin_df, munich_df)
# visualize_data(oldenburg_df, berlin_df, munich_df)
correlation(oldenburg_df, berlin_df, munich_df)






