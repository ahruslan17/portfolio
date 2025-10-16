"""
Report and visualization generation for Vulkan FPS analysis
"""

import os
from datetime import datetime
from typing import Dict

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

import config


def setup_plot_style():
    """Setup style for plots"""
    plt.style.use(config.PLOT_STYLE)
    sns.set_palette(config.PLOT_PALETTE)


def _save_plot(plots_dir: str, filename: str):
    """Common function for saving plots"""
    plt.tight_layout()
    plt.savefig(
        f"{plots_dir}/{filename}",
        dpi=config.PLOT_DPI,
        bbox_inches="tight",
    )
    plt.close()


def _get_plots_dir() -> str:
    """Gets directory for plots"""
    create_plots_directory()
    return config.PLOTS_DIR


def _ensure_plots_dir(plots_dir: str = None) -> str:
    """Ensures getting correct directory for plots"""
    if plots_dir is None:
        return _get_plots_dir()
    return plots_dir


def create_plots_directory():
    """Creates directory for plots"""
    os.makedirs(config.PLOTS_DIR, exist_ok=True)


def plot_fps_delta_distribution(
    players_comparison: pd.DataFrame, plots_dir: str = None
):
    """FPS change distribution plot"""
    plots_dir = _ensure_plots_dir(plots_dir)

    _, axes = plt.subplots(1, 3, figsize=(18, 5))

    # Average FPS
    axes[0].hist(
        players_comparison["c_FpsAvg_delta"],
        bins=50,
        edgecolor="black",
        alpha=0.7,
    )
    axes[0].axvline(0, color="red", linestyle="--", linewidth=2)
    axes[0].set_xlabel("Change in Average FPS")
    axes[0].set_ylabel("Number of Players")
    axes[0].set_title("Distribution of Average FPS Changes")
    axes[0].grid(True, alpha=0.3)

    # Minimum FPS
    axes[1].hist(
        players_comparison["c_FpsAvgMin_delta"],
        bins=50,
        edgecolor="black",
        alpha=0.7,
        color="orange",
    )
    axes[1].axvline(0, color="red", linestyle="--", linewidth=2)
    axes[1].set_xlabel("Change in Minimum FPS")
    axes[1].set_ylabel("Number of Players")
    axes[1].set_title("Distribution of Minimum FPS Changes")
    axes[1].grid(True, alpha=0.3)

    # 1% percentile FPS
    axes[2].hist(
        players_comparison["c_FpsAvgOnePercentile_delta"],
        bins=50,
        edgecolor="black",
        alpha=0.7,
        color="green",
    )
    axes[2].axvline(0, color="red", linestyle="--", linewidth=2)
    axes[2].set_xlabel("Change in 1% Percentile FPS")
    axes[2].set_ylabel("Number of Players")
    axes[2].set_title("Distribution of 1% Percentile FPS Changes")
    axes[2].grid(True, alpha=0.3)

    _save_plot(plots_dir, "fps_delta_distribution.png")


def plot_fps_before_after_boxplot(
    players_comparison: pd.DataFrame, plots_dir: str = None
):
    """Box plot comparing FPS before/after"""
    plots_dir = _ensure_plots_dir(plots_dir)

    _, axes = plt.subplots(1, 3, figsize=(18, 5))

    metrics_to_plot = [
        ("c_FpsAvg", "Average FPS"),
        ("c_FpsAvgMin", "Minimum FPS"),
        ("c_FpsAvgOnePercentile", "1% Percentile FPS"),
    ]

    for idx, (metric, title) in enumerate(metrics_to_plot):
        before_data = players_comparison[f"{metric}_before"]
        after_data = players_comparison[f"{metric}_after"]

        positions = [1, 2]
        data_to_plot = [before_data, after_data]

        bp = axes[idx].boxplot(
            data_to_plot,
            positions=positions,
            widths=0.6,
            patch_artist=True,
            showmeans=True,
            meanline=True,
        )

        for patch in bp["boxes"]:
            patch.set_facecolor("lightblue")

        axes[idx].set_xticks(positions)
        axes[idx].set_xticklabels(["Before Vulkan", "After Vulkan"])
        axes[idx].set_ylabel("FPS")
        axes[idx].set_title(title)
        axes[idx].grid(True, alpha=0.3)

    _save_plot(plots_dir, "fps_before_after_boxplot.png")


