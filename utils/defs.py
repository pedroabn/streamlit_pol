# core/load_data.py
import streamlit as st
import pandas as pd
import geopandas as gpd
from pathlib import Path

DATA_DIR = Path("dados")

@st.cache_data
def load_cad_data(path: str | None = None) -> pd.DataFrame:
    if path is None:
        path = DATA_DIR / "Cadastrados.xlsx"
    df = pd.read_excel(path)
    df['bairro'] = df['bairro'].apply(limpar_acento).str.upper()
    return df.query('bairro in @recife')

@st.cache_data
def load_geo(path: str | None = None) -> gpd.GeoDataFrame:
    if path is None:
        path = DATA_DIR / "Infopbruto.geojson"
    return gpd.read_file(path, engine="pyogrio")
#%%
RPA1 = ['RECIFE', 'BOA VISTA', 'CABANGA', 'COELHOS', 'ILHA DO LEITE', "JOANA BEZERRA", 'PAISSANDU', 'SANTO AMARO', 'SANTO ANTÔNIO', 'SÃO JOSÉ', 'SOLEDADE']
RPA2 = ['ÁGUA FRIA', 'ALTO SANTA TEREZINHA', 'ARRUDA', 'BEBERIBE', 'BOMBA DO HEMETÉRIO', 'CAJUEIRO', 'CAMPINA DO BARRETO', 'CAMPO GRANDE', 'DOIS UNIDOS', 'ENCRUZILHADA', 'FUNDÃO', 'HIPÓDROMO', 'LINHA DO TIRO', 'PEIXINHOS', 'PONTO DE PARADA', 'PORTO DA MADEIRA', 'ROSARINHO']
RPA3 = ['AFLITOS', 'ALTO DO MANDU', 'ALTO JOSÉ BONIFÁCIO', 'ALTO JOSÉ DO PINHO', 'APIPUCOS', 'BREJO DA GUABIRABA', 'BREJO DE BEBERIBE',' CASA AMARELA', 'CASA FORTE', 'CÓRREGO DO JENIPAPO', 'DERBY', 'DOIS IRMÃOS', 'ESPINHEIRO', 'GRAÇAS', 'GUABIRABA', 'JAQUEIRA', 'MACAXEIRA', 'MANGABEIRA', 'MONTEIRO', 'MORRO DA CONCEIÇÃO', 'NOVA DESCOBERTA', 'PARNAMIRIM', 'PASSARINHO', 'PAU-FERRO', 'POÇO', 'SANTANA',' SÍTIO DOS PINTOS', 'TAMARINEIRA', 'VASCO DA GAMA']
RPA4 = ['CAXANGÁ',' CIDADE UNIVERSITÁRIA', 'CORDEIRO',' ENGENHO DO MEIO', 'ILHA DO RETIRO', 'IPUTINGA', 'MADALENA', 'PRADO', 'TORRÕES', 'TORRE', 'VÁRZEA', 'ZUMBI']
RPA5 = ['AFOGADOS', 'AREIAS', 'BARRO', 'BONGI', 'CAÇOTE', 'COQUEIRAL', 'CURADO', 'ESTÂNCIA',' JARDIM SÃO PAULO', 'JIQUIÁ', 'MANGUEIRA', 'MUSTARDINHA', 'SAN MARTIN', 'SANCHO', 'TEJIPIÓ', 'TOTÓ']
RPA6 = ['BOA VIAGEM', "BRASÍLIA TEIMOSA", "COHAB", 'IBURA', "IMBIRIBEIRA", 'IPSEP', 'JORDÃO', "PINA"]



@st.cache_data
def load_data(df):
    df = pd.read_excel(df)
    df = df.fillna(0)
    df["RPA"] = np.select(
        [   df["EBAIRRNOMEOF"].isin(RPA1),
            df["EBAIRRNOMEOF"].isin(RPA2),
            df["EBAIRRNOMEOF"].isin(RPA3),
            df["EBAIRRNOMEOF"].isin(RPA4),
            df["EBAIRRNOMEOF"].isin(RPA5),
            df["EBAIRRNOMEOF"].isin(RPA6)],
            [   'RPA1',
                'RPA2',
                'RPA3',
                "RPA4",
                'RPA5',
                "RPA6"],
                default="Fora")
    return df


@st.cache_data
def local(json):
  df = pd.read_json(json)