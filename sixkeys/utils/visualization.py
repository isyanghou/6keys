#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Visualization utilities for Six Keys Criticality framework.

六鑰臨界可視化工具：提供統一的繪圖和可視化功能

This module provides comprehensive visualization tools for the Six Keys
Criticality framework, including radar charts, phase diagrams, and summary plots.
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Optional, Tuple, Any, Union
import warnings
from matplotlib.patches import Circle
from matplotlib.collections import LineCollection


def setup_plot_style(style: str = 'seaborn-v0_8', dpi: int = 120, 
                    font_size: int = 11) -> None:
    """
    Setup consistent plotting style for all visualizations.
    
    Parameters
    ----------
    style : str, default='seaborn-v0_8'
        Matplotlib style to use
    dpi : int, default=120
        Figure DPI for high-quality plots
    font_size : int, default=11
        Base font size
    """
    try:
        plt.style.use(style)
    except OSError:
        # Fallback to default style if seaborn not available
        plt.style.use('default')
        warnings.warn(f"Style '{style}' not available, using default")
    
    plt.rcParams.update({
        'figure.dpi': dpi,
        'font.size': font_size,
        'axes.labelsize': font_size,
        'axes.titlesize': font_size + 2,
        'xtick.labelsize': font_size - 1,
        'ytick.labelsize': font_size - 1,
        'legend.fontsize': font_size - 1,
        'figure.titlesize': font_size + 4,
        'axes.grid': True,
        'grid.alpha': 0.3,
    })


def plot_radar_chart(results: Dict[str, Dict], 
                    zeta_names: Optional[List[str]] = None,
                    figsize: Tuple[int, int] = (8, 8),
                    title: str = 'Six Keys Criticality Radar Chart',
                    colors: Optional[List[str]] = None) -> plt.Figure:
    """
    Create radar chart for ζ indicators across different states.
    
    Parameters
    ----------
    results : dict
        Dictionary with state names as keys and results as values
    zeta_names : list, optional
        List of ζ indicator names to plot
    figsize : tuple, default=(8, 8)
        Figure size
    title : str, default='Six Keys Criticality Radar Chart'
        Chart title
    colors : list, optional
        Colors for each state
        
    Returns
    -------
    fig : matplotlib.figure.Figure
        Figure object
    """
    # Extract ζ values
    if zeta_names is None:
        # Auto-detect from results
        all_zetas = set()
        for result in results.values():
            if hasattr(result, 'zeta_values'):
                all_zetas.update(result.zeta_values.keys())
            elif isinstance(result, dict) and 'zeta_values' in result:
                all_zetas.update(result['zeta_values'].keys())
            else:
                # Try to extract zeta values directly
                for key in result.keys():
                    if key.startswith('zeta') or key.startswith('z'):
                        all_zetas.add(key)
        zeta_names = sorted(list(all_zetas))
    
    n_indicators = len(zeta_names)
    if n_indicators == 0:
        raise ValueError("No ζ indicators found in results")
    
    # Setup colors
    if colors is None:
        colors = ['tab:green', 'tab:orange', 'tab:red', 'tab:blue', 'tab:purple']
    
    # Create radar chart
    fig, ax = plt.subplots(figsize=figsize, subplot_kw=dict(projection='polar'))
    
    # Angles for each indicator
    angles = np.linspace(0, 2 * np.pi, n_indicators, endpoint=False).tolist()
    angles += angles[:1]  # Complete the circle
    
    # Plot each state
    for i, (state_name, result) in enumerate(results.items()):
        values = []
        
        # Extract values for each ζ indicator
        for zeta_name in zeta_names:
            if hasattr(result, 'zeta_values'):
                value = result.zeta_values.get(zeta_name, 0.0)
            elif isinstance(result, dict):
                if 'zeta_values' in result:
                    value = result['zeta_values'].get(zeta_name, 0.0)
                else:
                    value = result.get(zeta_name, 0.0)
            else:
                value = 0.0
            values.append(value)
        
        values += values[:1]  # Complete the circle
        
        color = colors[i % len(colors)]
        ax.plot(angles, values, 'o-', linewidth=2, label=state_name, 
               color=color, markersize=6)
        ax.fill(angles, values, alpha=0.25, color=color)
    
    # Customize chart
    ax.set_xticks(angles[:-1])
    
    # Create nice labels
    labels = []
    for i, zeta in enumerate(zeta_names):
        if zeta.startswith('zeta'):
            num = zeta.replace('zeta', '')
            labels.append(f'ζ{num}')
        else:
            labels.append(zeta)
    
    ax.set_xticklabels(labels)
    ax.set_ylim(-2, 2)
    ax.set_title(title, size=16, pad=20)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
    ax.grid(True)
    
    # Add reference circles
    for radius in [0.5, 1.0, 1.5]:
        circle = Circle((0, 0), radius, fill=False, color='gray', 
                       alpha=0.3, linestyle='--', transform=ax.transData._b)
    
    plt.tight_layout()
    return fig