def plot_top_devices_improvement(
    device_analysis_filtered: pd.DataFrame, plots_dir: str = None
):
    """TOP-20 devices improvement percentage plot"""
    plots_dir = _ensure_plots_dir(plots_dir)

    if len(device_analysis_filtered) == 0:
        return

    top_devices = device_analysis_filtered.head(20)

    _, ax = plt.subplots(figsize=(14, 8))

    colors = [
        config.COLOR_GREEN if x > 0.5 else config.COLOR_RED
        for x in top_devices["improvement_rate"]
    ]

    y_pos = np.arange(len(top_devices))
    ax.barh(y_pos, top_devices["improvement_rate"] * 100, color=colors, alpha=0.7)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(
        [
            f"{device} (n={int(row['player_count'])})"
            for device, row in top_devices.iterrows()
        ]
    )
    ax.set_xlabel("Percentage of Players with FPS Improvement (%)")
    ax.set_title("TOP-20 Devices by Player Count\n(FPS Improvement Percentage)")
    ax.axvline(50, color="black", linestyle="--", linewidth=1)
    ax.grid(True, alpha=0.3, axis="x")

    _save_plot(plots_dir, "top_devices_improvement_rate.png")


def plot_top_gpu_improvement(
    gpu_analysis_filtered: pd.DataFrame, plots_dir: str = None
):
    """TOP-20 GPU improvement percentage plot"""
    plots_dir = _ensure_plots_dir(plots_dir)

    if len(gpu_analysis_filtered) == 0:
        return

    top_gpus = gpu_analysis_filtered.head(20)

    _, ax = plt.subplots(figsize=(14, 8))

    colors = [
        config.COLOR_GREEN if x > 0.5 else config.COLOR_RED
        for x in top_gpus["improvement_rate"]
    ]

    y_pos = np.arange(len(top_gpus))
    ax.barh(y_pos, top_gpus["improvement_rate"] * 100, color=colors, alpha=0.7)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(
        [f"{gpu} (n={int(row['player_count'])})" for gpu, row in top_gpus.iterrows()]
    )
    ax.set_xlabel("Percentage of Players with FPS Improvement (%)")
    ax.set_title("TOP-20 GPU by Player Count\n(FPS Improvement Percentage)")
    ax.axvline(50, color="black", linestyle="--", linewidth=1)
    ax.grid(True, alpha=0.3, axis="x")

    _save_plot(plots_dir, "top_gpu_improvement_rate.png")


def plot_fps_scatter(players_comparison: pd.DataFrame, plots_dir: str = None):
    """Scatter plot: FPS before vs after (for all key metrics)"""
    plots_dir = _ensure_plots_dir(plots_dir)

    _, axes = plt.subplots(1, 3, figsize=(20, 6))

    metrics = [
        ("c_FpsAvg", "Average FPS"),
        ("c_FpsAvgMin", "Minimum FPS"),
        ("c_FpsAvgOnePercentile", "1% Percentile FPS"),
    ]

    for idx, (metric, title) in enumerate(metrics):
        ax = axes[idx]

        # Determine status for each metric
        improved = players_comparison[
            players_comparison[f"{metric}_delta"] > config.MINIMUM_CHANGE_THRESHOLD
        ]
        unchanged = players_comparison[
            abs(players_comparison[f"{metric}_delta"])
            <= config.MINIMUM_CHANGE_THRESHOLD
        ]
        worsened = players_comparison[
            players_comparison[f"{metric}_delta"] < -config.MINIMUM_CHANGE_THRESHOLD
        ]

        # Draw points
        if len(worsened) > 0:
            ax.scatter(
                worsened[f"{metric}_before"],
                worsened[f"{metric}_after"],
                alpha=0.5,
                s=30,
                c=config.COLOR_RED,
                label="Worsened",
            )
        if len(unchanged) > 0:
            ax.scatter(
                unchanged[f"{metric}_before"],
                unchanged[f"{metric}_after"],
                alpha=0.5,
                s=30,
                c=config.COLOR_ORANGE,
                label="Unchanged",
            )
        if len(improved) > 0:
            ax.scatter(
                improved[f"{metric}_before"],
                improved[f"{metric}_after"],
                alpha=0.5,
                s=30,
                c=config.COLOR_GREEN,
                label="Improved",
            )

        # y=x line (no changes)
        max_val = max(
            players_comparison[f"{metric}_before"].max(),
            players_comparison[f"{metric}_after"].max(),
        )
        min_val = min(
            players_comparison[f"{metric}_before"].min(),
            players_comparison[f"{metric}_after"].min(),
        )
        ax.plot(
            [min_val, max_val],
            [min_val, max_val],
            "k--",
            linewidth=2,
            label="No Change Line",
        )

        ax.set_xlabel(f"{title} Before Vulkan")
        ax.set_ylabel(f"{title} After Vulkan")
        ax.set_title(f"Comparison: {title}")
        ax.legend()
        ax.grid(True, alpha=0.3)

    _save_plot(plots_dir, "fps_before_after_scatter.png")


