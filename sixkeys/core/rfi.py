# -*- coding: utf-8 -*-
"""
RFI (Ricci Flow Index) - ζ₃ Indicator

六鑰臨界第三鑰：Ricci曲率流指標

This module implements the Ricci Flow Index (RFI) for neural criticality analysis.
RFI measures the mean Ricci curvature dynamics and evaluates whether the system
remains in the critical flat zone.
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Optional, Tuple, Union, Any
import warnings
from dataclasses import dataclass


@dataclass
class RFIResults:
    """
    Results from RFI analysis.
    
    Attributes
    ----------
    kappa_series : np.ndarray
        Time series of mean Ricci curvature κ̄(t)
    zeta_3 : float
        Normalized coordinate ζ₃
    C_RFI : int
        Binary criterion (1 if in critical zone, 0 otherwise)
    D_w : float
        Weighted distance contribution
    time_points : np.ndarray
        Time points for the analysis
    parameters : dict
        Analysis parameters used
    """
    kappa_series: np.ndarray
    zeta_3: float
    C_RFI: int
    D_w: float
    time_points: np.ndarray
    parameters: Dict[str, Any]


class RFI:
    """
    Ricci Flow Index (RFI) - ζ₃ Indicator
    
    Implements the third key of Six Keys Criticality framework.
    Analyzes mean Ricci curvature dynamics to assess neural criticality.
    
    Parameters
    ----------
    kappa_min : float, default=-0.02
        Lower bound of critical flat zone
    kappa_max : float, default=0.02
        Upper bound of critical flat zone
    tau_samples : int, default=200
        Number of samples for RFI window analysis
    weight : float, default=0.22
        Weight factor for distance calculation
    settle_time : float, default=8.0
        Time constant for exponential relaxation in simulation
    noise_level : float, default=0.005
        Noise level for synthetic data generation
    """
    
    def __init__(self, 
                 kappa_min: float = -0.02,
                 kappa_max: float = 0.02,
                 tau_samples: int = 200,
                 weight: float = 0.22,
                 settle_time: float = 8.0,
                 noise_level: float = 0.005):
        
        self.kappa_min = kappa_min
        self.kappa_max = kappa_max
        self.tau_samples = tau_samples
        self.weight = weight
        self.settle_time = settle_time
        self.noise_level = noise_level
        
        # Validation
        if kappa_min >= kappa_max:
            raise ValueError("kappa_min must be less than kappa_max")
        if tau_samples <= 0:
            raise ValueError("tau_samples must be positive")
        if weight <= 0:
            raise ValueError("weight must be positive")
    
    def simulate_kappa_series(self, 
                            time_points: np.ndarray, 
                            kappa_target: float) -> np.ndarray:
        """
        Generate synthetic mean Ricci curvature time series.
        
        Parameters
        ----------
        time_points : np.ndarray
            Time points for simulation
        kappa_target : float
            Target curvature value for relaxation
            
        Returns
        -------
        np.ndarray
            Simulated κ̄(t) time series
        """
        kappa = np.zeros_like(time_points)
        
        for i in range(1, len(time_points)):
            dt = time_points[i] - time_points[i-1]
            # First-order exponential approach with noise
            kappa[i] = kappa[i-1] + (kappa_target - kappa[i-1]) * dt / self.settle_time
        
        # Add Gaussian noise
        kappa += np.random.normal(0, self.noise_level, len(time_points))
        
        return kappa
    
    def compute_rfi(self, kappa_series: np.ndarray) -> Tuple[float, int]:
        """
        Compute RFI indicator from Ricci curvature time series.
        
        Parameters
        ----------
        kappa_series : np.ndarray
            Mean Ricci curvature time series κ̄(t)
            
        Returns
        -------
        tuple
            (ζ₃, C_RFI) - normalized coordinate and binary criterion
        """
        if len(kappa_series) < self.tau_samples:
            warnings.warn(f"Series length ({len(kappa_series)}) < tau_samples ({self.tau_samples})")
            analysis_window = kappa_series
        else:
            # Use last tau_samples for analysis
            analysis_window = kappa_series[-self.tau_samples:]
        
        # Check if values remain in critical flat zone
        in_zone = np.all((analysis_window >= self.kappa_min) & 
                        (analysis_window <= self.kappa_max))
        C_RFI = 1 if in_zone else 0
        
        # Compute normalized coordinate ζ₃
        mean_kappa = np.mean(analysis_window)
        
        if C_RFI == 1:
            # In critical zone: ζ₃ based on position within zone
            zone_center = (self.kappa_min + self.kappa_max) / 2
            zone_width = self.kappa_max - self.kappa_min
            zeta_3 = (mean_kappa - zone_center) / (zone_width / 2)
        else:
            # Outside critical zone: ζ₃ based on distance from zone
            if mean_kappa < self.kappa_min:
                zeta_3 = (mean_kappa - self.kappa_min) / abs(self.kappa_min)
            else:  # mean_kappa > self.kappa_max
                zeta_3 = (mean_kappa - self.kappa_max) / abs(self.kappa_max)
        
        return zeta_3, C_RFI
    
    def analyze(self, 
                data: Optional[np.ndarray] = None,
                time_points: Optional[np.ndarray] = None,
                kappa_target: Optional[float] = None,
                sim_time: float = 60.0,
                dt: float = 0.05) -> RFIResults:
        """
        Perform RFI analysis on data or generate synthetic data.
        
        Parameters
        ----------
        data : np.ndarray, optional
            Real Ricci curvature data. If None, synthetic data is generated.
        time_points : np.ndarray, optional
            Time points corresponding to data
        kappa_target : float, optional
            Target curvature for synthetic data generation
        sim_time : float, default=60.0
            Simulation time for synthetic data
        dt : float, default=0.05
            Time step for synthetic data
            
        Returns
        -------
        RFIResults
            Complete analysis results
        """
        if data is not None:
            # Use provided data
            kappa_series = np.array(data)
            if time_points is not None:
                time_array = np.array(time_points)
            else:
                time_array = np.arange(len(kappa_series)) * dt
        else:
            # Generate synthetic data
            if kappa_target is None:
                kappa_target = 0.0  # Default to critical zone center
            
            time_array = np.arange(0, sim_time, dt)
            kappa_series = self.simulate_kappa_series(time_array, kappa_target)
        
        # Compute RFI indicators
        zeta_3, C_RFI = self.compute_rfi(kappa_series)
        
        # Compute weighted distance
        D_w = np.sqrt(self.weight * zeta_3**2)
        
        # Store parameters
        parameters = {
            'kappa_min': self.kappa_min,
            'kappa_max': self.kappa_max,
            'tau_samples': self.tau_samples,
            'weight': self.weight,
            'settle_time': self.settle_time,
            'noise_level': self.noise_level,
            'kappa_target': kappa_target if data is None else None,
            'data_type': 'synthetic' if data is None else 'real'
        }
        
        return RFIResults(
            kappa_series=kappa_series,
            zeta_3=zeta_3,
            C_RFI=C_RFI,
            D_w=D_w,
            time_points=time_array,
            parameters=parameters
        )
    
    def plot_analysis(self, results: RFIResults, figsize: Tuple[int, int] = (12, 8)) -> None:
        """
        Create comprehensive visualization of RFI analysis.
        
        Parameters
        ----------
        results : RFIResults
            Analysis results to visualize
        figsize : tuple, default=(12, 8)
            Figure size (width, height)
        """
        fig, axes = plt.subplots(2, 2, figsize=figsize)
        fig.suptitle('RFI (Ricci Flow Index) Analysis - ζ₃', fontsize=16, fontweight='bold')
        
        # Plot 1: κ̄(t) time series with critical zone
        ax1 = axes[0, 0]
        ax1.plot(results.time_points, results.kappa_series, 'b-', linewidth=1.5, alpha=0.8)
        ax1.axhspan(self.kappa_min, self.kappa_max, alpha=0.2, color='green', 
                   label=f'Critical Zone [{self.kappa_min:.3f}, {self.kappa_max:.3f}]')
        ax1.axhline(self.kappa_min, color='green', linestyle='--', alpha=0.7)
        ax1.axhline(self.kappa_max, color='green', linestyle='--', alpha=0.7)
        ax1.set_xlabel('Time (s)')
        ax1.set_ylabel('Mean Ricci Curvature κ̄(t)')
        ax1.set_title('Ricci Curvature Dynamics')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Analysis window detail
        ax2 = axes[0, 1]
        if len(results.kappa_series) >= self.tau_samples:
            window_data = results.kappa_series[-self.tau_samples:]
            window_time = results.time_points[-self.tau_samples:]
        else:
            window_data = results.kappa_series
            window_time = results.time_points
        
        ax2.plot(window_time, window_data, 'r-', linewidth=2, label='Analysis Window')
        ax2.axhspan(self.kappa_min, self.kappa_max, alpha=0.2, color='green')
        ax2.axhline(np.mean(window_data), color='orange', linestyle='-', 
                   label=f'Mean = {np.mean(window_data):.4f}')
        ax2.set_xlabel('Time (s)')
        ax2.set_ylabel('κ̄(t)')
        ax2.set_title(f'Analysis Window (τ = {self.tau_samples} samples)')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: RFI indicators
        ax3 = axes[1, 0]
        indicators = ['ζ₃', 'C_RFI', 'D_w']
        values = [results.zeta_3, results.C_RFI, results.D_w]
        colors = ['blue', 'green' if results.C_RFI else 'red', 'purple']
        
        bars = ax3.bar(indicators, values, color=colors, alpha=0.7)
        ax3.set_ylabel('Value')
        ax3.set_title('RFI Indicators')
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
RFI Analysis Summary
{'='*25}

Indicators:
  ζ₃ = {results.zeta_3:.4f}
  C_RFI = {results.C_RFI} ({'PASS' if results.C_RFI else 'FAIL'})
  D_w = {results.D_w:.4f}

Parameters:
  Critical Zone: [{self.kappa_min:.3f}, {self.kappa_max:.3f}]
  Analysis Window: {self.tau_samples} samples
  Weight: {self.weight:.3f}
  
Data Type: {results.parameters.get('data_type', 'unknown')}
"""
        
        ax4.text(0.05, 0.95, param_text, transform=ax4.transAxes, 
                fontsize=10, verticalalignment='top', fontfamily='monospace',
                bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.8))
        
        plt.tight_layout()
        plt.show()
    
    def print_summary(self, results: RFIResults) -> None:
        """
        Print detailed analysis summary.
        
        Parameters
        ----------
        results : RFIResults
            Analysis results to summarize
        """
        print("\n" + "="*50)
        print("RFI (Ricci Flow Index) Analysis Summary")
        print("="*50)
        
        print(f"\nKey Indicators:")
        print(f"  ζ₃ (Normalized Coordinate): {results.zeta_3:.6f}")
        print(f"  C_RFI (Binary Criterion):  {results.C_RFI} ({'PASS' if results.C_RFI else 'FAIL'})")
        print(f"  D_w (Weighted Distance):    {results.D_w:.6f}")
        
        print(f"\nCritical Zone Analysis:")
        print(f"  Zone Bounds: [{self.kappa_min:.4f}, {self.kappa_max:.4f}]")
        print(f"  Mean κ̄: {np.mean(results.kappa_series):.6f}")
        print(f"  Std κ̄:  {np.std(results.kappa_series):.6f}")
        
        if len(results.kappa_series) >= self.tau_samples:
            window_data = results.kappa_series[-self.tau_samples:]
            print(f"  Window Mean κ̄: {np.mean(window_data):.6f}")
            print(f"  Window Std κ̄:  {np.std(window_data):.6f}")
        
        print(f"\nParameters:")
        print(f"  Analysis Window: {self.tau_samples} samples")
        print(f"  Weight Factor: {self.weight:.3f}")
        print(f"  Data Points: {len(results.kappa_series)}")
        print(f"  Time Range: {results.time_points[0]:.2f} - {results.time_points[-1]:.2f} s")
        print(f"  Data Type: {results.parameters.get('data_type', 'unknown')}")
        
        if results.parameters.get('data_type') == 'synthetic':
            print(f"  Target κ̄: {results.parameters.get('kappa_target', 'N/A')}")
            print(f"  Settle Time: {self.settle_time:.1f} s")
            print(f"  Noise Level: {self.noise_level:.4f}")


