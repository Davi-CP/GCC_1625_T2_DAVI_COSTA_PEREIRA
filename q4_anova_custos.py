"""Q4 - ANOVA dos custos de materiais por disciplina."""
from pathlib import Path
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "data9.xls"
OUT = ROOT / "resultados"


def main() -> None:
    OUT.mkdir(exist_ok=True)
    data = pd.read_excel(DATA)
    numeric = data.select_dtypes(include="number")
    if numeric.shape[1] < 3:
        raise ValueError("data9.xls deve conter três colunas numéricas de custos.")
    numeric = numeric.iloc[:, :3].dropna()
    groups = {str(column): numeric[column].astype(float) for column in numeric.columns}
    samples = list(groups.values())
    anova = stats.f_oneway(*samples)
    result = {
        "group_sizes": {name: int(len(values)) for name, values in groups.items()},
        "group_means": {name: float(values.mean()) for name, values in groups.items()},
        "anova_statistic": float(anova.statistic), "anova_pvalue": float(anova.pvalue),
        "alpha": 0.01, "decision": "reject_H0" if anova.pvalue < 0.01 else "fail_to_reject_H0",
        "hypotheses": "H0: todas as médias são iguais; H1: pelo menos uma média difere",
    }
    (OUT / "q4_resultados.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.boxplot(samples, tick_labels=list(groups))
    ax.set(ylabel="Custo", title="Custos de materiais por disciplina")
    fig.tight_layout(); fig.savefig(OUT / "q4_custos.png", dpi=150); plt.close(fig)


if __name__ == "__main__":
    main()