def plot_overall_effect_pie(overall_stats: Dict, plots_dir: str = None):
    """Overall effect pie chart"""
    plots_dir = _ensure_plots_dir(plots_dir)

    _, ax = plt.subplots(figsize=(8, 8))

    improved_count = overall_stats["improved_count"]
    unchanged_count = overall_stats["unchanged_count"]
    worsened_count = overall_stats["worsened_count"]

    sizes = [improved_count, unchanged_count, worsened_count]
    labels = [
        f"Improved\n({improved_count} players, {overall_stats['improved_pct']:.1f}%)",
        f"Unchanged\n({unchanged_count} players, {overall_stats['unchanged_pct']:.1f}%)",
        f"Worsened\n({worsened_count} players, {overall_stats['worsened_pct']:.1f}%)",
    ]
    colors = [config.COLOR_IMPROVED, config.COLOR_UNCHANGED, config.COLOR_WORSENED]
    explode = (0.05, 0.05, 0.05)

    ax.pie(
        sizes,
        explode=explode,
        labels=labels,
        colors=colors,
        autopct="%1.1f%%",
        shadow=True,
        startangle=90,
        textprops={"fontsize": 12, "weight": "bold"},
    )
    ax.set_title(
        "Overall Distribution of Vulkan Implementation Effect",
        fontsize=14,
        weight="bold",
    )

    _save_plot(plots_dir, "overall_effect_pie.png")


def generate_all_plots(players_comparison: pd.DataFrame, analysis_results: Dict):
    """Generates all plots"""
    setup_plot_style()
    plots_dir = _get_plots_dir()

    plot_fps_delta_distribution(players_comparison, plots_dir)
    plot_fps_before_after_boxplot(players_comparison, plots_dir)
    plot_top_devices_improvement(
        analysis_results["device_analysis"]["filtered"], plots_dir
    )
    plot_top_gpu_improvement(analysis_results["gpu_analysis"]["filtered"], plots_dir)
    plot_fps_scatter(players_comparison, plots_dir)
    plot_overall_effect_pie(analysis_results["overall_stats"], plots_dir)


def _get_metric_names_map() -> Dict[str, str]:
    """Returns mapping of metric keys to their names"""
    return {
        "avg": "Average FPS",
        "min": "Minimum FPS",
        "percentile_1": "1% Percentile FPS",
    }


def _create_table_header(columns: list) -> str:
    """Creates table header"""
    header = "| " + " | ".join(columns) + " |\n"
    separator = "|" + "|".join(["---"] * len(columns)) + "|\n"
    return header + separator


def _create_table_row(values: list) -> str:
    """Creates table row"""
    return "| " + " | ".join(str(v) for v in values) + " |\n"


