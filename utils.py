import pandas as pd

df = pd.read_csv('exchange 2021-2024.csv')

print(df.head())

# Convertir la columna de fechas al formato deseado
df['fecha'] = pd.to_datetime(df['fecha']).dt.strftime('%Y-%m-%d')

# Guardar el DataFrame de nuevo en un archivo CSV
df.to_csv('datos_modificados.csv', index=False)

print("Formato de fechas actualizado y guardado en 'datos_modificados.csv'")
