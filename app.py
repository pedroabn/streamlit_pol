#%%
# Importando bibliotecas #
import streamlit as st
import pandas as pd
import plotly.express as px
from core.carregar import load_cand, load_localvoto
#%%
df_cand = load_cand()
df_votos = load_localvoto()

with st.sidebar:
    st.title("Resultado Eleições 2024 - Recife")
    candidato = st.selectbox("Candidato (a)",df_cand["nome_urna"].sort_values().unique())
    RPA = st.selectbox("RPA",["TODOS","RPA1","RPA2","RPA3","RPA4","RPA5","RPA6"])

if RPA == "TODOS":
    pass
else:
    df_votos = df_votos[df_votos["RPA"] == RPA]

df_vt_loc = df_votos[df_votos['nome_candidato'] == candidato]
df_candidato = df_cand[df_cand["nome_urna"] == candidato]

# FICHA DO CANDIDATO
# Criando a função para obtenção dos dados
def dict_candidato(df,df_voto):
    nome = df['nome_urna'].iloc[0]
    genero = str(df['genero'].iloc[0])
    sigla_partido = df['sigla_partido'].iloc[0]
    idade = df['idade'].iloc[0]
    raca = df['raca'].iloc[0]
    resultado = df['Resultado'].iloc[0]
    votos = df_voto['votos_recebidos'].sum()

    dicionario = {
        "NOME":nome,
        "GÊNERO": genero,
        "PARTIDO":sigla_partido,
        "IDADE":idade,
        'RAÇA':raca,
        "RESULTADO":resultado,
        "VOTOS": votos
    }

    return dicionario

dicionario = dict_candidato(df_candidato,df_vt_loc)
## Escrevendo a ficha

st.markdown(
    f"""
<style>
.table-full {{
    width: 100%;
    border-collapse: collapse;
}}
.table-full th, .table-full td {{
    border: 0.5px solid #ddd;
    padding: 8px;
}}
.table-full th {{
    font-weight: bold;
    text-align: center;
}}
.table-full td:nth-child(2) {{
    text-align: center;
}}
</style>

<table class="table-full">
    <tr><th>Métrica</th><th>Valor</th></tr>
    <tr><td>Número de votos</td><td>{dicionario["VOTOS"]}</td></tr>
    <tr><td>Partido</td><td>{dicionario["PARTIDO"]}</td></tr>
    <tr><td>Idade</td><td>{dicionario["IDADE"]} anos</td></tr>
    <tr><td>Gênero</td><td>{dicionario["GÊNERO"]}</td></tr>
    <tr><td>Raça</td><td>{dicionario["RAÇA"]}</td></tr>
    <tr><td>Eleito?</td><td>{dicionario["RESULTADO"]}</td></tr>
</table>
""",
    unsafe_allow_html=True,
)

# MAPA DE VOTAÇÃO
def display_mapa(df):
    # Limpando o Dataframe
    df_agrupado = df.groupby(['local','EBAIRRNOMEOF', 'latitude', 'longitude'],
    as_index=False)['QT_VOTOS'].sum()
    df_agrupado = df_agrupado.sort_values(by='QT_VOTOS', ascending=False)

    # Construindo o mapa
    fig = px.scatter_mapbox(df_agrupado, lat = 'y', lon='x',
    hover_data=['NM_LOCAL_VOTACAO','BAIRRO'],
    zoom=9, color= 'QT_VOTOS',size='QT_VOTOS',
    color_continuous_scale='RdBu_r')
    fig.update_layout(mapbox_style = 'open-street-map')

    return fig

mapa = display_mapa(df_candidato)
st.markdown(f"### :round_pushpin: **Mapa de votação {candidato}**")
st.plotly_chart(mapa)

# BIG NUMBERS ELEITORAIS
def display_big_numbers_cand(df):
    #Organizando planilha de dados
    df = df.groupby(['NM_LOCAL_VOTACAO','BAIRRO'],as_index=False)['QT_VOTOS'].sum()
    
    #Separando dados
    total_votos = df["QT_VOTOS"].sum()
    mediana_votos = df["QT_VOTOS"].median()
    locais_votacao = len((df["NM_LOCAL_VOTACAO"].unique()).tolist())

    dicionario2 = {
        "Total de votos":total_votos,
        "Mediana": mediana_votos,
        "N Locais de votação":locais_votacao
    }

    return dicionario2