def plot_phase_diagram(results: Dict[str, Dict],
                      theta_c: float = 1.0,
                      figsize: Tuple[int, int] = (12, 5),
                      title: str = 'Criticality Phase Diagram') -> plt.Figure:
    """
    Create phase diagram showing D_total vs θ_c and phase space.
    
    Parameters
    ----------
    results : dict
        Dictionary with state names as keys and results as values
    theta_c : float, default=1.0
        Critical threshold
    figsize : tuple, default=(12, 5)
        Figure size
    title : str, default='Criticality Phase Diagram'
        Chart title
        
    Returns
    -------
    fig : matplotlib.figure.Figure
        Figure object
    """
    fig, axes = plt.subplots(1, 2, figsize=figsize)
    
    # Extract data
    state_names = list(results.keys())
    d_totals = []
    consciousness_states = []
    
    for state in state_names:
        result = results[state]
        if hasattr(result, 'd_total'):
            d_totals.append(result.d_total)
            consciousness_states.append(result.consciousness_state)
        elif isinstance(result, dict):
            d_totals.append(result.get('D_w', result.get('d_total', 0.0)))
            # Determine consciousness state
            d_val = d_totals[-1]
            consciousness_states.append('Conscious' if d_val < theta_c else 'Non-conscious')
    
    # Color mapping
    color_map = {'Conscious': 'green', 'Non-conscious': 'red'}
    colors = [color_map.get(state, 'blue') for state in consciousness_states]
    
    # Plot 1: D_total comparison
    ax1 = axes[0]
    bars = ax1.bar(state_names, d_totals, color=colors, alpha=0.7, edgecolor='black')
    ax1.axhline(theta_c, color='black', linestyle='--', linewidth=2,
               label=f'θc = {theta_c}')
    ax1.set_ylabel('D_total / D_w')
    ax1.set_title('Total Pipeline Distance')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Add value labels
    for bar, value in zip(bars, d_totals):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                f'{value:.3f}', ha='center', va='bottom', fontweight='bold')
    
    # Add consciousness/non-consciousness regions
    ax1.axhspan(0, theta_c, alpha=0.1, color='green', label='Conscious Region')
    ax1.axhspan(theta_c, max(d_totals) * 1.1, alpha=0.1, color='red', 
               label='Non-conscious Region')
    
    # Plot 2: Phase space (if we have multiple indicators)
    ax2 = axes[1]
    
    # Try to extract two ζ values for phase space
    zeta_values_all = {}
    for state_name, result in results.items():
        if hasattr(result, 'zeta_values'):
            zeta_values_all[state_name] = result.zeta_values
        elif isinstance(result, dict):
            if 'zeta_values' in result:
                zeta_values_all[state_name] = result['zeta_values']
            else:
                # Try to extract zeta values directly
                zeta_vals = {}
                for key, value in result.items():
                    if key.startswith('zeta') or key.startswith('z'):
                        zeta_vals[key] = value
                zeta_values_all[state_name] = zeta_vals
    
    if zeta_values_all and len(list(zeta_values_all.values())[0]) >= 2:
        # Get first two ζ indicators
        zeta_names = list(list(zeta_values_all.values())[0].keys())[:2]
        
        x_vals = [zeta_values_all[state][zeta_names[0]] for state in state_names]
        y_vals = [zeta_values_all[state][zeta_names[1]] for state in state_names]
        
        # Create scatter plot
        scatter = ax2.scatter(x_vals, y_vals, c=colors, s=150, alpha=0.7, 
                            edgecolors='black', linewidth=2)
        
        # Add state labels
        for i, state in enumerate(state_names):
            ax2.annotate(state, (x_vals[i], y_vals[i]), 
                       xytext=(10, 10), textcoords='offset points',
                       fontweight='bold', fontsize=10,
                       bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7))
        
        # Create nice labels
        xlabel = zeta_names[0]
        ylabel = zeta_names[1]
        if xlabel.startswith('zeta'):
            xlabel = f'ζ{xlabel.replace("zeta", "")}'
        if ylabel.startswith('zeta'):
            ylabel = f'ζ{ylabel.replace("zeta", "")}'
        
        ax2.set_xlabel(xlabel)
        ax2.set_ylabel(ylabel)
        ax2.set_title('Phase Space')
        ax2.grid(True, alpha=0.3)
        ax2.axhline(0, color='black', linewidth=0.5)
        ax2.axvline(0, color='black', linewidth=0.5)
        
        # Add quadrant labels
        xlim = ax2.get_xlim()
        ylim = ax2.get_ylim()
        ax2.text(xlim[1]*0.8, ylim[1]*0.8, 'Q1', fontsize=12, alpha=0.5)
        ax2.text(xlim[0]*0.8, ylim[1]*0.8, 'Q2', fontsize=12, alpha=0.5)
        ax2.text(xlim[0]*0.8, ylim[0]*0.8, 'Q3', fontsize=12, alpha=0.5)
        ax2.text(xlim[1]*0.8, ylim[0]*0.8, 'Q4', fontsize=12, alpha=0.5)
        
    else:
        ax2.text(0.5, 0.5, 'Phase space requires\n≥2 indicators', 
                ha='center', va='center', transform=ax2.transAxes,
                fontsize=14, bbox=dict(boxstyle='round', facecolor='lightgray'))
        ax2.set_title('Phase Space (Not Available)')
    
    fig.suptitle(title, fontsize=16, fontweight='bold')
    plt.tight_layout()
    return fig


