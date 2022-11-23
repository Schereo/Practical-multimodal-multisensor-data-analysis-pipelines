

from pathlib import Path

from matplotlib import pyplot as plt


def visuzalize_forecasting(df1, df2, df3):
    Path("visualizations/forecasting").mkdir(parents=True, exist_ok=True)

def plot_linear_regression(df, slope, intercept, predictions, y):
    f, ax = plt.subplots()
    plt.figure(figsize=(20, 8))
    plt.text(0.4, 1.5, f'slope: {round(slope, 6)} \n intercept: {round(intercept, 3)}', horizontalalignment='center', verticalalignment='center', transform = ax.transAxes)
    plt.scatter(df.index, y,c='black')
    plt.plot(df.index, predictions, c='blue', linewidth=2)
    plt.title('Linear Regression')
    plt.ylabel('Precipitation (mm)')
    plt.xlabel('Days of the year')
    plt.show()