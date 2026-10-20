"""Q3 - ANOVA de MPG por categoria de carro."""
from pathlib import Path
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "resultados"
GROUPS = {
    "compactos": [20, 25, 25, 20, 22, 22, 24, 26, 20, 24, 24, 23, 20, 23, 21, 21],
    "medios": [18, 19, 22, 22, 19, 16, 21, 21, 21, 20, 17, 18, 18, 17, 19, 19, 18, 21, 23, 19, 22, 20],
    "grandes_vans": [19, 16, 16, 17, 20, 20, 20, 18, 18, 19, 19, 15, 18, 17, 15, 18, 17, 18, 18, 17],
}


def main() -> None:
    OUT.mkdir(exist_ok=True)
    arrays = [np.asarray(values, dtype=float) for values in GROUPS.values()]
    normality = {}
    for name, values in zip(GROUPS, arrays):
        test = stats.shapiro(values)
        normality[name] = {"test": "Shapiro-Wilk", "statistic": float(test.statistic), "pvalue": float(test.pvalue), "alpha": 0.05}
    levene = stats.levene(*arrays, center="median")
    anova = stats.f_oneway(*arrays)
    result = {
        "group_sizes": {name: len(values) for name, values in GROUPS.items()},
        "group_means": {name: float(values.mean()) for name, values in zip(GROUPS, arrays)},
        "normality_tests": normality,
        "levene_statistic": float(levene.statistic), "levene_pvalue": float(levene.pvalue),
        "anova_statistic": float(anova.statistic), "anova_pvalue": float(anova.pvalue),
        "alpha": 0.05, "decision": "reject_H0" if anova.pvalue < 0.05 else "fail_to_reject_H0",
    }
    (OUT / "q3_resultados.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.boxplot(arrays, tick_labels=["Compactos", "Médios", "Grandes/Vans"])
    ax.set(ylabel="MPG", title="MPG por categoria de carro")
    fig.tight_layout(); fig.savefig(OUT / "q3_grupos.png", dpi=150); plt.close(fig)


if __name__ == "__main__":
    main()
