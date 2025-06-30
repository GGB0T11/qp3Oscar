from os import makedirs

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier, plot_tree

# Criando o diretório para salvar as imagens
makedirs("imagens", exist_ok=True)

# Carregando o csv
df = pd.read_csv(
    "https://raw.githubusercontent.com/GGB0T11/qp3Oscar/refs/heads/main/world_ampas_oscar_winner_demographics.csv"
)

# calculando idade na premiação
df["age"] = df["year_edition"] - df["birth_year"]

# Preenchedo valores ausentes
df.fillna("Desconhecido", inplace=True)

# Codificando variáveis categóricas
le_race = LabelEncoder()
le_religion = LabelEncoder()
le_orientation = LabelEncoder()
le_category = LabelEncoder()

df["race"] = le_race.fit_transform(df["race_ethnicity"])
df["religion"] = le_religion.fit_transform(df["religion"])
df["orientation"] = le_orientation.fit_transform(df["sexual_orientation"])
df["category_encoded"] = le_category.fit_transform(df["category"])

# Iniciando Treinamento da Árvore de Decisão
features = ["age", "race", "religion", "orientation"]
X = df[features]
y = df["category_encoded"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

clf = DecisionTreeClassifier(max_depth=5, random_state=42)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)

# Avaliação do modelo
print("\n-> Relatório de Classificação")
print(classification_report(y_test, y_pred, target_names=le_category.classes_))
print(f"Acurácia: {accuracy_score(y_test, y_pred):.2f}")

# Importância das Features (para responder a pergunta 2)
importances = clf.feature_importances_
print("\n-> Importância das Variáveis")
for feature, importance in zip(features, importances):
    print(f"{feature}: {importance:.2f}")

# Visualização da Árvore
plt.figure(figsize=(20, 10))
plot_tree(clf, feature_names=features, class_names=le_category.classes_, filled=True, rounded=True, fontsize=10)
plt.title("Árvore de Decisão - Previsão da Categoria com Perfil Demográfico")
plt.tight_layout()
plt.savefig("imagens/arvore_categoria_idade.png")
plt.show()
