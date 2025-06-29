#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Six Keys Criticality Analysis Script

Command-line tool for performing neural criticality analysis using the Six Keys framework.

Usage:
    python analyze.py --help
    python analyze.py --demo
    python analyze.py --input data.csv --output results/
    python analyze.py --config config.yaml

Author: You Yang Hou
License: BSD 3-Clause
"""

import argparse
import sys
import os
import json
import yaml
import pickle
from pathlib import Path
from typing import Dict, Any, Optional

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm

# Add the parent directory to the path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from sixkeys import SixKeysAnalyzer
    from sixkeys.core import FELC, TEB
    from sixkeys.utils.visualization import plot_radar_chart, plot_comprehensive_summary
except ImportError as e:
    print(f"Error importing sixkeys: {e}")
    print("Please ensure the sixkeys package is properly installed.")
    sys.exit(1)


def load_config(config_path: str) -> Dict[str, Any]:
    """
    Load configuration from YAML file.
    
    Parameters
    ----------
    config_path : str
        Path to the configuration file
        
    Returns
    -------
    Dict[str, Any]
        Configuration dictionary
    """
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        return config
    except Exception as e:
        print(f"Error loading config file {config_path}: {e}")
        sys.exit(1)


def load_data(input_path: str) -> np.ndarray:
    """
    Load neural data from various file formats.
    
    Parameters
    ----------
    input_path : str
        Path to the input data file
        
    Returns
    -------
    np.ndarray
        Neural data array
    """
    input_path = Path(input_path)
    
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    try:
        if input_path.suffix.lower() == '.csv':
            data = pd.read_csv(input_path).values
        elif input_path.suffix.lower() in ['.npy']:
            data = np.load(input_path)
        elif input_path.suffix.lower() in ['.pkl', '.pickle']:
            with open(input_path, 'rb') as f:
                data = pickle.load(f)
        elif input_path.suffix.lower() in ['.txt']:
            data = np.loadtxt(input_path)
        else:
            raise ValueError(f"Unsupported file format: {input_path.suffix}")
            
        # Ensure data is 2D
        if data.ndim == 1:
            data = data.reshape(-1, 1)
            
        print(f"Loaded data with shape: {data.shape}")
        return data
        
    except Exception as e:
        print(f"Error loading data from {input_path}: {e}")
        sys.exit(1)


def save_results(results: Dict[str, Any], output_dir: str, format_type: str = 'json'):
    """
    Save analysis results to files.
    
    Parameters
    ----------
    results : Dict[str, Any]
        Analysis results
    output_dir : str
        Output directory
    format_type : str
        Output format ('json', 'pickle', 'csv')
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    if format_type == 'json':
        # Convert numpy types to Python types for JSON serialization
        json_results = {}
        for key, value in results.items():
            if isinstance(value, dict):
                json_results[key] = {k: float(v) if isinstance(v, (np.floating, np.integer)) else v 
                                   for k, v in value.items()}
            else:
                json_results[key] = float(value) if isinstance(value, (np.floating, np.integer)) else value
        
        with open(output_path / 'results.json', 'w', encoding='utf-8') as f:
            json.dump(json_results, f, ensure_ascii=False, indent=2)
            
    elif format_type == 'pickle':
        with open(output_path / 'results.pkl', 'wb') as f:
            pickle.dump(results, f)
            
    elif format_type == 'csv':
        # Create a summary DataFrame
        summary_data = []
        for key, value in results.items():
            if isinstance(value, dict) and 'indicators' in value:
                row = {'state': key, 'total_distance': value.get('total_distance', 0),
                       'classification': value.get('classification', 'unknown')}
                row.update(value['indicators'])
                summary_data.append(row)
        
        if summary_data:
            df = pd.DataFrame(summary_data)
            df.to_csv(output_path / 'results.csv', index=False)
    
    print(f"Results saved to {output_path}")


