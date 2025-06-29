#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TEB (Thermodynamic Efficiency Balance) - ζ₂ Indicator

資訊-能耗效率平衡指標：基於熱力學效率的臨界狀態檢測

This module implements the TEB (ζ₂) indicator for analyzing information-energy
efficiency in neural systems.
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, Tuple, Optional
import warnings


class TEB:
    """
    Thermodynamic Efficiency Balance (TEB) analyzer.
    
    This class implements the ζ₂ indicator based on information-energy efficiency
    to detect critical transitions in neural consciousness states.
    
    Parameters
    ----------
    sim_time : float, default=50.0
        Simulation time in seconds
    dt : float, default=0.05
        Time step for simulation
    tau_smp : int, default=200
        Number of recent samples for TEB stability check
    eta_min : float, default=0.85
        Minimum efficiency threshold (kbit/J)
    eta_max : float, default=1.15
        Maximum efficiency threshold (kbit/J)
    w7 : float, default=0.15
        Weight for ζ₂ in D_w calculation
    theta_c : float, default=1.0
        Critical threshold for CTM pipeline
    in_band_thr : float, default=0.90
        Threshold for in-band ratio (≥90% points in band)
    noise_level : float, default=0.03
        Noise level for simulation
    settle_time : float, default=6.0
        Time constant for system settling
    """
    
    def __init__(self,
                 sim_time: float = 50.0,
                 dt: float = 0.05,
                 tau_smp: int = 200,
                 eta_min: float = 0.85,
                 eta_max: float = 1.15,
                 w7: float = 0.15,
                 theta_c: float = 1.0,
                 in_band_thr: float = 0.90,
                 noise_level: float = 0.03,
                 settle_time: float = 6.0):
        
        self.sim_time = sim_time
        self.dt = dt
        self.tau_smp = tau_smp
        self.eta_min = eta_min
        self.eta_max = eta_max
        self.w7 = w7
        self.theta_c = theta_c
        self.in_band_thr = in_band_thr
        self.noise_level = noise_level
        self.settle_time = settle_time
        
        # Time array
        self.t = np.arange(0, sim_time, dt)
        
        # Derived parameters
        self.eta_ast = 0.5 * (eta_min + eta_max)  # Reference efficiency
        self.eps7 = 0.5 * (eta_max - eta_min)     # Half-band width
        
        # State parameters
        self.state_params = {
            "Optimal": {"eta_target": 1.00, "color": "tab:green"},
            "Sub-Optimal": {"eta_target": 0.90, "color": "tab:orange"},
            "Inefficient": {"eta_target": 0.70, "color": "tab:red"},
        }
    
    def simulate_pair(self, eta_target: float, 
                     noise: Optional[float] = None) -> Tuple[np.ndarray, np.ndarray]:
        """
        Simulate information rate and power consumption pair.
        
        Parameters
        ----------
        eta_target : float
            Target efficiency (kbit/J)
        noise : float, optional
            Noise level (uses self.noise_level if None)
            
        Returns
        -------
        I : ndarray
            Information rate time series (kbit/s)
        P : ndarray
            Power consumption time series (mW)
        """
        if noise is None:
            noise = self.noise_level
        
        I = np.zeros_like(self.t)  # Information rate (kbit/s)
        P = np.zeros_like(self.t)  # Power consumption (mW)
        
        # Initial conditions
        I[0] = 100.0
        P[0] = I[0] / eta_target
        
        # Simulate dynamics with exponential settling
        for i in range(1, len(self.t)):
            dt = self.t[i] - self.t[i-1]
            
            # Information rate settling to baseline
            I[i] = I[i-1] + (100.0 - I[i-1]) * dt / self.settle_time
            
            # Power consumption tracking target efficiency
            P_target = I[i] / eta_target
            P[i] = P[i-1] + (P_target - P[i-1]) * dt / self.settle_time
        
        # Add noise
        if noise > 0:
            I += np.random.normal(0, noise * I.mean(), len(self.t))
            P += np.random.normal(0, noise * P.mean(), len(self.t))
        
        # Ensure positive power
        P = np.clip(P, 1e-3, None)
        
        return I, P
    
    def calculate_teb_metrics(self, I: np.ndarray, P: np.ndarray) -> Dict[str, float]:
        """
        Calculate TEB metrics for given information rate and power consumption.
        
        Parameters
        ----------
        I : ndarray
            Information rate time series (kbit/s)
        P : ndarray
            Power consumption time series (mW)
            
        Returns
        -------
        metrics : dict
            Dictionary containing:
            - C_TEB: TEB stability indicator (0 or 1)
            - D_w: Pipeline distance
            - zeta2: ζ₂ indicator value
            - eta: Efficiency time series
            - in_band_ratio: Ratio of points in efficiency band
        """
        # Calculate efficiency
        eta = I / P  # kbit/J
        
        # Analyze recent samples
        recent = eta[-self.tau_smp:]
        
        # In-band analysis
        in_band_mask = ((recent >= self.eta_min) & (recent <= self.eta_max))
        in_band_ratio = np.mean(in_band_mask)
        
        # TEB stability indicator
        C_TEB = 1 if in_band_ratio >= self.in_band_thr else 0
        
        # Calculate ζ₂ indicator
        zeta2 = (recent.mean() - self.eta_ast) / self.eps7
        
        # Pipeline distance
        D_w = np.sqrt(self.w7 * zeta2**2)
        
        return {
            'C_TEB': C_TEB,
            'D_w': D_w,
            'zeta2': zeta2,
            'eta': eta,
            'in_band_ratio': in_band_ratio,
            'I': I,
            'P': P
        }
    
    def analyze_states(self, states: Optional[Dict[str, Dict]] = None) -> Dict[str, Dict]:
        """
        Analyze multiple efficiency states.
        
        Parameters
        ----------
        states : dict, optional
            Dictionary of state parameters. Uses default if None.
            
        Returns
        -------
        results : dict
            Analysis results for each state
        """
        if states is None:
            states = self.state_params
        
        results = {}
        
        for state_name, params in states.items():
            # Simulate information-power pair
            I, P = self.simulate_pair(params["eta_target"])
            
            # Calculate metrics
            metrics = self.calculate_teb_metrics(I, P)
            
            # Store results
            results[state_name] = {
                **metrics,
                'color': params.get('color', 'blue'),
                'eta_target': params["eta_target"]
            }
        
        return results
    
    def plot_results(self, results: Dict[str, Dict], 
                    figsize: Tuple[int, int] = (15, 4)) -> plt.Figure:
        """
        Plot TEB analysis results.
        
        Parameters
        ----------
        results : dict
            Results from analyze_states()
        figsize : tuple, default=(15, 4)
            Figure size
            
        Returns
        -------
        fig : matplotlib.figure.Figure
            Figure object
        """
        fig, axes = plt.subplots(1, 3, figsize=figsize)
        
        # Efficiency vs time
        ax1 = axes[0]
        ax1.fill_between([0, self.sim_time], self.eta_min, self.eta_max,
                        color="tab:green", alpha=0.12, label="Critical η-band")
        
        for name, data in results.items():
            ax1.plot(self.t, data['eta'], color=data['color'], 
                    label=f"{name} (η={data['eta_target']:.2f})", linewidth=1.5)
        
        ax1.set_xlabel('Time (s)')
        ax1.set_ylabel(r'Efficiency $\eta(t)$ (kbit J$^{-1}$)')
        ax1.set_title('Information-Energy Efficiency vs Time')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # C_TEB and ζ₂ comparison
        ax2 = axes[1]
        states = list(results.keys())
        x = np.arange(len(states))
        width = 0.35
        
        # C_TEB bars
        c_teb_values = [results[state]['C_TEB'] for state in states]
        ax2.bar(x - width/2, c_teb_values, width, 
               color='lightgray', label='C_TEB (binary)', alpha=0.7)
        ax2.set_ylim(-0.1, 1.1)
        ax2.set_ylabel('C_TEB', color='gray')
        ax2.set_xticks(x)
        ax2.set_xticklabels(states, rotation=10)
        
        # ζ₂ line plot
        ax3 = ax2.twinx()
        zeta2_values = [results[state]['zeta2'] for state in states]
        ax3.plot(x + width/2, zeta2_values, 'o-', 
                color='tab:blue', label=r'$\zeta_2$', markersize=8)
        ax3.set_ylabel(r'Normalised coord. $\zeta_2$', color='tab:blue')
        
        # Combined legend
        lines1, labels1 = ax2.get_legend_handles_labels()
        lines2, labels2 = ax3.get_legend_handles_labels()
        ax2.legend(lines1 + lines2, labels1 + labels2, loc='upper right')
        ax2.set_title('C_TEB and ζ₂ per State')
        ax2.grid(True, alpha=0.3)
        
        # D_w comparison
        ax4 = axes[2]
        d_w_values = [results[state]['D_w'] for state in states]
        colors = [results[state]['color'] for state in states]
        
        bars = ax4.bar(states, d_w_values, color=colors, alpha=0.7)
        ax4.axhline(self.theta_c, color='red', linestyle='--', 
                   label=f'θc = {self.theta_c}')
        ax4.set_ylabel('D_w')
        ax4.set_title('Pipeline Distance')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        # Add value labels on bars
        for bar, value in zip(bars, d_w_values):
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                    f'{value:.3f}', ha='center', va='bottom')
        
        plt.tight_layout()
        return fig
    
    def print_summary(self, results: Dict[str, Dict]) -> None:
        """
        Print analysis summary.
        
        Parameters
        ----------
        results : dict
            Results from analyze_states()
        """
        print("=" * 60)
        print("📋 TEB Analysis Results Summary")
        print("=" * 60)
        
        for name, data in results.items():
            efficiency_flag = (data['C_TEB'] == 1 and data['D_w'] < self.theta_c)
            flag_txt = "✅ Efficient" if efficiency_flag else "❌ Inefficient"
            print(f"{name:<15} | C_TEB: {data['C_TEB']} | "
                  f"in-band: {data['in_band_ratio']*100:5.1f}% | "
                  f"ζ₂: {data['zeta2']:+6.3f} | D_w: {data['D_w']:.3f} | {flag_txt}")
        
        print("\n🎯 Theory Validation Points:")
        print("1. Optimal: C_TEB=1 & D_w<θc (high efficiency)")
        print("2. Inefficient: C_TEB=0 & D_w>θc (low efficiency)")
        print("3. Consistent with 六鑰臨界: efficiency loss ⇒ CTM pipeline escape")
        
        print(f"\nℹ️  Efficiency band: [{self.eta_min:.2f}, {self.eta_max:.2f}] kbit/J; "
              f"in-band thr = {self.in_band_thr:.0%}")
    
    def analyze(self, target_efficiency: float = 0.75, noise_level: float = 0.03,
                sim_time: float = 10.0, **kwargs) -> 'TEBResult':
        """
        Analyze TEB indicator for given parameters.
        
        Parameters
        ----------
        target_efficiency : float, default=0.75
            Target efficiency level (kbit/J)
        noise_level : float, default=0.03
            Noise level for simulation
        sim_time : float, default=10.0
            Simulation time in seconds
        **kwargs
            Additional parameters
            
        Returns
        -------
        result : TEBResult
            Analysis result containing zeta_2 and C_TEB
        """
        # Input validation
        if sim_time <= 0:
            raise ValueError("sim_time must be positive")
        if self.dt <= 0:
            raise ValueError("dt must be positive")
        if sim_time <= self.dt:
            raise ValueError("sim_time must be greater than dt")
        
        # Temporarily store original parameters
        original_sim_time = self.sim_time
        original_noise_level = self.noise_level
        
        # Update parameters for this analysis
        self.sim_time = sim_time
        self.noise_level = noise_level
        self.t = np.arange(0, sim_time, self.dt)
        
        # Ensure we have at least one time point
        if len(self.t) == 0:
            raise ValueError("Time array is empty - check sim_time and dt parameters")
        
        try:
            # Simulate information-power pair
            I, P = self.simulate_pair(target_efficiency, noise=noise_level)
            
            # Calculate metrics
            metrics = self.calculate_teb_metrics(I, P)
            
            # Create result object
            result = TEBResult(
                zeta_2=metrics['zeta2'],
                C_TEB=metrics['C_TEB'],
                D_w=metrics['D_w'],
                eta=metrics['eta'],
                in_band_ratio=metrics['in_band_ratio'],
                I=metrics['I'],
                P=metrics['P']
            )
            
            return result
            
        finally:
            # Restore original parameters
            self.sim_time = original_sim_time
            self.noise_level = original_noise_level
            self.t = np.arange(0, original_sim_time, self.dt)


