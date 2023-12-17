import numpy as np
import pandas as pd

# Parámetros
num_datos_acumular = 25
frecuencia_muestreo = 100  # Frecuencia de muestreo en Hz

# Inicializar listas para acumular datos
acelerometro_x = []
acelerometro_y = []

# Función para acumular datos del acelerómetro
def acumular_datos_acelerometro(x, y):
    acelerometro_x.extend(x)
    acelerometro_y.extend(y)

    # Verificar si tenemos suficientes datos acumulados
    if len(acelerometro_x) >= num_datos_acumular:
        # Procesar los últimos num_datos_acumular datos
        procesar_datos()

# Función para procesar los datos acumulados
def procesar_datos():
    # Calcular la FFT y la fase
    fft_result = calcular_fft(acelerometro_x, acelerometro_y)
    fase_result = calcular_fase(acelerometro_x, acelerometro_y)

    # Crear DataFrames para los resultados
    fft_dataframe = pd.DataFrame(fft_result, columns=['Frecuencia', 'Amplitud X', 'Amplitud Y'])
    fase_dataframe = pd.DataFrame(fase_result, columns=['Frecuencia', 'Fase X', 'Fase Y'])

    # Guardar los resultados en archivos CSV
    fft_dataframe.to_csv('fft_result.csv', index=False)
    fase_dataframe.to_csv('fase_result.csv', index=False)

    # Limpiar los datos acumulados
    limpiar_datos()

# Función para calcular la FFT
def calcular_fft(x, y):
    datos_acelerometro = x + y
    fft_result = np.fft.fft(datos_acelerometro)
    frecuencias = np.fft.fftfreq(len(fft_result), d=1/frecuencia_muestreo)
    amplitud_x = np.abs(fft_result.real)
    amplitud_y = np.abs(fft_result.imag)

    # Devolver un array con las columnas 'Frecuencia', 'Amplitud X' y 'Amplitud Y'
    return np.column_stack((frecuencias, amplitud_x, amplitud_y))

# Función para calcular la fase
def calcular_fase(x, y):
    fase_x = np.angle(np.fft.fft(x))
    fase_y = np.angle(np.fft.fft(y))
    
    # Devolver un array con las columnas 'Frecuencia', 'Fase X' y 'Fase Y'
    return np.column_stack((frecuencias, fase_x, fase_y))

# Función para limpiar los datos acumulados
def limpiar_datos():
    del acelerometro_x[:]
    del acelerometro_y[:]

# Ejemplo de uso
# Supongamos que obtienes nuevos datos del acelerómetro en cada iteración
# Puedes llamar a la función acumular_datos_acelerometro con tus nuevos datos
# Aquí, por simplicidad, se usa una lista de ceros como datos de ejemplo
acelerometro_nuevos_datos_x = [0.0] * num_datos_acumular
acelerometro_nuevos_datos_y = [0.0] * num_datos_acumular
acumular_datos_acelerometro(acelerometro_nuevos_datos_x, acelerometro_nuevos_datos_y)
