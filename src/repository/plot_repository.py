import os
import re
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.cm as cm

RESULTS_DIR = "results"
PLOTS_DIR = "plots"
PALETTE_COLORS = ["#e876e0", "#a012e8", "#333bca", "#6dc1db", "#4eab31", "#a4ec78", "#f6eb75", "#e3a460", "#d33733"]
SOLVED_COLORS = { 0: "red", 1: "green" }
BODY_COLOR = "#eaeaf2"
MARGIN_COLOR_BOX = "#c0f7ff"
MARGIN_COLOR_BAR = "#f7f7c8"

def load_results():
    all_data = []
    csv_files = [f for f in os.listdir(RESULTS_DIR) if f.endswith(".csv")]
    
    for csv_file in csv_files:
        csv_path = os.path.join(RESULTS_DIR, csv_file)
        df = pd.read_csv(csv_path, sep=";")

        name = os.path.splitext(csv_file)[0]
        parts = name.split("_")
        algorithm = parts[0].replace("_", " ").upper()
        
        if len(parts) == 1:
            heuristic = ""
        else:
            heuristic = " ".join(parts[1:])

        df["algorithm"] = algorithm
        df["heuristic"] = heuristic

        if heuristic:
            df["algo_heuristic"] = f"{algorithm}\n({heuristic})"
        else:
            df["algo_heuristic"] = f"{algorithm}"

        df["level"] = df["title"].apply(lambda t: int(re.search(r"\d+", t).group()))

        all_data.append(df)

    if not all_data:
        raise FileNotFoundError("No data!")
    
    return pd.concat(all_data, ignore_index=True)

def plot_boxplot(results, metric, metric_name, title, filename):
    plt.figure(figsize=(10, 6), facecolor=MARGIN_COLOR_BOX)

    results['heuristic_display'] = results['heuristic'].replace("none", "")
    results['algo_heuristic'] = results['algorithm'] + \
                                results['heuristic_display'].apply(lambda h: f"\n({h})" if h else "")

    mean_values = results.groupby("algo_heuristic")[metric].mean()
    labels_sorted = mean_values.sort_values().index.tolist()
    palette_dict = {label: PALETTE_COLORS[i % len(PALETTE_COLORS)] for i, label in enumerate(labels_sorted)}

    ax = sns.boxplot(
        x="algo_heuristic",
        y=metric,
        data=results,
        palette=palette_dict,
        hue="algo_heuristic",
        dodge=False,
        showfliers=False,
        order=labels_sorted
    )

    sns.stripplot(
        x="algo_heuristic",
        y=metric,
        data=results,
        hue="solved",
        palette=SOLVED_COLORS,
        alpha=0.6,
        dodge=False,
        ax=ax,
        marker="o",
        edgecolor="black",
        linewidth=0.5,
        size=4
    )

    ax.set_facecolor(BODY_COLOR)
    ax.grid(True, color="white", linewidth=1)
    ax.set_title(title, fontsize=16)
    ax.set_ylabel(metric_name, fontsize=12)
    ax.set_xlabel("Algorithm")
    
    if ax.get_legend() is not None:
        ax.get_legend().remove()

    plt.xticks(rotation=45)
    plt.tight_layout()

    os.makedirs(PLOTS_DIR, exist_ok=True)
    path = os.path.join(PLOTS_DIR, filename)

    plt.savefig(path, dpi=300, bbox_inches="tight")
    plt.close()

def plot_barplot(results, metric, metric_name, title, filename):
    plt.figure(figsize=(10,6), facecolor=MARGIN_COLOR_BAR)

    results['heuristic_display'] = results['heuristic'].replace("none", "")
    results['algo_heuristic'] = results['algorithm'] + \
                                results['heuristic_display'].apply(lambda h: f"\n({h})" if h else "")

    mean_values = results.groupby("algo_heuristic")[metric].mean().sort_values()
    labels_sorted = mean_values.index.tolist()
    values_sorted = mean_values.values

    norm = mcolors.Normalize(vmin=min(values_sorted), vmax=max(values_sorted))
    cmap = cm.get_cmap('RdYlGn_r')
    colors_sorted = [cmap(norm(val)) for val in values_sorted]

    plt.bar(
        labels_sorted,
        values_sorted,
        color=colors_sorted,
        edgecolor="black",
        linewidth=1,
        zorder=2
    )
    
    plt.grid(
        axis="y",
        color="black",
        linewidth=0.5,
        linestyle="--",
        zorder=1
    )

    plt.xticks(rotation=45)
    plt.ylabel(metric_name, fontsize=12)
    plt.title(title, fontsize=16)
    plt.tight_layout()

    os.makedirs(PLOTS_DIR, exist_ok=True)
    path = os.path.join(PLOTS_DIR, filename)
    plt.savefig(path, dpi=300, bbox_inches="tight")
    plt.close()

def plot():
    results = load_results()

    metrics = ["nodes_visited", "total_steps", "pushes", "processing_time_seconds", "nodes_left_in_frontier"]
    metric_labels = [m.replace("_", " ").capitalize() for m in metrics]
    metric_labels[3] = "seconds"

    for metric, metric_label in zip(metrics, metric_labels):
        metric_name = metric.replace("_", " ").capitalize()
        plot_boxplot(results, metric, metric_label, f"Performance Distribution ({metric_name})", f"{metric}_box.png")
        plot_barplot(results, metric, metric_label, f"Average Performance ({metric_name})", f"{metric}_bar.png")
        
    summary = results.groupby(["algorithm", "heuristic"])[metrics].describe()

    print(summary)

    # TODO: heurísticas entre algoritmos, comparativa métodos informados y no informados