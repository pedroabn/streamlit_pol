#%%
import numpy as np
import pandas as pd
import re
from utils.api_bd import load_votos, load_geo, load_cand
#%%

locais = load_geo()
candidatos = load_cand()
votos = load_votos()
#%%
def get_ze(valor):
    """Explode string de seções em lista de inteiros"""
    if pd.isna(valor): return []
    s = str(valor)
    parts = [p.strip() for p in re.split(r",|;|\n", s) if p.strip()]
    secoes = []
    for p in parts:
        m = re.match(r"^(\d{1,4})\s*(?:-|–|a|até)\s*(\d{1,4})$", p)
        if m:
            a, b = int(m.group(1)), int(m.group(2))
            secoes.extend(range(min(a,b), max(a,b)+1))
        else:
            num = re.sub(r"[^\d]", "", p)
            if num: secoes.append(int(num))
    return secoes

def zona_sec(df):
    df['CD_Local'] = df['CD_Local'].astype(int)
    linhas = []
    for _, r in df.iterrows():
        for s in get_ze(r["secao"]):
            linhas.append({
                "zona": int(r["zona"]),
                "secao": s,
                "CD_Local": int(r["CD_Local"]),
                "local": r["Nome do Local"],
                "endereco": r["Endereço"],
                "EBAIRRNOMEOF": r["Bairro"],
                "latitude": str(r["Latitude"]),
                "longitude": str(r["Longitude"])
            })
    zonas = pd.DataFrame(linhas)
    return zonas

RPA1 = ['RECIFE', 'BOA VISTA', 'CABANGA',
        'COELHOS', 'ILHA DO LEITE', "JOANA BEZERRA", 'PAISSANDU', 'SANTO AMARO', 'SANTO ANTÔNIO', 'SÃO JOSÉ', 'SOLEDADE']
RPA2 = ['ÁGUA FRIA', 'ALTO SANTA TEREZINHA',
        'ARRUDA', 'BEBERIBE', 'BOMBA DO HEMETÉRIO', 'CAJUEIRO', 'CAMPINA DO BARRETO', 'CAMPO GRANDE', 'DOIS UNIDOS', 'ENCRUZILHADA', 'FUNDÃO', 'HIPÓDROMO', 'LINHA DO TIRO', 'PEIXINHOS', 'PONTO DE PARADA', 'PORTO DA MADEIRA', 'ROSARINHO']
RPA3 = ['AFLITOS', 'ALTO DO MANDU',
        'ALTO JOSÉ BONIFÁCIO', 'ALTO JOSÉ DO PINHO', 'APIPUCOS', 'BREJO DA GUABIRABA', 'BREJO DE BEBERIBE',' CASA AMARELA', 'CASA FORTE', 'CÓRREGO DO JENIPAPO', 'DERBY', 'DOIS IRMÃOS', 'ESPINHEIRO', 'GRAÇAS', 'GUABIRABA', 'JAQUEIRA', 'MACAXEIRA', 'MANGABEIRA', 'MONTEIRO', 'MORRO DA CONCEIÇÃO', 'NOVA DESCOBERTA', 'PARNAMIRIM', 'PASSARINHO', 'PAU-FERRO', 'POÇO', 'SANTANA',' SÍTIO DOS PINTOS', 'TAMARINEIRA', 'VASCO DA GAMA']
RPA4 = ['CAXANGÁ',' CIDADE UNIVERSITÁRIA',
        'CORDEIRO',' ENGENHO DO MEIO', 'ILHA DO RETIRO', 'IPUTINGA', 'MADALENA', 'PRADO', 'TORRÕES', 'TORRE', 'VÁRZEA', 'ZUMBI']
RPA5 = ['AFOGADOS', 'AREIAS', 'BARRO',
        'BONGI', 'CAÇOTE', 'COQUEIRAL', 'CURADO', 'ESTÂNCIA',' JARDIM SÃO PAULO', 'JIQUIÁ', 'MANGUEIRA', 'MUSTARDINHA', 'SAN MARTIN', 'SANCHO', 'TEJIPIÓ', 'TOTÓ']
RPA6 = ['BOA VIAGEM', "BRASÍLIA TEIMOSA",
        "COHAB", 'IBURA', "IMBIRIBEIRA", 'IPSEP', 'JORDÃO', "PINA"]

def load_cluster(df):
    df = pd.read_excel(df)
    # Leitura do tse e divisão para cada seção e 
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

#%%
