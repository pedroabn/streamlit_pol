import pandas as pd
import plotly.express as px
from app import candidato
# Definindo funções
def graph_candidatos(df):
    # Organizando dados
    df = df.groupby(["nome_candidato","sigla_partido"],as_index=False)['votos'].sum()
    df = df.sort_values(by='votos', ascending=False)
    df = df.head(10)
    #Definindo cores
    cores_partidos = {
    "MDB": "blue",
    "NOVO": "orange",
    "PSD": "cyan",
    "PDT": "pink",
    "PODE": "coral",
    "REPUBLICANOS": "gold",
    "CIDADANIA": "brown",
    'MOBILIZA':'salmon',
    "PL": "darkgreen",
    "PV": "lime",
    "PP": "teal",
    "PRD": "green",
    "SOLIDARIEDADE": "olive",
    "PRTB": "navy",
    "UP": "maroon",
    "PT": "red",
    "REDE": "indigo",
    "PSOL": "purple",
    "AGIR": "skyblue",
    "PSDB": "cornflowerblue",
    "PSB": "yellow",
    "UNIÃO": "darkblue",
    "AVANTE": "darkred",
    "PSTU": "darkorange",
    "PC do B": "darkviolet"
    }

    # Organizando o Plot
    fig = px.bar(df, x='votos', y='nome_candidato', orientation = 'h',
    hover_data="sigla_partido",title=f"Top 10 mais votados", labels ={"nome_candidato":"",
    "votos":"Quantidade de votos"})

    fig.update_traces(marker_color=[cores_partidos[p] for p in df['sigla_partido']])

    return fig


def graph_candidatos_chapa(df):
    # Organizando dados
    sigla_partido = df_candidato["SG_PARTIDO"].values[0]
    df = df[df["SG_PARTIDO"] == sigla_partido]
    df = df.groupby(["NM_URNA_CANDIDATO","DS_GENERO"],as_index=False)['QT_VOTOS'].sum()
    df = df.sort_values(by='QT_VOTOS', ascending=False)
    df = df.head(10)

    # Definindo as cores
    cores_genero = {"MASCULINO":"blue","FEMININO":"pink"}

    # Organizando plot
    fig = px.bar(df, x='QT_VOTOS', y='NM_URNA_CANDIDATO', orientation = 'h',
    hover_data="DS_GENERO",title=f"Top 10 mais votados do {sigla_partido}",
     labels ={"NM_URNA_CANDIDATO":"", "QT_VOTOS":"Quantidade de votos"})

    fig.update_traces(marker_color=[cores_genero[p] for p in df['DS_GENERO']])

    return fig

def graph_bairros(df):
    # Organizando dados
    df = df.groupby(["RPA","EBAIRRNOMEOF"],as_index=False)['votos'].sum()
    df = df.sort_values(by='votos', ascending=False)
    df = df.head(10)

    # Definindo as cores
    cores_itens = {
    "RPA1": "#1f77b4",  # Azul
    "RPA2": "#ff7f0e",  # Laranja
    "RPA3": "#2ca02c",  # Verde
    "RPA4": "#d62728",  # Vermelho
    "RPA5": "#9467bd",  # Roxo
    "RPA6": "#8c564b"}  # Marrom    
    # Organizando plot
    fig = px.bar(df, x='QT_VOTOS', y='BAIRRO', orientation = 'h',
    hover_data="DISTRITO_ADM",title=f"Top 10 bairros {candidato}",
     labels ={"BAIRRO":"", "QT_VOTOS":"Quantidade de votos"})

    fig.update_traces(marker_color=[cores_itens[p] for p in df['DISTRITO_ADM']])

    return fig

def graph_locais(df):
    # Organizando dados
    df = df.groupby(["NM_LOCAL_VOTACAO","BAIRRO","DISTRITO_ADM"],as_index=False)['QT_VOTOS'].sum()
    df = df.sort_values(by='QT_VOTOS', ascending=False)
    df = df.head(10)

    # Definindo as cores
    cores_itens = {
    "DABEL": "#1f77b4",  # Azul
    "DABEN": "#ff7f0e",  # Laranja
    "DAENT": "#2ca02c",  # Verde
    "DAGUA": "#d62728",  # Vermelho
    "DAICO": "#9467bd",  # Roxo
    "DAMOS": "#8c564b",  # Marrom
    "DAOUT": "#e377c2",  # Rosa
    "DASAC": "#7f7f7f"   # Cinza
    }

    # Organizando plots
    fig = px.bar(df, x='QT_VOTOS', y='NM_LOCAL_VOTACAO', orientation = 'h',
    hover_data=["BAIRRO","DISTRITO_ADM"],title=f"Top 10 locais de votação {candidato}",
     labels ={"NM_LOCAL_VOTACAO":"", "QT_VOTOS":"Votos"})

    fig.update_traces(marker_color=[cores_itens[p] for p in df['DISTRITO_ADM']])

    return fig
