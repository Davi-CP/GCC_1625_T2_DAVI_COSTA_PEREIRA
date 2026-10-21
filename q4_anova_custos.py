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
    columns = {str(column).strip().lower(): column for column in data.columns}
    cost_column = columns.get("cost") or columns.get("custo")
    if cost_column is None:
        numeric_columns = data.select_dtypes(include="number").columns
        if len(numeric_columns) == 1:
            cost_column = numeric_columns[0]
        else:
            raise ValueError("data9.xls deve conter uma coluna de custos.")

    course_column = columns.get("cource") or columns.get("course") or columns.get("disciplina")
    if course_column is None:
        non_numeric_columns = data.select_dtypes(exclude="number").columns
        if len(non_numeric_columns) == 1:
            course_column = non_numeric_columns[0]
        else:
            raise ValueError("data9.xls deve conter uma coluna identificando as disciplinas.")

    observations = pd.DataFrame(
        {
            "course": data[course_column].astype("string").str.strip(),
            "cost": pd.to_numeric(data[cost_column], errors="coerce"),
        }
    ).dropna()
    observations["group"] = observations["course"].str.extract(r"^([A-Za-z]+)", expand=False)
    observations = observations.dropna(subset=["group"])
    groups = {
        str(name): values.astype(float)
        for name, values in observations.groupby("group", sort=False)["cost"]
    }
    if len(groups) != 3 or any(values.empty for values in groups.values()):
        raise ValueError("data9.xls deve conter custos para três disciplinas.")

    samples = list(groups.values())
    # Teste principal do ANOVA: H0: todas as médias são iguais | H1: pelo menos uma média difere
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
