from preprocessing.download_data import get_data
from preprocessing.clean_data import convert_to_datetime, remove_error_data
from preprocessing.visualization import print_stats, visualize_data

debug = False

oldenburg_df, berlin_df, munich_df = get_data()

if debug:
    print_stats('Oldenburg (uncleaned)', oldenburg_df)
    print_stats('Berlin (uncleaned)', berlin_df)
    print_stats('Munich (uncleaned)', munich_df)


oldenburg_df = remove_error_data(oldenburg_df)
berlin_df = remove_error_data(berlin_df)
munich_df = remove_error_data(munich_df)

oldenburg_df = convert_to_datetime(oldenburg_df)
berlin_df = convert_to_datetime(berlin_df)
munich_df = convert_to_datetime(munich_df)

print(oldenburg_df['eor'].describe())
print(oldenburg_df['QN_8'].describe())
print(oldenburg_df['WRTR'].describe())

if debug:
    print_stats('Oldenburg (err removed)', oldenburg_df)
    print_stats('Berlin (err removed)', berlin_df)
    print_stats('Munich (err removed)', munich_df)

print(oldenburg_df.head())
print(berlin_df.head())
print(munich_df.head())

visualize_data(oldenburg_df)
visualize_data(berlin_df)
visualize_data(munich_df)




