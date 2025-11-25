#%%
# Importando bibliotecas #
import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_folium import st_folium
from visuals.mapa import display_mapa
from core.header import dict_candidato
from core.dados_pt import dados_pt
from core.dados_voto import dados_votocao
from core.carregar import load_cand, load_localvoto, load_map, load_vtpart
#%%
df_cand = load_cand()
df_votos = load_localvoto()
df_map = load_map()
df_partidos = load_vtpart()

with st.sidebar:
    st.title("Resultado Eleições 2024 - Recife")
    candidato = st.selectbox("Candidato (a)",df_cand["nome_urna"].sort_values().unique())
    RPA = st.selectbox("RPA",["TODOS","RPA1","RPA2","RPA3","RPA4","RPA5","RPA6"])

df_vt_loc = df_votos.copy()
df_candidato = df_cand.copy()
df_vt_ptc = df_map.copy()


df_vt_loc = df_vt_loc[df_vt_loc['nome_candidato'] == candidato]
df_candidato = df_candidato[df_candidato["nome_urna"] == candidato]
df_map = df_map[df_map['nome_candidato']== candidato]

if RPA == "TODOS":
    pass
else:
    df_vt_loc = df_votos[df_votos["RPA"] == RPA]
    df_map = df_map[df_map["RPA"] == RPA]
    df_vt_ptc = df_vt_ptc[df_vt_ptc["RPA"] == RPA]
    
    
# FICHA DO CANDIDATO
# Criando a função para obtenção dos dados
header = dict_candidato(df_candidato)
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
    <tr><td>Número de votos</td><td>{header["VOTOS"]}</td></tr>
    <tr><td>Partido</td><td>{header["PARTIDO"]}</td></tr>
    <tr><td>Idade</td><td>{header["IDADE"]} anos</td></tr>
    <tr><td>Gênero</td><td>{header["GÊNERO"]}</td></tr>
    <tr><td>Raça</td><td>{header["RAÇA"]}</td></tr>
    <tr><td>Eleito?</td><td>{header["RESULTADO"]}</td></tr>
</table>
""",
    unsafe_allow_html=True,
)

# MAPA DE VOTAÇÃO
mapa = display_mapa(df_map)
st.markdown(f"### :round_pushpin: **Mapa de votação {candidato}**")
st_folium(mapa, width=800, height=700)

# Dados de votação
infovoto = dados_votocao(df_map)

infopartido = dados_pt(df_partidos, df_candidato)

st.markdown("### :ballot_box_with_ballot: **Dados eleitorais & Partidários**")
#Definindo estrutura de exposição
col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.metric(
            label = "Total de votos",
            value = infovoto["Total de votos"]
        )
    with st.container(border=True):    
        st.metric(
            label = "% votos em relação à chapa",
            value = infopartido["Percentual votos"]        
        )

with col2:
    with st.container(border=True):
        st.metric(
            label = "Mediana dos votos",
            value = infovoto["Mediana"],
       )
    with st.container(border=True):
        st.metric(
            label = "Total votos da chapa",
            value = infopartido["Votos totais da chapa"]
        )
        

st.markdown(":keycap_star: Nesta análise foram considerados apenas os votos nominais para vereador.")

# GRÁFICOS

st.markdown("""\n""")
st.markdown("### :bar_chart: **Gráficos**")

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
plot_votos_candidatos = graph_candidatos(df_vt_ptc)
st.plotly_chart(plot_votos_candidatos)

col1, col2 = st.columns(2)

plot_votos_candidatos = graph_candidatos(df_candidato)
plot_bairros = graph_bairros(df)
with col1:
    st.plotly_chart(plot_votos_candidatos)

    # st.plotly_chart(plot_bairros)


plot_votos_chapa = graph_candidatos_chapa(df)
plot_locais = graph_locais(df)
with col2:
    st.plotly_chart(plot_votos_chapa)

    st.plotly_chart(plot_locais)