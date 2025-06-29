# -*- coding: utf-8 -*-
"""
ACI (Astrocyte-Coupling Index) - ζ₆ Indicator

六鑰臨界第六鑰：星形膠質細胞耦合指標

This module implements the Astrocyte-Coupling Index (ACI) for neural criticality analysis.
ACI measures the coupling strength between astrocytes and neurons to assess criticality.
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Optional, Tuple, Union, Any
import warnings
from dataclasses import dataclass


@dataclass
class ACIResults:
    """
    Results from ACI analysis.
    
    Attributes
    ----------
    coupling_series : np.ndarray
        Time series of coupling strength A(t)
    zeta_6 : float
        Normalized coordinate ζ₆
    C_ACI : int
        Binary criterion (1 if in critical zone, 0 otherwise)
    D_w : float
        Weighted distance contribution
    time_points : np.ndarray
        Time points for the analysis
    parameters : dict
        Analysis parameters used
    """
    coupling_series: np.ndarray
    zeta_6: float
    C_ACI: int
    D_w: float
    time_points: np.ndarray
    parameters: Dict[str, Any]


class ACI:
    """
    Astrocyte-Coupling Index (ACI) - ζ₆ Indicator
    
    Implements the sixth key of Six Keys Criticality framework.
    Analyzes astrocyte-neuron coupling strength to assess criticality.
    
    Parameters
    ----------
    a_min : float, default=0.3
        Lower bound of critical coupling zone
    a_max : float, default=0.7
        Upper bound of critical coupling zone
    tau_samples : int, default=160
        Number of samples for ACI window analysis
    weight : float, default=0.12
        Weight factor for distance calculation
    settle_time : float, default=15.0
        Time constant for exponential relaxation in simulation
    noise_level : float, default=0.06
        Noise level for synthetic data generation
    """
    
    def __init__(self, 
                 a_min: float = 0.3,
                 a_max: float = 0.7,
                 tau_samples: int = 160,
                 weight: float = 0.12,
                 settle_time: float = 15.0,
                 noise_level: float = 0.06):
        
        self.a_min = a_min
        self.a_max = a_max
        self.tau_samples = tau_samples
        self.weight = weight
        self.settle_time = settle_time
        self.noise_level = noise_level
        
        # Validation
        if a_min >= a_max:
            raise ValueError("a_min must be less than a_max")
        if not (0 <= a_min <= 1 and 0 <= a_max <= 1):
            raise ValueError("Coupling bounds must be between 0 and 1")
        if tau_samples <= 0:
            raise ValueError("tau_samples must be positive")
        if weight <= 0:
            raise ValueError("weight must be positive")
    
    def simulate_coupling_series(self, 
                               time_points: np.ndarray, 
                               a_target: float) -> np.ndarray:
        """
        Generate synthetic astrocyte coupling time series.
        
        Parameters
        ----------
        time_points : np.ndarray
            Time points for simulation
        a_target : float
            Target coupling strength for relaxation
            
        Returns
        -------
        np.ndarray
            Simulated A(t) time series
        """
        if not (0 <= a_target <= 1):
            raise ValueError("a_target must be between 0 and 1")
        
        coupling = np.zeros_like(time_points)
        coupling[0] = 0.5  # Start at middle value
        
        for i in range(1, len(time_points)):
            dt = time_points[i] - time_points[i-1]
            # First-order exponential approach with slow oscillations
            coupling[i] = coupling[i-1] + (a_target - coupling[i-1]) * dt / self.settle_time
            # Add slow oscillatory component to simulate astrocyte dynamics
            coupling[i] += 0.03 * np.sin(2 * np.pi * time_points[i] / 20.0)
        
        # Add Gaussian noise and clip to [0, 1]
        coupling += np.random.normal(0, self.noise_level, len(time_points))
        coupling = np.clip(coupling, 0, 1)
        
        return coupling
    
    def compute_aci(self, coupling_series: np.ndarray) -> Tuple[float, int]:
        """
        Compute ACI indicator from coupling time series.
        
        Parameters
        ----------
        coupling_series : np.ndarray
            Astrocyte coupling strength time series A(t)
            
        Returns
        -------
        tuple
            (ζ₆, C_ACI) - normalized coordinate and binary criterion
        """
        if len(coupling_series) < self.tau_samples:
            warnings.warn(f"Series length ({len(coupling_series)}) < tau_samples ({self.tau_samples})")
            analysis_window = coupling_series
        else:
            # Use last tau_samples for analysis
            analysis_window = coupling_series[-self.tau_samples:]
        
        # Check if values remain in critical coupling zone
        in_zone = np.all((analysis_window >= self.a_min) & 
                        (analysis_window <= self.a_max))
        C_ACI = 1 if in_zone else 0
        
        # Compute normalized coordinate ζ₆
        mean_a = np.mean(analysis_window)
        
        if C_ACI == 1:
            # In critical zone: ζ₆ based on position within zone
            zone_center = (self.a_min + self.a_max) / 2
            zone_width = self.a_max - self.a_min
            zeta_6 = (mean_a - zone_center) / (zone_width / 2)
        else:
            # Outside critical zone: ζ₆ based on distance from zone
            if mean_a < self.a_min:
                zeta_6 = (mean_a - self.a_min) / self.a_min
            else:  # mean_a > self.a_max
                zeta_6 = (mean_a - self.a_max) / (1 - self.a_max)
        
        return zeta_6, C_ACI
    
    def analyze(self, 
                data: Optional[np.ndarray] = None,
                time_points: Optional[np.ndarray] = None,
                a_target: Optional[float] = None,
                sim_time: float = 60.0,
                dt: float = 0.12) -> ACIResults:
        """
        Perform ACI analysis on data or generate synthetic data.
        
        Parameters
        ----------
        data : np.ndarray, optional
            Real coupling data. If None, synthetic data is generated.
        time_points : np.ndarray, optional
            Time points corresponding to data
        a_target : float, optional
            Target coupling strength for synthetic data generation
        sim_time : float, default=60.0
            Simulation time for synthetic data
        dt : float, default=0.12
            Time step for synthetic data
            
        Returns
        -------
        ACIResults
            Complete analysis results
        """
        if data is not None:
            # Use provided data
            coupling_series = np.array(data)
            if time_points is not None:
                time_array = np.array(time_points)
            else:
                time_array = np.arange(len(coupling_series)) * dt
        else:
            # Generate synthetic data
            if a_target is None:
                a_target = (self.a_min + self.a_max) / 2  # Default to critical zone center
            
            time_array = np.arange(0, sim_time, dt)
            coupling_series = self.simulate_coupling_series(time_array, a_target)
        
        # Compute ACI indicators
        zeta_6, C_ACI = self.compute_aci(coupling_series)
        
        # Compute weighted distance
        D_w = np.sqrt(self.weight * zeta_6**2)
        
        # Store parameters
        parameters = {
            'a_min': self.a_min,
            'a_max': self.a_max,
            'tau_samples': self.tau_samples,
            'weight': self.weight,
            'settle_time': self.settle_time,
            'noise_level': self.noise_level,
            'a_target': a_target if data is None else None,
            'data_type': 'synthetic' if data is None else 'real'
        }
        
        return ACIResults(
            coupling_series=coupling_series,
            zeta_6=zeta_6,
            C_ACI=C_ACI,
            D_w=D_w,
            time_points=time_array,
            parameters=parameters
        )
    
    def plot_analysis(self, results: ACIResults, figsize: Tuple[int, int] = (12, 8)) -> None:
        """
        Create comprehensive visualization of ACI analysis.
        
        Parameters
        ----------
        results : ACIResults
            Analysis results to visualize
        figsize : tuple, default=(12, 8)
            Figure size (width, height)
        """
        fig, axes = plt.subplots(2, 2, figsize=figsize)
        fig.suptitle('ACI (Astrocyte-Coupling Index) Analysis - ζ₆', 
                    fontsize=16, fontweight='bold')
        
        # Plot 1: A(t) time series with critical zone
        ax1 = axes[0, 0]
        ax1.plot(results.time_points, results.coupling_series, 'b-', 
                linewidth=1.5, alpha=0.8, label='A(t)')
        ax1.axhspan(self.a_min, self.a_max, alpha=0.2, color='green', 
                   label=f'Critical Zone [{self.a_min:.2f}, {self.a_max:.2f}]')
        ax1.axhline(self.a_min, color='green', linestyle='--', alpha=0.7)
        ax1.axhline(self.a_max, color='green', linestyle='--', alpha=0.7)
        ax1.set_xlabel('Time (s)')
        ax1.set_ylabel('Astrocyte Coupling Strength A(t)')
        ax1.set_title('Astrocyte-Neuron Coupling Dynamics')
        ax1.set_ylim(0, 1)
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Analysis window detail
        ax2 = axes[0, 1]
        if len(results.coupling_series) >= self.tau_samples:
            window_data = results.coupling_series[-self.tau_samples:]
            window_time = results.time_points[-self.tau_samples:]
        else:
            window_data = results.coupling_series
            window_time = results.time_points
        
        ax2.plot(window_time, window_data, 'r-', linewidth=2, label='Analysis Window')
        ax2.axhspan(self.a_min, self.a_max, alpha=0.2, color='green')
        ax2.axhline(np.mean(window_data), color='orange', linestyle='-', 
                   label=f'Mean = {np.mean(window_data):.3f}')
        ax2.set_xlabel('Time (s)')
        ax2.set_ylabel('A(t)')
        ax2.set_title(f'Analysis Window (τ = {self.tau_samples} samples)')
        ax2.set_ylim(0, 1)
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: ACI indicators
        ax3 = axes[1, 0]
        indicators = ['ζ₆', 'C_ACI', 'D_w']
        values = [results.zeta_6, results.C_ACI, results.D_w]
        colors = ['blue', 'green' if results.C_ACI else 'red', 'purple']
        
        bars = ax3.bar(indicators, values, color=colors, alpha=0.7)
        ax3.set_ylabel('Value')
        ax3.set_title('ACI Indicators')
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
ACI Analysis Summary
{'='*25}

Indicators:
  ζ₆ = {results.zeta_6:.4f}
  C_ACI = {results.C_ACI} ({'PASS' if results.C_ACI else 'FAIL'})
  D_w = {results.D_w:.4f}

Parameters:
  Critical Zone: [{self.a_min:.2f}, {self.a_max:.2f}]
  Analysis Window: {self.tau_samples} samples
  Weight: {self.weight:.3f}
  
Data Type: {results.parameters.get('data_type', 'unknown')}
"""
        
        ax4.text(0.05, 0.95, param_text, transform=ax4.transAxes, 
                fontsize=10, verticalalignment='top', fontfamily='monospace',
                bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.8))
        
        plt.tight_layout()
        plt.show()
    
    def print_summary(self, results: ACIResults) -> None:
        """
        Print detailed analysis summary.
        
        Parameters
        ----------
        results : ACIResults
            Analysis results to summarize
        """
        print("\n" + "="*50)
        print("ACI (Astrocyte-Coupling Index) Analysis Summary")
        print("="*50)
        
        print(f"\nKey Indicators:")
        print(f"  ζ₆ (Normalized Coordinate): {results.zeta_6:.6f}")
        print(f"  C_ACI (Binary Criterion):  {results.C_ACI} ({'PASS' if results.C_ACI else 'FAIL'})")
        print(f"  D_w (Weighted Distance):    {results.D_w:.6f}")
        
        print(f"\nCoupling Analysis:")
        print(f"  Critical Zone: [{self.a_min:.3f}, {self.a_max:.3f}]")
        print(f"  Mean A(t): {np.mean(results.coupling_series):.6f}")
        print(f"  Std A(t):  {np.std(results.coupling_series):.6f}")
        
        if len(results.coupling_series) >= self.tau_samples:
            window_data = results.coupling_series[-self.tau_samples:]
            print(f"  Window Mean A(t): {np.mean(window_data):.6f}")
            print(f"  Window Std A(t):  {np.std(window_data):.6f}")
        
        print(f"\nParameters:")
        print(f"  Analysis Window: {self.tau_samples} samples")
        print(f"  Weight Factor: {self.weight:.3f}")
        print(f"  Data Points: {len(results.coupling_series)}")
        print(f"  Time Range: {results.time_points[0]:.2f} - {results.time_points[-1]:.2f} s")
        print(f"  Data Type: {results.parameters.get('data_type', 'unknown')}")
        
        if results.parameters.get('data_type') == 'synthetic':
            print(f"  Target A: {results.parameters.get('a_target', 'N/A')}")
            print(f"  Settle Time: {self.settle_time:.1f} s")
            print(f"  Noise Level: {self.noise_level:.4f}")


