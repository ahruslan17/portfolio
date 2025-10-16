"""
Analysis logic for the effect of Vulkan implementation on player FPS
"""

import pandas as pd
import numpy as np
from scipy import stats
from typing import Tuple, Dict, Set

import config


def load_data(filepath: str) -> pd.DataFrame:
    """Loads data from CSV file"""
    return pd.read_csv(filepath)


def load_and_merge_data(
    offer_fps_filepath: str, client_info_filepath: str
) -> pd.DataFrame:
    """Loads and merges offer_fps and client_info data by SessionId"""
    # Load data
    offer_fps_df = pd.read_csv(offer_fps_filepath)
    client_info_df = pd.read_csv(client_info_filepath)

    # Merge by SessionId, adding c_GraphicsDeviceType field
    merged_df = offer_fps_df.merge(
        client_info_df[["SessionId", "c_GraphicsDeviceType"]],
        on="SessionId",
        how="left",
    )

    return merged_df


def split_by_mission(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Splits data into before and after Vulkan"""
    df_before = df[df["s_MissionId"] == config.MISSION_BEFORE].copy()
    df_after = df[df["s_MissionId"] == config.MISSION_AFTER].copy()
    return df_before, df_after


def validate_vulkan_pairs(
    df_before: pd.DataFrame, df_after: pd.DataFrame
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Validates pairs - mission 967 should have Vulkan
    Returns:
        valid_before: before data for valid pairs
        valid_after: after data for valid pairs
        invalid_pairs: invalid pairs for reporting
    """
    # Find players with Vulkan on mission 967
    vulkan_players = set(
        df_after[df_after["c_GraphicsDeviceType"] == "Vulkan"]["AccountId"].unique()
    )

    # Find players who are in both missions
    accounts_before = set(df_before["AccountId"].unique())
    accounts_after = set(df_after["AccountId"].unique())
    accounts_both = accounts_before & accounts_after

    # Find invalid pairs (players who are in both missions but don't have Vulkan on 967)
    invalid_accounts = accounts_both - vulkan_players

    # Create DataFrame with invalid pairs (grouped by device and GPU)
    invalid_pairs = df_after[df_after["AccountId"].isin(invalid_accounts)][
        ["AccountId", "c_GraphicsDeviceType", "DeviceModel", "c_GraphicsDeviceName"]
    ].drop_duplicates()

    # Filter data only for valid players (exclude invalid pairs)
    valid_before = df_before[df_before["AccountId"].isin(vulkan_players)].copy()
    valid_after = df_after[df_after["AccountId"].isin(vulkan_players)].copy()

    return valid_before, valid_after, invalid_pairs


def find_matched_accounts(
    df_before: pd.DataFrame, df_after: pd.DataFrame
) -> Tuple[Set, Set, Set]:
    """Finds players who took the test before and after"""
    accounts_before = set(df_before["AccountId"].unique())
    accounts_after = set(df_after["AccountId"].unique())
    accounts_both = accounts_before & accounts_after
    return accounts_before, accounts_after, accounts_both


def filter_matched_players(
    df_before: pd.DataFrame, df_after: pd.DataFrame, accounts_both: Set
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Filters data only for players who took both tests"""
    df_before_matched = df_before[df_before["AccountId"].isin(accounts_both)].copy()
    df_after_matched = df_after[df_after["AccountId"].isin(accounts_both)].copy()
    return df_before_matched, df_after_matched


def aggregate_player_data(df_subset: pd.DataFrame) -> pd.DataFrame:
    """Aggregates data by player (median value)"""
    agg_dict = {
        "c_FpsAvg": "median",
        "c_FpsAvgMax": "median",
        "c_FpsAvgMin": "median",
        "c_FpsAvgOnePercentile": "median",
        "c_FpsAvgZeroOnePercentile": "median",
        "DeviceModel": "first",
        "c_GraphicsDeviceName": "first",
    }
    return df_subset.groupby("AccountId").agg(agg_dict).reset_index()


def merge_before_after(
    players_before: pd.DataFrame, players_after: pd.DataFrame
) -> pd.DataFrame:
    """Merges before and after data with column renaming"""
    players_before.columns = ["AccountId"] + [
        f"{col}_before" for col in players_before.columns[1:]
    ]
    players_after.columns = ["AccountId"] + [
        f"{col}_after" for col in players_after.columns[1:]
    ]
    return players_before.merge(players_after, on="AccountId")


def calculate_deltas(players_comparison: pd.DataFrame) -> pd.DataFrame:
    """Calculates absolute and percentage FPS changes"""
    for metric in config.FPS_METRICS:
        # Absolute change
        players_comparison[f"{metric}_delta"] = (
            players_comparison[f"{metric}_after"]
            - players_comparison[f"{metric}_before"]
        )

        # Percentage change
        players_comparison[f"{metric}_pct_change"] = (
            players_comparison[f"{metric}_delta"]
            / players_comparison[f"{metric}_before"].replace(0, np.nan)
        ) * 100

    return players_comparison


def calculate_improvement_flags(players_comparison: pd.DataFrame) -> pd.DataFrame:
    """Determines improvement flags for key metrics"""
    # Determine status for each metric: 1 = improved, 0 = unchanged, -1 = worsened
    players_comparison["fps_avg_status"] = players_comparison[
        f"{config.KEY_METRICS['avg']}_delta"
    ].apply(
        lambda x: (
            1
            if x > config.MINIMUM_CHANGE_THRESHOLD
            else (0 if abs(x) <= config.MINIMUM_CHANGE_THRESHOLD else -1)
        )
    )
    players_comparison["fps_min_status"] = players_comparison[
        f"{config.KEY_METRICS['min']}_delta"
    ].apply(
        lambda x: (
            1
            if x > config.MINIMUM_CHANGE_THRESHOLD
            else (0 if abs(x) <= config.MINIMUM_CHANGE_THRESHOLD else -1)
        )
    )
    players_comparison["fps_1pct_status"] = players_comparison[
        f"{config.KEY_METRICS['percentile_1']}_delta"
    ].apply(
        lambda x: (
            1
            if x > config.MINIMUM_CHANGE_THRESHOLD
            else (0 if abs(x) <= config.MINIMUM_CHANGE_THRESHOLD else -1)
        )
    )

    # Count improvements, worsenings and unchanged
    players_comparison["improvements_count"] = (
        (players_comparison["fps_avg_status"] == 1).astype(int)
        + (players_comparison["fps_min_status"] == 1).astype(int)
        + (players_comparison["fps_1pct_status"] == 1).astype(int)
    )
    players_comparison["worsenings_count"] = (
        (players_comparison["fps_avg_status"] == -1).astype(int)
        + (players_comparison["fps_min_status"] == -1).astype(int)
        + (players_comparison["fps_1pct_status"] == -1).astype(int)
    )
    players_comparison["unchanged_count"] = (
        (players_comparison["fps_avg_status"] == 0).astype(int)
        + (players_comparison["fps_min_status"] == 0).astype(int)
        + (players_comparison["fps_1pct_status"] == 0).astype(int)
    )

    # New evaluation logic:
    # - if 2/3 metrics improved = result - improvement
    # - if 3/3 metrics unchanged = result - unchanged
    # - if 1/3 improved, 2/3 unchanged = result - improvement
    # - otherwise worsened
    def determine_overall_status(row):
        improvements = row["improvements_count"]
        unchanged = row["unchanged_count"]

        # If 2+ metrics improved = improvement
        if improvements >= 2:
            return "improved"

        # If all 3 metrics unchanged = unchanged
        if unchanged == 3:
            return "unchanged"

        # If 1 improved and 2 unchanged = improvement
        if improvements == 1 and unchanged == 2:
            return "improved"

        # In all other cases = worsening
        return "worsened"

    players_comparison["overall_status"] = players_comparison.apply(
        determine_overall_status, axis=1
    )

    # Convert numeric statuses to text for backward compatibility
    def status_to_text(status):
        if status == 1:
            return "improved"
        elif status == 0:
            return "unchanged"
        else:  # status == -1
            return "worsened"

    players_comparison["fps_avg_improved"] = players_comparison["fps_avg_status"].apply(
        status_to_text
    )
    players_comparison["fps_min_improved"] = players_comparison["fps_min_status"].apply(
        status_to_text
    )
    players_comparison["fps_1pct_improved"] = players_comparison[
        "fps_1pct_status"
    ].apply(status_to_text)
    players_comparison["overall_improved"] = players_comparison["overall_status"]

    return players_comparison


def calculate_overall_stats(players_comparison: pd.DataFrame) -> Dict:
    """Calculates overall statistics for changes"""
    improved_count = (players_comparison["overall_status"] == "improved").sum()
    unchanged_count = (players_comparison["overall_status"] == "unchanged").sum()
    worsened_count = (players_comparison["overall_status"] == "worsened").sum()
    total_count = len(players_comparison)

    stats_dict = {
        "improved_count": int(improved_count),
        "unchanged_count": int(unchanged_count),
        "worsened_count": int(worsened_count),
        "total_count": total_count,
        "improved_pct": (improved_count / total_count * 100) if total_count > 0 else 0,
        "unchanged_pct": (
            (unchanged_count / total_count * 100) if total_count > 0 else 0
        ),
        "worsened_pct": (worsened_count / total_count * 100) if total_count > 0 else 0,
    }

    # Statistics by metrics
    for metric_key, metric_name in config.KEY_METRICS.items():
        before_mean = players_comparison[f"{metric_name}_before"].mean()
        after_mean = players_comparison[f"{metric_name}_after"].mean()
        delta_mean = players_comparison[f"{metric_name}_delta"].mean()

        # Correct percentage change calculation: from mean values
        pct_change = (delta_mean / before_mean * 100) if before_mean != 0 else 0

        stats_dict[f"{metric_key}_before_mean"] = before_mean
        stats_dict[f"{metric_key}_before_std"] = players_comparison[
            f"{metric_name}_before"
        ].std()
        stats_dict[f"{metric_key}_after_mean"] = after_mean
        stats_dict[f"{metric_key}_after_std"] = players_comparison[
            f"{metric_name}_after"
        ].std()
        stats_dict[f"{metric_key}_delta_mean"] = delta_mean
        stats_dict[f"{metric_key}_delta_std"] = players_comparison[
            f"{metric_name}_delta"
        ].std()
        stats_dict[f"{metric_key}_pct_change_mean"] = pct_change

    return stats_dict


def perform_statistical_tests(players_comparison: pd.DataFrame) -> Dict:
    """Performs paired t-tests for key metrics"""
    test_results = {}

    for metric_key, metric_name in config.KEY_METRICS.items():
        before_values = players_comparison[f"{metric_name}_before"]
        after_values = players_comparison[f"{metric_name}_after"]

        t_stat, p_value = stats.ttest_rel(after_values, before_values)

        test_results[metric_key] = {
            "metric_name": metric_name,
            "t_statistic": t_stat,
            "p_value": p_value,
            "is_significant": p_value < config.SIGNIFICANCE_LEVEL,
            "direction": "improvement" if t_stat > 0 else "worsening",
        }

    return test_results


def _aggregate_analysis_data(
    players_comparison: pd.DataFrame, group_by
) -> pd.DataFrame:
    """Common function for aggregating analysis data"""
    analysis = (
        players_comparison.groupby(group_by)
        .agg(
            {
                "AccountId": "count",
                "c_FpsAvg_before": "mean",
                "c_FpsAvgMin_before": "mean",
                "c_FpsAvgOnePercentile_before": "mean",
                "c_FpsAvg_after": "mean",
                "c_FpsAvgMin_after": "mean",
                "c_FpsAvgOnePercentile_after": "mean",
                "c_FpsAvg_delta": "mean",
                "c_FpsAvgMin_delta": "mean",
                "c_FpsAvgOnePercentile_delta": "mean",
                "overall_status": lambda x: (x == "improved").mean(),
            }
        )
        .rename(
            columns={
                "AccountId": "player_count",
                "overall_status": "improvement_rate",
            }
        )
    )
    return analysis.sort_values("player_count", ascending=False)


def analyze_by_device(players_comparison: pd.DataFrame) -> pd.DataFrame:
    """Analysis by devices"""
    return _aggregate_analysis_data(players_comparison, "DeviceModel_before")


def analyze_by_gpu(players_comparison: pd.DataFrame) -> pd.DataFrame:
    """Analysis by GPU"""
    return _aggregate_analysis_data(players_comparison, "c_GraphicsDeviceName_before")


def filter_by_min_players(
    analysis_df: pd.DataFrame, min_players: int = None
) -> pd.DataFrame:
    """Filters devices/GPU by minimum number of players"""
    if min_players is None:
        min_players = config.MIN_PLAYERS_FOR_DEVICE_GPU
    return analysis_df[analysis_df["player_count"] >= min_players].copy()


def classify_improved_worsened(
    analysis_df: pd.DataFrame,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Classifies devices/GPU into improved and worsened"""
    improved = analysis_df[
        analysis_df["improvement_rate"] > config.IMPROVEMENT_THRESHOLD
    ]
    worsened = analysis_df[analysis_df["improvement_rate"] < config.WORSENING_THRESHOLD]
    return improved, worsened


def get_dataset_stats(
    df: pd.DataFrame,
    df_before: pd.DataFrame,
    df_after: pd.DataFrame,
    df_before_valid: pd.DataFrame,
    df_after_valid: pd.DataFrame,
) -> Dict:
    """Gets dataset statistics"""
    return {
        "total_records": len(df),
        "records_before": len(df_before),
        "records_after": len(df_after),
        "records_before_valid": len(df_before_valid),
        "records_after_valid": len(df_after_valid),
    }


def get_account_stats(
    accounts_before: Set,
    accounts_after: Set,
    accounts_both: Set,
    accounts_before_valid: Set,
    accounts_after_valid: Set,
    accounts_both_valid: Set,
) -> Dict:
    """Gets player statistics"""
    return {
        "unique_before": len(accounts_before),
        "unique_after": len(accounts_after),
        "both": len(accounts_both),
        "unique_before_valid": len(accounts_before_valid),
        "unique_after_valid": len(accounts_after_valid),
        "both_valid": len(accounts_both_valid),
    }


def prepare_analysis_data(
    offer_fps_filepath: str, client_info_filepath: str
) -> Tuple[pd.DataFrame, Dict]:
    """
    Main function for preparing data for analysis

    Returns:
        players_comparison: DataFrame with player comparison
        metadata: Dictionary with analysis metadata
    """
    # Load and merge data
    df = load_and_merge_data(offer_fps_filepath, client_info_filepath)

    # Split by missions
    df_before, df_after = split_by_mission(df)

    # Validate pairs (Vulkan on mission 967)
    df_before_valid, df_after_valid, invalid_pairs = validate_vulkan_pairs(
        df_before, df_after
    )

    # Find players who took both tests (valid only)
    accounts_before, accounts_after, accounts_both = find_matched_accounts(
        df_before_valid, df_after_valid
    )

    # Filter data
    df_before_matched, df_after_matched = filter_matched_players(
        df_before_valid, df_after_valid, accounts_both
    )

    # Aggregate by players
    players_before = aggregate_player_data(df_before_matched)
    players_after = aggregate_player_data(df_after_matched)

    # Merge data
    players_comparison = merge_before_after(players_before, players_after)

    # Calculate changes
    players_comparison = calculate_deltas(players_comparison)
    players_comparison = calculate_improvement_flags(players_comparison)

    # Metadata
    metadata = {
        "dataset_stats": get_dataset_stats(
            df, df_before, df_after, df_before_valid, df_after_valid
        ),
        "account_stats": get_account_stats(
            accounts_before,
            accounts_after,
            accounts_both,
            set(df_before_valid["AccountId"].unique()),
            set(df_after_valid["AccountId"].unique()),
            accounts_both,
        ),
        "matched_records_before": len(df_before_matched),
        "matched_records_after": len(df_after_matched),
        "players_in_comparison": len(players_comparison),
        "invalid_pairs": invalid_pairs,
        "invalid_pairs_count": len(invalid_pairs),
    }

    return players_comparison, metadata


def perform_full_analysis(
    players_comparison: pd.DataFrame,
) -> Dict:
    """
    Performs full data analysis

    Returns:
        Dictionary with results of all analyses
    """
    results = {}

    # Overall statistics
    results["overall_stats"] = calculate_overall_stats(players_comparison)

    # Statistical tests
    results["statistical_tests"] = perform_statistical_tests(players_comparison)

    # Analysis by devices
    device_analysis = analyze_by_device(players_comparison)
    device_analysis_filtered = filter_by_min_players(device_analysis)
    devices_improved, devices_worsened = classify_improved_worsened(
        device_analysis_filtered
    )

    results["device_analysis"] = {
        "full": device_analysis,
        "filtered": device_analysis_filtered,
        "improved": devices_improved,
        "worsened": devices_worsened,
    }

    # Analysis by GPU
    gpu_analysis = analyze_by_gpu(players_comparison)
    gpu_analysis_filtered = filter_by_min_players(gpu_analysis)
    gpu_improved, gpu_worsened = classify_improved_worsened(gpu_analysis_filtered)

    results["gpu_analysis"] = {
        "full": gpu_analysis,
        "filtered": gpu_analysis_filtered,
        "improved": gpu_improved,
        "worsened": gpu_worsened,
    }

    return results
