"""Q5 - teste qui-quadrado de independência."""
from pathlib import Path
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "treatment.csv"
OUT = ROOT / "resultados"


def main() -> None:
    OUT.mkdir(exist_ok=True)
    data = pd.read_csv(DATA)
    required = {"treatment", "improvement"}
    if not required.issubset({str(column).strip().lower() for column in data.columns}):
        raise ValueError("treatment.csv deve conter treatment e improvement.")
    columns = {str(column).strip().lower(): column for column in data.columns}
    table = pd.crosstab(data[columns["treatment"]], data[columns["improvement"]])
    chi2, pvalue, df, expected = stats.chi2_contingency(table, correction=False)
    result = {
        "observed_table": table.astype(int).values.tolist(),
        "observed_labels": {"rows": [str(x) for x in table.index], "columns": [str(x) for x in table.columns]},
        "expected_table": expected.tolist(), "chi2_statistic": float(chi2),
        "df": int(df), "pvalue": float(pvalue), "alpha": 0.05,
        "decision": "reject_H0" if pvalue < 0.05 else "fail_to_reject_H0",
        "minimum_expected_frequency": float(expected.min()),
    }
    (OUT / "q5_resultados.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    fig, ax = plt.subplots(figsize=(7, 5))
    image = ax.imshow(table.values, cmap="Blues")
    ax.set(xticks=range(len(table.columns)), xticklabels=table.columns,
           yticks=range(len(table.index)), yticklabels=table.index,
           xlabel="Melhora", ylabel="Tratamento", title="Tabela de contingência")
    for row in range(table.shape[0]):
        for column in range(table.shape[1]):
            ax.text(column, row, int(table.iloc[row, column]), ha="center", va="center")
    fig.colorbar(image, ax=ax, label="Frequência")
    fig.tight_layout(); fig.savefig(OUT / "q5_contingencia.png", dpi=150); plt.close(fig)


if __name__ == "__main__":
    main()
