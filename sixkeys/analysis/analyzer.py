#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Six Keys Criticality Analyzer

六鑰臨界分析器：整合六個關鍵指標的主要分析類

This module provides the main analyzer class that integrates all six key indicators
for comprehensive neural criticality analysis.
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Optional, Union, Tuple, Any
import warnings
from dataclasses import dataclass

# Import core indicators
from ..core import FELC, TEB, RFI, ECGP, PWC, ACI


@dataclass
class CriticalityResults:
    """
    Data class for storing criticality analysis results.
    
    Attributes
    ----------
    zeta_values : dict
        Dictionary of ζ₁-ζ₆ indicator values
    d_total : float
        Total pipeline distance
    theta_c : float
        Critical threshold
    consciousness_state : str
        Predicted consciousness state
    individual_results : dict
        Detailed results from each indicator
    metadata : dict
        Analysis metadata and parameters
    """
    zeta_values: Dict[str, float]
    d_total: float
    theta_c: float
    consciousness_state: str
    individual_results: Dict[str, Dict]
    metadata: Dict[str, Any]


class SixKeysAnalyzer:
    """
    Main analyzer for Six Keys Criticality framework.
    
    This class integrates all six key indicators (ζ₁-ζ₆) to provide comprehensive
    analysis of neural criticality and consciousness states.
    
    Parameters
    ----------
    theta_c : float, default=1.0
        Critical threshold for consciousness detection
    weights : dict, optional
        Weights for each indicator in total distance calculation
    enable_indicators : list, optional
        List of indicators to enable (default: all available)
    random_state : int, optional
        Random seed for reproducible results
    """
    
    def __init__(self,
                 theta_c: float = 1.0,
                 weights: Optional[Dict[str, float]] = None,
                 enable_indicators: Optional[List[str]] = None,
                 random_state: Optional[int] = None):
        
        self.theta_c = theta_c
        self.random_state = random_state
        
        if random_state is not None:
            np.random.seed(random_state)
        
        # Default weights for each indicator
        self.default_weights = {
            'zeta1': 0.25,  # FELC
            'zeta2': 0.15,  # TEB
            'zeta3': 0.20,  # RFI
            'zeta4': 0.15,  # ECGP
            'zeta5': 0.15,  # PWC
            'zeta6': 0.10,  # ACI
        }
        
        self.weights = weights if weights is not None else self.default_weights.copy()
        
        # Available indicators (all six are now implemented)
        self.available_indicators = ['FELC', 'TEB', 'RFI', 'ECGP', 'PWC', 'ACI']
        
        if enable_indicators is None:
            self.enable_indicators = set(self.available_indicators)
        else:
            # Validate enabled indicators
            invalid = set(enable_indicators) - set(self.available_indicators)
            if invalid:
                warnings.warn(f"Unknown indicators: {invalid}. "
                             f"Available: {self.available_indicators}")
            self.enable_indicators = set(ind for ind in enable_indicators 
                                       if ind in self.available_indicators)
        
        # Initialize indicator instances
        self._init_indicators()
    
    def _init_indicators(self):
        """
        Initialize indicator instances.
        """
        self.indicators = {}
        
        if 'FELC' in self.enable_indicators:
            self.indicators['FELC'] = FELC()
        
        if 'TEB' in self.enable_indicators:
            self.indicators['TEB'] = TEB()
        
        if 'RFI' in self.enable_indicators:
            self.indicators['RFI'] = RFI()
        
        if 'ECGP' in self.enable_indicators:
            self.indicators['ECGP'] = ECGP()
        
        if 'PWC' in self.enable_indicators:
            self.indicators['PWC'] = PWC()
        
        if 'ACI' in self.enable_indicators:
            self.indicators['ACI'] = ACI()
    
    def analyze_data(self, data: np.ndarray, 
                    states: Optional[Dict[str, Dict]] = None) -> CriticalityResults:
        """
        Analyze neural data using enabled indicators.
        
        Parameters
        ----------
        data : ndarray, shape (n_timepoints, n_channels)
            Neural time series data
        states : dict, optional
            Custom state parameters for simulation-based analysis
            
        Returns
        -------
        results : CriticalityResults
            Comprehensive analysis results
        """
        # For now, we'll use simulation-based analysis
        # In the future, this will process real neural data
        return self.analyze_simulated_states(states)
    
    def analyze_simulated_data(self, 
                              consciousness_state: str = 'awake',
                              duration: float = 60.0,
                              dt: float = 0.01) -> CriticalityResults:
        """
        Analyze simulated neural data for different consciousness states.
        
        Parameters
        ----------
        consciousness_state : str, default='awake'
            Target consciousness state ('awake', 'light_sedation', 'deep_anesthesia')
        duration : float, default=60.0
            Simulation duration in seconds
        dt : float, default=0.01
            Time step for simulation
            
        Returns
        -------
        CriticalityResults
            Complete analysis results
        """
        # Input validation
        if duration <= 0:
            raise ValueError("Duration must be positive")
        if dt <= 0:
            raise ValueError("dt must be positive")
        if duration <= dt:
            raise ValueError("Duration must be greater than dt")
        
        # Define state-specific parameters for simulation
        state_params = {
            'awake': {
                'FELC': {'target_energy': 0.0, 'noise_level': 0.05},
                'TEB': {'target_efficiency': 0.75, 'noise_level': 0.03},
                'RFI': {'kappa_target': 0.0},
                'ECGP': {'p_target': 0.6},
                'PWC': {'gamma_target': 0.0},
                'ACI': {'a_target': 0.5},
            },
            'light_sedation': {
                'FELC': {'target_energy': -0.8, 'noise_level': 0.04},
                'TEB': {'target_efficiency': 0.45, 'noise_level': 0.025},
                'RFI': {'kappa_target': -0.05},
                'ECGP': {'p_target': 0.3},
                'PWC': {'gamma_target': -0.8},
                'ACI': {'a_target': 0.2},
            },
            'deep_anesthesia': {
                'FELC': {'target_energy': -2.5, 'noise_level': 0.02},
                'TEB': {'target_efficiency': 0.15, 'noise_level': 0.015},
                'RFI': {'kappa_target': 0.08},
                'ECGP': {'p_target': 0.9},
                'PWC': {'gamma_target': 0.9},
                'ACI': {'a_target': 0.85},
            }
        }
        
        if consciousness_state not in state_params:
            raise ValueError(f"Unknown consciousness state: {consciousness_state}")
        
        params = state_params[consciousness_state]
        
        # Generate time points
        time_points = np.arange(0, duration, dt)
        
        # Analyze with each indicator
        zeta_values = {}
        individual_results = {}
        
        # Set random seed for reproducibility
        np.random.seed(42 + hash(consciousness_state) % 1000)
        
        # FELC analysis
        if 'FELC' in self.enable_indicators:
            felc_result = self.indicators['FELC'].analyze(
                target_energy=params['FELC']['target_energy'],
                noise_level=params['FELC']['noise_level'],
                sim_time=duration,
                dt=dt
            )
            zeta_values['FELC'] = felc_result.zeta_1
            individual_results['FELC'] = felc_result
        
        # TEB analysis
        if 'TEB' in self.enable_indicators:
            teb_result = self.indicators['TEB'].analyze(
                target_efficiency=params['TEB']['target_efficiency'],
                noise_level=params['TEB']['noise_level'],
                sim_time=duration,
                dt=dt
            )
            zeta_values['TEB'] = teb_result.zeta_2
            individual_results['TEB'] = teb_result
        
        # RFI analysis
        if 'RFI' in self.enable_indicators:
            rfi_result = self.indicators['RFI'].analyze(
                kappa_target=params['RFI']['kappa_target'],
                sim_time=duration,
                dt=0.05  # RFI uses different dt
            )
            zeta_values['RFI'] = rfi_result.zeta_3
            individual_results['RFI'] = rfi_result
        
        # ECGP analysis
        if 'ECGP' in self.enable_indicators:
            ecgp_result = self.indicators['ECGP'].analyze(
                p_target=params['ECGP']['p_target'],
                sim_time=duration,
                dt=0.1  # ECGP uses different dt
            )
            zeta_values['ECGP'] = ecgp_result.zeta_4
            individual_results['ECGP'] = ecgp_result
        
        # PWC analysis
        if 'PWC' in self.enable_indicators:
            pwc_result = self.indicators['PWC'].analyze(
                gamma_target=params['PWC']['gamma_target'],
                sim_time=duration,
                dt=0.08  # PWC uses different dt
            )
            zeta_values['PWC'] = pwc_result.zeta_5
            individual_results['PWC'] = pwc_result
        
        # ACI analysis
        if 'ACI' in self.enable_indicators:
            aci_result = self.indicators['ACI'].analyze(
                a_target=params['ACI']['a_target'],
                sim_time=duration,
                dt=0.12  # ACI uses different dt
            )
            zeta_values['ACI'] = aci_result.zeta_6
            individual_results['ACI'] = aci_result
        
        # Calculate total distance
        d_total = self.compute_total_distance(zeta_values)
        
        # Classify consciousness state
        predicted_state = self.classify_consciousness_state(d_total)
        
        # Create results object
        results = CriticalityResults(
            zeta_values=zeta_values,
            d_total=d_total,
            theta_c=self.theta_c,
            consciousness_state=predicted_state,
            individual_results=individual_results,
            metadata={
                'analysis_type': 'simulated',
                'target_state': consciousness_state,
                'duration': duration,
                'dt': dt,
                'enabled_indicators': list(self.enable_indicators),
                'weights': self.weights.copy()
            }
        )
        
        self.last_results = results
        return results
    
    def compute_total_distance(self, zeta_values: Dict[str, float]) -> float:
        """
        Compute total pipeline distance from zeta values.
        
        Parameters
        ----------
        zeta_values : dict
            Dictionary of zeta values from indicators
            
        Returns
        -------
        d_total : float
            Total pipeline distance
        """
        total = 0.0
        weight_mapping = {
            'FELC': 'zeta1',
            'TEB': 'zeta2',
            'RFI': 'zeta3',
            'ECGP': 'zeta4',
            'PWC': 'zeta5',
            'ACI': 'zeta6'
        }
        
        for indicator, zeta_value in zeta_values.items():
            weight_key = weight_mapping.get(indicator, indicator.lower())
            weight = self.weights.get(weight_key, 0.0)
            total += weight * zeta_value**2
        
        return np.sqrt(total)
    
    def classify_consciousness_state(self, d_total: float) -> str:
        """
        Classify consciousness state based on total distance.
        
        Parameters
        ----------
        d_total : float
            Total pipeline distance
            
        Returns
        -------
        state : str
            Consciousness state classification
        """
        if d_total < self.theta_c:
            return "Conscious"
        else:
            return "Non-conscious"
    
    def analyze_simulated_states(self, 
                               states: Optional[Dict[str, Dict]] = None) -> Dict[str, CriticalityResults]:
        """
        Analyze simulated consciousness states.
        
        Parameters
        ----------
        states : dict, optional
            Custom state parameters
            
        Returns
        -------
        results : dict
            Results for each simulated state
        """
        all_results = {}
        individual_results = {}
        
        # Analyze each enabled indicator
        for indicator_name, indicator in self.indicators.items():
            individual_results[indicator_name] = indicator.analyze_states(states)
        
        # Get state names from first indicator
        if individual_results:
            first_indicator = list(individual_results.keys())[0]
            state_names = list(individual_results[first_indicator].keys())
        else:
            raise ValueError("No indicators enabled")
        
        # Combine results for each state
        for state_name in state_names:
            zeta_values = {}
            d_components = {}
            
            # Extract ζ values and D_w components
            for indicator_name, results in individual_results.items():
                state_result = results[state_name]
                
                if indicator_name == 'FELC':
                    zeta_values['zeta1'] = state_result['zeta1']
                    d_components['zeta1'] = state_result['zeta1']
                elif indicator_name == 'TEB':
                    zeta_values['zeta2'] = state_result['zeta2']
                    d_components['zeta2'] = state_result['zeta2']
                # Add other indicators as they become available
            
            # Calculate total pipeline distance
            d_total = self._calculate_total_distance(d_components)
            
            # Determine consciousness state
            consciousness_state = self._classify_consciousness_state(d_total)
            
            # Create results object
            all_results[state_name] = CriticalityResults(
                zeta_values=zeta_values,
                d_total=d_total,
                theta_c=self.theta_c,
                consciousness_state=consciousness_state,
                individual_results={ind: individual_results[ind][state_name] 
                                  for ind in individual_results},
                metadata={
                    'enabled_indicators': self.enable_indicators,
                    'weights': self.weights,
                    'random_state': self.random_state
                }
            )
        
        return all_results
    
    def _calculate_total_distance(self, d_components: Dict[str, float]) -> float:
        """
        Calculate total pipeline distance from individual components.
        
        Parameters
        ----------
        d_components : dict
            Dictionary of ζ values for each indicator
            
        Returns
        -------
        d_total : float
            Total pipeline distance
        """
        total = 0.0
        for zeta_name, zeta_value in d_components.items():
            weight = self.weights.get(zeta_name, 0.0)
            total += weight * zeta_value**2
        
        return np.sqrt(total)
    
    def _classify_consciousness_state(self, d_total: float) -> str:
        """
        Classify consciousness state based on total distance.
        
        Parameters
        ----------
        d_total : float
            Total pipeline distance
            
        Returns
        -------
        state : str
            Consciousness state classification
        """
        if d_total < self.theta_c:
            return "Conscious"
        else:
            return "Non-conscious"
    
    def plot_radar_chart(self, results: Dict[str, CriticalityResults],
                        figsize: Tuple[int, int] = (8, 8)) -> plt.Figure:
        """
        Plot radar chart of ζ indicators for all states.
        
        Parameters
        ----------
        results : dict
            Results from analyze_simulated_states()
        figsize : tuple, default=(8, 8)
            Figure size
            
        Returns
        -------
        fig : matplotlib.figure.Figure
            Figure object
        """
        # Get all unique ζ indicators
        all_zetas = set()
        for result in results.values():
            all_zetas.update(result.zeta_values.keys())
        
        zeta_names = sorted(list(all_zetas))
        n_indicators = len(zeta_names)
        
        if n_indicators == 0:
            raise ValueError("No ζ indicators found in results")
        
        # Create radar chart
        fig, ax = plt.subplots(figsize=figsize, subplot_kw=dict(projection='polar'))
        
        # Angles for each indicator
        angles = np.linspace(0, 2 * np.pi, n_indicators, endpoint=False).tolist()
        angles += angles[:1]  # Complete the circle
        
        # Plot each state
        colors = ['tab:green', 'tab:orange', 'tab:red', 'tab:blue', 'tab:purple']
        
        for i, (state_name, result) in enumerate(results.items()):
            values = []
            for zeta_name in zeta_names:
                values.append(result.zeta_values.get(zeta_name, 0.0))
            values += values[:1]  # Complete the circle
            
            color = colors[i % len(colors)]
            ax.plot(angles, values, 'o-', linewidth=2, label=state_name, color=color)
            ax.fill(angles, values, alpha=0.25, color=color)
        
        # Customize chart
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels([f'ζ{i+1}' for i in range(n_indicators)])
        ax.set_ylim(-2, 2)
        ax.set_title('Six Keys Criticality Radar Chart', size=16, pad=20)
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
        ax.grid(True)
        
        plt.tight_layout()
        return fig
    
    def plot_phase_diagram(self, results: Dict[str, CriticalityResults],
                          figsize: Tuple[int, int] = (10, 6)) -> plt.Figure:
        """
        Plot phase diagram showing D_total vs θ_c.
        
        Parameters
        ----------
        results : dict
            Results from analyze_simulated_states()
        figsize : tuple, default=(10, 6)
            Figure size
            
        Returns
        -------
        fig : matplotlib.figure.Figure
            Figure object
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
        
        # Extract data
        state_names = list(results.keys())
        d_totals = [results[state].d_total for state in state_names]
        consciousness_states = [results[state].consciousness_state for state in state_names]
        
        # Color mapping
        color_map = {'Conscious': 'green', 'Non-conscious': 'red'}
        colors = [color_map[state] for state in consciousness_states]
        
        # Plot 1: D_total comparison
        bars = ax1.bar(state_names, d_totals, color=colors, alpha=0.7)
        ax1.axhline(self.theta_c, color='black', linestyle='--', 
                   label=f'θc = {self.theta_c}')
        ax1.set_ylabel('D_total')
        ax1.set_title('Total Pipeline Distance')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Add value labels
        for bar, value in zip(bars, d_totals):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                    f'{value:.3f}', ha='center', va='bottom')
        
        # Plot 2: Phase space (if we have multiple indicators)
        if len(results) > 0 and len(list(results.values())[0].zeta_values) >= 2:
            zeta_names = list(list(results.values())[0].zeta_values.keys())
            if len(zeta_names) >= 2:
                x_vals = [results[state].zeta_values[zeta_names[0]] for state in state_names]
                y_vals = [results[state].zeta_values[zeta_names[1]] for state in state_names]
                
                scatter = ax2.scatter(x_vals, y_vals, c=colors, s=100, alpha=0.7)
                
                # Add state labels
                for i, state in enumerate(state_names):
                    ax2.annotate(state, (x_vals[i], y_vals[i]), 
                               xytext=(5, 5), textcoords='offset points')
                
                ax2.set_xlabel(f'{zeta_names[0]}')
                ax2.set_ylabel(f'{zeta_names[1]}')
                ax2.set_title('Phase Space')
                ax2.grid(True, alpha=0.3)
                ax2.axhline(0, color='black', linewidth=0.5)
                ax2.axvline(0, color='black', linewidth=0.5)
        else:
            ax2.text(0.5, 0.5, 'Phase space requires\n≥2 indicators', 
                    ha='center', va='center', transform=ax2.transAxes)
            ax2.set_title('Phase Space (Not Available)')
        
        plt.tight_layout()
        return fig
    
    def print_summary(self, results: Dict[str, CriticalityResults]) -> None:
        """
        Print comprehensive analysis summary.
        
        Parameters
        ----------
        results : dict
            Results from analyze_simulated_states()
        """
        print("=" * 80)
        print("🔑 Six Keys Criticality Analysis Summary")
        print("=" * 80)
        
        # Header
        zeta_names = []
        if results:
            zeta_names = list(list(results.values())[0].zeta_values.keys())
        
        header = f"{'State':<15} | {'D_total':<8} | {'Class':<12}"
        for zeta in zeta_names:
            header += f" | {zeta:<8}"
        print(header)
        print("-" * len(header))
        
        # Results for each state
        for state_name, result in results.items():
            consciousness_icon = "✅" if result.consciousness_state == "Conscious" else "❌"
            
            row = f"{state_name:<15} | {result.d_total:<8.3f} | "
            row += f"{consciousness_icon} {result.consciousness_state:<10}"
            
            for zeta in zeta_names:
                value = result.zeta_values.get(zeta, 0.0)
                row += f" | {value:<8.3f}"
            
            print(row)
        
        print("\n🎯 Analysis Parameters:")
        print(f"   Critical threshold (θc): {self.theta_c}")
        print(f"   Enabled indicators: {', '.join(self.enable_indicators)}")
        print(f"   Weights: {self.weights}")
        
        print("\n📊 Theory Validation:")
        print("   • D_total < θc → Conscious state")
        print("   • D_total ≥ θc → Non-conscious state")
        print("   • Consistent with 六鑰臨界 framework")


def demo():
    """
    Run Six Keys Analyzer demonstration.
    """
    # Set random seed for reproducibility
    np.random.seed(42)
    
    # Create analyzer
    analyzer = SixKeysAnalyzer(random_state=42)
    
    # Analyze simulated states
    results = analyzer.analyze_simulated_states()
    
    # Plot results
    radar_fig = analyzer.plot_radar_chart(results)
    phase_fig = analyzer.plot_phase_diagram(results)
    
    # Print summary
    analyzer.print_summary(results)
    
    return analyzer, results, radar_fig, phase_fig


if __name__ == "__main__":
    analyzer, results, radar_fig, phase_fig = demo()
    plt.show()