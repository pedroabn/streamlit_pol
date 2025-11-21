#%%
import pandas as pd
import numpy as np
import basedosdados as bd
billing_id = 'dados-eleicao-470222'
#%% Info candidato
candquery = """
    SELECT
        ano,
        data_eleicao,
        id_municipio,
        nome_urna,
        sigla_partido,
        idade,
        genero,
        raca,
    FROM `basedosdados.br_tse_eleicoes.candidatos`
    WHERE ano = 2024 AND id_municipio = '2611606' and cargo = 'vereador'
    ORDER BY nome_urna
"""
cadidatos = bd.read_sql(query = candquery, billing_project_id = billing_id)
candidatos = pd.DataFrame(cadidatos)
#%% Votação por setor
vtsquery = """
SELECT 
  c.nome_urna as Nome_candidato,
  r.secao as Secao,
  SUM(r.votos) as Votos_recebidos,
  r.zona as Zona
FROM
  basedosdados.br_tse_eleicoes.resultados_candidato_secao as r
LEFT JOIN
  basedosdados.br_tse_eleicoes.local_secao as l
  ON CAST(r.secao as string) = CAST(l.secao as string)
LEFT JOIN
  basedosdados.br_tse_eleicoes.candidatos as c
  ON (CAST(r.sequencial_candidato as string) = cast(c.sequencial as string) 
      AND CAST(r.numero_candidato as string) = CAST(c.numero as string))
WHERE
  r.ano = 2024 r.id_municipio = "2611606" and r.cargo = "vereador"
GROUP BY
  Nome_candidato,
  Secao,
  Zona;
"""
votosecao = bd.read_sql(query = vtsquery, billing_project_id = billing_id)
votosecao = pd.DataFrame(votosecao)