# -*- coding: utf-8 -*-
"""
ECGP (Effective Causal Graph Percolation) - ζ₄ Indicator

六鑰臨界第四鑰：有效因果圖滲透指標

This module implements the Effective Causal Graph Percolation (ECGP) for neural criticality analysis.
ECGP measures the percolation properties of effective causal networks to assess criticality.
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Optional, Tuple, Union, Any
import warnings
from dataclasses import dataclass


@dataclass
class ECGPResults:
    """
    Results from ECGP analysis.
    
    Attributes
    ----------
    percolation_series : np.ndarray
        Time series of percolation strength P(t)
    zeta_4 : float
        Normalized coordinate ζ₄
    C_ECGP : int
        Binary criterion (1 if in critical zone, 0 otherwise)
    D_w : float
        Weighted distance contribution
    time_points : np.ndarray
        Time points for the analysis
    parameters : dict
        Analysis parameters used
    """
    percolation_series: np.ndarray
    zeta_4: float
    C_ECGP: int
    D_w: float
    time_points: np.ndarray
    parameters: Dict[str, Any]


class ECGP:
    """
    Effective Causal Graph Percolation (ECGP) - ζ₄ Indicator
    
    Implements the fourth key of Six Keys Criticality framework.
    Analyzes percolation properties of effective causal networks.
    
    Parameters
    ----------
    p_min : float, default=0.4
        Lower bound of critical percolation zone
    p_max : float, default=0.8
        Upper bound of critical percolation zone
    tau_samples : int, default=150
        Number of samples for ECGP window analysis
    weight : float, default=0.18
        Weight factor for distance calculation
    settle_time : float, default=10.0
        Time constant for exponential relaxation in simulation
    noise_level : float, default=0.05
        Noise level for synthetic data generation
    """
    
    def __init__(self, 
                 p_min: float = 0.4,
                 p_max: float = 0.8,
                 tau_samples: int = 150,
                 weight: float = 0.18,
                 settle_time: float = 10.0,
                 noise_level: float = 0.05):
        
        self.p_min = p_min
        self.p_max = p_max
        self.tau_samples = tau_samples
        self.weight = weight
        self.settle_time = settle_time
        self.noise_level = noise_level
        
        # Validation
        if p_min >= p_max:
            raise ValueError("p_min must be less than p_max")
        if not (0 <= p_min <= 1 and 0 <= p_max <= 1):
            raise ValueError("Percolation bounds must be between 0 and 1")
        if tau_samples <= 0:
            raise ValueError("tau_samples must be positive")
        if weight <= 0:
            raise ValueError("weight must be positive")
    
    def simulate_percolation_series(self, 
                                  time_points: np.ndarray, 
                                  p_target: float) -> np.ndarray:
        """
        Generate synthetic percolation strength time series.
        
        Parameters
        ----------
        time_points : np.ndarray
            Time points for simulation
        p_target : float
            Target percolation strength for relaxation
            
        Returns
        -------
        np.ndarray
            Simulated P(t) time series
        """
        if not (0 <= p_target <= 1):
            raise ValueError("p_target must be between 0 and 1")
        
        percolation = np.zeros_like(time_points)
        percolation[0] = 0.5  # Start at middle value
        
        for i in range(1, len(time_points)):
            dt = time_points[i] - time_points[i-1]
            # First-order exponential approach with noise
            percolation[i] = percolation[i-1] + (p_target - percolation[i-1]) * dt / self.settle_time
        
        # Add Gaussian noise and clip to [0, 1]
        percolation += np.random.normal(0, self.noise_level, len(time_points))
        percolation = np.clip(percolation, 0, 1)
        
        return percolation
    
    def compute_ecgp(self, percolation_series: np.ndarray) -> Tuple[float, int]:
        """
        Compute ECGP indicator from percolation time series.
        
        Parameters
        ----------
        percolation_series : np.ndarray
            Percolation strength time series P(t)
            
        Returns
        -------
        tuple
            (ζ₄, C_ECGP) - normalized coordinate and binary criterion
        """
        if len(percolation_series) < self.tau_samples:
            warnings.warn(f"Series length ({len(percolation_series)}) < tau_samples ({self.tau_samples})")
            analysis_window = percolation_series
        else:
            # Use last tau_samples for analysis
            analysis_window = percolation_series[-self.tau_samples:]
        
        # Check if values remain in critical percolation zone
        in_zone = np.all((analysis_window >= self.p_min) & 
                        (analysis_window <= self.p_max))
        C_ECGP = 1 if in_zone else 0
        
        # Compute normalized coordinate ζ₄
        mean_p = np.mean(analysis_window)
        
        if C_ECGP == 1:
            # In critical zone: ζ₄ based on position within zone
            zone_center = (self.p_min + self.p_max) / 2
            zone_width = self.p_max - self.p_min
            zeta_4 = (mean_p - zone_center) / (zone_width / 2)
        else:
            # Outside critical zone: ζ₄ based on distance from zone
            if mean_p < self.p_min:
                zeta_4 = (mean_p - self.p_min) / self.p_min
            else:  # mean_p > self.p_max
                zeta_4 = (mean_p - self.p_max) / (1 - self.p_max)
        
        return zeta_4, C_ECGP
    
    def analyze(self, 
                data: Optional[np.ndarray] = None,
                time_points: Optional[np.ndarray] = None,
                p_target: Optional[float] = None,
                sim_time: float = 60.0,
                dt: float = 0.1) -> ECGPResults:
        """
        Perform ECGP analysis on data or generate synthetic data.
        
        Parameters
        ----------
        data : np.ndarray, optional
            Real percolation data. If None, synthetic data is generated.
        time_points : np.ndarray, optional
            Time points corresponding to data
        p_target : float, optional
            Target percolation strength for synthetic data generation
        sim_time : float, default=60.0
            Simulation time for synthetic data
        dt : float, default=0.1
            Time step for synthetic data
            
        Returns
        -------
        ECGPResults
            Complete analysis results
        """
        if data is not None:
            # Use provided data
            percolation_series = np.array(data)
            if time_points is not None:
                time_array = np.array(time_points)
            else:
                time_array = np.arange(len(percolation_series)) * dt
        else:
            # Generate synthetic data
            if p_target is None:
                p_target = (self.p_min + self.p_max) / 2  # Default to critical zone center
            
            time_array = np.arange(0, sim_time, dt)
            percolation_series = self.simulate_percolation_series(time_array, p_target)
        
        # Compute ECGP indicators
        zeta_4, C_ECGP = self.compute_ecgp(percolation_series)
        
        # Compute weighted distance
        D_w = np.sqrt(self.weight * zeta_4**2)
        
        # Store parameters
        parameters = {
            'p_min': self.p_min,
            'p_max': self.p_max,
            'tau_samples': self.tau_samples,
            'weight': self.weight,
            'settle_time': self.settle_time,
            'noise_level': self.noise_level,
            'p_target': p_target if data is None else None,
            'data_type': 'synthetic' if data is None else 'real'
        }
        
        return ECGPResults(
            percolation_series=percolation_series,
            zeta_4=zeta_4,
            C_ECGP=C_ECGP,
            D_w=D_w,
            time_points=time_array,
            parameters=parameters
        )
    
    def plot_analysis(self, results: ECGPResults, figsize: Tuple[int, int] = (12, 8)) -> None:
        """
        Create comprehensive visualization of ECGP analysis.
        
        Parameters
        ----------
        results : ECGPResults
            Analysis results to visualize
        figsize : tuple, default=(12, 8)
            Figure size (width, height)
        """
        fig, axes = plt.subplots(2, 2, figsize=figsize)
        fig.suptitle('ECGP (Effective Causal Graph Percolation) Analysis - ζ₄', 
                    fontsize=16, fontweight='bold')
        
        # Plot 1: P(t) time series with critical zone
        ax1 = axes[0, 0]
        ax1.plot(results.time_points, results.percolation_series, 'b-', 
                linewidth=1.5, alpha=0.8, label='P(t)')
        ax1.axhspan(self.p_min, self.p_max, alpha=0.2, color='green', 
                   label=f'Critical Zone [{self.p_min:.2f}, {self.p_max:.2f}]')
        ax1.axhline(self.p_min, color='green', linestyle='--', alpha=0.7)
        ax1.axhline(self.p_max, color='green', linestyle='--', alpha=0.7)
        ax1.set_xlabel('Time (s)')
        ax1.set_ylabel('Percolation Strength P(t)')
        ax1.set_title('Percolation Dynamics')
        ax1.set_ylim(0, 1)
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Analysis window detail
        ax2 = axes[0, 1]
        if len(results.percolation_series) >= self.tau_samples:
            window_data = results.percolation_series[-self.tau_samples:]
            window_time = results.time_points[-self.tau_samples:]
        else:
            window_data = results.percolation_series
            window_time = results.time_points
        
        ax2.plot(window_time, window_data, 'r-', linewidth=2, label='Analysis Window')
        ax2.axhspan(self.p_min, self.p_max, alpha=0.2, color='green')
        ax2.axhline(np.mean(window_data), color='orange', linestyle='-', 
                   label=f'Mean = {np.mean(window_data):.3f}')
        ax2.set_xlabel('Time (s)')
        ax2.set_ylabel('P(t)')
        ax2.set_title(f'Analysis Window (τ = {self.tau_samples} samples)')
        ax2.set_ylim(0, 1)
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: ECGP indicators
        ax3 = axes[1, 0]
        indicators = ['ζ₄', 'C_ECGP', 'D_w']
        values = [results.zeta_4, results.C_ECGP, results.D_w]
        colors = ['blue', 'green' if results.C_ECGP else 'red', 'purple']
        
        bars = ax3.bar(indicators, values, color=colors, alpha=0.7)
        ax3.set_ylabel('Value')
        ax3.set_title('ECGP Indicators')
        ax3.grid(True, alpha=0.3, axis='y')
        
        # Add value labels on bars
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                    f'{value:.3f}', ha='center', va='bottom')
        
        # Plot 4: Parameter summary
        ax4 = axes[1, 1]
        ax4.axis('off')
        
        # Create parameter text
        param_text = f"""
