from pandas import DataFrame
from preprocessing.clean_data import sum_up_to_days
from sklearn.linear_model import LinearRegression

from visualizing.visualize_forecasting import plot_linear_regression

def linear_regression(df1, df2, df3):
    print('Calculating linear regression...')
    df1 = sum_up_to_days(df1)
    df2 = sum_up_to_days(df2)
    df3 = sum_up_to_days(df3)
    _linear_regression(df1)
    _linear_regression(df2)
    _linear_regression(df3)



def _linear_regression(df: DataFrame):
    reg = LinearRegression()
    X = df.index.factorize()[0].reshape(-1,1)
    y = df['R1'].values.reshape(-1, 1)  # type: ignore
    reg.fit(X,y)
    slope = reg.coef_[0][0]
    intercept = reg.intercept_[0]  # type: ignore
    predictions = reg.predict(X.reshape(-1, 1))
    plot_linear_regression(df, slope, intercept, predictions, y)