def _create_analysis_table(
    analysis_data: pd.DataFrame, title: str, top_n: int = 20
) -> str:
    """Creates analysis table (devices/GPU)"""
    if len(analysis_data) == 0:
        return f"### {title}\n\n*No data to display*\n\n"

    top_data = analysis_data.head(top_n)
    columns = [
        "#",
        "Name",
        "Players",
        "% Improved",
        "Before (AVG)",
        "After (AVG)",
        "Δ (AVG)",
    ]
    table = _create_table_header(columns)

    for idx, (name, row) in enumerate(top_data.iterrows(), 1):
        values = [
            idx,
            name,
            int(row["player_count"]),
            f"{row['improvement_rate']*100:.1f}%",
            f"{row.get('c_FpsAvg_before', 0):.1f}",
            f"{row.get('c_FpsAvg_after', 0):.1f}",
            f"{row.get('c_FpsAvg_delta', 0):+.2f}",
        ]
        table += _create_table_row(values)

    return f"### {title}\n\n{table}\n"


def _create_analysis_section(
    analysis_data: Dict, section_title: str, plots_dir: str, plot_filename: str
) -> str:
    """Creates analysis section with tables and plot"""
    improved = analysis_data["improved"]
    worsened = analysis_data["worsened"]

    section = f"""## {section_title}

### Methodology

- **Minimum players for analysis:** {config.MIN_PLAYERS_FOR_DEVICE_GPU}
- **Stable improvement criterion:** >{config.IMPROVEMENT_THRESHOLD * 100}% of players showed improvement
- **Stable worsening criterion:** <{config.WORSENING_THRESHOLD * 100}% of players showed improvement

### 🟢 {section_title} with Stable Improvement

**Count:** {len(improved)}

"""

    if len(improved) > 0:
        section += _create_analysis_table(
            improved, f"{section_title} with Stable Improvement"
        )
    else:
        section += f"*No {section_title.lower()} meeting stable improvement criteria*\n"

    section += f"""

### 🔴 {section_title} with Stable Worsening

**Count:** {len(worsened)}

"""

    if len(worsened) > 0:
        section += _create_analysis_table(
            worsened, f"{section_title} with Stable Worsening"
        )
    else:
        section += f"*No {section_title.lower()} meeting stable worsening criteria*\n"

    section += f"""

### TOP-20 {section_title.lower()} by player count

![TOP-20 {section_title.lower()}]({plots_dir}/{plot_filename})

---
"""
    return section


