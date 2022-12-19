from torch import nn
import torch

class ShallowRegressionLSTM(nn.Module):
    def __init__(self, num_features, hidden_units):
        super().__init__()
        self.num_features = num_features  # this is the number of features
        self.hidden_units = hidden_units
        self.num_layers = 5

        self.lstm = nn.LSTM(
            input_size=num_features,
            hidden_size=hidden_units,
            batch_first=True,
            num_layers=self.num_layers
        )

        self.linear = nn.Linear(in_features=self.hidden_units, out_features=20)
        self.out = nn.Linear(in_features=20, out_features=1)

    def forward(self, x):
        batch_size = x.shape[0]
        h0 = torch.zeros(self.num_layers, batch_size, self.hidden_units, dtype=torch.float64).requires_grad_()
        c0 = torch.zeros(self.num_layers, batch_size, self.hidden_units, dtype=torch.float64).requires_grad_()
        x = x.double()
        _, (hn, _) = self.lstm(x, (h0, c0))
        out = self.linear(hn[0]) # First dim of Hn is num_layers, which is set to 1 above.
        out = self.out(out).flatten()

        return out