# Análise de Sobrevivência no Titanic

Análise exploratória do clássico dataset do Titanic, buscando entender **quais fatores mais influenciaram a chance de sobrevivência** dos passageiros: classe social, sexo, idade e tamanho da família a bordo.

## Sobre os dados

Dataset público com 891 passageiros do Titanic (nome, classe, sexo, idade, tarifa paga, porto de embarque, se sobreviveu, etc.). Fonte: dataset clássico usado em cursos e competições de ciência de dados (disponível via [Kaggle](https://www.kaggle.com/c/titanic) e biblioteca `seaborn`).

## O que foi feito

- Limpeza dos dados: preenchimento de idades ausentes com a mediana, remoção da coluna `deck` (muitos valores nulos) e das poucas linhas sem porto de embarque
- Cálculo da taxa geral de sobrevivência
- Três análises visuais cruzando sobrevivência com classe, sexo, idade e tamanho da família

## Principais descobertas

**Taxa geral de sobrevivência: 38,2%**

1. **Classe e sexo importaram muito.** Mulheres da 1ª classe tiveram 96,7% de chance de sobreviver, contra apenas 13,5% dos homens da 3ª classe — a maior diferença do dataset.

2. **Ser mulher foi o fator isolado mais forte**: 74% das mulheres sobreviveram, contra 18,9% dos homens — reflete a prioridade dada a mulheres e crianças na evacuação.

3. **Família em tamanho moderado ajudou.** Passageiros com 1 a 3 familiares a bordo tiveram taxas de sobrevivência mais altas (55% a 72%) do que quem estava sozinho (30%) ou em famílias muito grandes (acima de 4 pessoas, onde a taxa cai bastante).

## Gráficos

| Sobrevivência por classe e sexo | Distribuição de idade | Sobrevivência por família |
|---|---|---|
| ![classe e sexo](images/sobrevivencia_classe_sexo.png) | ![idade](images/distribuicao_idade.png) | ![família](images/sobrevivencia_familia.png) |

## Como rodar

```bash
pip install pandas matplotlib seaborn
python analise.py
```

Os gráficos são gerados na pasta `images/`.

## Tecnologias usadas

- Python
- pandas (limpeza e manipulação dos dados)
- matplotlib / seaborn (visualização)
