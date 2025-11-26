# 🗳️ Análise Eleitoral - Recife 2024

Dashboard interativo desenvolvido com Streamlit para visualização e análise dos resultados das eleições municipais de 2024 em Recife/PE, com foco nas eleições para vereador.

## 📊 Funcionalidades

- **Perfil do Candidato**: Visualização de dados individuais incluindo partido, idade, gênero, raça e resultado eleitoral
- **Mapa Interativo**: Visualização geográfica da distribuição de votos por local de votação
- **Análise por RPA**: Filtros por Região Político-Administrativa de Recife
- **Gráficos Comparativos**:
  - Top 10 candidatos mais votados
  - Top 10 candidatos mais votados por partido
  - Top 10 bairros com maior votação
  - Top 10 locais de votação

## 🚀 Tecnologias Utilizadas

- **Streamlit**: Framework principal para interface web
- **Pandas**: Manipulação e análise de dados
- **Plotly Express**: Visualizações gráficas interativas
- **Folium**: Mapas interativos
- **Base dos Dados**: Fonte de dados eleitorais do TSE

## 📁 Estrutura do Projeto

```
streamlit_pol/
├── app.py                      # Aplicação principal
├── core/
│   ├── carregar.py            # Funções de carregamento de dados
│   ├── dados_pt.py            # Processamento de dados partidários
│   ├── dados_voto.py          # Processamento de dados de votação
│   └── header.py              # Dados do cabeçalho do candidato
├── visuals/
│   ├── graficos.py            # Funções para geração de gráficos
│   └── mapa.py                # Visualização de mapas
├── manipulacao/
│   ├── defs.py                # Funções de transformação de dados
│   └── mapping.py             # Mapeamento de RPAs e vencedores
├── dados/                      # Arquivos CSV com dados processados
└── requirements.txt           # Requerimentos de bibliotecas
└── reuntime.txt               # Para rodar algumas bibliotecas, é necessário o python 3.13

```

## 🔧 Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/streamlit_pol.git
cd streamlit_pol
```

2. Crie um ambiente virtual (recomendado):
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

## ▶️ Como Usar

Execute a aplicação com o comando:

```bash
streamlit run app.py
```

A aplicação será aberta automaticamente no navegador em `http://localhost:8501`

### Navegação

1. **Sidebar**: Selecione o candidato e a RPA desejada
2. **Ficha do Candidato**: Visualize métricas principais
3. **Mapa**: Explore a distribuição geográfica dos votos
4. **Métricas Eleitorais**: Analise dados de votação e partidários
5. **Gráficos**: Compare desempenho entre candidatos e regiões

## 📋 Fonte de Dados

Os dados foram extraídos através da API do [Base dos Dados](https://basedosdados.org/), utilizando informações oficiais do TSE (Tribunal Superior Eleitoral) referentes às eleições municipais de 2024.

## 🗺️ Sobre as RPAs

As Regiões Político-Administrativas (RPAs) de Recife são divisões territoriais que agrupam bairros por características socioeconômicas e geográficas:

- **RPA 1**: Centro/Santo Amaro
- **RPA 2**: Norte
- **RPA 3**: Noroeste
- **RPA 4**: Oeste
- **RPA 5**: Sudoeste
- **RPA 6**: Sul

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👤 Autor

**Pedro Neiva**

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.