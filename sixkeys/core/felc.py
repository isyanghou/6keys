#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
FELC (Free Energy Limit Cycle) - ζ₁ Indicator

自由能極限環指標：基於Hopf振盪器的臨界狀態檢測

This module implements the FELC (ζ₁) indicator for detecting critical transitions
in neural systems through free energy limit cycle analysis.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from typing import Dict, Tuple, Optional, Union
import warnings


class FELC:
    """
    Free Energy Limit Cycle (FELC) analyzer.
    
    This class implements the ζ₁ indicator based on Hopf oscillator dynamics
    to detect critical transitions in neural consciousness states.
    
    Parameters
    ----------
    sim_time : float, default=60.0
        Simulation time in seconds
    dt : float, default=0.01
        Time step for integration
    tau_smp : int, default=200
        Number of recent samples for FELC stability check
    in_band_thr : float, default=0.9
        Threshold for in-band ratio (≥90% points in band)
    cv_thr : float, default=0.2
        Coefficient of variation threshold
    w1 : float, default=0.25
        Weight for ζ₁ in D_w calculation
    theta_c : float, default=1.0
        Critical threshold for CTM pipeline
    noise_level : float, default=0.003
        Noise level for simulation
    """
    
    def __init__(self, 
                 sim_time: float = 60.0,
                 dt: float = 0.01,
                 tau_smp: int = 200,
                 in_band_thr: float = 0.9,
                 cv_thr: float = 0.2,
                 w1: float = 0.25,
                 theta_c: float = 1.0,
                 noise_level: float = 0.003):
        
        # Parameter validation
        if sim_time <= 0:
            raise ValueError("sim_time must be positive")
        if dt <= 0:
            raise ValueError("dt must be positive")
        if tau_smp <= 0:
            raise ValueError("tau_smp must be positive")
        
        self.sim_time = sim_time
        self.dt = dt
        self.tau_smp = tau_smp
        self.in_band_thr = in_band_thr
        self.cv_thr = cv_thr
        self.w1 = w1
        self.theta_c = theta_c
        self.noise_level = noise_level
        
        # Time array
        self.t = np.arange(0, sim_time, dt)
        
        # Reference band parameters (will be set from awake state)
        self.r0_ref = None
        self.delta_r_ref = None
        
        # State parameters
        self.state_params = {
            "Awake": {"lambda_gain": 1.2, "color": "tab:green"},
            "Light-Sedation": {"lambda_gain": 0.6, "color": "tab:orange"},
            "Deep-Anesthesia": {"lambda_gain": -0.2, "color": "tab:red"},
        }
    
    @staticmethod
    def hopf_dynamics(state: np.ndarray, t: float, 
                     lambda_gain: float, alpha: float = 1.0, 
                     beta: float = 0.3, omega: float = 6.0,
                     gamma: float = 0.1, delta: float = 1.0) -> np.ndarray:
        """
        Hopf oscillator dynamics.
        
        Parameters
        ----------
        state : array-like, shape (2,)
            Current state [F, G]
        t : float
            Time (not used in autonomous system)
        lambda_gain : float
            Bifurcation parameter
        alpha, beta, omega, gamma, delta : float
            Hopf oscillator parameters
            
        Returns
        -------
        derivatives : ndarray, shape (2,)
            Time derivatives [dF/dt, dG/dt]
        """
        F, G = state
        dF = lambda_gain * F - alpha * F**3 + beta * G
        dG = -omega * F + gamma * G - delta * G**3
        return np.array([dF, dG])
    
    def simulate_state(self, lambda_gain: float, 
                      alpha: float = 1.0, beta: float = 0.3,
                      omega: float = 6.0, gamma: float = 0.1, 
                      delta: float = 1.0, init: Tuple[float, float] = (0.1, 0.1),
                      noise: Optional[float] = None) -> np.ndarray:
        """
        Simulate Hopf oscillator trajectory.
        
        Parameters
        ----------
        lambda_gain : float
            Bifurcation parameter
        alpha, beta, omega, gamma, delta : float
            Hopf oscillator parameters
        init : tuple, default=(0.1, 0.1)
            Initial conditions [F0, G0]
        noise : float, optional
            Noise level (uses self.noise_level if None)
            
        Returns
        -------
        trajectory : ndarray, shape (n_timepoints, 2)
            Simulated trajectory [F(t), G(t)]
        """
        if noise is None:
            noise = self.noise_level
            
        trajectory = odeint(self.hopf_dynamics, init, self.t, 
                           args=(lambda_gain, alpha, beta, omega, gamma, delta))
        
        if noise > 0:
            trajectory += np.random.normal(0, noise, trajectory.shape)
            
        return trajectory
    
    def set_reference_band(self, awake_trajectory: np.ndarray) -> None:
        """
        Set reference band parameters from awake state trajectory.
        
        Parameters
        ----------
        awake_trajectory : ndarray, shape (n_timepoints, 2)
            Awake state trajectory
        """
        radius = np.linalg.norm(awake_trajectory, axis=1)
        # Use second half of trajectory for stability
        phi_awake = radius[len(self.t)//2:].mean()
        self.r0_ref = phi_awake
        self.delta_r_ref = 0.2 * self.r0_ref
    
    def calculate_felc_metrics(self, trajectory: np.ndarray) -> Dict[str, float]:
        """
        Calculate FELC metrics for given trajectory.
        
        Parameters
        ----------
        trajectory : ndarray, shape (n_timepoints, 2)
            Trajectory data [F(t), G(t)]
            
        Returns
        -------
        metrics : dict
            Dictionary containing:
            - C_FELC: FELC stability indicator (0 or 1)
            - D_w: Pipeline distance
            - zeta1: ζ₁ indicator value
            - phi: Mean amplitude
            - in_band_ratio: Ratio of points in reference band
            - radius: Full radius time series
        """
        if self.r0_ref is None:
            raise ValueError("Reference band not set. Call set_reference_band() first.")
        
        radius = np.linalg.norm(trajectory, axis=1)
        recent = radius[-self.tau_smp:]
        
        # In-band analysis
        in_band_mask = ((recent >= self.r0_ref - self.delta_r_ref) & 
                       (recent <= self.r0_ref + self.delta_r_ref))
        in_band_ratio = np.mean(in_band_mask)
        in_band_ok = in_band_ratio >= self.in_band_thr
        
        # Coefficient of variation check
        cv_ok = (recent.std() / recent.mean()) < self.cv_thr
        
        # Amplitude check
        amp_ok = recent.mean() > 0.05
        
        # FELC stability indicator
        C_FELC = 1 if (in_band_ok and cv_ok and amp_ok) else 0
        
        # Calculate metrics
        phi = recent.mean()
        zeta1 = (phi - self.r0_ref) / self.delta_r_ref
        D_w = np.sqrt(self.w1 * zeta1**2)
        
        return {
            'C_FELC': C_FELC,
            'D_w': D_w,
            'zeta1': zeta1,
            'phi': phi,
            'in_band_ratio': in_band_ratio,
            'radius': radius
        }
    
    def analyze_states(self, states: Optional[Dict[str, Dict]] = None) -> Dict[str, Dict]:
        """
        Analyze multiple consciousness states.
        
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
        awake_trajectory = None
        
        # First pass: simulate all trajectories
        for state_name, params in states.items():
            trajectory = self.simulate_state(params["lambda_gain"])
            results[state_name] = {
                'trajectory': trajectory,
                'color': params.get('color', 'blue')
            }
            
            if state_name == "Awake":
                awake_trajectory = trajectory
        
        # Set reference band from awake state
        if awake_trajectory is not None:
            self.set_reference_band(awake_trajectory)
        else:
            warnings.warn("No 'Awake' state found. Using first state as reference.")
            first_trajectory = list(results.values())[0]['trajectory']
            self.set_reference_band(first_trajectory)
        
        # Second pass: calculate metrics
        for state_name, data in results.items():
            metrics = self.calculate_felc_metrics(data['trajectory'])
            data.update(metrics)
        
        return results
    
    def plot_results(self, results: Dict[str, Dict], 
                    figsize: Tuple[int, int] = (12, 4)) -> plt.Figure:
        """
        Plot FELC analysis results.
        
        Parameters
        ----------
        results : dict
            Results from analyze_states()
        figsize : tuple, default=(12, 4)
            Figure size
            
        Returns
        -------
        fig : matplotlib.figure.Figure
            Figure object
        """
        fig, axes = plt.subplots(1, 3, figsize=figsize)
        
        # Phase portrait
        ax1 = axes[0]
        for name, data in results.items():
            traj = data['trajectory']
            ax1.plot(traj[:, 0], traj[:, 1], 
                    color=data['color'], label=name, alpha=0.7)
        ax1.set_xlabel('F')
        ax1.set_ylabel('G')
        ax1.set_title('Phase Portrait')
        ax1.set_aspect('equal')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Radius vs time with FELC band
        ax2 = axes[1]
        if self.r0_ref is not None:
            ax2.axhspan(self.r0_ref - self.delta_r_ref, 
                       self.r0_ref + self.delta_r_ref,
                       color='green', alpha=0.15, label='FELC Band')
        
        for name, data in results.items():
            ax2.plot(self.t, data['radius'], 
                    color=data['color'], label=f'{name}', linewidth=1)
        
        ax2.set_xlabel('Time (s)')
        ax2.set_ylabel('Radius |φ|')
        ax2.set_title('Radius vs Time')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # D_w comparison
        ax3 = axes[2]
        states = list(results.keys())
        d_w_values = [results[state]['D_w'] for state in states]
        colors = [results[state]['color'] for state in states]
        
        bars = ax3.bar(states, d_w_values, color=colors, alpha=0.7)
        ax3.axhline(self.theta_c, color='red', linestyle='--', 
                   label=f'θc = {self.theta_c}')
        ax3.set_ylabel('D_w')
        ax3.set_title('Pipeline Distance')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # Add value labels on bars
        for bar, value in zip(bars, d_w_values):
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height + 0.01,
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
        print("📋 FELC Analysis Results Summary")
        print("=" * 60)
        
        for name, data in results.items():
            state_flag = (data['C_FELC'] == 1 and data['D_w'] < self.theta_c)
            flag_txt = "✅ Conscious" if state_flag else "❌ Non-conscious"
            print(f"{name:<15} | C_FELC: {data['C_FELC']} | "
                  f"D_w: {data['D_w']:.3f} | ζ₁: {data['zeta1']:.3f} | {flag_txt}")
        
        print("\n🎯 Theory Validation Points:")
        print("1. Awake: C_FELC=1 & D_w<θc")
        print("2. Anesthesia: C_FELC=0 & D_w>θc")
        print("3. Consistent with 六鑰臨界: collapse ⇒ CTM pipeline escape ⇒ consciousness loss")
        
        if self.r0_ref is not None:
            print(f"\nℹ️  Band reference: r0 = {self.r0_ref:.3f}, "
                  f"Δr = {self.delta_r_ref:.3f}; in-band thr = {self.in_band_thr:.0%}")
    
    def analyze(self, target_energy: float = 0.0, noise_level: float = 0.05, 
                sim_time: float = 10.0, **kwargs) -> 'FELCResult':
        """
        Analyze FELC indicator for given parameters.
        
        Parameters
        ----------
        target_energy : float, default=0.0
            Target energy level (affects lambda_gain)
        noise_level : float, default=0.05
            Noise level for simulation
        sim_time : float, default=10.0
            Simulation time in seconds
        **kwargs
            Additional parameters
            
        Returns
        -------
        result : FELCResult
            Analysis result containing zeta_1 and C_FELC
        """
        # Temporarily store original parameters
        original_sim_time = self.sim_time
        original_noise_level = self.noise_level
        
        # Update parameters for this analysis
        self.sim_time = sim_time
        self.noise_level = noise_level
        self.t = np.arange(0, sim_time, self.dt)
        
        try:
            # Map target_energy to lambda_gain
            # Higher target_energy corresponds to more awake state
            if target_energy > 0.5:
                lambda_gain = 1.2  # Awake
            elif target_energy > -0.5:
                lambda_gain = 0.6  # Light sedation
            else:
                lambda_gain = -0.2  # Deep anesthesia
            
            # Simulate awake state for reference
            awake_trajectory = self.simulate_state(1.2, noise=noise_level)
            self.set_reference_band(awake_trajectory)
            
            # Simulate target state
            trajectory = self.simulate_state(lambda_gain, noise=noise_level)
            
            # Calculate metrics
            metrics = self.calculate_felc_metrics(trajectory)
            
            # Create result object
            result = FELCResult(
                zeta_1=metrics['zeta1'],
                C_FELC=metrics['C_FELC'],
                D_w=metrics['D_w'],
                phi=metrics['phi'],
                in_band_ratio=metrics['in_band_ratio'],
                trajectory=trajectory,
                radius=metrics['radius']
            )
            
            return result
            
        finally:
            # Restore original parameters
            self.sim_time = original_sim_time
            self.noise_level = original_noise_level
            self.t = np.arange(0, original_sim_time, self.dt)


class FELCResult:
    """
    Result object for FELC analysis.
    
    Attributes
    ----------
    zeta_1 : float
        ζ₁ indicator value
    C_FELC : int
        FELC stability indicator (0 or 1)
    D_w : float
        Pipeline distance
    phi : float
        Mean amplitude
    in_band_ratio : float
        Ratio of points in reference band
    trajectory : ndarray
        Simulated trajectory
    radius : ndarray
        Radius time series
    """
    
    def __init__(self, zeta_1: float, C_FELC: int, D_w: float, 
                 phi: float, in_band_ratio: float, 
                 trajectory: np.ndarray, radius: np.ndarray):
        self.zeta_1 = zeta_1
        self.C_FELC = C_FELC
        self.D_w = D_w
        self.phi = phi
        self.in_band_ratio = in_band_ratio
        self.trajectory = trajectory
        self.radius = radius
    
    def __repr__(self):
        return (f"FELCResult(zeta_1={self.zeta_1:.3f}, C_FELC={self.C_FELC}, "
                f"D_w={self.D_w:.3f}, phi={self.phi:.3f})")


def demo():
    """
    Run FELC demonstration.
    """
    # Set random seed for reproducibility
    np.random.seed(0)
    
    # Create FELC analyzer
    felc = FELC()
    
    # Analyze states
    results = felc.analyze_states()
    
    # Plot results
    fig = felc.plot_results(results)
    
    # Print summary
    felc.print_summary(results)
    
    return felc, results, fig


if __name__ == "__main__":
    felc, results, fig = demo()
    plt.show()