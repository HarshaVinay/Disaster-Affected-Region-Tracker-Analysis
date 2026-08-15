from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
CLEAN = ROOT / "data" / "clean"
OUT = ROOT / "output"
OUT.mkdir(exist_ok=True)

def load_fact():
    path = CLEAN / "disaster_fact_clean.csv"
    if not path.exists():
        raise FileNotFoundError("Run: python src/etl.py first")
    return pd.read_csv(path, parse_dates=["event_date"])

def plot_top5(df):
    x = (df.groupby("region", as_index=False)["affected_people"]
           .sum()
           .sort_values("affected_people", ascending=False)
           .head(5)
           .sort_values("affected_people"))
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(x["region"], x["affected_people"])
    ax.set_title("Top 5 Regions by Total Affected Population")
    ax.set_xlabel("Total Affected People")
    ax.set_ylabel("Region")
    fig.tight_layout()
    fig.savefig(OUT / "01_top5_regions.png", dpi=150)
    plt.close(fig)

def plot_severity(df):
    x = pd.crosstab(df["disaster_type"], df["severity"])
    ax = x.plot(kind="bar", figsize=(10, 6))
    ax.set_title("Disaster Severity Distribution by Disaster Type")
    ax.set_xlabel("Disaster Type")
    ax.set_ylabel("Number of Events")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.savefig(OUT / "02_severity_by_type.png", dpi=150)
    plt.close()

def plot_monthly_trend(df):
    x = df.dropna(subset=["event_date"]).copy()
    x["month"] = x["event_date"].dt.to_period("M").astype(str)
    x = x.groupby("month").size().reset_index(name="disaster_count")
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(x["month"], x["disaster_count"], marker="o")
    ax.set_title("Monthly Disaster Trend")
    ax.set_xlabel("Month")
    ax.set_ylabel("Number of Disasters")
    plt.xticks(rotation=45, ha="right")
    fig.tight_layout()
    fig.savefig(OUT / "03_monthly_disaster_trend.png", dpi=150)
    plt.close(fig)

def plot_loss_vs_affected(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    for disaster_type, group in df.groupby("disaster_type"):
        ax.scatter(group["affected_people"], group["economic_loss_musd"],
                   alpha=0.65, label=disaster_type)
    ax.set_title("Economic Loss vs Affected Population")
    ax.set_xlabel("Affected People")
    ax.set_ylabel("Economic Loss (USD million)")
    ax.legend(title="Disaster Type")
    fig.tight_layout()
    fig.savefig(OUT / "04_loss_vs_affected.png", dpi=150)
    plt.close(fig)

def plot_heatmap(df):
    x = pd.crosstab(df["region"], df["disaster_type"])
    fig, ax = plt.subplots(figsize=(10, 6))
    im = ax.imshow(x.values, aspect="auto")
    ax.set_title("Region-wise Disaster Frequency Heatmap")
    ax.set_xlabel("Disaster Type")
    ax.set_ylabel("Region")
    ax.set_xticks(np.arange(len(x.columns)))
    ax.set_xticklabels(x.columns, rotation=30, ha="right")
    ax.set_yticks(np.arange(len(x.index)))
    ax.set_yticklabels(x.index)
    for r in range(x.shape[0]):
        for c in range(x.shape[1]):
            ax.text(c, r, int(x.iloc[r, c]), ha="center", va="center")
    fig.colorbar(im, ax=ax, label="Disaster Count")
    fig.tight_layout()
    fig.savefig(OUT / "05_region_disaster_heatmap.png", dpi=150)
    plt.close(fig)

def main():
    df = load_fact()
    plot_top5(df)
    plot_severity(df)
    plot_monthly_trend(df)
    plot_loss_vs_affected(df)
    plot_heatmap(df)
    print(f"Dashboard charts created in: {OUT}")

if __name__ == "__main__":
    main()
