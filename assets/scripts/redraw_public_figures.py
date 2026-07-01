from __future__ import annotations

import json
import shutil
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]


def redraw_antibody_source_robust_figures() -> None:
    metrics_path = ROOT / "antibody-sequence-ml" / "reports" / "metrics" / "source_robust_public_plot_metrics.json"
    with metrics_path.open() as handle:
        payload = json.load(handle)
    frame = pd.DataFrame(payload["rows"])
    figures_dir = ROOT / "antibody-sequence-ml" / "figures"
    docs_figures_dir = ROOT / "docs" / "assets" / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)
    docs_figures_dir.mkdir(parents=True, exist_ok=True)

    y_positions = range(len(frame))
    labels = frame["display_name"].tolist()

    fig, ax = plt.subplots(figsize=(12, 5.5))
    offset = 0.18
    ax.barh([y - offset for y in y_positions], frame["weighted_pr_auc"], height=0.32, label="PR-AUC")
    ax.barh([y + offset for y in y_positions], frame["weighted_roc_auc"], height=0.32, label="ROC-AUC")
    ax.set_yticks(list(y_positions), labels)
    ax.invert_yaxis()
    ax.set_xlim(0, 1.0)
    ax.set_xlabel("Metric value")
    ax.set_title("Source-robust antibody model comparison")
    ax.legend(loc="lower right")
    fig.tight_layout()
    combined_path = figures_dir / "source_robust_model_comparison.png"
    fig.savefig(combined_path, dpi=180)
    plt.close(fig)
    shutil.copyfile(combined_path, docs_figures_dir / "antibody_source_robust_model_comparison.png")

    for metric_key, title, filename in [
        ("weighted_pr_auc", "Weighted leave-source-out PR-AUC", "source_robust_pr_auc_by_model.png"),
        ("weighted_roc_auc", "Weighted leave-source-out ROC-AUC", "source_robust_roc_auc_by_model.png"),
    ]:
        fig, ax = plt.subplots(figsize=(12, 5.5))
        ax.barh(labels, frame[metric_key])
        ax.invert_yaxis()
        ax.set_xlim(0, 1.0)
        ax.set_xlabel("Metric value")
        ax.set_title(title)
        fig.tight_layout()
        fig.savefig(figures_dir / filename, dpi=180)
        plt.close(fig)


def main() -> None:
    redraw_antibody_source_robust_figures()


if __name__ == "__main__":
    main()
