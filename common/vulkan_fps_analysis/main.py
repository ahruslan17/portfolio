"""
Main script for analyzing the effect of Vulkan implementation on player FPS
"""

import warnings
import config
import analysis
import report_generator

warnings.filterwarnings("ignore")


def main():
    """Main analysis function"""

    print("=== ANALYSIS OF VALID PLAYERS (WITH VULKAN) ===")

    # Step 1: Prepare data for valid players
    players_comparison, metadata = analysis.prepare_analysis_data(
        config.INPUT_FILE, config.CLIENT_INFO_FILE
    )

    # Step 2: Perform analysis of valid players
    analysis_results = analysis.perform_full_analysis(players_comparison)

    # Step 3: Generate visualizations
    report_generator.generate_all_plots(players_comparison, analysis_results)

    # Step 4: Generate report
    report_content = report_generator.generate_markdown_report(
        players_comparison, metadata, analysis_results
    )
    report_generator.save_report(report_content, config.OUTPUT_REPORT)

    # Step 5: Save CSV files
    report_generator.save_csv_outputs(players_comparison, analysis_results)

    print("=== ANALYSIS COMPLETED ===")
    print(f"Report for valid players: {config.OUTPUT_REPORT}")


if __name__ == "__main__":
    main()
