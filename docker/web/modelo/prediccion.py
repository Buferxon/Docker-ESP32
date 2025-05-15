import numpy as np
from keras.metrics import MeanSquaredError
from tensorflow.keras.models import load_model
import joblib
import pandas as pd
from datetime import datetime, timedelta

import os

base_path = "/var/www/html/storage/app/public"

model = load_model(os.path.join(base_path, "modelo_clima.h5"), custom_objects={'mse': MeanSquaredError()})
label_encoder = joblib.load(os.path.join(base_path, "label_encoder_sky.pkl"))
scaler_X = joblib.load(os.path.join(base_path, "scaler_X.pkl"))
scaler_y = joblib.load(os.path.join(base_path, "scaler_y.pkl"))
print(label_encoder.classes_)

# Obtener la fecha y hora actual
now = datetime.now()

# Crear una lista con las dos horas siguientes
predicciones_horas = [(now + timedelta(hours=i)).replace(minute=0, second=0, microsecond=0) for i in range(1, 3)]

# Preparar las entradas para las predicciones
entradas = []
for prediccion_hora in predicciones_horas:
    hora = prediccion_hora.hour
    dia = prediccion_hora.day
    mes = prediccion_hora.month
    entradas.append([hora, dia, mes])

# Preparar el input
entrada = np.array([[hora, dia, mes]])
entrada_df = pd.DataFrame(entrada, columns=['hour', 'day', 'month'])
entrada_escalada = scaler_X.transform(entrada_df)

# Hacer la predicción
prediccion_escalada = model.predict(entrada_escalada)
prediccion = scaler_y.inverse_transform(prediccion_escalada)

# Mostrar resultados
temperatura, humedad, presion, sky_codificado = prediccion[0]

print(f"TEMPERATURA={temperatura:.2f}")
print(f"HUMEDAD={humedad:.2f}")
print(f"PRESION={presion:.2f}")

# Asegurarse que el cielo predicho sea un entero válido
sky_codificado = np.argmax(prediccion[0][-len(label_encoder.classes_):])

# Ahora decodificar
try:
    tipo_cielo = label_encoder.inverse_transform([sky_codificado])[0]
except Exception as e:
    tipo_cielo = f"Desconocido (código {sky_codificado})"

print(f"TIPO_CIELO={tipo_cielo}")