def plot_time_series(data: Dict[str, np.ndarray],
                    figsize: Tuple[int, int] = (12, 8),
                    title: str = 'Time Series Analysis') -> plt.Figure:
    """
    Plot time series data for multiple indicators.
    
    Parameters
    ----------
    data : dict
        Dictionary with indicator names as keys and time series as values
    figsize : tuple, default=(12, 8)
        Figure size
    title : str, default='Time Series Analysis'
        Chart title
        
    Returns
    -------
    fig : matplotlib.figure.Figure
        Figure object
    """
    n_series = len(data)
    fig, axes = plt.subplots(n_series, 1, figsize=figsize, sharex=True)
    
    if n_series == 1:
        axes = [axes]
    
    colors = plt.cm.tab10(np.linspace(0, 1, n_series))
    
    for i, (name, series) in enumerate(data.items()):
        ax = axes[i]
        
        if isinstance(series, dict) and 'time' in series and 'values' in series:
            time = series['time']
            values = series['values']
        else:
            time = np.arange(len(series))
            values = series
        
        ax.plot(time, values, color=colors[i], linewidth=1.5, label=name)
        ax.set_ylabel(name)
        ax.grid(True, alpha=0.3)
        ax.legend()
    
    axes[-1].set_xlabel('Time')
    fig.suptitle(title, fontsize=16, fontweight='bold')
    plt.tight_layout()
    return fig