def demo():
    """
    Demonstration of ACI analysis with different consciousness states.
    """
    print("ACI (Astrocyte-Coupling Index) Demonstration")
    print("===========================================\n")
    
    # Initialize ACI analyzer
    aci = ACI()
    
    # Define consciousness states with different target coupling strengths
    states = {
        'Awake': 0.5,           # Critical zone center
        'Light Sedation': 0.2,  # Below critical zone
        'Deep Anesthesia': 0.85 # Above critical zone
    }
    
    results = {}
    
    # Analyze each state
    for state_name, a_target in states.items():
        print(f"\nAnalyzing {state_name} state (A_target = {a_target})...")
        
        # Set random seed for reproducibility
        np.random.seed(42 + hash(state_name) % 1000)
        
        # Perform analysis
        result = aci.analyze(a_target=a_target, sim_time=60.0, dt=0.12)
        results[state_name] = result
        
        # Print summary
        aci.print_summary(result)
    
    # Create comparison visualization
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('ACI Analysis: Consciousness State Comparison', fontsize=16, fontweight='bold')
    
    # Plot 1: All A(t) series
    ax1 = axes[0, 0]
    colors = ['green', 'orange', 'red']
    for i, (state, result) in enumerate(results.items()):
        ax1.plot(result.time_points, result.coupling_series, 
                color=colors[i], label=state, alpha=0.8)
    
    ax1.axhspan(aci.a_min, aci.a_max, alpha=0.2, color='gray', 
               label='Critical Zone')
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Astrocyte Coupling Strength A(t)')
    ax1.set_title('Coupling Dynamics Comparison')
    ax1.set_ylim(0, 1)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: ζ₆ comparison
    ax2 = axes[0, 1]
    state_names = list(results.keys())
    zeta_values = [results[state].zeta_6 for state in state_names]
    bars = ax2.bar(state_names, zeta_values, color=colors, alpha=0.7)
    ax2.set_ylabel('ζ₆')
    ax2.set_title('Normalized Coordinate ζ₆')
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
        summary_text += f"  ζ₆ = {result.zeta_6:.4f}\n"
        summary_text += f"  C_ACI = {result.C_ACI} ({'PASS' if result.C_ACI else 'FAIL'})\n"
        summary_text += f"  D_w = {result.D_w:.4f}\n\n"
    
    ax4.text(0.05, 0.95, summary_text, transform=ax4.transAxes,
            fontsize=11, verticalalignment='top', fontfamily='monospace',
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
    
    plt.tight_layout()
    plt.show()
    
    print("\n" + "="*50)
    print("ACI Demonstration Complete")
    print("="*50)


if __name__ == "__main__":
    demo()