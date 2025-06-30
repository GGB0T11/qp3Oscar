from os import makedirs

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder, StandardScaler

# Criando o diretório para salvar as imagens
makedirs("imagens", exist_ok=True)

# Carregando o dataset
df = pd.read_csv("https://raw.githubusercontent.com/GGB0T11/qp3Oscar/refs/heads/main/world_ampas_oscar_winner_demographics.csv")

# Calculando a idade na premiação
df["age"] = df["year_edition"] - df["birth_year"]

# Criando década
df["decade"] = (df["year_edition"] // 10) * 10

# Preenchendo dados faltantes
df.fillna("Desconhecido", inplace=True)

# Codificando variáveis categóricas
le_race = LabelEncoder()
le_religion = LabelEncoder()
le_orientation = LabelEncoder()

df["race"] = le_race.fit_transform(df["race_ethnicity"])
df["religion"] = le_religion.fit_transform(df["religion"])
df["orientation"] = le_orientation.fit_transform(df["sexual_orientation"])

# Selecionando variáveis para clustering
features = ["age", "race", "religion", "orientation"]
X = df[features]

# Padronizando os dados
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Aplicando K-Means
kmeans = KMeans(n_clusters=4, random_state=42)
df["cluster"] = kmeans.fit_predict(X_scaled)

# Gráfico de dispersão idade x raça, colorido por cluster
plt.figure(figsize=(10, 6))
sns.scatterplot(x="age", y="race", hue="cluster", data=df, palette="Set2")
plt.title("Agrupamento por Idade e Raça")
plt.savefig("imagens/kmeans_idade_raca.png")
plt.show()

# Composição por cluster
print("\n-> Composição por Cluster")
print(df.groupby("cluster")[["age", "race", "religion", "orientation"]].mean())

# Frequência de cada grupo por década
pivot = df.pivot_table(index="decade", columns="cluster", values="name", aggfunc="count")
pivot.plot(kind="bar", stacked=True, figsize=(12, 6), colormap="tab20")
plt.title("Distribuição dos Clusters por Década")
plt.ylabel("Número de vencedores")
plt.xlabel("Década")
plt.tight_layout()
plt.savefig("imagens/kmeans_por_decada.png")
plt.show()

# Análize de perfis dos clusters
for c in sorted(df["cluster"].unique()):
    print(f"\n-> Cluster {c}")
    grupo = df[df["cluster"] == c]
    print("Tamanho:", len(grupo))
    print("Raças mais comuns:\n", grupo["race_ethnicity"].value_counts().head(3))
    print("Religiões mais comuns:\n", grupo["religion"].value_counts().head(3))
    print("Orientações mais comuns:\n", grupo["sexual_orientation"].value_counts().head(3))
    print("Categorias mais premiadas:\n", grupo["category"].value_counts().head(3))