def plot_criticality_summary(results: Dict[str, Dict],
                            theta_c: float = 1.0,
                            figsize: Tuple[int, int] = (15, 10)) -> plt.Figure:
    """
    Create comprehensive summary plot with multiple visualizations.
    
    Parameters
    ----------
    results : dict
        Dictionary with state names as keys and results as values
    theta_c : float, default=1.0
        Critical threshold
    figsize : tuple, default=(15, 10)
        Figure size
        
    Returns
    -------
    fig : matplotlib.figure.Figure
        Figure object
    """
    fig = plt.figure(figsize=figsize)
    
    # Create grid layout
    gs = fig.add_gridspec(2, 3, hspace=0.3, wspace=0.3)
    
    # 1. Radar chart (top left)
    ax1 = fig.add_subplot(gs[0, 0], projection='polar')
    
    # Extract ζ values for radar chart
    zeta_names = []
    if results:
        first_result = list(results.values())[0]
        if hasattr(first_result, 'zeta_values'):
            zeta_names = list(first_result.zeta_values.keys())
        elif isinstance(first_result, dict):
            if 'zeta_values' in first_result:
                zeta_names = list(first_result['zeta_values'].keys())
            else:
                for key in first_result.keys():
                    if key.startswith('zeta') or key.startswith('z'):
                        zeta_names.append(key)
    
    if zeta_names:
        angles = np.linspace(0, 2 * np.pi, len(zeta_names), endpoint=False).tolist()
        angles += angles[:1]
        
        colors = ['tab:green', 'tab:orange', 'tab:red', 'tab:blue']
        
        for i, (state_name, result) in enumerate(results.items()):
            values = []
            for zeta_name in zeta_names:
                if hasattr(result, 'zeta_values'):
                    value = result.zeta_values.get(zeta_name, 0.0)
                elif isinstance(result, dict):
                    if 'zeta_values' in result:
                        value = result['zeta_values'].get(zeta_name, 0.0)
                    else:
                        value = result.get(zeta_name, 0.0)
                else:
                    value = 0.0
                values.append(value)
            
            values += values[:1]
            color = colors[i % len(colors)]
            ax1.plot(angles, values, 'o-', linewidth=2, label=state_name, color=color)
            ax1.fill(angles, values, alpha=0.25, color=color)
        
        ax1.set_xticks(angles[:-1])
        ax1.set_xticklabels([f'ζ{i+1}' for i in range(len(zeta_names))])
        ax1.set_ylim(-2, 2)
        ax1.set_title('Radar Chart', pad=20)
        ax1.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
    
    # 2. D_total comparison (top middle)
    ax2 = fig.add_subplot(gs[0, 1])
    
    state_names = list(results.keys())
    d_totals = []
    for state in state_names:
        result = results[state]
        if hasattr(result, 'd_total'):
            d_totals.append(result.d_total)
        elif isinstance(result, dict):
            d_totals.append(result.get('D_w', result.get('d_total', 0.0)))
    
    colors = ['green' if d < theta_c else 'red' for d in d_totals]
    bars = ax2.bar(state_names, d_totals, color=colors, alpha=0.7)
    ax2.axhline(theta_c, color='black', linestyle='--', label=f'θc = {theta_c}')
    ax2.set_ylabel('D_total')
    ax2.set_title('Pipeline Distance')
    ax2.legend()
    
    for bar, value in zip(bars, d_totals):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                f'{value:.3f}', ha='center', va='bottom')
    
    # 3. Individual indicators (top right)
    ax3 = fig.add_subplot(gs[0, 2])
    
    if zeta_names and len(zeta_names) > 0:
        x = np.arange(len(state_names))
        width = 0.8 / len(zeta_names)
        
        for i, zeta in enumerate(zeta_names):
            values = []
            for state in state_names:
                result = results[state]
                if hasattr(result, 'zeta_values'):
                    value = result.zeta_values.get(zeta, 0.0)
                elif isinstance(result, dict):
                    if 'zeta_values' in result:
                        value = result['zeta_values'].get(zeta, 0.0)
                    else:
                        value = result.get(zeta, 0.0)
                else:
                    value = 0.0
                values.append(value)
            
            ax3.bar(x + i * width, values, width, label=f'ζ{i+1}', alpha=0.7)
        
        ax3.set_xlabel('States')
        ax3.set_ylabel('ζ Values')
        ax3.set_title('Individual Indicators')
        ax3.set_xticks(x + width * (len(zeta_names) - 1) / 2)
        ax3.set_xticklabels(state_names)
        ax3.legend()
        ax3.axhline(0, color='black', linewidth=0.5)
    
    # 4. Summary table (bottom)
    ax4 = fig.add_subplot(gs[1, :])
    ax4.axis('tight')
    ax4.axis('off')
    
    # Create summary table
    table_data = []
    headers = ['State', 'D_total', 'Classification'] + [f'ζ{i+1}' for i in range(len(zeta_names))]
    
    for state_name, result in results.items():
        row = [state_name]
        
        # D_total
        if hasattr(result, 'd_total'):
            row.append(f"{result.d_total:.3f}")
            classification = result.consciousness_state
        elif isinstance(result, dict):
            d_val = result.get('D_w', result.get('d_total', 0.0))
            row.append(f"{d_val:.3f}")
            classification = 'Conscious' if d_val < theta_c else 'Non-conscious'
        
        row.append(classification)
        
        # ζ values
        for zeta in zeta_names:
            if hasattr(result, 'zeta_values'):
                value = result.zeta_values.get(zeta, 0.0)
            elif isinstance(result, dict):
                if 'zeta_values' in result:
                    value = result['zeta_values'].get(zeta, 0.0)
                else:
                    value = result.get(zeta, 0.0)
            else:
                value = 0.0
            row.append(f"{value:.3f}")
        
        table_data.append(row)
    
    table = ax4.table(cellText=table_data, colLabels=headers,
                     cellLoc='center', loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.5)
    
    # Color code the classification column
    for i, row in enumerate(table_data):
        classification = row[2]
        color = 'lightgreen' if classification == 'Conscious' else 'lightcoral'
        table[(i+1, 2)].set_facecolor(color)
    
    ax4.set_title('Summary Table', fontsize=14, fontweight='bold', pad=20)
    
    fig.suptitle('Six Keys Criticality - Comprehensive Analysis', 
                fontsize=18, fontweight='bold')
    
    return fig


