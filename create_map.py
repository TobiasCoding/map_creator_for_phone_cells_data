import pandas as pd
import folium
from folium.plugins import MarkerCluster
from IPython.display import display

# Leer el archivo de Excel creado anteriormente
impactos = pd.read_excel('Impactos_con_celdas.xlsx')

# Convertir las columnas de latitud y longitud a numéricas, forzando errores a NaN
impactos['Latitud'] = pd.to_numeric(impactos['Latitud'], errors='coerce')
impactos['Longitud'] = pd.to_numeric(impactos['Longitud'], errors='coerce')

# Eliminar filas con valores NaN en las columnas de latitud y longitud
impactos = impactos.dropna(subset=['Latitud', 'Longitud'])

# Crear un mapa centrado en la primera coordenada válida
if not impactos.empty:
    m = folium.Map(location=[impactos['Latitud'].mean(), impactos['Longitud'].mean()], zoom_start=10)

    # Crear un cluster de marcadores
    marker_cluster = MarkerCluster().add_to(m)

    # Añadir círculos para cada impacto al cluster de marcadores
    for _, row in impactos.iterrows():
        try:
          radio = int(row['Radio'])*1000
          folium.Circle(
              location=[row['Latitud'], row['Longitud']],
              radius=radio,  # Convertir km a metros  / Puede cambiar y llamarse "Radio_Cobertura_en_KM" según ISP
              popup=(
                  f"Fecha: {row['Fecha']}<br>"
                  f"Evento: {row['Evento']}<br>"    # Puede cambiar a segun ISP:    f"Hora: {row['Hora']}<br>"
                  f"Nro. Pagador: {row['Nro. Pagador']}<br>"
                  f"Dirección Evento: {row['Dirección Evento']}<br>"
                  f"Duración: {row['Duración en Seg.']}<br>"
                  f"IMEI: {row['IMEI']}<br>"
                  f"Tipo: {row['Tipo Tráfico']}<br>"
                  f"Estado: {row['Estado']}"
              ),
              color='blue',
              fill=True,
              fill_opacity=0.5
          ).add_to(marker_cluster)
        except:
          pass

    # Crear una lista de coordenadas para la línea cronológica
    coordenadas = list(zip(impactos['Latitud'], impactos['Longitud']))

    # Añadir una línea cronológica
    folium.PolyLine(
        locations=coordenadas,
        color='red',
        weight=2.5,
        opacity=1
    ).add_to(m)

    # Mostrar el mapa en Jupyter Notebook
    display(m)
    m.save("mapa_impactos.html")
else:
    print("No hay datos para mostrar en el mapa.")
