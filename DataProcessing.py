import asyncio
import websockets
import json
import matplotlib.pyplot as plt
from collections import deque
import numpy as np
from scipy.fft import fft
import socket

# Colas para almacenar los datos del acelerómetro
acceleration_data = {'x': deque(maxlen=100), 'y': deque(maxlen=100), 'z': deque(maxlen=100)}

# Tamaño del paquete de datos del acelerómetro
tamano_paquete = 25

def graficar_fft_y_fases(fft_magnitud_x, fft_magnitud_y, fase_x, fase_y):
    plt.figure(figsize=(12, 6))

    plt.subplot(2, 1, 1)
    plt.plot(fft_magnitud_x, label='FFT Magnitud X')
    plt.plot(fft_magnitud_y, label='FFT Magnitud Y')
    plt.title('FFT Magnitud')
    plt.xlabel('Frecuencia')
    plt.ylabel('Amplitud')
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.plot(fase_x, label='Fase X')
    plt.plot(fase_y, label='Fase Y')
    plt.title('Fase')
    plt.xlabel('Frecuencia')
    plt.ylabel('Fase (radianes)')
    plt.legend()

    plt.tight_layout()
    plt.show()


def calcular_fft_y_fases(paquete_datos):
    # Calcular la FFT para cada eje
    fft_result_x = fft(paquete_datos['x'])
    fft_result_y = fft(paquete_datos['y'])
    # Calcular la fase para cada eje
    fase_x = np.angle(fft_result_x)
    fase_y = np.angle(fft_result_y)

    return np.abs(fft_result_x), np.abs(fft_result_y), fase_x, fase_y

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

hostname = socket.gethostname()
IPAddr = get_ip()
print("Your Computer Name is: " + hostname)
print("Your Computer IP Address is: " + IPAddr)
print(
    "* Enter {0}:5000 in the app.\n* Press the 'Set IP Address' button.\n* Select the sensors to stream.\n* Update the 'update interval' by entering a value in ms.".format(IPAddr))

async def echo(websocket, path):
    async for message in websocket:
        if path == '/accelerometer':
            data = await websocket.recv()
            print(data)
            f = open("accelerometer.txt", "a")
            f.write(data + "\n")

            # Parseamos los datos del acelerómetro
            parsed_data = json.loads(data)
            x = parsed_data['x']
            y = parsed_data['y']

            # Almacenar los datos del acelerómetro en las colas
            acceleration_data['x'].append(float(x))
            acceleration_data['y'].append(float(y))

            # Verificar si hemos acumulado suficientes datos para calcular la FFT
            if len(acceleration_data['x']) == tamano_paquete:
                # Crear el paquete de datos
                paquete_datos = {'x': np.array(acceleration_data['x']), 'y': np.array(acceleration_data['y'])}

                # Calcular la FFT y las fases utilizando la función
                fft_magnitud_x, fft_magnitud_y, fase_x, fase_y = calcular_fft_y_fases(paquete_datos)

                # Imprimir o utilizar los resultados según sea necesario
                print("FFT Magnitud X:", fft_magnitud_x)
                print("FFT Magnitud Y:", fft_magnitud_y)
                print("Fase X:", fase_x)
                print("Fase Y:", fase_y)

                #graficar_fft_y_fases(fft_magnitud_x, fft_magnitud_y, fase_x, fase_y)

                # Limpiar las colas después de procesar la FFT
                acceleration_data['x'].clear()
                acceleration_data['y'].clear()

# Resto del código sin cambios...

async def main():
    async with websockets.serve(echo, '0.0.0.0', 5000, max_size=1_000_000_000):
        await asyncio.Future()

asyncio.run(main())
