from matplotlib import pyplot as plt

def print_stats(name, df):
    print()
    print(name)
    print(df.info())
    print(df['R1'].describe())

def visualize_data(df):
    plt.plot(df['MESS_DATUM'], df['R1'])
    plt.show()