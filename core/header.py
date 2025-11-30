def dict_candidato(df):
    nome = df['nome_urna'].iloc[0]
    genero = str(df['genero'].iloc[0])
    sigla_partido = df['sigla_partido'].iloc[0]
    idade = df['idade'].iloc[0]
    raca = df['raca'].iloc[0]
    resultado = df['Resultado'].iloc[0]
    votos = df['votos'].sum()

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
