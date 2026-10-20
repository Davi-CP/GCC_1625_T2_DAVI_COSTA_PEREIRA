"""Q1 - teste pareado para pontuações com tacos originais e experimentais."""
from pathlib import Path
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "golfe.csv"
OUT = ROOT / "resultados"

# função para identificar as duas colunas numericas de pontuação. Se existirem as colunas "Old Score" e "New Score", elas serão usadas. Caso contrário, serão selecionadas as duas primeiras colunas numéricas.
def _numeric_columns(data: pd.DataFrame) -> list[str]:
    data = data.rename(columns=lambda column: str(column).strip())
    preferred = {
        "old score": next((column for column in data.columns if column.lower() == "old score"), None),
        "new score": next((column for column in data.columns if column.lower() == "new score"), None),
    }
    if all(preferred.values()):
        return [preferred["old score"], preferred["new score"]]

    columns = [
        column for column in data.select_dtypes(include="number").columns
        if str(column).strip().lower() not in {"id", "index"}
    ]
    if len(columns) < 2:
        raise ValueError(
            "golfe.csv deve conter as colunas 'Old Score' e 'New Score' "
            "ou pelo menos duas colunas numéricas de pontuação."
        )
    return columns[:2]


def main() -> None:
    OUT.mkdir(exist_ok=True)
    # leitura do arquivo de dados
    data = pd.read_csv(DATA, sep=";", encoding="utf-8-sig")
    # remove espaços em branco dos nomes das colunas
    data.columns = data.columns.str.strip()
    original_col, experimental_col = _numeric_columns(data)
    # Construção das diferenças | Se a diferença for positiva, significa que a pontuação original é maior que a experimental, ou seja, o taco original é melhor. Se for negativa, significa que a pontuação experimental é maior, ou seja, o taco experimental é melhor.
    paired = data[[original_col, experimental_col]].dropna()
    differences = paired[original_col] - paired[experimental_col]
    if len(differences) < 3:
        raise ValueError("São necessárias pelo menos três observações pareadas.")
    # Item 1: verificação da normalidade das diferenças usando teste de Shapiro-Wilk
    # p-value < 0,05 rejeita a normalidade | p-value >= 0,05 não rejeita a normalidade
    normality_statistic, normality_pvalue = stats.shapiro(differences)
    # Item 2: teste t pareado.
    t_statistic, pvalue = stats.ttest_rel(
        paired[original_col], paired[experimental_col], alternative="greater"
    )
    alpha_normality = 0.05
    alpha = 0.01
    result = {
        "n": int(len(differences)),
        "columns": {"original": original_col, "experimental": experimental_col},
        "difference_definition": f"{original_col} - {experimental_col}",
        "difference_mean": float(differences.mean()),
        "normality_test": "Shapiro-Wilk",
        "normality_statistic": float(normality_statistic),
        "normality_pvalue": float(normality_pvalue),
        "normality_alpha": alpha_normality,
        "t_statistic": float(t_statistic),
        "df": int(len(differences) - 1),
        "pvalue": float(pvalue),
        "alpha": alpha,
        "decision": "reject_H0" if pvalue < alpha else "fail_to_reject_H0",
        "alternative": "mean_original_minus_experimental > 0",
    }
    (OUT / "q1_resultados.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    axes[0].hist(differences, bins="auto", edgecolor="black", color="#4472C4")
    axes[0].axvline(0, color="black", linestyle="--")
    axes[0].set(title="Diferenças pareadas", xlabel="Original - experimental", ylabel="Frequência")
    stats.probplot(differences, dist="norm", plot=axes[1])
    axes[1].set_title("Q-Q plot das diferenças")
    fig.tight_layout()
    fig.savefig(OUT / "q1_diferencas.png", dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    main()