def run_demo():
    """
    Run a demonstration analysis with simulated data.
    """
    print("Running Six Keys Criticality Demo...")
    print("=" * 50)
    
    # Create analyzer
    analyzer = SixKeysAnalyzer()
    
    # Generate simulated data for different consciousness states
    print("Generating simulated neural data...")
    
    states_data = {
        'awake': np.random.randn(1000, 10) + 0.5,
        'anesthesia': np.random.randn(1000, 10) * 0.3,
        'recovery': np.random.randn(1000, 10) + 0.2
    }
    
    # Analyze each state
    results = {}
    for state_name, data in tqdm(states_data.items(), desc="Analyzing states"):
        print(f"\nAnalyzing {state_name} state...")
        result = analyzer.analyze(data)
        results[state_name] = result
        
        print(f"  Total Distance: {result['total_distance']:.4f}")
        print(f"  Classification: {result['classification']}")
        print(f"  Indicators: {result['indicators']}")
    
    # Generate visualizations
    print("\nGenerating visualizations...")
    
    # Create output directory
    output_dir = Path('demo_results')
    output_dir.mkdir(exist_ok=True)
    
    # Plot radar charts
    fig, axes = plt.subplots(1, 3, figsize=(15, 5), subplot_kw=dict(projection='polar'))
    
    for i, (state_name, result) in enumerate(results.items()):
        indicators = result['indicators']
        values = [indicators.get(key, 0) for key in ['FELC', 'TEB']]
        labels = ['FELC', 'TEB']
        
        angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
        values += values[:1]
        angles += angles[:1]
        
        axes[i].plot(angles, values, 'o-', linewidth=2, label=state_name)
        axes[i].fill(angles, values, alpha=0.25)
        axes[i].set_xticks(angles[:-1])
        axes[i].set_xticklabels(labels)
        axes[i].set_ylim(0, 1)
        axes[i].set_title(f'{state_name.title()} State', size=12, weight='bold')
        axes[i].grid(True)
    
    plt.tight_layout()
    plt.suptitle('Six Keys Criticality Analysis - Demo Results', size=16, weight='bold', y=1.02)
    plt.savefig(output_dir / 'radar_charts.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Save results
    save_results(results, output_dir, 'json')
    save_results(results, output_dir, 'csv')
    
    print(f"\nDemo completed! Results saved to {output_dir}")
    print("\nSummary:")
    for state_name, result in results.items():
        print(f"  {state_name}: Distance={result['total_distance']:.4f}, Class={result['classification']}")


def run_analysis(input_path: str, output_dir: str, config: Optional[Dict[str, Any]] = None):
    """
    Run analysis on real data.
    
    Parameters
    ----------
    input_path : str
        Path to input data file
    output_dir : str
        Output directory for results
    config : Optional[Dict[str, Any]]
        Configuration parameters
    """
    print(f"Running Six Keys Criticality Analysis on {input_path}...")
    print("=" * 60)
    
    # Load data
    print("Loading data...")
    data = load_data(input_path)
    
    # Create analyzer with config parameters
    analyzer_params = {}
    if config and 'analyzer' in config:
        analyzer_params.update(config['analyzer'])
    
    analyzer = SixKeysAnalyzer(**analyzer_params)
    
    # Run analysis
    print("Running analysis...")
    result = analyzer.analyze(data)
    
    print(f"Analysis completed!")
    print(f"Total Distance: {result['total_distance']:.4f}")
    print(f"Classification: {result['classification']}")
    print(f"Indicators: {result['indicators']}")
    
    # Save results
    output_formats = ['json', 'csv']
    if config and 'output' in config:
        output_formats = config['output'].get('formats', output_formats)
    
    for fmt in output_formats:
        save_results({'analysis': result}, output_dir, fmt)
    
    # Generate visualizations if requested
    if config is None or config.get('visualization', {}).get('enabled', True):
        print("Generating visualizations...")
        
        output_path = Path(output_dir)
        
        # Create a simple radar chart
        indicators = result['indicators']
        values = [indicators.get(key, 0) for key in ['FELC', 'TEB']]
        labels = ['FELC', 'TEB']
        
        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))
        
        angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
        values += values[:1]
        angles += angles[:1]
        
        ax.plot(angles, values, 'o-', linewidth=2, color='blue')
        ax.fill(angles, values, alpha=0.25, color='blue')
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels)
        ax.set_ylim(0, 1)
        ax.set_title('Six Keys Criticality Analysis Results', size=14, weight='bold', pad=20)
        ax.grid(True)
        
        plt.tight_layout()
        plt.savefig(output_path / 'analysis_radar.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    print(f"\nAnalysis completed! Results saved to {output_dir}")


def create_sample_config():
    """
    Create a sample configuration file.
    """
    config = {
        'analyzer': {
            'indicators': ['FELC', 'TEB'],
            'classification_threshold': 0.5
        },
        'felc': {
            'simulation_time': 10.0,
            'dt': 0.01,
            'num_samples': 100,
            'in_band_threshold': 0.5,
            'cv_threshold': 0.1
        },
        'teb': {
            'simulation_time': 10.0,
            'dt': 0.01,
            'num_samples': 100
        },
        'output': {
            'formats': ['json', 'csv', 'pickle']
        },
        'visualization': {
            'enabled': True,
            'save_plots': True,
            'plot_format': 'png',
            'dpi': 300
        }
    }
    
    with open('sixkeys_config.yaml', 'w', encoding='utf-8') as f:
        yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
    
    print("Sample configuration file created: sixkeys_config.yaml")


def main():
    """
    Main function for command-line interface.
    """
    parser = argparse.ArgumentParser(
        description="Six Keys Criticality Analysis Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --demo                           # Run demonstration
  %(prog)s --input data.csv --output results/  # Analyze data file
  %(prog)s --config config.yaml --input data.npy  # Use configuration file
  %(prog)s --create-config                  # Create sample config file

Supported input formats: .csv, .npy, .pkl, .txt
Output formats: JSON, CSV, Pickle
        """
    )
    
    parser.add_argument('--demo', action='store_true',
                       help='Run demonstration with simulated data')
    parser.add_argument('--input', '-i', type=str,
                       help='Input data file path')
    parser.add_argument('--output', '-o', type=str, default='results',
                       help='Output directory (default: results)')
    parser.add_argument('--config', '-c', type=str,
                       help='Configuration file path (YAML format)')
    parser.add_argument('--create-config', action='store_true',
                       help='Create a sample configuration file')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose output')
    parser.add_argument('--version', action='version', version='%(prog)s 0.1.0')
    
    args = parser.parse_args()
    
    # Set up logging level
    if args.verbose:
        import logging
        logging.basicConfig(level=logging.INFO)
    
    try:
        if args.create_config:
            create_sample_config()
            return
        
        if args.demo:
            run_demo()
            return
        
        if not args.input:
            parser.error("Either --demo or --input must be specified")
        
        # Load configuration if provided
        config = None
        if args.config:
            config = load_config(args.config)
        
        # Run analysis
        run_analysis(args.input, args.output, config)
        
    except KeyboardInterrupt:
        print("\nAnalysis interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()