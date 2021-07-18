from tensorflow.keras.models import load_model
from ml.model_utils import loss_mse_warmup

model = load_model('weights/Atascocita C560.csv-weights', custom_objects={'loss_mse_warmup': loss_mse_warmup})