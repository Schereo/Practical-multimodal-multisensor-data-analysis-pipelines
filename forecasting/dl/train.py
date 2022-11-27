

import pandas as pd
import torch
from torch import nn
from forecasting.dl.dataset import SequenceDataset
from torch.utils.data import DataLoader

from forecasting.dl.lstm import ShallowRegressionLSTM

i = 2
sequence_length = 10
learning_rate = 1e-3
num_hidden_units = 16
batch_size = 32
def lstm(d1):
    # split df1 into 20/80 datasets
    train_size = int(len(d1) * 0.8)
    test_size = len(d1) - train_size
    train, test = d1.iloc[0:train_size], d1.iloc[train_size:len(d1)]

    target = "R1"
    target_mean = train[target].mean()
    target_stdev = train[target].std()

    for c in train.columns:
        mean = train[c].mean()
        stdev = train[c].std()
        train[c] = (train[c] - mean) / stdev
        test[c] = (test[c] - mean) / stdev
    train_dataset = SequenceDataset(train, sequence_length)
    test_dataset = SequenceDataset(test, sequence_length)
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)
    
    

    model = ShallowRegressionLSTM(num_features=3, hidden_units=num_hidden_units).double()
    loss_function = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    print("Untrained test\n--------")
    test_model(test_loader, model, loss_function)
    print()

    for ix_epoch in range(5):
        print(f"Epoch {ix_epoch}\n---------")
        train_model(train_loader, model, loss_function, optimizer=optimizer)
        # test_model(test_loader, model, loss_function)
        print()

    train_eval_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=False)

    ystar_col = "Model forecast"
    
    train[ystar_col] = predict(train_eval_loader, model).numpy()
    test[ystar_col] = predict(test_loader, model).numpy()

    df_out = pd.concat((train, test))[[target, ystar_col]]

    for c in df_out.columns:
        df_out[c] = df_out[c] * target_stdev + target_mean

    print(df_out)
    # save df_out to csv
    df_out.to_csv('lstm_out.csv')

def train_model(data_loader, model, loss_function, optimizer):
    num_batches = len(data_loader)
    total_loss = 0
    model.train()
    
    for X, y in data_loader:

        output = model(X)
        # print(output.dtype)
        loss = loss_function(output, y)
        # print(loss.dtype)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

    avg_loss = total_loss / num_batches
    print(f"Train loss: {avg_loss}")

def test_model(data_loader, model, loss_function):
    
    num_batches = len(data_loader)
    total_loss = 0

    model.eval()
    with torch.no_grad():
        for X, y in data_loader:
            # print(X.dtype)
            # print(y.dtype)
            # covert dtype of y to double
            y = y.double()
            X = X.double()
            output = model(X)
            total_loss += loss_function(output, y).item()

    avg_loss = total_loss / num_batches
    print(f"Test loss: {avg_loss}")

def predict(data_loader, model):

    output = torch.tensor([])
    model.eval()
    with torch.no_grad():
        for X, _ in data_loader:
            y_star = model(X)
            output = torch.cat((output, y_star), 0)
    
    return output


    