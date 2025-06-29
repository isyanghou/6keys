# -*- coding: utf-8 -*-
"""
PWC (Phase-Wrapped Circulation) - ζ₅ Indicator

六鑰臨界第五鑰：相位包裹環流指標

This module implements the Phase-Wrapped Circulation (PWC) for neural criticality analysis.
PWC measures the circulation properties of phase-wrapped neural dynamics.
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Optional, Tuple, Union, Any
import warnings
from dataclasses import dataclass


@dataclass
class PWCResults:
    """
    Results from PWC analysis.
    
    Attributes
    ----------
    circulation_series : np.ndarray
        Time series of circulation strength Γ(t)
    zeta_5 : float
        Normalized coordinate ζ₅
    C_PWC : int
        Binary criterion (1 if in critical zone, 0 otherwise)
    D_w : float
        Weighted distance contribution
    time_points : np.ndarray
        Time points for the analysis
    parameters : dict
        Analysis parameters used
    """
    circulation_series: np.ndarray
    zeta_5: float
    C_PWC: int
    D_w: float
    time_points: np.ndarray
    parameters: Dict[str, Any]


class PWC:
    """
    Phase-Wrapped Circulation (PWC) - ζ₅ Indicator
    
    Implements the fifth key of Six Keys Criticality framework.
    Analyzes circulation properties of phase-wrapped neural dynamics.
    
    Parameters
    ----------
    gamma_min : float, default=-0.5
        Lower bound of critical circulation zone
    gamma_max : float, default=0.5
        Upper bound of critical circulation zone
    tau_samples : int, default=180
        Number of samples for PWC window analysis
    weight : float, default=0.15
        Weight factor for distance calculation
    settle_time : float, default=12.0
        Time constant for exponential relaxation in simulation
    noise_level : float, default=0.08
        Noise level for synthetic data generation
    """
    
    def __init__(self, 
                 gamma_min: float = -0.5,
                 gamma_max: float = 0.5,
                 tau_samples: int = 180,
                 weight: float = 0.15,
                 settle_time: float = 12.0,
                 noise_level: float = 0.08):
        
        self.gamma_min = gamma_min
        self.gamma_max = gamma_max
        self.tau_samples = tau_samples
        self.weight = weight
        self.settle_time = settle_time
        self.noise_level = noise_level
        
        # Validation
        if gamma_min >= gamma_max:
            raise ValueError("gamma_min must be less than gamma_max")
        if tau_samples <= 0:
            raise ValueError("tau_samples must be positive")
        if weight <= 0:
            raise ValueError("weight must be positive")
    
    def simulate_circulation_series(self, 
                                  time_points: np.ndarray, 
                                  gamma_target: float) -> np.ndarray:
        """
        Generate synthetic circulation strength time series.
        
        Parameters
        ----------
        time_points : np.ndarray
            Time points for simulation
        gamma_target : float
            Target circulation strength for relaxation
            
        Returns
        -------
        np.ndarray
            Simulated Γ(t) time series
        """
        circulation = np.zeros_like(time_points)
        circulation[0] = 0.0  # Start at zero circulation
        
        for i in range(1, len(time_points)):
            dt = time_points[i] - time_points[i-1]
            # First-order exponential approach with oscillatory component
            circulation[i] = circulation[i-1] + (gamma_target - circulation[i-1]) * dt / self.settle_time
            # Add small oscillatory component to simulate phase dynamics
            circulation[i] += 0.02 * np.sin(2 * np.pi * time_points[i] / 5.0)
        
        # Add Gaussian noise
        circulation += np.random.normal(0, self.noise_level, len(time_points))
        
        return circulation
    
    def compute_pwc(self, circulation_series: np.ndarray) -> Tuple[float, int]:
        """
        Compute PWC indicator from circulation time series.
        
        Parameters
        ----------
        circulation_series : np.ndarray
            Circulation strength time series Γ(t)
            
        Returns
        -------
        tuple
            (ζ₅, C_PWC) - normalized coordinate and binary criterion
        """
        if len(circulation_series) < self.tau_samples:
            warnings.warn(f"Series length ({len(circulation_series)}) < tau_samples ({self.tau_samples})")
            analysis_window = circulation_series
        else:
            # Use last tau_samples for analysis
            analysis_window = circulation_series[-self.tau_samples:]
        
        # Check if values remain in critical circulation zone
        in_zone = np.all((analysis_window >= self.gamma_min) & 
                        (analysis_window <= self.gamma_max))
        C_PWC = 1 if in_zone else 0
        
        # Compute normalized coordinate ζ₅
        mean_gamma = np.mean(analysis_window)
        
        if C_PWC == 1:
            # In critical zone: ζ₅ based on position within zone
            zone_center = (self.gamma_min + self.gamma_max) / 2
            zone_width = self.gamma_max - self.gamma_min
            zeta_5 = (mean_gamma - zone_center) / (zone_width / 2)
        else:
            # Outside critical zone: ζ₅ based on distance from zone
            if mean_gamma < self.gamma_min:
                zeta_5 = (mean_gamma - self.gamma_min) / abs(self.gamma_min)
            else:  # mean_gamma > self.gamma_max
                zeta_5 = (mean_gamma - self.gamma_max) / abs(self.gamma_max)
        
        return zeta_5, C_PWC
    
    def analyze(self, 
                data: Optional[np.ndarray] = None,
                time_points: Optional[np.ndarray] = None,
                gamma_target: Optional[float] = None,
                sim_time: float = 60.0,
                dt: float = 0.08) -> PWCResults:
        """
        Perform PWC analysis on data or generate synthetic data.
        
        Parameters
        ----------
        data : np.ndarray, optional
            Real circulation data. If None, synthetic data is generated.
        time_points : np.ndarray, optional
            Time points corresponding to data
        gamma_target : float, optional
            Target circulation strength for synthetic data generation
        sim_time : float, default=60.0
            Simulation time for synthetic data
        dt : float, default=0.08
            Time step for synthetic data
            
        Returns
        -------
        PWCResults
            Complete analysis results
        """
        if data is not None:
            # Use provided data
            circulation_series = np.array(data)
            if time_points is not None:
                time_array = np.array(time_points)
            else:
                time_array = np.arange(len(circulation_series)) * dt
        else:
            # Generate synthetic data
            if gamma_target is None:
                gamma_target = (self.gamma_min + self.gamma_max) / 2  # Default to critical zone center
            
            time_array = np.arange(0, sim_time, dt)
            circulation_series = self.simulate_circulation_series(time_array, gamma_target)
        
        # Compute PWC indicators
        zeta_5, C_PWC = self.compute_pwc(circulation_series)
        
        # Compute weighted distance
        D_w = np.sqrt(self.weight * zeta_5**2)
        
        # Store parameters
        parameters = {
            'gamma_min': self.gamma_min,
            'gamma_max': self.gamma_max,
            'tau_samples': self.tau_samples,
            'weight': self.weight,
            'settle_time': self.settle_time,
            'noise_level': self.noise_level,
            'gamma_target': gamma_target if data is None else None,
            'data_type': 'synthetic' if data is None else 'real'
        }
        
        return PWCResults(
            circulation_series=circulation_series,
            zeta_5=zeta_5,
            C_PWC=C_PWC,
            D_w=D_w,
            time_points=time_array,
            parameters=parameters
        )
    
    def plot_analysis(self, results: PWCResults, figsize: Tuple[int, int] = (12, 8)) -> None:
        """
        Create comprehensive visualization of PWC analysis.
        
        Parameters
        ----------
        results : PWCResults
            Analysis results to visualize
        figsize : tuple, default=(12, 8)
            Figure size (width, height)
        """
        fig, axes = plt.subplots(2, 2, figsize=figsize)
        fig.suptitle('PWC (Phase-Wrapped Circulation) Analysis - ζ₅', 
                    fontsize=16, fontweight='bold')
        
        # Plot 1: Γ(t) time series with critical zone
        ax1 = axes[0, 0]
        ax1.plot(results.time_points, results.circulation_series, 'b-', 
                linewidth=1.5, alpha=0.8, label='Γ(t)')
        ax1.axhspan(self.gamma_min, self.gamma_max, alpha=0.2, color='green', 
                   label=f'Critical Zone [{self.gamma_min:.2f}, {self.gamma_max:.2f}]')
        ax1.axhline(self.gamma_min, color='green', linestyle='--', alpha=0.7)
        ax1.axhline(self.gamma_max, color='green', linestyle='--', alpha=0.7)
        ax1.axhline(0, color='black', linestyle='-', alpha=0.3)
        ax1.set_xlabel('Time (s)')
        ax1.set_ylabel('Circulation Strength Γ(t)')
        ax1.set_title('Phase-Wrapped Circulation Dynamics')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Analysis window detail
        ax2 = axes[0, 1]
        if len(results.circulation_series) >= self.tau_samples:
            window_data = results.circulation_series[-self.tau_samples:]
            window_time = results.time_points[-self.tau_samples:]
        else:
            window_data = results.circulation_series
            window_time = results.time_points
        
        ax2.plot(window_time, window_data, 'r-', linewidth=2, label='Analysis Window')
        ax2.axhspan(self.gamma_min, self.gamma_max, alpha=0.2, color='green')
        ax2.axhline(np.mean(window_data), color='orange', linestyle='-', 
                   label=f'Mean = {np.mean(window_data):.3f}')
        ax2.axhline(0, color='black', linestyle='-', alpha=0.3)
        ax2.set_xlabel('Time (s)')
        ax2.set_ylabel('Γ(t)')
        ax2.set_title(f'Analysis Window (τ = {self.tau_samples} samples)')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: PWC indicators
        ax3 = axes[1, 0]
        indicators = ['ζ₅', 'C_PWC', 'D_w']
        values = [results.zeta_5, results.C_PWC, results.D_w]
        colors = ['blue', 'green' if results.C_PWC else 'red', 'purple']
        
        bars = ax3.bar(indicators, values, color=colors, alpha=0.7)
        ax3.set_ylabel('Value')
        ax3.set_title('PWC Indicators')
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
PWC Analysis Summary
{'='*25}

Indicators:
  ζ₅ = {results.zeta_5:.4f}
  C_PWC = {results.C_PWC} ({'PASS' if results.C_PWC else 'FAIL'})
  D_w = {results.D_w:.4f}

Parameters:
  Critical Zone: [{self.gamma_min:.2f}, {self.gamma_max:.2f}]
  Analysis Window: {self.tau_samples} samples
  Weight: {self.weight:.3f}
  
Data Type: {results.parameters.get('data_type', 'unknown')}
"""
        
        ax4.text(0.05, 0.95, param_text, transform=ax4.transAxes, 
                fontsize=10, verticalalignment='top', fontfamily='monospace',
                bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.8))
        
        plt.tight_layout()
        plt.show()
    
    def print_summary(self, results: PWCResults) -> None:
        """
        Print detailed analysis summary.
        
        Parameters
        ----------
        results : PWCResults
            Analysis results to summarize
        """
        print("\n" + "="*50)
        print("PWC (Phase-Wrapped Circulation) Analysis Summary")
        print("="*50)
        
        print(f"\nKey Indicators:")
        print(f"  ζ₅ (Normalized Coordinate): {results.zeta_5:.6f}")
        print(f"  C_PWC (Binary Criterion):  {results.C_PWC} ({'PASS' if results.C_PWC else 'FAIL'})")
        print(f"  D_w (Weighted Distance):    {results.D_w:.6f}")
        
        print(f"\nCirculation Analysis:")
        print(f"  Critical Zone: [{self.gamma_min:.3f}, {self.gamma_max:.3f}]")
        print(f"  Mean Γ(t): {np.mean(results.circulation_series):.6f}")
        print(f"  Std Γ(t):  {np.std(results.circulation_series):.6f}")
        
        if len(results.circulation_series) >= self.tau_samples:
            window_data = results.circulation_series[-self.tau_samples:]
            print(f"  Window Mean Γ(t): {np.mean(window_data):.6f}")
            print(f"  Window Std Γ(t):  {np.std(window_data):.6f}")
        
        print(f"\nParameters:")
        print(f"  Analysis Window: {self.tau_samples} samples")
        print(f"  Weight Factor: {self.weight:.3f}")
        print(f"  Data Points: {len(results.circulation_series)}")
        print(f"  Time Range: {results.time_points[0]:.2f} - {results.time_points[-1]:.2f} s")
        print(f"  Data Type: {results.parameters.get('data_type', 'unknown')}")
        
        if results.parameters.get('data_type') == 'synthetic':
            print(f"  Target Γ: {results.parameters.get('gamma_target', 'N/A')}")
            print(f"  Settle Time: {self.settle_time:.1f} s")
            print(f"  Noise Level: {self.noise_level:.4f}")