def _build_report_header() -> str:
    """Forms report header and table of contents"""
    return f"""# Analysis of Vulkan Implementation Effect on Player FPS

**Analysis Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Task:** FORT-43631

---

## Table of Contents

1. [Task Description](#task-description)
2. [Research Methodology](#research-methodology)
3. [Data Loading and Preparation](#data-loading-and-preparation)
4. [Overall Results](#overall-results)
5. [Statistical Analysis](#statistical-analysis)
6. [Device Analysis](#device-analysis)
7. [GPU Analysis](#gpu-analysis)
8. [Visualizations](#visualizations)
9. [Conclusions and Recommendations](#conclusions-and-recommendations)

---

## Task Description

### Context

Players were offered to take an FPS test:
- **Before Vulkan implementation**: Mission {config.MISSION_BEFORE}
- **After Vulkan implementation**: Mission {config.MISSION_AFTER}

### Analysis Goals

1. Evaluate the overall effect of Vulkan implementation (FPS improvement or degradation)
2. Identify devices for which the effect is consistently positive/negative
3. Identify GPUs for which the effect is consistently positive/negative

---

## Research Methodology

### Stage 1: Player Identification for Comparison

**Approach:**
- From the entire dataset, players who took the test BEFORE (mission {config.MISSION_BEFORE}) and AFTER (mission {config.MISSION_AFTER}) Vulkan implementation are identified
- This ensures paired comparison, which is critical for correct effect evaluation
- Players who took only one test are excluded from analysis

**Rationale:**
- Paired comparison eliminates individual player variability
- Allows isolating the effect specifically from Vulkan implementation, not from differences in player skills or behavior

### Stage 2: Data Aggregation

**Approach:**
- Each player may have multiple measurements within one mission
- Median value is used for player data aggregation
- Median is chosen over mean for robustness to outliers

**FPS Metrics:**
- `c_FpsAvg` - average FPS per session
- `c_FpsAvgMin` - minimum average FPS (important for evaluating "dips")
- `c_FpsAvgOnePercentile` - 1% percentile (shows worst 1% of moments)

### Stage 3: Change Calculation

**Approach:**
- For each metric, the following are calculated:
  - Absolute change: `Δ = FPS_after - FPS_before`
  - Percentage change: `Δ% = (Δ / FPS_before) × 100%`

**Change Evaluation Criteria:**
- For each player, 3 key metrics are evaluated:
  - Average FPS (`c_FpsAvg`)
  - Minimum FPS (`c_FpsAvgMin`)
  - 1% Percentile FPS (`c_FpsAvgOnePercentile`)

- **Significant change threshold:** {config.MINIMUM_CHANGE_THRESHOLD} FPS
  - Improvement: Δ > {config.MINIMUM_CHANGE_THRESHOLD} FPS
  - No change: |Δ| ≤ {config.MINIMUM_CHANGE_THRESHOLD} FPS  
  - Worsening: Δ < -{config.MINIMUM_CHANGE_THRESHOLD} FPS

- **Overall player evaluation:**
  - **Improvement**: if 2/3 metrics improved OR if 1/3 improved + 2/3 unchanged
  - **No change**: if 3/3 metrics unchanged
  - **Worsening**: in all other cases

### Stage 4: Statistical Analysis

**Approach:**
- Paired Student's t-test is applied
- Hypothesis tested: H0: mean change = 0 vs H1: mean change ≠ 0
- Significance level: α = {config.SIGNIFICANCE_LEVEL}

**Rationale:**
- Paired t-test is suitable for comparing two related samples (before/after)
- p-value < {config.SIGNIFICANCE_LEVEL} indicates statistically significant change

### Stage 5: Device Analysis

**Approach:**
- Data is aggregated by device models (`DeviceModel`)
- For each device, the following are calculated:
  - Number of players
  - Mean changes in key FPS metrics
  - Percentage of players with improvement (`improvement_rate`)

**Filtering Criteria:**
- Only devices with **minimum {config.MIN_PLAYERS_FOR_DEVICE_GPU} players** are analyzed (for statistical significance)

**Classification Criteria:**
- **Stable improvement**: improvement_rate > {config.IMPROVEMENT_THRESHOLD * 100}%
- **Stable worsening**: improvement_rate < {config.WORSENING_THRESHOLD * 100}%
- **Neutral effect**: {config.WORSENING_THRESHOLD * 100}% ≤ improvement_rate ≤ {config.IMPROVEMENT_THRESHOLD * 100}%

### Stage 6: GPU Analysis

**Approach:**
- Similar to device analysis, but aggregated by GPU (`c_GraphicsDeviceName`)
- Same filtering and classification criteria are applied

**Rationale:**
- Vulkan is a graphics API, so the effect may strongly depend on GPU architecture
- Important to identify GPUs where Vulkan shows best/worst optimization

---

"""


def _build_data_loading_section(metadata: Dict) -> str:
    """Forms section with data loading information"""
    section = f"""## Data Loading and Preparation

### Source Data

- **Source:** `{config.INPUT_FILE}` and `{config.CLIENT_INFO_FILE}`
- **Total records:** {metadata['dataset_stats']['total_records']}
- **Records before Vulkan (mission {config.MISSION_BEFORE}):** {metadata['dataset_stats']['records_before']}
- **Records after Vulkan (mission {config.MISSION_AFTER}):** {metadata['dataset_stats']['records_after']}

### Player Matching

- **Unique players before:** {metadata['account_stats']['unique_before']}
- **Unique players after:** {metadata['account_stats']['unique_after']}
- **Players who took both tests:** {metadata['account_stats']['both']}

### Pair Validation

- **Valid players (with Vulkan on mission 967):** {metadata['account_stats']['both_valid']}

### Analysis Data

- **Players in final sample:** {metadata['players_in_comparison']}
- **Records before (matched):** {metadata['matched_records_before']}
- **Records after (matched):** {metadata['matched_records_after']}

---
"""

    return section


