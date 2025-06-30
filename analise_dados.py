# Código simples para análise de dados
# Basta alterar o nome do arquivo CSV na linha 'arquivo_csv'

import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# Configuração para gráficos mais bonitos
plt.style.use('seaborn-v0_8')
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 12

print("="*60)
print("ANÁLISE EXPLORATÓRIA BÁSICA DE DADOS")
print("="*60)

# ===== PARTE 1: CARREGANDO O DATASET =====
# ALTERE APENAS ESTA LINHA COM O NOME DO SEU ARQUIVO CSV
arquivo_csv = "world_ampas_oscar_winner_demographics.csv"  # <-- MUDE AQUI

# Criando a pasta para salvar os gráficos
pasta_visualizacoes = 'visualizacoes'
if not os.path.exists(pasta_visualizacoes):
    os.makedirs(pasta_visualizacoes)

# Tentando carregar o arquivo com diferentes codificações
try:
    # Tentativa com UTF-8 (padrão)
    df = pd.read_csv(arquivo_csv)
    print(f"\nArquivo '{arquivo_csv}' carregado com sucesso!")
except UnicodeDecodeError:
    try:
        # Tentativa com latin-1 (comum para arquivos brasileiros)
        df = pd.read_csv(arquivo_csv, encoding='latin-1', sep=",")
        print(f"\nArquivo '{arquivo_csv}' carregado com sucesso (codificação latin-1)!")
    except:
        try:
            # Última tentativa
            df = pd.read_csv(arquivo_csv, encoding='ISO-8859-1', sep=",")
            print(f"\nArquivo '{arquivo_csv}' carregado com sucesso (codificação ISO-8859-1)!")
        except Exception as e:
            print(f"\nERRO ao carregar o arquivo: {e}")
            print("Verifique se o nome do arquivo está correto e se ele está na mesma pasta deste script.")
            exit()

# ===== PARTE 2: INFORMAÇÕES BÁSICAS =====
print("\n" + "="*60)
print("INFORMAÇÕES BÁSICAS DO DATASET")
print("="*60)

# Tamanho do dataset
print(f"\nTamanho do dataset: {df.shape[0]} linhas e {df.shape[1]} colunas")

# Primeiras linhas
print("\nPrimeiras 5 linhas do dataset:")
print(df.head())

# Tipos de dados
print("\nTipos de dados de cada coluna:")
print(df.dtypes)

# Valores ausentes
print("\nValores ausentes por coluna:")
valores_ausentes = df.isnull().sum()
if valores_ausentes.sum() > 0:
    print(valores_ausentes[valores_ausentes > 0])
else:
    print("Não há valores ausentes no dataset!")

# ===== PARTE 3: ESTATÍSTICAS DESCRITIVAS =====
print("\n" + "="*60)
print("ESTATÍSTICAS DESCRITIVAS")
print("="*60)

# Identificando colunas numéricas e categóricas
colunas_numericas = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
colunas_categoricas = df.select_dtypes(include=['object', 'category']).columns.tolist()

# Estatísticas para colunas numéricas
if colunas_numericas:
    print("\nEstatísticas para colunas numéricas:")
    estatisticas = df[colunas_numericas].describe().round(2)
    print(estatisticas)
    
    # Salvando as estatísticas em um arquivo CSV
    estatisticas.to_csv(f"{pasta_visualizacoes}/estatisticas_numericas.csv")
    print(f"Estatísticas salvas em {pasta_visualizacoes}/estatisticas_numericas.csv")
else:
    print("\nNão foram encontradas colunas numéricas no dataset.")

# Contagem para colunas categóricas
if colunas_categoricas:
    print("\nContagem das principais categorias:")
    for coluna in colunas_categoricas[:3]:  # Limitando a 3 colunas para não ficar muito grande
        if df[coluna].nunique() < 15:  # Se tiver menos de 15 categorias diferentes
            print(f"\nColuna '{coluna}':")
            print(df[coluna].value_counts().head(10))
        else:
            print(f"\nColuna '{coluna}' tem {df[coluna].nunique()} valores únicos (primeiros 5):")
            print(df[coluna].value_counts().head(5))
else:
    print("\nNão foram encontradas colunas categóricas no dataset.")

# ===== PARTE 4: CRIANDO VISUALIZAÇÕES =====
print("\n" + "="*60)
print("CRIANDO VISUALIZAÇÕES")
print("="*60)
print(f"Todos os gráficos serão salvos na pasta '{pasta_visualizacoes}'")

# 1. Histogramas para variáveis numéricas
if colunas_numericas:
    print("\nCriando histogramas para variáveis numéricas...")
    for coluna in colunas_numericas[:5]:  # Limitando a 5 colunas
        plt.figure(figsize=(10, 6))
        sns.histplot(df[coluna].dropna(), kde=True)
        plt.title(f'Distribuição de {coluna}')
        plt.grid(True, alpha=0.3)
        plt.savefig(f'{pasta_visualizacoes}/histograma_{coluna}.png')
        plt.close()
    print("✓ Histogramas criados com sucesso!")

