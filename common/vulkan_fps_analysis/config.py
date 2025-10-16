"""
Vulkan FPS Analysis Configuration
"""

# Files
INPUT_FILE = "offer_fps.csv"
CLIENT_INFO_FILE = "client_info.csv"
OUTPUT_REPORT = "vulkan_analysis_report.md"
OUTPUT_PLAYERS_CSV = "players_comparison_detailed.csv"
OUTPUT_DEVICES_CSV = "devices_analysis.csv"
OUTPUT_GPU_CSV = "gpu_analysis.csv"
PLOTS_DIR = "plots"

# Mission parameters
MISSION_BEFORE = 966  # Before Vulkan implementation
MISSION_AFTER = 967  # After Vulkan implementation

# FPS metrics for analysis
FPS_METRICS = [
    "c_FpsAvg",
    "c_FpsAvgMax",
    "c_FpsAvgMin",
    "c_FpsAvgOnePercentile",
    "c_FpsAvgZeroOnePercentile",
]

# Key metrics for determining improvement
KEY_METRICS = {
    "avg": "c_FpsAvg",
    "min": "c_FpsAvgMin",
    "percentile_1": "c_FpsAvgOnePercentile",
}

# Analysis parameters
MIN_PLAYERS_FOR_DEVICE_GPU = 3  # Minimum players for statistical significance
IMPROVEMENT_THRESHOLD = 0.7  # >70% players = stable improvement
WORSENING_THRESHOLD = 0.3  # <30% players = stable worsening
SIGNIFICANCE_LEVEL = 0.05  # Significance level for t-test
MINIMUM_CHANGE_THRESHOLD = (
    1.0  # Minimum FPS change to determine improvement/worsening (in FPS)
)

# Visualization parameters
PLOT_DPI = 300
PLOT_STYLE = "seaborn-v0_8-darkgrid"
PLOT_PALETTE = "husl"
DEFAULT_FIGSIZE = (12, 6)
DEFAULT_FONTSIZE = 10

# Colors for visualizations
COLOR_IMPROVED = "#2ecc71"
COLOR_UNCHANGED = "#f39c12"
COLOR_WORSENED = "#e74c3c"
COLOR_GREEN = "green"
COLOR_ORANGE = "orange"
COLOR_RED = "red"