class TEBResult:
    """
    Result object for TEB analysis.
    
    Attributes
    ----------
    zeta_2 : float
        ζ₂ indicator value
    C_TEB : int
        TEB stability indicator (0 or 1)
    D_w : float
        Pipeline distance
    eta : ndarray
        Efficiency time series
    in_band_ratio : float
        Ratio of points in efficiency band
    I : ndarray
        Information rate time series
    P : ndarray
        Power consumption time series
    """
    
    def __init__(self, zeta_2: float, C_TEB: int, D_w: float, 
                 eta: np.ndarray, in_band_ratio: float, 
                 I: np.ndarray, P: np.ndarray):
        self.zeta_2 = zeta_2
        self.C_TEB = C_TEB
        self.D_w = D_w
        self.eta = eta
        self.in_band_ratio = in_band_ratio
        self.I = I
        self.P = P
    
    def __repr__(self):
        return (f"TEBResult(zeta_2={self.zeta_2:.3f}, C_TEB={self.C_TEB}, "
                f"D_w={self.D_w:.3f}, in_band_ratio={self.in_band_ratio:.3f})")


def demo():
    """
    Run TEB demonstration.
    """
    # Set random seed for reproducibility
    np.random.seed(2025)
    
    # Create TEB analyzer
    teb = TEB()
    
    # Analyze states
    results = teb.analyze_states()
    
    # Plot results
    fig = teb.plot_results(results)
    
    # Print summary
    teb.print_summary(results)
    
    return teb, results, fig


if __name__ == "__main__":
    teb, results, fig = demo()
    plt.show()