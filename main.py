import streamlit as st
import random
import time
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt


# Documentación y ayuda contextual
st.sidebar.markdown("### Descripción")
st.sidebar.markdown("""
    Para adaptar el código a sensores reales que miden presión, temperatura y vibración en un compresor, se necesitarían algunos pasos adicionales dependiendo de cómo esté estructurado el código actualmente. Aquí una guía general sobre como puede hacerse:
    
   
    
1.	Identificar el hardware y protocolo de comunicación: Asegurarnos de conocer qué tipos de sensores se están utilizando (por ejemplo, sensores analógicos, digitales, con qué protocolo se comunican, como I2C, SPI, UART, etc.).
2.	Conexión física: Conectar los sensores al sistema donde se está ejecutando el código. Esto podría ser un microcontrolador como Arduino, una Raspberry Pi u otro sistema embebido.
3.	Librerías y drivers: Si los sensores requieren drivers específicos o librerías para la comunicación, asegurarse de tener estas librerías instaladas y configuradas en tu entorno de desarrollo.
4.	Lectura de datos: Modificar el código para incluir las rutinas de lectura de los sensores. Dependiendo del tipo de sensor, esto podría implicar leer un voltaje analógico y convertirlo a una unidad de medida como temperatura o presión, o podría ser una lectura digital directa.
5.	Procesamiento de datos: Una vez que se hayan obtenido los datos de los sensores, podríamos necesitar procesarlos según las necesidades de la aplicación. Esto puede incluir filtrado de datos, promediado, conversión de unidades, etc.
6.	Integración en el código existente: Integrar las lecturas de los sensores en el código actual donde se realiza el procesamiento principal. A menudo, esto implica modificar variables o estructuras de datos existentes para almacenar y manejar los nuevos datos de los sensores.
7.	Manejo de errores y excepciones: Asegurarnos de manejar adecuadamente errores y excepciones que puedan surgir durante la lectura de los sensores, como problemas de comunicación o lecturas fuera de rango.
8.	Pruebas y ajustes: Realizar pruebas exhaustivas para verificar que los datos de los sensores sean precisos y consistentes con las expectativas. Ajusta cualquier parámetro según sea necesario.

""")



# Función para simular la obtención de datos del compresor
def obtener_datos_compresor():
    presion = random.uniform(50, 100)
    temperatura = random.uniform(20, 40)
    vibracion = random.uniform(0, 10)
    return presion, temperatura, vibracion

# Configuración de la aplicación Streamlit
st.title('Monitoreo de Compresor')

# Controles deslizantes para definir los umbrales
umbral_presion = st.slider("Umbral de Presión", min_value=0, max_value=150, value=90)
umbral_temperatura = st.slider("Umbral de Temperatura", min_value=0, max_value=50, value=30)
umbral_vibracion = st.slider("Umbral de Vibración", min_value=0, max_value=20, value=8)

# Entradas para definir el tiempo de actualización
st.write("Puedes indicar el tiempo de monitoreo")
horas = st.number_input("Horas", min_value=0, max_value=24, value=0)
minutos = st.number_input("Minutos", min_value=0, max_value=59, value=0)

# Calcular el tiempo total en segundos
tiempo_total_segundos = horas * 3600 + minutos * 60

# Botón para actualizar la página
if st.button('Actualizar'):
    st.experimental_rerun()

# Inicializar listas para almacenar datos
tiempos = []
datos_presion = []
datos_temperatura = []
datos_vibracion = []

# Contenedores para los gráficos y la tabla
grafico_presion = st.empty()
grafico_temperatura = st.empty()
grafico_vibracion = st.empty()
tabla_datos = st.empty()

# Inicializar el DataFrame
df = pd.DataFrame(columns=["Fecha y Hora", "Presión", "Temperatura", "Vibración"])

# Variable para controlar la visualización de gráficos y el mensaje de detención
mostrar_graficos = True

# Tiempo de inicio
inicio_tiempo = time.time()