ECGP Analysis Summary
{'='*25}

Indicators:
  ζ₄ = {results.zeta_4:.4f}
  C_ECGP = {results.C_ECGP} ({'PASS' if results.C_ECGP else 'FAIL'})
  D_w = {results.D_w:.4f}

Parameters:
  Critical Zone: [{self.p_min:.2f}, {self.p_max:.2f}]
  Analysis Window: {self.tau_samples} samples
  Weight: {self.weight:.3f}
  
Data Type: {results.parameters.get('data_type', 'unknown')}
"""
        
        ax4.text(0.05, 0.95, param_text, transform=ax4.transAxes, 
                fontsize=10, verticalalignment='top', fontfamily='monospace',
                bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.8))
        
        plt.tight_layout()
        plt.show()
    
    def print_summary(self, results: ECGPResults) -> None:
        """
        Print detailed analysis summary.
        
        Parameters
        ----------
        results : ECGPResults
            Analysis results to summarize
        """
        print("\n" + "="*50)
        print("ECGP (Effective Causal Graph Percolation) Analysis Summary")
        print("="*50)
        
        print(f"\nKey Indicators:")
        print(f"  ζ₄ (Normalized Coordinate): {results.zeta_4:.6f}")
        print(f"  C_ECGP (Binary Criterion):  {results.C_ECGP} ({'PASS' if results.C_ECGP else 'FAIL'})")
        print(f"  D_w (Weighted Distance):    {results.D_w:.6f}")
        
        print(f"\nPercolation Analysis:")
        print(f"  Critical Zone: [{self.p_min:.3f}, {self.p_max:.3f}]")
        print(f"  Mean P(t): {np.mean(results.percolation_series):.6f}")
        print(f"  Std P(t):  {np.std(results.percolation_series):.6f}")
        
        if len(results.percolation_series) >= self.tau_samples:
            window_data = results.percolation_series[-self.tau_samples:]
            print(f"  Window Mean P(t): {np.mean(window_data):.6f}")
            print(f"  Window Std P(t):  {np.std(window_data):.6f}")
        
        print(f"\nParameters:")
        print(f"  Analysis Window: {self.tau_samples} samples")
        print(f"  Weight Factor: {self.weight:.3f}")
        print(f"  Data Points: {len(results.percolation_series)}")
        print(f"  Time Range: {results.time_points[0]:.2f} - {results.time_points[-1]:.2f} s")
        print(f"  Data Type: {results.parameters.get('data_type', 'unknown')}")
        
        if results.parameters.get('data_type') == 'synthetic':
            print(f"  Target P: {results.parameters.get('p_target', 'N/A')}")
            print(f"  Settle Time: {self.settle_time:.1f} s")
            print(f"  Noise Level: {self.noise_level:.4f}")


def demo():
    """
    Demonstration of ECGP analysis with different consciousness states.
    """
    print("ECGP (Effective Causal Graph Percolation) Demonstration")
    print("======================================================\n")
    
    # Initialize ECGP analyzer
    ecgp = ECGP()
    
    # Define consciousness states with different target percolation strengths
    states = {
        'Awake': 0.6,           # Critical zone center
        'Light Sedation': 0.3,  # Below critical zone
        'Deep Anesthesia': 0.9  # Above critical zone
    }
    
    results = {}
    
    # Analyze each state
    for state_name, p_target in states.items():
        print(f"\nAnalyzing {state_name} state (P_target = {p_target})...")
        
        # Set random seed for reproducibility
        np.random.seed(42 + hash(state_name) % 1000)
        
        # Perform analysis
        result = ecgp.analyze(p_target=p_target, sim_time=60.0, dt=0.1)
        results[state_name] = result
        
        # Print summary
        ecgp.print_summary(result)
    
    # Create comparison visualization
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('ECGP Analysis: Consciousness State Comparison', fontsize=16, fontweight='bold')
    
    # Plot 1: All P(t) series
    ax1 = axes[0, 0]
    colors = ['green', 'orange', 'red']
    for i, (state, result) in enumerate(results.items()):
        ax1.plot(result.time_points, result.percolation_series, 
                color=colors[i], label=state, alpha=0.8)
    
    ax1.axhspan(ecgp.p_min, ecgp.p_max, alpha=0.2, color='gray', 
               label='Critical Zone')
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Percolation Strength P(t)')
    ax1.set_title('Percolation Dynamics Comparison')
    ax1.set_ylim(0, 1)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: ζ₄ comparison
    ax2 = axes[0, 1]
    state_names = list(results.keys())
    zeta_values = [results[state].zeta_4 for state in state_names]
    bars = ax2.bar(state_names, zeta_values, color=colors, alpha=0.7)
    ax2.set_ylabel('ζ₄')
    ax2.set_title('Normalized Coordinate ζ₄')
    ax2.grid(True, alpha=0.3, axis='y')
    
    for bar, value in zip(bars, zeta_values):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                f'{value:.3f}', ha='center', va='bottom')
    
    # Plot 3: D_w comparison
    ax3 = axes[1, 0]
    dw_values = [results[state].D_w for state in state_names]
    bars = ax3.bar(state_names, dw_values, color=colors, alpha=0.7)
    ax3.set_ylabel('D_w')
    ax3.set_title('Weighted Distance D_w')
    ax3.grid(True, alpha=0.3, axis='y')
    
    for bar, value in zip(bars, dw_values):
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                f'{value:.3f}', ha='center', va='bottom')
    
    # Plot 4: Summary table
    ax4 = axes[1, 1]
    ax4.axis('off')
    
    summary_text = "Analysis Summary\n" + "="*20 + "\n\n"
    for state in state_names:
        result = results[state]
        summary_text += f"{state}:\n"
        summary_text += f"  ζ₄ = {result.zeta_4:.4f}\n"
        summary_text += f"  C_ECGP = {result.C_ECGP} ({'PASS' if result.C_ECGP else 'FAIL'})\n"
        summary_text += f"  D_w = {result.D_w:.4f}\n\n"
    
    ax4.text(0.05, 0.95, summary_text, transform=ax4.transAxes,
            fontsize=11, verticalalignment='top', fontfamily='monospace',
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
    
    plt.tight_layout()
    plt.show()
    
    print("\n" + "="*50)
    print("ECGP Demonstration Complete")
    print("="*50)


if __name__ == "__main__":
    demo()