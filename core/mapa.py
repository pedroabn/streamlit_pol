# visuals/mapa.py
import folium
from folium.plugins import MarkerCluster, MiniMap, GroupedLayerControl
import branca.colormap as cm
import pandas as pd

def display_mapa(df, dfgb):
    recife_coords = [-8.05428, -34.88126]
    m = folium.Map(location=recife_coords, zoom_start=13, tiles="OpenStreetMap")

    MiniMap(toggle_display=True).add_to(m)

    # Cluster geral
    for row in df.itertuples():
        popup = folium.Popup(
            f"Local: {row.local} \n Raça: {row.raca} \n Estilo: {row.area_atuacao}",
            parse_html=True,
            max_width="100",
        )
        folium.Circle(
            location=(row.latitude, row.longitude),
            radius = max(row['QT_VOTOS'] / dfgb['QT_VOTOS'].max() * 15, 3)
            fill_color="green",
            fill_opacity=0.4,
            color="white",
            popup=popup,
        ).add_to(marker_cluster)

    return m
