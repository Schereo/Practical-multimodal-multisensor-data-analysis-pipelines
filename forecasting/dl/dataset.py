from pandas import DataFrame
import torch
from torch.utils.data import Dataset

class SequenceDataset(Dataset):
    def __init__(self, dataframe: DataFrame, seq_len: int):
        self.data = dataframe
        self.features_year = dataframe.index.year
        self.features_month = dataframe.index.month
        self.features_day = dataframe.index.dayofyear
        self.target = dataframe['R1'].values
        self.seq_len = seq_len

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        dtype = torch.float64
        idx_start = idx - self.seq_len + 1
        idx_end = idx + 1
        if idx >= self.seq_len -1:   
            x = torch.stack([torch.tensor(self.features_year[idx_start:idx_end], dtype=dtype),
                                torch.tensor(self.features_month[idx_start:idx_end], dtype=dtype),
                                torch.tensor(self.features_day[idx_start:idx_end], dtype=dtype)], dim=1)
        else:
            padding = torch.tensor([self.features_year[0], self.features_month[0], self.features_day[0]], dtype=dtype).repeat(self.seq_len - idx - 1, 1)
            x = torch.stack([torch.tensor(self.features_year[0:idx_end], dtype=dtype), torch.tensor(self.features_month[0:idx_end], dtype=dtype), torch.tensor(self.features_day[0:idx_end], dtype=dtype)], dim=1)
            x = torch.cat((padding, x), dim=0)
        y = torch.tensor(self.target[idx], dtype=dtype)
        return x, y