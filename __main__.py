from preprocessing.download_data import get_data
from preprocessing.clean_data import remove_error_data
from preprocessing.visualization import print_stats

debug = True

oldenburg_df, berlin_df, munich_df = get_data()

if debug:
    print_stats('Oldenburg (uncleaned)', oldenburg_df)
    print_stats('Berlin (uncleaned)', berlin_df)
    print_stats('Munich (uncleaned)', munich_df)


oldenburg_df = remove_error_data(oldenburg_df)
berlin_df = remove_error_data(berlin_df)
munich_df = remove_error_data(munich_df)

if debug:
    print_stats('Oldenburg (err removed)', oldenburg_df)
    print_stats('Berlin (err removed)', berlin_df)
    print_stats('Munich (err removed)', munich_df)



