#!/usr/bin/env python3
"""Demonstration Script for SixKeys Visualization Modules

This script demonstrates how to use the optional visualization modules
in the sixkeys.demos package. These modules provide integrated visualizations
for the six key indicators of consciousness analysis.

Usage:
    python demo_visualization.py [--module MODULE] [--no-plots] [--save]
    
Modules:
    - radar: Six Keys Radar Chart
    - public: Public Data Re-analysis
    - cross: Cross-Validation Analysis
    - all: Run all demonstrations (default)
"""

import argparse
import sys
import os
from pathlib import Path

# Add the sixkeys package to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from sixkeys.demos import (
        SixKeysRadarChart, 
        PublicDataAnalysis, 
        CrossValidationAnalysis,
        check_demo_dependencies
    )
except ImportError as e:
    print(f"Error importing sixkeys.demos: {e}")
    print("Please ensure the sixkeys package is properly installed.")
    sys.exit(1)


def run_radar_demo(show_plots=True, save_files=False, output_dir="./"):
    """Run the Six Keys Radar Chart demonstration."""
    print("\n" + "="*60)
    print("SIX KEYS RADAR CHART DEMONSTRATION")
    print("="*60)
    
    try:
        radar = SixKeysRadarChart()
        fig_radar, fig_bar = radar.simulate_and_plot(
            show_plots=show_plots,
            save_plots=save_files,
            output_dir=output_dir
        )
        print("✓ Radar chart demonstration completed successfully.")
        return True
    except Exception as e:
        print(f"✗ Error in radar chart demo: {e}")
        return False


def run_public_data_demo(show_plots=True, save_files=False, output_dir="./"):
    """Run the Public Data Re-analysis demonstration."""
    print("\n" + "="*60)
    print("PUBLIC DATA RE-ANALYSIS DEMONSTRATION")
    print("="*60)
    
    try:
        analyzer = PublicDataAnalysis()
        fig, summary = analyzer.generate_and_analyze(
            show_plots=show_plots,
            save_files=save_files,
            output_dir=output_dir
        )
        print("✓ Public data analysis demonstration completed successfully.")
        return True
    except Exception as e:
        print(f"✗ Error in public data demo: {e}")
        return False


def run_cross_validation_demo(show_plots=True, save_files=False, output_dir="./"):
    """Run the Cross-Validation Analysis demonstration."""
    print("\n" + "="*60)
    print("CROSS-VALIDATION ANALYSIS DEMONSTRATION")
    print("="*60)
    
    try:
        cv = CrossValidationAnalysis()
        fig, results = cv.generate_and_analyze(
            show_plots=show_plots,
            save_files=save_files,
            output_dir=output_dir
        )
        print("✓ Cross-validation demonstration completed successfully.")
        return True
    except Exception as e:
        print(f"✗ Error in cross-validation demo: {e}")
        return False


def main():
    """Main demonstration function."""
    parser = argparse.ArgumentParser(
        description="SixKeys Visualization Demonstrations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  python demo_visualization.py                    # Run all demos with plots
  python demo_visualization.py --module radar     # Run only radar chart demo
  python demo_visualization.py --no-plots --save  # Save files without showing plots
  python demo_visualization.py --output results/  # Save to specific directory
        """
    )
    
    parser.add_argument(
        '--module', 
        choices=['radar', 'public', 'cross', 'all'],
        default='all',
        help='Which demonstration module to run (default: all)'
    )
    
    parser.add_argument(
        '--no-plots',
        action='store_true',
        help='Do not display plots (useful for headless environments)'
    )
    
    parser.add_argument(
        '--save',
        action='store_true',
        help='Save generated plots and data files'
    )
    
    parser.add_argument(
        '--output',
        default='./',
        help='Output directory for saved files (default: current directory)'
    )
    
    args = parser.parse_args()
    
    # Check dependencies
    print("Checking demonstration dependencies...")
    if not check_demo_dependencies():
        print("\nSome dependencies are missing. Install them with:")
        print("pip install matplotlib seaborn scipy pandas")
        return 1
    
    print("✓ All dependencies are available.")
    
    # Create output directory if needed
    if args.save:
        os.makedirs(args.output, exist_ok=True)
        print(f"Output directory: {os.path.abspath(args.output)}")
    
    show_plots = not args.no_plots
    success_count = 0
    total_count = 0
    
    # Run demonstrations
    if args.module in ['radar', 'all']:
        total_count += 1
        if run_radar_demo(show_plots, args.save, args.output):
            success_count += 1
    
    if args.module in ['public', 'all']:
        total_count += 1
        if run_public_data_demo(show_plots, args.save, args.output):
            success_count += 1
    
    if args.module in ['cross', 'all']:
        total_count += 1
        if run_cross_validation_demo(show_plots, args.save, args.output):
            success_count += 1
    
    # Summary
    print("\n" + "="*60)
    print("DEMONSTRATION SUMMARY")
    print("="*60)
    print(f"Completed: {success_count}/{total_count} demonstrations")
    
    if success_count == total_count:
        print("🎉 All demonstrations completed successfully!")
        print("\nThese visualization modules are now ready for use in your analysis.")
        print("You can import them directly:")
        print("  from sixkeys.demos import SixKeysRadarChart, PublicDataAnalysis, CrossValidationAnalysis")
        return 0
    else:
        print("⚠️  Some demonstrations failed. Check the error messages above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())