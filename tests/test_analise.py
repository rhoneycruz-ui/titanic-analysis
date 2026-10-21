import subprocess
import sys
from pathlib import Path

import pytest


DATASET = Path(__file__).parents[1] / "titanic.csv"


def test_cleaning_preserves_expected_dataset_contract():
    from analise import clean_data, load_data, summarize

    raw = load_data(DATASET)
    cleaned = clean_data(raw)
    summary = summarize(raw, cleaned)

    assert summary == {
        "passageiros_originais": 891,
        "passageiros_analisados": 889,
        "idades_preenchidas": 177,
        "sobreviventes": 340,
        "taxa_sobrevivencia": pytest.approx(38.24521934758155),
    }
    assert "deck" not in cleaned.columns
    assert cleaned["age"].isna().sum() == 0
    assert cleaned["embarked"].isna().sum() == 0
    assert cleaned["familia"].equals(cleaned["sibsp"] + cleaned["parch"])


def test_generate_charts_writes_three_nonempty_png_files(tmp_path):
    from analise import clean_data, generate_charts, load_data

    data = clean_data(load_data(DATASET))
    generated = generate_charts(data, tmp_path)

    assert [path.name for path in generated] == [
        "sobrevivencia_classe_sexo.png",
        "distribuicao_idade.png",
        "sobrevivencia_familia.png",
    ]
    assert all(path.parent == tmp_path for path in generated)
    assert all(path.stat().st_size > 10_000 for path in generated)


def test_cli_runs_from_any_directory_with_explicit_paths(tmp_path):
    script = Path(__file__).parents[1] / "analise.py"
    output_dir = tmp_path / "graficos"

    result = subprocess.run(
        [
            sys.executable,
            str(script),
            "--input",
            str(DATASET),
            "--output",
            str(output_dir),
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert "Passageiros analisados: 889 de 891" in result.stdout
    assert "Taxa geral de sobrevivência: 38.2%" in result.stdout
    assert sorted(path.name for path in output_dir.glob("*.png")) == sorted(
        [
            "sobrevivencia_classe_sexo.png",
            "distribuicao_idade.png",
            "sobrevivencia_familia.png",
        ]
    )
