from tensorflow.keras.models import load_model
from joblib import load
from numpy import expand_dims

from ml.model_utils import loss_mse_warmup
from get_weather import weather_forecast

weight_dir = 'weights/stations/'

def forecast_AQI(station_name):
    model = load_model(weight_dir + station_name + '/weights', custom_objects={'loss_mse_warmup': loss_mse_warmup})
    x_scaler = load(weight_dir + station_name + '/x-scaler.gz')
    y_scaler = load(weight_dir + station_name + '/y-scaler.gz')

    df = weather_forecast(station_name)
    x_data = df[['air_temp', 'dew_point_temp', 'sea_level_pressure', 'wind_speed', 'visibility']].values

    x = x_scaler.transform(x_data)
    x = expand_dims(x, axis=0)

    preds = model.predict(x)

    y_pred_rescaled = y_scaler.inverse_transform(preds[0]).ravel().astype(int)
    y_pred_rescaled[0] = df.AQI.iloc[0]

    return y_pred_rescaled

print(forecast_AQI('Baytown Garth C1017'))