# 2. Gráficos de barras para variáveis categóricas
if colunas_categoricas:
    print("\nCriando gráficos de barras para variáveis categóricas...")
    for coluna in colunas_categoricas[:3]:  # Limitando a 3 colunas
        if df[coluna].nunique() < 15:  # Se não tiver muitas categorias
            plt.figure(figsize=(12, 6))
            contagem = df[coluna].value_counts().head(10)
            sns.barplot(x=contagem.index, y=contagem.values)
            plt.title(f'Frequência das principais categorias de {coluna}')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig(f'{pasta_visualizacoes}/barras_{coluna}.png')
            plt.close()
    print("✓ Gráficos de barras criados com sucesso!")

# 3. Matriz de correlação (se houver pelo menos 2 variáveis numéricas)
if len(colunas_numericas) >= 2:
    print("\nCriando matriz de correlação...")
    plt.figure(figsize=(12, 10))
    correlation = df[colunas_numericas].corr().round(2)
    sns.heatmap(correlation, annot=True, cmap='coolwarm', linewidths=0.5)
    plt.title('Matriz de Correlação')
    plt.tight_layout()
    plt.savefig(f'{pasta_visualizacoes}/matriz_correlacao.png')
    plt.close()
    
    # Salvando a correlação em um arquivo CSV
    correlation.to_csv(f"{pasta_visualizacoes}/matriz_correlacao.csv")
    print("✓ Matriz de correlação criada com sucesso!")
    
    # Identificando as correlações mais fortes
    print("\nCorrelações mais fortes:")
    correlacoes_ordenadas = []
    
    # Pegando apenas o triângulo superior da matriz para evitar duplicações
    for i in range(len(colunas_numericas)):
        for j in range(i+1, len(colunas_numericas)):
            var1 = colunas_numericas[i]
            var2 = colunas_numericas[j]
            corr = correlation.iloc[i, j]
            correlacoes_ordenadas.append((var1, var2, corr, abs(corr)))
    
    # Ordenando pelo valor absoluto da correlação
    correlacoes_ordenadas.sort(key=lambda x: x[3], reverse=True)
    
    # Mostrando as 5 correlações mais fortes
    for var1, var2, corr, _ in correlacoes_ordenadas[:5]:
        print(f"• {var1} e {var2}: {corr:.2f}")
    
    # 4. Gráfico de dispersão para as duas variáveis mais correlacionadas
    if correlacoes_ordenadas:
        print("\nCriando gráfico de dispersão para as variáveis mais correlacionadas...")
        var1, var2, corr, _ = correlacoes_ordenadas[0]
        
        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=df, x=var1, y=var2)
        plt.title(f'Relação entre {var1} e {var2} (correlação: {corr:.2f})')
        plt.grid(True, alpha=0.3)
        plt.savefig(f'{pasta_visualizacoes}/dispersao_{var1}_vs_{var2}.png')
        plt.close()
        print("✓ Gráfico de dispersão criado com sucesso!")

# 5. Boxplots para variáveis numéricas
if colunas_numericas:
    print("\nCriando boxplots para variáveis numéricas...")
    for coluna in colunas_numericas[:5]:  # Limitando a 5 colunas
        plt.figure(figsize=(10, 6))
        sns.boxplot(y=df[coluna])
        plt.title(f'Boxplot de {coluna}')
        plt.grid(True, alpha=0.3, axis='x')
        plt.tight_layout()
        plt.savefig(f'{pasta_visualizacoes}/boxplot_{coluna}.png')
        plt.close()
    print("✓ Boxplots criados com sucesso!")

# 6. Comparação por grupo (se houver variáveis categóricas e numéricas)
if colunas_categoricas and colunas_numericas:
    # Escolhendo a primeira coluna categórica com menos de 10 categorias
    coluna_cat = None
    for col in colunas_categoricas:
        if df[col].nunique() < 10:
            coluna_cat = col
            break
    
    if coluna_cat:
        print(f"\nCriando gráficos comparativos para grupos de '{coluna_cat}'...")
        for coluna_num in colunas_numericas[:2]:  # Limitando a 2 colunas numéricas
            plt.figure(figsize=(12, 6))
            sns.boxplot(x=coluna_cat, y=coluna_num, data=df)
            plt.title(f'Comparação de {coluna_num} por {coluna_cat}')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig(f'{pasta_visualizacoes}/comparacao_{coluna_num}_por_{coluna_cat}.png')
            plt.close()
        print("✓ Gráficos comparativos criados com sucesso!")

# ===== PARTE 5: RESUMO DA ANÁLISE =====
print("\n" + "="*60)
print("RESUMO DA ANÁLISE")
print("="*60)

print(f"""
Dataset analisado: {arquivo_csv}
Tamanho: {df.shape[0]} linhas x {df.shape[1]} colunas
Colunas numéricas: {len(colunas_numericas)}
Colunas categóricas: {len(colunas_categoricas)}
Valores ausentes: {'Sim' if valores_ausentes.sum() > 0 else 'Não'}

Arquivos gerados:
- Estatísticas numéricas (CSV)
- Histogramas
- Gráficos de barras
- Matriz de correlação
- Gráfico de dispersão
- Boxplots
- Gráficos comparativos

Todos os arquivos foram salvos na pasta '{pasta_visualizacoes}'
""")

print("\n" + "="*60)
print("ANÁLISE CONCLUÍDA!")
print("="*60)
print("Você pode usar estas visualizações no seu relatório do projeto.")