if tiempo_total_segundos > 0:
    while mostrar_graficos:
        # Tiempo actual
        tiempo_actual = time.time()

        # Verificar si ha pasado el tiempo límite
        if tiempo_actual - inicio_tiempo > tiempo_total_segundos:
            mostrar_graficos = False

        # Simular obtención de datos
        presion, temperatura, vibracion = obtener_datos_compresor()

        # Obtener la fecha y hora actual
        fecha_hora_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Guardar datos
        tiempos.append(len(tiempos) + 1)
        datos_presion.append(presion)
        datos_temperatura.append(temperatura)
        datos_vibracion.append(vibracion)

        # Registrar los datos con la fecha y hora actual en el DataFrame
        nuevo_registro = pd.DataFrame({
            "Fecha y Hora": [fecha_hora_actual],
            "Presión": [presion],
            "Temperatura": [temperatura],
            "Vibración": [vibracion]
        })
        df = pd.concat([df, nuevo_registro], ignore_index=True)

        # Crear figuras de matplotlib para los gráficos
        fig_presion, ax_presion = plt.subplots()
        fig_temperatura, ax_temperatura = plt.subplots()
        fig_vibracion, ax_vibracion = plt.subplots()

        # Actualizar datos en los gráficos de presión
        ax_presion.plot(tiempos, datos_presion, marker='o', linestyle='-', color='b')
        ax_presion.axhline(y=umbral_presion, color='r', linestyle='--', label=f'Umbral Presión ({umbral_presion})')
        ax_presion.set_title('Presión')
        ax_presion.set_xlabel('Tiempo (cada 3 segundos)')
        ax_presion.set_ylabel('Presión')
        ax_presion.legend()

        # Actualizar datos en los gráficos de temperatura
        ax_temperatura.plot(tiempos, datos_temperatura, marker='o', linestyle='-', color='g')
        ax_temperatura.axhline(y=umbral_temperatura, color='r', linestyle='--', label=f'Umbral Temperatura ({umbral_temperatura})')
        ax_temperatura.set_title('Temperatura')
        ax_temperatura.set_xlabel('Tiempo (cada 3 segundos)')
        ax_temperatura.set_ylabel('Temperatura')
        ax_temperatura.legend()

        # Actualizar datos en los gráficos de vibración
        ax_vibracion.plot(tiempos, datos_vibracion, marker='o', linestyle='-', color='m')
        ax_vibracion.axhline(y=umbral_vibracion, color='r', linestyle='--', label=f'Umbral Vibración ({umbral_vibracion})')
        ax_vibracion.set_title('Vibración')
        ax_vibracion.set_xlabel('Tiempo (cada 3 segundos)')
        ax_vibracion.set_ylabel('Vibración')
        ax_vibracion.legend()

        # Mostrar los gráficos en los contenedores de Streamlit si no se ha detenido la visualización
        if mostrar_graficos:
            with grafico_presion:
                st.pyplot(fig_presion)
            with grafico_temperatura:
                st.pyplot(fig_temperatura)
            with grafico_vibracion:
                st.pyplot(fig_vibracion)

        # Mostrar el DataFrame en un contenedor de Streamlit
        with tabla_datos:
            # Aplicar estilos condicionales al DataFrame
            def estilo_presion(valor):
                if valor > umbral_presion:
                    return 'background-color: red'
                else:
                    return ''

            def estilo_temperatura(valor):
                if valor > umbral_temperatura:
                    return 'background-color: yellow'
                else:
                    return ''

            def estilo_vibracion(valor):
                if valor > umbral_vibracion:
                    return 'background-color: blue'
                else:
                    return ''

            styled_df = df.style.applymap(estilo_presion, subset=pd.IndexSlice[:, ['Presión']])
            styled_df = styled_df.applymap(estilo_temperatura, subset=pd.IndexSlice[:, ['Temperatura']])
            styled_df = styled_df.applymap(estilo_vibracion, subset=pd.IndexSlice[:, ['Vibración']])

            st.dataframe(styled_df)

        # Esperar 3 segundos antes de la próxima actualización
        time.sleep(3)

    # Mostrar el DataFrame con los datos actuales
    st.write("Se detuvo la actualización de los gráficos")
    st.dataframe(df.copy())
else:
    st.write("El tiempo de monitoreo es cero. No se generaron datos.")
    
    
    
# Créditos del creador
st.sidebar.markdown("---")
st.sidebar.text("Creado por:")
st.sidebar.markdown("<span style='color: black;'>Javier Horacio Pérez Ricárdez</span>", unsafe_allow_html=True)    
    
