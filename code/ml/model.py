import pandas as pd
import tensorflow
from kerastuner.tuners import RandomSearch
from tensorflow.keras.layers import LSTM, Dropout, Dense
from tensorflow.keras.models import Sequential

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


df = pd.read_parquet("../kaggle_data/prices_AAPL.parquet")
df.drop(columns=['volume'], inplace=True)
df.sort_values(by='day_date', ascending=True, inplace=True)
df.set_index("day_date", inplace=True)

print("---dataframe head---")
print(df.head())

print("--scaling data---")
data = sc.fit_transform(df)

train_ind = int(0.6 * len(df))
val_ind = train_ind + int(0.2 * len(df))

train = data[:train_ind]
val = data[train_ind:val_ind]
test = data[val_ind:]

print("--shapes--")
print("train,test,val", train.shape, test.shape, val.shape)

xtrain, ytrain, xval, yval, xtest, ytest = train[:, :4], train[:, 3], val[:, :4], val[:, 3], test[:, :4], test[:, 3]
print(xtest.shape, ytest.shape)

lookback = 60
n_features = 4
train_len = len(xtrain) - lookback
test_len = len(xtest) - lookback
val_len = len(xval) - lookback

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

x_val = np.zeros((val_len, lookback, n_features))
y_val = np.zeros((val_len))
for i in range(val_len):
    ytemp = i + lookback
    x_val[i] = xval[i:ytemp]
    y_val[i] = yval[ytemp]
print("x_val", x_val.shape)
print("y_val", y_val.shape)

X_train, X_test = x_train, x_test


def build_model(hp):
    model = Sequential()
    # number of hidden layer
    hidden = hp.Int("n_hidden", min_value=0, max_value=3)
    # first LSTM−Layer
    model.add(LSTM(units=hp.Int("n_units1", min_value=17, max_value=500, step=50),
                   activation=hp.Choice("v_activation", values=["relu", "tanh", "sigmoid"], default="relu"),
                   input_shape=(X_train.shape[1], X_train.shape[2]),
                   return_sequences=True if hidden > 0 else False))

    if hidden > 0:
        for layer in range(hidden):
            model.add(Dropout(hp.Float("v_dropout_hidden" + str(layer + 1), min_value=0.05, max_value=0.95, step=0.05)))
            model.add(LSTM(units=hp.Int("n_units_hidden" + str(layer + 1), min_value=17,
                                        max_value=250,
                                        step=50),
                           activation="relu",
                           return_sequences=True if layer != hidden else False))

    model.add(Dropout(hp.Float("v_dropout", min_value=0.05, max_value=0.95, step=0.05)))
    model.add(Dense(units=1))
    model.compile(optimizer="adam", loss="mean_squared_error")

    return model


tuner = RandomSearch(build_model,
                     objective="val_loss", max_trials=50,
                     seed=1,
                     executions_per_trial=3, directory="",
                     project_name="")

early_stopping_cb = tensorflow.keras.callbacks.EarlyStopping(patience=10, restore_best_weights=True)
tuner.search(X_train, y_train,
             epochs=10,
             # epochs=1500,
             batch_size=32,
             validation_split=0.2, callbacks=[early_stopping_cb], verbose=1)

best_model = tuner.get_best_models(num_models=1)[0]
# save best model for that variable combination
best_model.save("best_model.h5")
# Evaluate the best model with test data
loss = best_model.evaluate(X_test, y_test)
