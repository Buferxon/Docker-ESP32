import numpy as np
from keras.metrics import MeanSquaredError
from tensorflow.keras.models import load_model
import joblib
import pandas as pd
from datetime import datetime, timedelta
import json
# Cargar el modelo y los escaladores
model = load_model('modelo_clima.h5', custom_objects={'mse': MeanSquaredError()})
scaler_X = joblib.load('scaler_X.pkl')
scaler_y = joblib.load('scaler_y.pkl')
label_encoder = joblib.load('label_encoder_sky.pkl')

# print(label_encoder.classes_)

# Pedir al usuario que ingrese la fecha
# Calcular automáticamente el día siguiente al mediodía
mañana = datetime.now() + timedelta(days=1)
mañana_mediodia = mañana.replace(hour=12, minute=0, second=0, microsecond=0)

hora = mañana_mediodia.hour
dia = mañana_mediodia.day
mes = mañana_mediodia.month



# Preparar el input
entrada = np.array([[hora, dia, mes]])
entrada_df = pd.DataFrame(entrada, columns=['hour', 'day', 'month'])
entrada_escalada = scaler_X.transform(entrada_df)

# Hacer la predicción
pred_reg, pred_cat = model.predict(entrada_escalada)

# Desescalar solo la parte de regresión
pred_reg_des = scaler_y.inverse_transform(pred_reg)

temperatura, humedad, presion = pred_reg_des[0]

# Obtener la clase predicha para el cielo
sky_codificado = np.argmax(pred_cat[0])
tipo_cielo = label_encoder.inverse_transform([sky_codificado])[0]

# Crear un diccionario con los resultados
resultados = {
    'temperatura': float(temperatura),
    'humedad': float(humedad),
    'presion': float(presion),
    'tipo_cielo': tipo_cielo,
    'fecha': mañana_mediodia.strftime('%Y-%m-%d %H:%M:%S')
}

# Devolver los resultados como JSON
print(json.dumps(resultados, indent=4))