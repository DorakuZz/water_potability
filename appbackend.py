from fastapi import FastAPI
from pydantic import BaseModel
import joblib

# Carga del modelo (ajusta según cómo esté guardado tu .pkl)
modelo_dict = joblib.load("modelo_calidad_agua_completo.pkl")
modelo = modelo_dict['modelo']  # <- asegúrate que sea la clave correcta

app = FastAPI()

class WaterData(BaseModel):
    ph: float
    Hardness: float
    Solids: float
    Chloramines: float
    Sulfate: float
    Conductivity: float
    Organic_carbon: float
    Trihalomethanes: float
    Turbidity: float

@app.get("/")
def root():
    return {"message": "API de predicción de potabilidad del agua"}

@app.post("/predict")
def predict(data: WaterData):
    valores = [[
        data.ph, data.Hardness, data.Solids, data.Chloramines,
        data.Sulfate, data.Conductivity, data.Organic_carbon,
        data.Trihalomethanes, data.Turbidity
    ]]
    resultado = modelo.predict(valores)[0]
    return {"potability": int(resultado)}