def _build_overall_results_section(overall_stats: Dict, plots_dir: str = None) -> str:
    """Forms section with overall results"""
    plots_dir = _ensure_plots_dir(plots_dir)

    return f"""## Overall Results

### Effect Distribution

| Result | Player Count | Percentage |
|--------|-------------|------------|
| 🟢 Improvement | {overall_stats['improved_count']} | {overall_stats['improved_pct']:.1f}% |
| 🟡 No Change | {overall_stats['unchanged_count']} | {overall_stats['unchanged_pct']:.1f}% |
| 🔴 Worsening | {overall_stats['worsened_count']} | {overall_stats['worsened_pct']:.1f}% |
| **Total** | **{overall_stats['total_count']}** | **100.0%** |

![Overall Distribution]({plots_dir}/overall_effect_pie.png)

### Statistics by Key Metrics

#### 1. Average FPS (c_FpsAvg)

| Period | Mean | Std Dev |
|--------|------|---------|
| Before Vulkan | {overall_stats['avg_before_mean']:.2f} | {overall_stats['avg_before_std']:.2f} |
| After Vulkan | {overall_stats['avg_after_mean']:.2f} | {overall_stats['avg_after_std']:.2f} |
| **Change (Δ)** | **{overall_stats['avg_delta_mean']:.2f}** | **{overall_stats['avg_delta_std']:.2f}** |
| **Change (%)** | **{overall_stats['avg_pct_change_mean']:.2f}%** | - |

#### 2. Minimum FPS (c_FpsAvgMin)

| Period | Mean | Std Dev |
|--------|------|---------|
| Before Vulkan | {overall_stats['min_before_mean']:.2f} | {overall_stats['min_before_std']:.2f} |
| After Vulkan | {overall_stats['min_after_mean']:.2f} | {overall_stats['min_after_std']:.2f} |
| **Change (Δ)** | **{overall_stats['min_delta_mean']:.2f}** | **{overall_stats['min_delta_std']:.2f}** |
| **Change (%)** | **{overall_stats['min_pct_change_mean']:.2f}%** | - |

#### 3. 1% Percentile FPS (c_FpsAvgOnePercentile)

| Period | Mean | Std Dev |
|--------|------|---------|
| Before Vulkan | {overall_stats['percentile_1_before_mean']:.2f} | {overall_stats['percentile_1_before_std']:.2f} |
| After Vulkan | {overall_stats['percentile_1_after_mean']:.2f} | {overall_stats['percentile_1_after_std']:.2f} |
| **Change (Δ)** | **{overall_stats['percentile_1_delta_mean']:.2f}** | **{overall_stats['percentile_1_delta_std']:.2f}** |
| **Change (%)** | **{overall_stats['percentile_1_pct_change_mean']:.2f}%** | - |

---
"""


def _format_statistical_test_result(metric_name: str, test_result: Dict) -> str:
    """Formats result of one statistical test"""
    significance = (
        "✅ **STATISTICALLY SIGNIFICANT**"
        if test_result["is_significant"]
        else "❌ **NOT SIGNIFICANT**"
    )
    direction = (
        "↑ Improvement" if test_result["direction"] == "improvement" else "↓ Worsening"
    )

    return f"""#### {metric_name}

| Parameter | Value |
|-----------|-------|
| t-statistic | {test_result['t_statistic']:.4f} |
| p-value | {test_result['p_value']:.6f} |
| Direction | {direction} |
| Result | {significance} |

"""


def _build_statistical_analysis_section(statistical_tests: Dict) -> str:
    """Forms section with statistical analysis"""
    section = f"""## Statistical Analysis

### Paired Student's t-test

Tests the hypothesis about significance of FPS change after Vulkan implementation.

**Null hypothesis (H0):** Mean FPS change = 0 (no effect)  
**Alternative hypothesis (H1):** Mean FPS change ≠ 0 (there is an effect)  
**Significance level:** α = {config.SIGNIFICANCE_LEVEL}

"""

    metric_names_map = _get_metric_names_map()
    for metric_key, test_result in statistical_tests.items():
        metric_name = metric_names_map.get(metric_key, metric_key)
        section += _format_statistical_test_result(metric_name, test_result)

    section += """### Interpretation

- **p-value < 0.05** means the change is statistically significant (probability of randomness < 5%)
- **t-statistic > 0** indicates positive change (improvement)
- **t-statistic < 0** indicates negative change (worsening)

---
"""
    return section