def demo():
    """
    Demonstration of RFI analysis with different consciousness states.
    """
    print("RFI (Ricci Flow Index) Demonstration")
    print("====================================\n")
    
    # Initialize RFI analyzer
    rfi = RFI()
    
    # Define consciousness states with different target curvatures
    states = {
        'Awake': 0.0,           # Critical zone center
        'Light Sedation': -0.05, # Below critical zone
        'Deep Anesthesia': 0.08  # Above critical zone
    }
    
    results = {}
    
    # Analyze each state
    for state_name, kappa_target in states.items():
        print(f"\nAnalyzing {state_name} state (κ_target = {kappa_target})...")
        
        # Set random seed for reproducibility
        np.random.seed(42 + hash(state_name) % 1000)
        
        # Perform analysis
        result = rfi.analyze(kappa_target=kappa_target, sim_time=60.0, dt=0.05)
        results[state_name] = result
        
        # Print summary
        rfi.print_summary(result)
    
    # Create comparison visualization
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('RFI Analysis: Consciousness State Comparison', fontsize=16, fontweight='bold')
    
    # Plot 1: All κ̄(t) series
    ax1 = axes[0, 0]
    colors = ['green', 'orange', 'red']
    for i, (state, result) in enumerate(results.items()):
        ax1.plot(result.time_points, result.kappa_series, 
                color=colors[i], label=state, alpha=0.8)
    
    ax1.axhspan(rfi.kappa_min, rfi.kappa_max, alpha=0.2, color='gray', 
               label='Critical Zone')
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Mean Ricci Curvature κ̄(t)')
    ax1.set_title('Ricci Curvature Dynamics Comparison')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: ζ₃ comparison
    ax2 = axes[0, 1]
    state_names = list(results.keys())
    zeta_values = [results[state].zeta_3 for state in state_names]
    bars = ax2.bar(state_names, zeta_values, color=colors, alpha=0.7)
    ax2.set_ylabel('ζ₃')
    ax2.set_title('Normalized Coordinate ζ₃')
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
        summary_text += f"  ζ₃ = {result.zeta_3:.4f}\n"
        summary_text += f"  C_RFI = {result.C_RFI} ({'PASS' if result.C_RFI else 'FAIL'})\n"
        summary_text += f"  D_w = {result.D_w:.4f}\n\n"
    
    ax4.text(0.05, 0.95, summary_text, transform=ax4.transAxes,
            fontsize=11, verticalalignment='top', fontfamily='monospace',
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
    
    plt.tight_layout()
    plt.show()
    
    print("\n" + "="*50)
    print("RFI Demonstration Complete")
    print("="*50)


if __name__ == "__main__":
    demo()