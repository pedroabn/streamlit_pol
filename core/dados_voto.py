def dados_votocao(df):
    #Organizando planilha de dados
    df = df.groupby(['local','EBAIRRNOMEOF'],as_index=False)['votos'].sum()
    
    #Separando dados
    total_votos = df["votos"].sum()
    mediana_votos = df["votos"].median()
    locais_votacao = len((df["local"].unique()).tolist())

    dicionario = {
        "Total de votos":total_votos,
        "Mediana": mediana_votos,
        "N Locais de votação":locais_votacao
    }

    return dicionario