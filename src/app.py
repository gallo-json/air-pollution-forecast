from tensorflow.keras.models import load_model
from joblib import load
from numpy import expand_dims

from ml.model_utils import loss_mse_warmup
from get_weather import weather_forecast

weight_dir = 'weights/stations/'

model = load_model(weight_dir + 'Atascocita C560/weights', custom_objects={'loss_mse_warmup': loss_mse_warmup})
x_scaler = load(weight_dir + 'Atascocita C560/x-scaler.gz')
y_scaler = load(weight_dir + 'Atascocita C560/y-scaler.gz')

df = weather_forecast('Atascocita C560')
x_data = df[['air_temp', 'dew_point_temp', 'sea_level_pressure', 'wind_speed', 'visibility']].values

x = x_scaler.transform(x_data)
x = expand_dims(x, axis=0)

preds = model.predict(x)

y_pred_rescaled = y_scaler.inverse_transform(preds[0])

print(y_pred_rescaled)
print(df)