#Retornando o dicionário dados candidato
dicionario2 = display_big_numbers_cand(df_candidato)

# Definindo função dados eleitorais
def display_dados_eleitorais(df):
    # Minerando dados
    sigla_partido = df_candidato["SG_PARTIDO"].values[0]
    df_partido = df[df["SG_PARTIDO"] == sigla_partido]
    df_partido = df_partido.groupby(['NM_URNA_CANDIDATO','NR_CANDIDATO','DS_SIT_TOT_TURNO'
    ],as_index=False)['QT_VOTOS'].sum()

    # Separando dados
    perct_votos = f"{(dicionario2["Total de votos"]/df_partido["QT_VOTOS"].sum())*100 :.1f} %"
    numero_cadeiras = df_partido["DS_SIT_TOT_TURNO"].isin(["ELEITO POR QP",
    "ELEITO POR MÉDIA"]).sum()
    votos_totais_chapa = df_partido["QT_VOTOS"].sum()

    dicionario3 = {
        "Percentual votos":perct_votos,
        "Quantidade de cadeiras": numero_cadeiras,
        "Votos totais da chapa": votos_totais_chapa
    }

    return dicionario3

dicionario3 = display_dados_eleitorais(df)

st.markdown("### :ballot_box_with_ballot: **Dados eleitorais & Partidários**")
#Definindo estrutura de exposição
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label = "Total de votos",
        value = dicionario2["Total de votos"],
        border = True
    )
    st.metric(
        label = "% votos em relação à chapa",
        value = dicionario3["Percentual votos"],
        border = True
    )

with col2:
    st.metric(
        label = "Mediana dos votos",
        value = dicionario2["Mediana"],
        border = True
    )
    st.metric(
        label = "Quantidade de cadeiras",
        value = dicionario3["Quantidade de cadeiras"],
        border = True
    )

with col3:
    st.metric(
        label = "Locais de votação atendidos",
        value = dicionario2["N Locais de votação"],
        border = True
    )
    st.metric(
        label = "Total votos da chapa",
        value = dicionario3["Votos totais da chapa"],
        border = True
    )

st.markdown(":keycap_star: Nesta análise foram considerados apenas os votos nominais para vereador.")

# GRÁFICOS

st.markdown("""\n""")
st.markdown("### :bar_chart: **Gráficos**")

# Definindo funções
def graph_candidatos(df):
    # Organizando dados
    df = df.groupby(["NM_URNA_CANDIDATO","SG_PARTIDO"],as_index=False)['QT_VOTOS'].sum()
    df = df.sort_values(by='QT_VOTOS', ascending=False)
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
    "PL": "goldenrod",
    "PV": "lime",
    "PP": "teal",
    "PRD": "green",
    "DC": "olive",
    "PRTB": "navy",
    "UP": "maroon",
    "PT": "red",
    "REDE": "indigo",
    "PSOL": "purple",
    "AGIR": "skyblue",
    "PSDB": "darkgreen",
    "PSB": "salmon",
    "UNIÃO": "darkblue",
    "AVANTE": "darkred",
    "PSTU": "darkorange",
    "PC do B": "darkviolet"
    }
    
    # Organizando o Plot
    fig = px.bar(df, x='QT_VOTOS', y='NM_URNA_CANDIDATO', orientation = 'h',
    hover_data="SG_PARTIDO",title=f"Top 10 mais votados", labels ={"NM_URNA_CANDIDATO":"",
    "QT_VOTOS":"Quantidade de votos"})

    fig.update_traces(marker_color=[cores_partidos[p] for p in df['SG_PARTIDO']])

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
    df = df.groupby(["DISTRITO_ADM","BAIRRO"],as_index=False)['QT_VOTOS'].sum()
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


# Plotando gráficos
col1, col2 = st.columns(2)

plot_votos_candidatos = graph_candidatos(df)
plot_bairros = graph_bairros(df_candidato)
with col1:
    st.plotly_chart(plot_votos_candidatos)

    st.plotly_chart(plot_bairros)


plot_votos_chapa = graph_candidatos_chapa(df)
plot_locais = graph_locais(df_candidato)
with col2:
    st.plotly_chart(plot_votos_chapa)

    st.plotly_chart(plot_locais)