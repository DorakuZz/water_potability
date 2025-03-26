# -*- coding: utf-8 -*-
"""Proyecto_IA.py

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/14VWuzI39HhraknUF9Q3a71ZV4AMaKri4

**Importar librerias, importar módulos e importar los datos**
"""

#Importar librerias para graficar y traer el DataFrame desde GitHub
import pandas as pd
import numpy as np

import seaborn as sns
#seaborn tambien para graficar

#graficar
import matplotlib.pyplot as plt

import matplotlib.ticker as ticker


#sistema operativo
import os

#leer archivos de web
import urllib

# Importación del módulo urllib para realizar operaciones con URLs
import urllib.request

# Definición de la URL del archivo de texto que se encuentra en un repositorio de GitHub
urlvariables = "https://raw.githubusercontent.com/DorakuZz/water_potability/refs/heads/main/variables"

# Apertura de la URL utilizando urllib, que permite leer el contenido del archivo en la URL
variables = urllib.request.urlopen(urlvariables)

# Iteración sobre cada línea en el archivo abierto
for linea in variables:
    # Decodificación de cada línea desde bytes a una cadena de texto utilizando UTF-8
    print(linea.decode("utf-8"))

# Importación de la biblioteca pandas, generalmente importada como pd por convención
import pandas as pd

# URL del archivo CSV que se encuentra en un repositorio de GitHub
url = "https://raw.githubusercontent.com/DorakuZz/water_potability/refs/heads/main/water_potability.csv"

# Lectura del archivo CSV desde la URL utilizando pandas
# El parámetro sep=";" especifica que el separador de columnas en el archivo CSV es un punto y coma
df = pd.read_csv(url, sep=",")

# Mostrar el contenido del DataFrame df
# En un entorno interactivo como Jupyter Notebook, esta línea muestra las primeras y últimas filas del DataFrame
df

#Visualizar cúales son los nombres de las columnas en el DataFrame
df.columns

#Visualizar los estadisticos del DataFrame
df.describe()

#Hacer una copia del DataFrame para modificar la copia y no el DataFrame original
dfc = df.copy()

#Consultar qué tipo de dato es cada variable
dfc.dtypes

#Visualizar la dimensionalidad del DataFrame
dfc.shape

#Con este comando podemos visualizar cuántos valores diferentes existen en cada columna
for column in dfc.columns:
    num_distinct_values = len(dfc[column].unique())
    print(f"{column}: {num_distinct_values} Valores diferentes")

#Este comando comprueba la existencia de filas duplicadas en el dataframe
duplicate_rows_data = dfc[dfc.duplicated()]
print("numero de filas duplicadas es: ", duplicate_rows_data.shape[0])

"""**Manejo de nulos en el DataFrame**"""

#Consultar si existen nulos en el DataFrame
dfc.isnull().sum()

# Mapa de calor para visualizar nulos
sns.heatmap(df.isnull(), cbar=False, cmap="viridis")
plt.title("Mapa de Valores Nulos")
plt.show()

# Porcentaje de valores nulos por columna
missing_percentage = df.isnull().mean() * 100
print(missing_percentage)

# Visualización del porcentaje de nulos
missing_percentage.plot(kind='bar', title='Porcentaje de Nulos por Columna')
plt.ylabel('Porcentaje')
plt.show()

# Rellenar valores nulos en "ph" con la media
dfc["ph"] = dfc["ph"].fillna(dfc["ph"].mean())

# Rellenar valores nulos en "Sulfate" con la media
dfc["Sulfate"] = dfc["Sulfate"].fillna(dfc["Sulfate"].mean())

# Rellenar valores nulos en "Trihalomethanes" con la media
dfc["Trihalomethanes"] = dfc["Trihalomethanes"].fillna(dfc["Trihalomethanes"].mean())

dfc.isnull().sum()

"""**Finalización de la vista minable**"""

# Separar las características (X) y la variable objetivo (y)
X = dfc.drop('Potability', axis=1)
y = dfc['Potability']

from imblearn.over_sampling import SMOTE
# Aplicar SMOTE
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X, y)

# Crear un nuevo DataFrame balanceado
dfc_balanceado = pd.concat([pd.DataFrame(X_resampled, columns=X.columns),
                             pd.DataFrame(y_resampled, columns=['Potability'])],
                             axis=1)

# Verificar la distribución de clases antes y después del balanceo
print("Distribución original:")
print(y.value_counts())
print("\nDistribución después de SMOTE:")
print(y_resampled.value_counts())

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_resampled)
X_scaled = pd.DataFrame(X_scaled, columns=X.columns)
X_scaled

dfc = X_scaled

dfc.describe()

X_scaled.var()

dfc.columns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report


# Dividir datos
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y_resampled,
    test_size=0.2,
    random_state=99
)

# Opción 2: Random Forest
modelo_rf = RandomForestClassifier(n_estimators=100, random_state=42)
modelo_rf.fit(X_train, y_train)
predicciones_rf = modelo_rf.predict(X_test)

print("\n\nMétricas de Random Forest:")
print("Accuracy:", accuracy_score(y_test, predicciones_rf))
print("\nReporte de Clasificación:\n", classification_report(y_test, predicciones_rf))
print("\nMatriz de Confusión:\n", confusion_matrix(y_test, predicciones_rf))

# Método 1: Usando joblib (recomendado para scikit-learn)
import joblib

# Guardar modelo de Random Forest
joblib.dump(modelo_rf, 'modelo_calidad_agua_rf.pkl')

# Guardar el scaler junto con el modelo
joblib.dump({
    'modelo': modelo_rf,
    'scaler': scaler
}, 'modelo_calidad_agua_completo.pkl')