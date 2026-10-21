"""Q2 - comparação de MPG entre transmissões automática e manual."""
from pathlib import Path
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "mtcars.csv"
OUT = ROOT / "resultados"


def _column(data: pd.DataFrame, name: str) -> str:
    matches = {str(column).strip().lower(): column for column in data.columns}
    if name.lower() not in matches:
        raise ValueError(f"mtcars.csv deve conter a coluna {name!r}.")
    return matches[name.lower()]


def main() -> None:
    OUT.mkdir(exist_ok=True)
    data = pd.read_csv(DATA)
    # separa as colunas de interesse, removendo linhas com valores ausentes
    mpg_col, am_col = _column(data, "mpg"), _column(data, "am")
    clean = data[[mpg_col, am_col]].dropna()
    automatic = clean.loc[clean[am_col].astype(int) == 0, mpg_col].astype(float)
    manual = clean.loc[clean[am_col].astype(int) == 1, mpg_col].astype(float)
    if len(automatic) < 3 or len(manual) < 3:
        raise ValueError("Cada grupo deve conter pelo menos três observações.")

    normality = {}
    for label, sample in (("automatic", automatic), ("manual", manual)):
        # Testes de normalidade Shapiro-Wilk e D'Agostino-Pearson para cada grupo. p-value < 0,05 rejeita a normalidade | p-value >= 0,05 não rejeita a normalidade
        shapiro = stats.shapiro(sample)
        dagostino = stats.normaltest(sample)
        normality[label] = {
            "shapiro_wilk": {"statistic": float(shapiro.statistic), "pvalue": float(shapiro.pvalue)},
            "dagostino_pearson": {"statistic": float(dagostino.statistic), "pvalue": float(dagostino.pvalue)},
            "alpha": 0.05,
        }
    # Calcula diferença de automático - manual
    difference = float(automatic.mean() - manual.mean())
    welch = stats.ttest_ind(automatic, manual, equal_var=False)
    # Calcula graus de liberdade de Welch
    df = float(
        (automatic.var(ddof=1) / len(automatic) + manual.var(ddof=1) / len(manual)) ** 2
        / (
            (automatic.var(ddof=1) / len(automatic)) ** 2 / (len(automatic) - 1)
            + (manual.var(ddof=1) / len(manual)) ** 2 / (len(manual) - 1)
        )
    )
    # Valor crítico para IC de 95%
    critical = stats.t.ppf(0.975, df)
    standard_error = (automatic.var(ddof=1) / len(automatic) + manual.var(ddof=1) / len(manual)) ** 0.5
    # Construção do intervalo de confiança
    ci = [difference - critical * standard_error, difference + critical * standard_error]
    one_sided = stats.ttest_ind(automatic, manual, equal_var=False, alternative="less")
    result = {
        "n_automatic": int(len(automatic)), "n_manual": int(len(manual)),
        "means": {"automatic": float(automatic.mean()), "manual": float(manual.mean())},
        "normality_tests": normality, "welch_ci95": [float(value) for value in ci],
        "mean_difference_automatic_minus_manual": difference,
        "t_statistic": float(one_sided.statistic), "df": df,
        "pvalue": float(one_sided.pvalue), "alpha": 0.05,
        "decision": "reject_H0" if one_sided.pvalue < 0.05 else "fail_to_reject_H0",
        "alternative": "mean_automatic < mean_manual",
    }
    (OUT / "q2_resultados.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    labels = ["Automática", "Manual"]
    fig, ax = plt.subplots(figsize=(7, 5))
    # Analise grafica: boxplot e histogramas
    ax.boxplot([automatic, manual], tick_labels=labels)
    ax.set(ylabel="MPG", title="Consumo por tipo de transmissão")
    fig.tight_layout(); fig.savefig(OUT / "q2_boxplot.png", dpi=150); plt.close(fig)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(automatic, bins="auto", alpha=0.6, label=labels[0], edgecolor="black")
    ax.hist(manual, bins="auto", alpha=0.6, label=labels[1], edgecolor="black")
    ax.set(xlabel="MPG", ylabel="Frequência", title="Histogramas de MPG"); ax.legend()
    fig.tight_layout(); fig.savefig(OUT / "q2_histogramas.png", dpi=150); plt.close(fig)


if __name__ == "__main__":
    main()
