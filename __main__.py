from argparse import ArgumentParser
import argparse
from clustering.clustering import cluster
from correlation.pearson import correlation
from forecasting.arma import arma
from forecasting.dl.train import lstm
from forecasting.linear_regression import linear_regression
from preprocessing.download_data import get_data
from preprocessing.clean_data import preprocess
from visualizing.visualization import print_stats, visualize_data


parser = ArgumentParser()
parser.add_argument("-d", "--debug", default=False,
                    help="Print additional debug information", action=argparse.BooleanOptionalAction)
parser.add_argument("-v", "--visualize", default=False,
                    help="Visualize data", action=argparse.BooleanOptionalAction)
parser.add_argument("--lstm", default=False, help="Train LSTM model", action=argparse.BooleanOptionalAction)
parser.add_argument("--regression", default=False,
                    help="Train linear regression model", action=argparse.BooleanOptionalAction)
parser.add_argument("--correlation", default=False, help="Calculate correlation", action=argparse.BooleanOptionalAction)
parser.add_argument("--cluster", default=False, help="Calculate clusters", action=argparse.BooleanOptionalAction)
args = parser.parse_args()

oldenburg_df, berlin_df, munich_df = get_data()

if args.debug:
    print_stats('Oldenburg (uncleaned)', oldenburg_df)
    print_stats('Berlin (uncleaned)', berlin_df)
    print_stats('Munich (uncleaned)', munich_df)

oldenburg_df, berlin_df, munich_df = preprocess(
    oldenburg_df, berlin_df, munich_df)

if args.debug:
    print_stats('Oldenburg (err removed)', oldenburg_df)
    print_stats('Berlin (err removed)', berlin_df)
    print_stats('Munich (err removed)', munich_df)


# If one argument is supplied, execute only the corresponding function, otherwise execute all
if args.lstm:
    lstm(oldenburg_df)
elif args.regression:
    linear_regression(oldenburg_df, berlin_df, munich_df)
elif args.visualize:
    visualize_data(oldenburg_df, berlin_df, munich_df)
elif args.correlation:
    correlation(oldenburg_df, berlin_df, munich_df)
elif args.cluster:
    cluster(oldenburg_df)
else:
    lstm(oldenburg_df) 
    linear_regression(oldenburg_df, berlin_df, munich_df)
    visualize_data(oldenburg_df, berlin_df, munich_df)
    correlation(oldenburg_df, berlin_df, munich_df)
    cluster(oldenburg_df)