def _build_device_analysis_section(device_analysis: Dict, plots_dir: str = None) -> str:
    """Forms section with device analysis"""
    plots_dir = _ensure_plots_dir(plots_dir)
    return _create_analysis_section(
        device_analysis,
        "Device Analysis",
        plots_dir,
        "top_devices_improvement_rate.png",
    )


def _build_gpu_analysis_section(gpu_analysis: Dict, plots_dir: str = None) -> str:
    """Forms section with GPU analysis"""
    plots_dir = _ensure_plots_dir(plots_dir)
    return _create_analysis_section(
        gpu_analysis, "GPU Analysis", plots_dir, "top_gpu_improvement_rate.png"
    )


def _build_visualizations_section(plots_dir: str = None) -> str:
    """Forms section with visualizations"""
    plots_dir = _ensure_plots_dir(plots_dir)

    return f"""## Visualizations

### FPS Change Distribution

![Change Distribution]({plots_dir}/fps_delta_distribution.png)

**Interpretation:**
- Histograms show the distribution of changes for three key metrics
- Red dashed line (x=0) separates improvement and worsening
- Distribution shift to the right of zero indicates overall improvement
- Shift to the left indicates worsening

### Before/After Comparison (Box Plot)

![Box Plot Before/After]({plots_dir}/fps_before_after_boxplot.png)

**Interpretation:**
- Box plot shows median, quartiles, and outliers
- Allows visual assessment of central tendency and spread changes
- Green line inside boxes - mean value

### Scatter Plot: Before vs After

![Scatter Plot]({plots_dir}/fps_before_after_scatter.png)

**Interpretation:**
- Three plots for comparison: Average FPS, Minimum FPS, 1% Percentile FPS
- Each point represents one player
- Black dashed line - "no change" line (y=x)
- Green points - improvement for corresponding metric (Δ > {config.MINIMUM_CHANGE_THRESHOLD} FPS)
- Orange points - no change for corresponding metric (|Δ| ≤ {config.MINIMUM_CHANGE_THRESHOLD} FPS)
- Red points - worsening for corresponding metric (Δ < -{config.MINIMUM_CHANGE_THRESHOLD} FPS)
- Point color is determined independently for each metric (by its delta)

---
"""


def _format_significance_conclusion(
    metric_key: str, test_result: Dict, metric_names_map: Dict
) -> str:
    """Formats conclusion on statistical significance for one metric"""
    metric_name = metric_names_map.get(metric_key, metric_key)
    if test_result["is_significant"]:
        direction = (
            "improvement" if test_result["direction"] == "improvement" else "worsening"
        )
        return f"   - {metric_name}: statistically significant {direction} (p={test_result['p_value']:.6f})\n"
    return (
        f"   - {metric_name}: change not significant (p={test_result['p_value']:.6f})\n"
    )


