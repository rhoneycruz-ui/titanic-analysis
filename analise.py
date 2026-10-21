"""Análise exploratória da sobrevivência dos passageiros do Titanic."""

import argparse
from collections.abc import Sequence
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


sns.set_theme(style="whitegrid")

CHART_FILENAMES = (
    "sobrevivencia_classe_sexo.png",
    "distribuicao_idade.png",
    "sobrevivencia_familia.png",
)
PROJECT_ROOT = Path(__file__).resolve().parent


def load_data(csv_path: Path | str) -> pd.DataFrame:
    """Carrega o dataset sem alterar os dados originais."""
    return pd.read_csv(csv_path)


def clean_data(raw_data: pd.DataFrame) -> pd.DataFrame:
    """Aplica as regras documentadas de limpeza e cria tamanho da família."""
    cleaned = raw_data.copy()
    cleaned["age"] = cleaned["age"].fillna(cleaned["age"].median())
    cleaned = cleaned.drop(columns=["deck"])
    cleaned = cleaned.dropna(subset=["embarked"]).copy()
    cleaned["familia"] = cleaned["sibsp"] + cleaned["parch"]
    return cleaned


def summarize(raw_data: pd.DataFrame, cleaned_data: pd.DataFrame) -> dict[str, int | float]:
    """Retorna as métricas centrais da análise em formato serializável."""
    return {
        "passageiros_originais": len(raw_data),
        "passageiros_analisados": len(cleaned_data),
        "idades_preenchidas": int(raw_data["age"].isna().sum()),
        "sobreviventes": int(cleaned_data["survived"].sum()),
        "taxa_sobrevivencia": float(cleaned_data["survived"].mean() * 100),
    }


def generate_charts(data: pd.DataFrame, output_dir: Path | str) -> list[Path]:
    """Gera as três visualizações da análise e retorna seus caminhos."""
    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    generated = [destination / name for name in CHART_FILENAMES]

    figure, axis = plt.subplots(figsize=(9, 5.5))
    sns.barplot(
        data=data,
        x="class",
        y="survived",
        hue="sex",
        order=["First", "Second", "Third"],
        hue_order=["female", "male"],
        palette={"female": "#D4A72C", "male": "#355C7D"},
        errorbar=None,
        ax=axis,
    )
    axis.set(
        title="Sobrevivência por classe e sexo",
        xlabel="Classe",
        ylabel="Taxa de sobrevivência",
        ylim=(0, 1),
    )
    axis.set_xticks(axis.get_xticks(), labels=["1ª classe", "2ª classe", "3ª classe"])
    axis.legend(title="Sexo", labels=["Mulheres", "Homens"], frameon=False)
    figure.tight_layout()
    figure.savefig(generated[0], dpi=160, bbox_inches="tight")
    plt.close(figure)

    figure, axis = plt.subplots(figsize=(9, 5.5))
    sns.histplot(
        data=data,
        x="age",
        hue="survived",
        hue_order=[0, 1],
        multiple="stack",
        bins=30,
        palette={0: "#C95C54", 1: "#2A9D8F"},
        ax=axis,
    )
    axis.set(
        title="Distribuição de idade por situação de sobrevivência",
        xlabel="Idade",
        ylabel="Número de passageiros",
    )
    legend = axis.get_legend()
    if legend:
        legend.set_title("Sobreviveu")
        for label, text in zip(["Não", "Sim"], legend.get_texts(), strict=True):
            text.set_text(label)
        legend.set_frame_on(False)
    figure.tight_layout()
    figure.savefig(generated[1], dpi=160, bbox_inches="tight")
    plt.close(figure)

    figure, axis = plt.subplots(figsize=(9, 5.5))
    sns.barplot(
        data=data,
        x="familia",
        y="survived",
        color="#355C7D",
        errorbar=None,
        ax=axis,
    )
    axis.set(
        title="Sobrevivência por número de familiares a bordo",
        xlabel="Familiares a bordo",
        ylabel="Taxa de sobrevivência",
        ylim=(0, 1),
    )
    figure.tight_layout()
    figure.savefig(generated[2], dpi=160, bbox_inches="tight")
    plt.close(figure)

    return generated


def run_analysis(input_path: Path | str, output_dir: Path | str) -> dict[str, int | float]:
    """Executa o fluxo completo e retorna as métricas calculadas."""
    raw_data = load_data(input_path)
    data = clean_data(raw_data)
    summary = summarize(raw_data, data)
    generate_charts(data, output_dir)
    return summary


def build_parser() -> argparse.ArgumentParser:
    """Configura a interface de linha de comando."""
    parser = argparse.ArgumentParser(
        description="Gera métricas e gráficos da análise de sobrevivência do Titanic."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=PROJECT_ROOT / "titanic.csv",
        help="Caminho do CSV (padrão: titanic.csv do repositório).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=PROJECT_ROOT / "images",
        help="Diretório para os gráficos (padrão: images/ do repositório).",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> None:
    """Executa a análise pela interface de linha de comando."""
    args = build_parser().parse_args(argv)
    summary = run_analysis(args.input, args.output)

    print(
        "Passageiros analisados: "
        f"{summary['passageiros_analisados']} de {summary['passageiros_originais']}"
    )
    print(f"Idades preenchidas pela mediana: {summary['idades_preenchidas']}")
    print(f"Taxa geral de sobrevivência: {summary['taxa_sobrevivencia']:.1f}%")
    print(f"Gráficos salvos em: {args.output.resolve()}")


if __name__ == "__main__":
    main()
