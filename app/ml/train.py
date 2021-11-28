import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from time import time
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Activation, Dropout, Flatten
from tensorflow.keras.layers import LSTM
from tensorflow.keras.optimizers import Adam
from time import time
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.metrics import r2_score
from sklearn.preprocessing import MinMaxScaler

sc = MinMaxScaler()

if __name__ == "__main__":
    df = pd.read_csv("../data_process/merged_AAPL_30m_191001_191231.csv")
    df.drop(columns=['<VOL>'], inplace=True)
    # df = df.iloc[: , 1:]
    df.sort_values(by='<TIME>', ascending=True, inplace=True)
    df.set_index("<TIME>", inplace=True)

    print("---dataframe head---")
    print(df.head())

    print("--scaling data---")
    data = sc.fit_transform(df)

    train_ind = int(0.8 * len(df))
    # val_ind = train_ind + int(0.2*len(df))

    train = data[:train_ind]
    # val = data[train_ind:val_ind]
    # test = data[val_ind:]
    test = data[train_ind:]

    print("--shapes--")
    print("train, test", train.shape, test.shape)

    xtrain, ytrain, xtest, ytest = train[:, :4], train[:, 3], test[:, :4], test[:, 3]
    print(xtest.shape, ytest.shape)

    # lookback = 60
    lookback = 1

    n_features = 4
    train_len = len(xtrain) - lookback
    test_len = len(xtest) - lookback
    # val_len = len(xval) - lookback

    x_train = np.zeros((train_len, lookback, n_features))
    y_train = np.zeros((train_len))
    for i in range(train_len):
        ytemp = i + lookback
        x_train[i] = xtrain[i:ytemp]
        y_train[i] = ytrain[ytemp]
    print("x_train", x_train.shape)
    print("y_train", y_train.shape)

    x_test = np.zeros((test_len, lookback, n_features))
    y_test = np.zeros((test_len))
    for i in range(test_len):
        ytemp = i + lookback
        x_test[i] = xtest[i:ytemp]
        y_test[i] = ytest[ytemp]
    print("x_test", x_test.shape)
    print("y_test", y_test.shape)

    earlystop = EarlyStopping(monitor='val_loss', min_delta=0.0001, patience=80, verbose=1, mode='min')