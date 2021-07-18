from numpy.core.numeric import base_repr
import tensorflow as tf
import pandas as pd
import numpy as np
import joblib
import os

from sklearn.preprocessing import MinMaxScaler

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, Dense, GRU
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.backend import square, mean

from model_utils import batch_generator, loss_mse_warmup

base_dir = "/home/jose/Programming/aiml/Data/houston-AQI-weather/filled-in-data/"

for csv_file in os.listdir(base_dir):
    df = pd.read_csv(base_dir + csv_file)
    del df['Unnamed: 0']
    df.dropna(axis=0, how='any', inplace=True)
    df = df[df.AQI != 'NV']

    x_data = df[['air_temp', 'dew_point_temp', 'sea_level_pressure', 'wind_speed', 'visibility']].values
    y_data = df.AQI.values

    train_test_split = 0.8

    num_train = int(len(x_data) * train_test_split)
    num_test = len(x_data) - num_train

    x_train = x_data[0:num_train]
    x_test = x_data[num_train:]

    # Expanding dimension to (None, 1) (to a vector) instead of just an array of shape (None,)
    # Used in order to feed into the MinMaxScaler (does not support 1D arrays)
    y_train = np.expand_dims(y_data[:num_train], axis=1)
    y_test = np.expand_dims(y_data[num_train:], axis=1)

    x_scaler = MinMaxScaler()
    x_train_scaled = x_scaler.fit_transform(x_train)
    x_test_scaled = x_scaler.transform(x_test)

    joblib.dump(x_scaler, 'weights/stations/' + csv_file[:-4] + '/x-scaler.gz')

    y_scaler = MinMaxScaler()
    y_train_scaled = y_scaler.fit_transform(y_train)
    y_test_scaled = y_scaler.transform(y_test)

    joblib.dump(y_scaler, 'weights/stations/' + csv_file[:-4] + '/y-scaler.gz')

    generator = batch_generator(num_train, x_train_scaled, y_train_scaled)
    x_batch, y_batch = next(generator)

    validation_data = (np.expand_dims(x_test_scaled, axis=0),
                   np.expand_dims(y_test_scaled, axis=0))

    callback_early_stopping = EarlyStopping(monitor='val_loss',
                        patience=5, verbose=1)

    callback_reduce_lr = ReduceLROnPlateau(monitor='val_loss',
                                       factor=0.1,
                                       min_lr=1e-4,
                                       patience=0,
                                       verbose=1)

    callbacks = [callback_early_stopping,
             callback_reduce_lr]

    model = Sequential()

    model.add(GRU(units=512,
                return_sequences=True,
                input_shape=(None, x_test.shape[1],)))
    model.add(Dense(1, activation='sigmoid'))

    model.compile(loss=loss_mse_warmup, optimizer=RMSprop(lr=1e-3))

    model.fit(x=generator,
            epochs=50,
            steps_per_epoch=100,
            validation_data=validation_data,
            callbacks=callbacks)

    model.save('weights/stations/' + csv_file[:-4] + '/weights')