"""Six Keys Radar Chart Visualization

This module provides integrated radar chart visualization for all six key indicators
of consciousness analysis. It simulates the dimensionless coordinates ζ_i, binary
critical flags C_i, and weighted distances D_w_i for different consciousness states.

Example:
    >>> from sixkeys.demos import SixKeysRadarChart
    >>> radar = SixKeysRadarChart()
    >>> radar.simulate_and_plot()
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, Tuple, List, Optional


class SixKeysRadarChart:
    """Six Keys Integrated Radar Chart Visualization.
    
    This class simulates and visualizes the six key indicators (FELC, RFI, ECGP, 
    PWC, ACI, TEB) using radar charts and bar plots to demonstrate consciousness
    state transitions.
    """
    
    def __init__(self, 
                 keys: Optional[List[str]] = None,
                 weights: Optional[np.ndarray] = None,
                 theta_c: float = 1.0,
                 random_seed: int = 2025):
        """Initialize the radar chart visualizer.
        
        Args:
            keys: List of key indicator names. Defaults to standard six keys.
            weights: Weight array for each indicator. Defaults to equal weights.
            theta_c: Global critical threshold. Defaults to 1.0.
            random_seed: Random seed for reproducible results.
        """
        self.keys = keys or ["FELC", "RFI", "ECGP", "PWC", "ACI", "TEB"]
        self.n_keys = len(self.keys)
        self.weights = weights if weights is not None else np.full(self.n_keys, 1.0 / self.n_keys)
        self.theta_c = theta_c
        self.random_seed = random_seed
        
        # Default consciousness state parameters
        self.state_mu = {
            "Awake": 0.00,
            "Light-Sedation": -0.60,
            "Deep-Anesthesia": -1.80,
        }
        self.sigma_z = 0.10  # ζ perturbation standard deviation
        
        # Set random seed
        np.random.seed(self.random_seed)
        
        # Results storage
        self.results = {}
    
    def simulate_state(self, mu: float) -> Tuple[np.ndarray, np.ndarray, np.ndarray, float]:
        """Simulate a consciousness state with given mean ζ value.
        
        Args:
            mu: Mean value for ζ distribution
            
        Returns:
            Tuple of (zetas, critical_flags, weighted_distances, total_distance)
        """
        zetas = np.random.normal(mu, self.sigma_z, self.n_keys)
        critical_flags = (np.abs(zetas) <= 1.0).astype(int)  # |ζ|≤1 considered passing
        weighted_distances = np.sqrt(self.weights * zetas**2)
        total_distance = np.sqrt(np.sum(self.weights * zetas**2))
        
        return zetas, critical_flags, weighted_distances, total_distance
    
    def simulate_all_states(self) -> Dict:
        """Simulate all predefined consciousness states.
        
        Returns:
            Dictionary containing simulation results for each state
        """
        self.results = {}
        for state, mu in self.state_mu.items():
            z, C, Dw, Dtot = self.simulate_state(mu)
            self.results[state] = {
                'z': z, 
                'C': C, 
                'Dw': Dw, 
                'Dtot': Dtot
            }
        return self.results
    
    def plot_radar_chart(self, figsize: Tuple[int, int] = (6, 5)) -> plt.Figure:
        """Create radar chart visualization.
        
        Args:
            figsize: Figure size tuple
            
        Returns:
            Matplotlib figure object
        """
        if not self.results:
            self.simulate_all_states()
        
        angles = np.linspace(0, 2*np.pi, self.n_keys + 1)
        fig, ax = plt.subplots(subplot_kw={"polar": True}, figsize=figsize)
        
        colors = ["tab:green", "tab:orange", "tab:red"]
        
        for (state, color) in zip(self.state_mu.keys(), colors):
            vals = np.abs(self.results[state]["z"])
            vals = np.concatenate([vals, [vals[0]]])  # Close the polygon
            ax.plot(angles, vals, "o-", lw=1.8, label=state, color=color)
            ax.fill(angles, vals, alpha=0.12, color=color)
        
        ax.set_thetagrids(angles[:-1] * 180/np.pi, self.keys)
        ax.set_title("Six-Key |ζ| Radar Chart")
        ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.25), ncol=3, frameon=False)
        
        return fig
    
    def plot_distance_bar(self, figsize: Tuple[int, int] = (5, 3)) -> plt.Figure:
        """Create total distance bar chart.
        
        Args:
            figsize: Figure size tuple
            
        Returns:
            Matplotlib figure object
        """
        if not self.results:
            self.simulate_all_states()
        
        fig, ax = plt.subplots(figsize=figsize)
        
        states = list(self.state_mu.keys())
        D_vals = [self.results[s]["Dtot"] for s in states]
        colors = ["tab:green", "tab:orange", "tab:red"]
        
        bars = ax.bar(states, D_vals, color=colors)
        ax.axhline(self.theta_c, ls="--", lw=1, label=f"θ_c = {self.theta_c}")
        ax.set_ylabel("D_total")
        ax.set_title("Global Consciousness Margin")
        ax.legend()
        
        return fig
    
    def print_summary(self) -> None:
        """Print detailed summary of simulation results."""
        if not self.results:
            self.simulate_all_states()
        
        print("=== Six-Key Integration — Summary ===")
        
        states = list(self.state_mu.keys())
        for state in states:
            d = self.results[state]
            status = 'PASS' if d['Dtot'] < self.theta_c else 'FAIL'
            print(f"\n[{state}]  D_total = {d['Dtot']:.3f}  {status}  | θ_c={self.theta_c}")
            
            for k, ζ, c, dw in zip(self.keys, d['z'], d['C'], d['Dw']):
                print(f"  {k:4s}: ζ={ζ:+5.2f}  C={c}  D_w={dw:.3f}")
    
    def simulate_and_plot(self, 
                         show_plots: bool = True, 
                         save_plots: bool = False,
                         output_dir: str = "./") -> Tuple[plt.Figure, plt.Figure]:
        """Complete simulation and visualization workflow.
        
        Args:
            show_plots: Whether to display plots
            save_plots: Whether to save plots to files
            output_dir: Directory to save plots
            
        Returns:
            Tuple of (radar_figure, bar_figure)
        """
        # Configure matplotlib
        plt.rcParams.update({"figure.dpi": 120, "font.size": 11})
        
        # Simulate all states
        self.simulate_all_states()
        
        # Create visualizations
        fig_radar = self.plot_radar_chart()
        fig_bar = self.plot_distance_bar()
        
        # Save plots if requested
        if save_plots:
            fig_radar.savefig(f"{output_dir}/sixkeys_radar_chart.png", 
                            dpi=300, bbox_inches='tight')
            fig_bar.savefig(f"{output_dir}/sixkeys_distance_bar.png", 
                          dpi=300, bbox_inches='tight')
        
        # Show plots if requested
        if show_plots:
            plt.show()
        
        # Print summary
        self.print_summary()
        
        return fig_radar, fig_bar
    
    def update_state_parameters(self, new_state_mu: Dict[str, float]) -> None:
        """Update consciousness state parameters.
        
        Args:
            new_state_mu: Dictionary mapping state names to mean ζ values
        """
        self.state_mu.update(new_state_mu)
        # Clear previous results
        self.results = {}
    
    def add_custom_state(self, state_name: str, mu: float) -> None:
        """Add a custom consciousness state.
        
        Args:
            state_name: Name of the new state
            mu: Mean ζ value for the new state
        """
        self.state_mu[state_name] = mu
        # Clear previous results to force re-simulation
        self.results = {}


# Convenience function for quick usage
def quick_demo(show_plots: bool = True) -> None:
    """Quick demonstration of the radar chart functionality.
    
    Args:
        show_plots: Whether to display the plots
    """
    radar = SixKeysRadarChart()
    radar.simulate_and_plot(show_plots=show_plots)


if __name__ == "__main__":
    # Run demo when script is executed directly
    quick_demo()