def dados_pt(df, df_candidato):
    # Minerando dados
    sigla_partido = df_candidato["sigla_partido"].iloc[0]
    df_partido = df[df["sigla_partido"] == sigla_partido]

    # Separando dados
    perct_votos = f"{(df_candidato["votos"].sum()/df_partido["votos"].sum())*100 :.1f} %"
    votos_totais_chapa = df_partido["votos"].sum()

    dicionario= {
        "Percentual votos":perct_votos,
        "Votos totais da chapa": votos_totais_chapa
    }

    return dicionario