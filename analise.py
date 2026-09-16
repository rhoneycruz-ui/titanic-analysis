"""
Análise Exploratória - Sobreviventes do Titanic
Autor: Rhoney

Objetivo: entender quais fatores (classe, sexo, idade) mais influenciaram
a chance de sobrevivência dos passageiros do Titanic.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")

# ---------------------------------------------------------
# 1. Carregar e limpar os dados
# ---------------------------------------------------------
df = pd.read_csv("data/titanic.csv")

print("Dimensões originais:", df.shape)
print("\nValores nulos por coluna:")
print(df.isnull().sum())

# Preenche idades nulas com a mediana (evita distorcer a distribuição)
df["age"] = df["age"].fillna(df["age"].median())

# Remove coluna 'deck' (muitos valores nulos, pouco útil aqui)
df = df.drop(columns=["deck"])

# Remove as poucas linhas sem porto de embarque
df = df.dropna(subset=["embarked"])

print("\nDimensões após limpeza:", df.shape)

# ---------------------------------------------------------
# 2. Estatísticas gerais
# ---------------------------------------------------------
taxa_geral = df["survived"].mean() * 100
print(f"\nTaxa geral de sobrevivência: {taxa_geral:.1f}%")

# ---------------------------------------------------------
# 3. Gráfico 1 — Sobrevivência por classe e sexo
# ---------------------------------------------------------
plt.figure(figsize=(8, 5))
sns.barplot(data=df, x="class", y="survived", hue="sex", palette="Set2")
plt.title("Taxa de sobrevivência por classe e sexo")
plt.ylabel("Taxa de sobrevivência")
plt.xlabel("Classe")
plt.ylim(0, 1)
plt.legend(title="Sexo")
plt.tight_layout()
plt.savefig("images/sobrevivencia_classe_sexo.png", dpi=150)
plt.close()

# ---------------------------------------------------------
# 4. Gráfico 2 — Distribuição de idade: sobreviventes x não sobreviventes
# ---------------------------------------------------------
plt.figure(figsize=(8, 5))
sns.histplot(data=df, x="age", hue="survived", multiple="stack",
             bins=30, palette=["#d9534f", "#5cb85c"])
plt.title("Distribuição de idade — sobreviventes x não sobreviventes")
plt.xlabel("Idade")
plt.ylabel("Número de passageiros")
plt.legend(title="Sobreviveu", labels=["Sim", "Não"])
plt.tight_layout()
plt.savefig("images/distribuicao_idade.png", dpi=150)
plt.close()

# ---------------------------------------------------------
# 5. Gráfico 3 — Sobrevivência por tamanho da família a bordo
# ---------------------------------------------------------
df["familia"] = df["sibsp"] + df["parch"]

plt.figure(figsize=(8, 5))
sns.barplot(data=df, x="familia", y="survived", color="#4C72B0")
plt.title("Taxa de sobrevivência por tamanho da família a bordo")
plt.xlabel("Nº de familiares a bordo (irmãos/cônjuge + pais/filhos)")
plt.ylabel("Taxa de sobrevivência")
plt.tight_layout()
plt.savefig("images/sobrevivencia_familia.png", dpi=150)
plt.close()

print("\nGráficos salvos na pasta images/")
