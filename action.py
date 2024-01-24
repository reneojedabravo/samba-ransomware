import os
import re
import requests
import time
from collections import deque
import subprocess
import threading

# Función para buscar extensiones en una línea
def buscar_extensiones(linea, lista_extensiones):
    # Iterar sobre cada extensión
    for extension in lista_extensiones:
        # Escapar caracteres especiales en la extensión
        extension_escapada = re.escape(extension)

        # Reemplazar el comodín "*" con la expresión regular ".+"
        extension_regex = extension_escapada.replace(r'\*', r'.+')

        # Buscar coincidencias en la línea
        coincidencias = re.findall(extension_regex, linea)

        # Si hay coincidencias, extraer información y ejecutar el script bash
        if coincidencias:
            usuario, ip, nombre_equipo = extraer_informacion(linea)
            if usuario is not None:
                print(f'¡Extensión detectada en la línea: {linea.strip()}!')
                #print(f'Usuario: {usuario}, IP: {ip}, Nombre del equipo: {nombre_equipo}')
                ejecutar_script_bash(usuario, ip, nombre_equipo)
            return True

    # Si no se encontraron extensiones, devolver False
    return False

# Función para extraer información de la línea
def extraer_informacion(linea):
    # Patrón para extraer información
    patron = re.compile(r'(\w+)\|(\d+\.\d+\.\d+\.\d+)\|([^\|]+)\|')

    # Buscar coincidencias en la línea
    coincidencias = patron.search(linea)

    if coincidencias:
        usuario = coincidencias.group(1)
        ip = coincidencias.group(2)
        nombre_equipo = coincidencias.group(3)
        
        return usuario, ip, nombre_equipo

    return None, None, None

# Función para obtener la lista de extensiones
def obtener_extensiones():
    # URL de la lista de extensiones
    url = "https://fsrm.experiant.ca/api/v1/combined"

    # Realizar la solicitud para obtener la lista de extensiones
    response = requests.get(url)

    # Verificar si la solicitud fue exitosa
    if response.status_code == 200:
        # Extraer la lista de extensiones desde la respuesta JSON
        data = response.json()
        filters = data["filters"]
        
        # Excluir las extensiones por ejemplo "*.blend", "*.skynet", "*.etc"...
        filters = [extension for extension in filters if extension not in ["*.blend"]]
        
        # Guardar la lista en el archivo extensiones.txt
        with open("extensiones.txt", "w") as extension_file:
            for extension in filters:
                extension_file.write(extension + "\n")
        
        print("Lista descargada")
        print("Procesando...")
        return filters
    else:
        # Mostrar un mensaje de error si la solicitud falla
        print(f"No se pudo encontrar la lista. Código de estado: {response.status_code}")
        return []

# Función para ejecutar el script en bash
def ejecutar_script_bash(usuario, ip, nombre_equipo):
    subprocess.run(["bash", "action.sh", usuario, ip, nombre_equipo])
    print("Deteniendo la ejecución del script")
    os._exit(0)  # Detener la ejecución del script

# Función para procesar el archivo temporal
def procesar_archivo_temporal(archivo_temporal, lista_extensiones):
    try:
        with open(archivo_temporal, "r") as temp_file:
            for linea in temp_file:
                if buscar_extensiones(linea, lista_extensiones):
                    return
    except Exception as e:
        print(f"Error al leer el archivo temporal: {str(e)}")

# Función principal
def main():
    # Ruta del archivo de registro
    archivo_log = "/var/log/samba/audit.log"
    # Ruta del archivo temporal
    archivo_temporal = "temp_log.txt"

    # Descargar la lista de extensiones al inicio
    lista_extensiones = obtener_extensiones()

    while True:
        try:
            # Leer las últimas 10 líneas del archivo de registro
            with open(archivo_log, "r") as file:
                # Usar deque para mantener solo las últimas 10 líneas
                cola_lineas = deque(file, maxlen=10)

            # Crear el archivo temporal si no existe
            if not os.path.exists(archivo_temporal):
                with open(archivo_temporal, "w"):
                    pass

            # Guardar las últimas 10 líneas en el archivo temporal
            with open(archivo_temporal, "w") as temp_file:
                temp_file.writelines(cola_lineas)

            # Procesar el archivo temporal
            procesar_archivo_temporal(archivo_temporal, lista_extensiones)

            # Esperar antes de volver a revisar el archivo de registro
            time.sleep(1)

        except Exception as e:
            # Mostrar un mensaje de error si hay un problema al leer el archivo
            print(f"Error al leer el archivo de registro: {str(e)}")

if __name__ == "__main__":
    main()
