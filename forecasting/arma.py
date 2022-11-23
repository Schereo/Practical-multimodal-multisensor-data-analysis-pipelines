from matplotlib import pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
import seaborn as sns

# AutoRegressive-Moving Average
# Two polynomials, the first is for the autoregressive part, the second for the moving average part

def arma(df1):
    df1 = _sum_up_to_days(df1)
    train, test = _split_test_train_data(df1)
    _plot(train, test)
    # fitted_model = _fit_model(train)
    # _predict(fitted_model, test)


def _split_test_train_data(df1):
    # cut data into train and test data
    # remove all columns expect R1 and MES_DATUM
    
    train = df1[:int(0.8*(len(df1)))]
    test = df1[int(0.8*(len(df1))):]
    return train, test

def _plot(train, test):
    # plot train data with seaborn
    sns.lineplot(data=train, x=train.index, y='R1')
    # show plotted data
    plt.show()
    # plt.plot(train, color = "black")
    # plt.plot(test, color = "red")
    # plt.show()

def _fit_model(train):
    # fit model
    model = SARIMAX(train['R1'], order=(1, 1, 1))
    model_fit = model.fit()
    return model_fit

def _predict(fitted_model, test):
    # make prediction
    y_pred = fitted_model.get_forecast(len(test.index))
    y_pred_df = y_pred.conf_int(alpha = 0.05) 
    y_pred_df["Predictions"]  = fitted_model.predict(start = y_pred_df.index[0], end = y_pred_df.index[-1])
    y_pred_df.index = test.index
    y_pred_out = y_pred_df["Predictions"] 
    plt.plot(y_pred_out, color='green', label = 'Predictions')
    plt.legend()
    # plt.show()


    