def _build_conclusions_section(
    overall_stats: Dict,
    statistical_tests: Dict,
    device_analysis: Dict,
    gpu_analysis: Dict,
) -> str:
    """Forms section with conclusions and recommendations"""
    # Determine overall effect based on new logic
    if overall_stats["improved_count"] > overall_stats["worsened_count"]:
        overall_conclusion = "positive"
        overall_emoji = "✅"
    elif overall_stats["unchanged_count"] > max(
        overall_stats["improved_count"], overall_stats["worsened_count"]
    ):
        overall_conclusion = "neutral"
        overall_emoji = "⚪"
    else:
        overall_conclusion = "negative"
        overall_emoji = "⚠️"

    section = f"""## Conclusions and Recommendations

### Overall Conclusions

{overall_emoji} **Overall effect of Vulkan implementation: {overall_conclusion.upper()}**

1. **Audience coverage:**
   - {overall_stats['total_count']} players participated in the analysis
   - {overall_stats['improved_count']} players ({overall_stats['improved_pct']:.1f}%) showed FPS improvement
   - {overall_stats['unchanged_count']} players ({overall_stats['unchanged_pct']:.1f}%) remained unchanged
   - {overall_stats['worsened_count']} players ({overall_stats['worsened_pct']:.1f}%) showed FPS worsening

2. **Changes by metrics:**
   - Average FPS: {overall_stats['avg_delta_mean']:+.2f} FPS ({overall_stats['avg_pct_change_mean']:+.2f}%)
   - Minimum FPS: {overall_stats['min_delta_mean']:+.2f} FPS ({overall_stats['min_pct_change_mean']:+.2f}%)
   - 1% Percentile FPS: {overall_stats['percentile_1_delta_mean']:+.2f} FPS ({overall_stats['percentile_1_pct_change_mean']:+.2f}%)
   
   *Note: percentage change = (delta) / (before value) × 100%*

3. **Statistical significance:**
"""

    metric_names_map = _get_metric_names_map()
    for metric_key, test_result in statistical_tests.items():
        section += _format_significance_conclusion(
            metric_key, test_result, metric_names_map
        )

    devices_improved = device_analysis["improved"]
    devices_worsened = device_analysis["worsened"]

    section += f"""

### Device Conclusions

- **Devices with stable improvement:** {len(devices_improved)}
- **Devices with stable worsening:** {len(devices_worsened)}
"""

    if len(devices_improved) > 0:
        top_device = devices_improved.iloc[0]
        section += f"\n**Improvement leader:** {devices_improved.index[0]} ({top_device['improvement_rate']*100:.1f}% players, Δ={top_device['c_FpsAvg_delta']:.2f} FPS)\n"

    if len(devices_worsened) > 0:
        worst_device = devices_worsened.iloc[0]
        section += f"\n**Greatest worsening:** {devices_worsened.index[0]} ({worst_device['improvement_rate']*100:.1f}% players, Δ={worst_device['c_FpsAvg_delta']:.2f} FPS)\n"

    gpu_improved = gpu_analysis["improved"]
    gpu_worsened = gpu_analysis["worsened"]

    section += f"""

### GPU Conclusions

- **GPU with stable improvement:** {len(gpu_improved)}
- **GPU with stable worsening:** {len(gpu_worsened)}
"""

    if len(gpu_improved) > 0:
        top_gpu = gpu_improved.iloc[0]
        section += f"\n**Improvement leader:** {gpu_improved.index[0]} ({top_gpu['improvement_rate']*100:.1f}% players, Δ={top_gpu['c_FpsAvg_delta']:.2f} FPS)\n"

    if len(gpu_worsened) > 0:
        worst_gpu = gpu_worsened.iloc[0]
        section += f"\n**Greatest worsening:** {gpu_worsened.index[0]} ({worst_gpu['improvement_rate']*100:.1f}% players, Δ={worst_gpu['c_FpsAvg_delta']:.2f} FPS)\n"

    section += """

---

**End of Report**
"""
    return section


def generate_markdown_report(
    _players_comparison: pd.DataFrame,
    metadata: Dict,
    analysis_results: Dict,
) -> str:
    """
    Generates full Markdown report

    Returns:
        String with report content in Markdown format
    """
    overall_stats = analysis_results["overall_stats"]
    statistical_tests = analysis_results["statistical_tests"]
    device_analysis = analysis_results["device_analysis"]
    gpu_analysis = analysis_results["gpu_analysis"]

    report = _build_report_header()
    plots_dir = config.PLOTS_DIR

    report += _build_data_loading_section(metadata)
    report += _build_overall_results_section(overall_stats, plots_dir)
    report += _build_statistical_analysis_section(statistical_tests)
    report += _build_device_analysis_section(device_analysis, plots_dir)
    report += _build_gpu_analysis_section(gpu_analysis, plots_dir)
    report += _build_visualizations_section(plots_dir)
    report += _build_conclusions_section(
        overall_stats, statistical_tests, device_analysis, gpu_analysis
    )

    return report


def save_report(report_content: str, filepath: str):
    """Saves report to file"""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(report_content)


def save_csv_outputs(players_comparison: pd.DataFrame, analysis_results: Dict):
    """Saves CSV files with results"""
    # Detailed player data
    players_comparison.to_csv(config.OUTPUT_PLAYERS_CSV, index=False, encoding="utf-8")

    # Analysis by devices
    analysis_results["device_analysis"]["full"].to_csv(
        config.OUTPUT_DEVICES_CSV, encoding="utf-8"
    )

    # Analysis by GPU
    analysis_results["gpu_analysis"]["full"].to_csv(
        config.OUTPUT_GPU_CSV, encoding="utf-8"
    )