def demo():
    """
    Demonstration of PWC analysis with different consciousness states.
    """
    print("PWC (Phase-Wrapped Circulation) Demonstration")
    print("============================================\n")
    
    # Initialize PWC analyzer
    pwc = PWC()
    
    # Define consciousness states with different target circulation strengths
    states = {
        'Awake': 0.0,           # Critical zone center
        'Light Sedation': -0.8, # Below critical zone
        'Deep Anesthesia': 0.9  # Above critical zone
    }
    
    results = {}
    
    # Analyze each state
    for state_name, gamma_target in states.items():
        print(f"\nAnalyzing {state_name} state (Γ_target = {gamma_target})...")
        
        # Set random seed for reproducibility
        np.random.seed(42 + hash(state_name) % 1000)
        
        # Perform analysis
        result = pwc.analyze(gamma_target=gamma_target, sim_time=60.0, dt=0.08)
        results[state_name] = result
        
        # Print summary
        pwc.print_summary(result)
    
    # Create comparison visualization
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('PWC Analysis: Consciousness State Comparison', fontsize=16, fontweight='bold')
    
    # Plot 1: All Γ(t) series
    ax1 = axes[0, 0]
    colors = ['green', 'orange', 'red']
    for i, (state, result) in enumerate(results.items()):
        ax1.plot(result.time_points, result.circulation_series, 
                color=colors[i], label=state, alpha=0.8)
    
    ax1.axhspan(pwc.gamma_min, pwc.gamma_max, alpha=0.2, color='gray', 
               label='Critical Zone')
    ax1.axhline(0, color='black', linestyle='-', alpha=0.3)
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Circulation Strength Γ(t)')
    ax1.set_title('Circulation Dynamics Comparison')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: ζ₅ comparison
    ax2 = axes[0, 1]
    state_names = list(results.keys())
    zeta_values = [results[state].zeta_5 for state in state_names]
    bars = ax2.bar(state_names, zeta_values, color=colors, alpha=0.7)
    ax2.set_ylabel('ζ₅')
    ax2.set_title('Normalized Coordinate ζ₅')
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
        summary_text += f"  ζ₅ = {result.zeta_5:.4f}\n"
        summary_text += f"  C_PWC = {result.C_PWC} ({'PASS' if result.C_PWC else 'FAIL'})\n"
        summary_text += f"  D_w = {result.D_w:.4f}\n\n"
    
    ax4.text(0.05, 0.95, summary_text, transform=ax4.transAxes,
            fontsize=11, verticalalignment='top', fontfamily='monospace',
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
    
    plt.tight_layout()
    plt.show()
    
    print("\n" + "="*50)
    print("PWC Demonstration Complete")
    print("="*50)


if __name__ == "__main__":
    demo()