# Convenience function for quick plotting
def quick_plot(results: Dict[str, Dict], plot_type: str = 'summary', **kwargs) -> plt.Figure:
    """
    Quick plotting function for common visualizations.
    
    Parameters
    ----------
    results : dict
        Analysis results
    plot_type : str, default='summary'
        Type of plot: 'radar', 'phase', 'summary', 'time_series'
    **kwargs
        Additional arguments for specific plot functions
        
    Returns
    -------
    fig : matplotlib.figure.Figure
        Figure object
    """
    setup_plot_style()
    
    if plot_type == 'radar':
        return plot_radar_chart(results, **kwargs)
    elif plot_type == 'phase':
        return plot_phase_diagram(results, **kwargs)
    elif plot_type == 'summary':
        return plot_criticality_summary(results, **kwargs)
    elif plot_type == 'time_series':
        return plot_time_series(results, **kwargs)
    else:
        raise ValueError(f"Unknown plot type: {plot_type}. "
                        f"Available: 'radar', 'phase', 'summary', 'time_series'")


if __name__ == "__main__":
    # Demo with synthetic data
    setup_plot_style()
    
    # Create sample results
    sample_results = {
        'Awake': {
            'zeta_values': {'zeta1': 0.2, 'zeta2': -0.1},
            'd_total': 0.8,
            'consciousness_state': 'Conscious'
        },
        'Light-Sedation': {
            'zeta_values': {'zeta1': 0.8, 'zeta2': 0.3},
            'd_total': 1.2,
            'consciousness_state': 'Non-conscious'
        },
        'Deep-Anesthesia': {
            'zeta_values': {'zeta1': 1.5, 'zeta2': 1.0},
            'd_total': 1.8,
            'consciousness_state': 'Non-conscious'
        }
    }
    
    # Create plots
    fig1 = plot_radar_chart(sample_results)
    fig2 = plot_phase_diagram(sample_results)
    fig3 = plot_criticality_summary(sample_results)
    
    plt.show()