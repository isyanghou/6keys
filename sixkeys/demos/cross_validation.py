"""Cross-Validation Analysis Module

This module provides cross-validation analysis with correlation matrices for
the six key indicators under different consciousness states. It generates
synthetic time-series data and computes correlation matrices to demonstrate
the relationships between indicators in awake vs unaware conditions.

Example:
    >>> from sixkeys.demos import CrossValidationAnalysis
    >>> cv = CrossValidationAnalysis()
    >>> cv.generate_and_analyze()
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from typing import Dict, Tuple, Optional, List, Union
try:
    import seaborn as sns
    HAS_SEABORN = True
except ImportError:
    HAS_SEABORN = False


class CrossValidationAnalysis:
    """Cross-Validation Analysis for Six Key Indicators.
    
    This class generates synthetic time-series data for six key indicators
    and analyzes their correlations under different consciousness states.
    """
    
    def __init__(self, 
                 keys: Optional[List[str]] = None,
                 n_samples: int = 300,
                 random_seed: int = 42,
                 awake_correlation: float = 0.7,
                 unaware_noise_factor: float = 1.1):
        """Initialize the cross-validation analyzer.
        
        Args:
            keys: List of key indicator names. Uses default six keys if None.
            n_samples: Number of time samples to generate.
            random_seed: Random seed for reproducible results.
            awake_correlation: Correlation strength between FELC and RFI in awake state.
            unaware_noise_factor: Noise multiplication factor for unaware state.
        """
        self.keys = keys or ['FELC', 'RFI', 'ECGP', 'PWC', 'TEB', 'ACI']
        self.n_keys = len(self.keys)
        self.n_samples = n_samples
        self.random_seed = random_seed
        self.awake_correlation = awake_correlation
        self.unaware_noise_factor = unaware_noise_factor
        
        # Set random seed
        np.random.seed(self.random_seed)
        
        # Data storage
        self.awake_data = None
        self.unaware_data = None
        self.corr_awake = None
        self.corr_unaware = None
    
    def generate_synthetic_data(self) -> Tuple[np.ndarray, np.ndarray]:
        """Generate synthetic time-series data for both consciousness states.
        
        Returns:
            Tuple of (awake_data, unaware_data) arrays
        """
        # Generate awake data with FELC-RFI correlation
        self.awake_data = np.random.randn(self.n_samples, self.n_keys)
        
        # Create strong positive correlation between FELC (index 0) and RFI (index 1)
        if self.n_keys >= 2:
            self.awake_data[:, 1] = (self.awake_correlation * self.awake_data[:, 0] + 
                                   (1 - self.awake_correlation) * np.random.randn(self.n_samples))
        
        # Generate unaware data: uncorrelated and noisier
        self.unaware_data = self.unaware_noise_factor * np.random.randn(self.n_samples, self.n_keys)
        
        return self.awake_data, self.unaware_data
    
    def compute_correlations(self) -> Tuple[np.ndarray, np.ndarray]:
        """Compute correlation matrices for both states.
        
        Returns:
            Tuple of (awake_correlation_matrix, unaware_correlation_matrix)
        """
        if self.awake_data is None or self.unaware_data is None:
            self.generate_synthetic_data()
        
        self.corr_awake = np.corrcoef(self.awake_data, rowvar=False)
        self.corr_unaware = np.corrcoef(self.unaware_data, rowvar=False)
        
        return self.corr_awake, self.corr_unaware
    
    def plot_correlation_heatmaps(self, 
                                 figsize: Tuple[int, int] = (11, 4.5),
                                 use_seaborn: bool = None) -> plt.Figure:
        """Create side-by-side correlation heatmaps.
        
        Args:
            figsize: Figure size tuple
            use_seaborn: Whether to use seaborn. Auto-detects if None.
            
        Returns:
            Matplotlib figure object
        """
        if self.corr_awake is None or self.corr_unaware is None:
            self.compute_correlations()
        
        if use_seaborn is None:
            use_seaborn = HAS_SEABORN
        
        if use_seaborn and HAS_SEABORN:
            return self._plot_with_seaborn(figsize)
        else:
            return self._plot_with_matplotlib(figsize)
    
    def _plot_with_seaborn(self, figsize: Tuple[int, int]) -> plt.Figure:
        """Create heatmaps using seaborn."""
        sns.set(style='white', font_scale=1.0)
        fig, axes = plt.subplots(1, 2, figsize=figsize,
                               gridspec_kw={'width_ratios': [1, 1], 'wspace': 0.05})
        cbar_ax = fig.add_axes([0.92, 0.25, 0.02, 0.5])
        
        for ax, corr, title in zip(axes,
                                 [self.corr_awake, self.corr_unaware],
                                 ['Awake', 'Unaware']):
            sns.heatmap(corr, vmin=-1, vmax=1, cmap='coolwarm',
                       xticklabels=self.keys, yticklabels=self.keys,
                       square=True, annot=True, fmt='.2f',
                       linewidths=0.5, cbar=ax is axes[0],
                       cbar_ax=None if ax is not axes[0] else cbar_ax,
                       ax=ax)
            ax.set_title(title)
        
        fig.suptitle('Six-Key Correlation Matrices: Awake vs Unaware', fontsize=14)
        plt.tight_layout(rect=[0, 0, 0.9, 0.92])
        
        return fig
    
    def _plot_with_matplotlib(self, figsize: Tuple[int, int]) -> plt.Figure:
        """Create heatmaps using matplotlib only."""
        fig, axes = plt.subplots(1, 2, figsize=figsize)
        
        for ax, corr, title in zip(axes,
                                 [self.corr_awake, self.corr_unaware],
                                 ['Awake', 'Unaware']):
            im = ax.imshow(corr, cmap='coolwarm', vmin=-1, vmax=1, aspect='equal')
            
            # Add text annotations
            for i in range(self.n_keys):
                for j in range(self.n_keys):
                    text = ax.text(j, i, f'{corr[i, j]:.2f}',
                                 ha="center", va="center", color="black")
            
            ax.set_xticks(range(self.n_keys))
            ax.set_yticks(range(self.n_keys))
            ax.set_xticklabels(self.keys)
            ax.set_yticklabels(self.keys)
            ax.set_title(title)
        
        # Add colorbar
        fig.colorbar(im, ax=axes, shrink=0.8)
        fig.suptitle('Six-Key Correlation Matrices: Awake vs Unaware', fontsize=14)
        plt.tight_layout()
        
        return fig
    
    def get_correlation_dataframes(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Get correlation matrices as pandas DataFrames.
        
        Returns:
            Tuple of (awake_df, unaware_df)
        """
        if self.corr_awake is None or self.corr_unaware is None:
            self.compute_correlations()
        
        awake_df = pd.DataFrame(self.corr_awake, 
                               index=self.keys, 
                               columns=self.keys)
        unaware_df = pd.DataFrame(self.corr_unaware, 
                                 index=self.keys, 
                                 columns=self.keys)
        
        return awake_df, unaware_df
    
    def analyze_key_correlations(self, 
                               key_pairs: Optional[List[Tuple[str, str]]] = None) -> Dict:
        """Analyze specific key pair correlations.
        
        Args:
            key_pairs: List of key pairs to analyze. Uses default pairs if None.
            
        Returns:
            Dictionary containing correlation analysis results
        """
        if self.corr_awake is None or self.corr_unaware is None:
            self.compute_correlations()
        
        if key_pairs is None:
            key_pairs = [('FELC', 'RFI'), ('ECGP', 'PWC'), ('TEB', 'ACI')]
        
        results = {}
        
        for key1, key2 in key_pairs:
            if key1 in self.keys and key2 in self.keys:
                idx1 = self.keys.index(key1)
                idx2 = self.keys.index(key2)
                
                awake_corr = self.corr_awake[idx1, idx2]
                unaware_corr = self.corr_unaware[idx1, idx2]
                
                results[f"{key1}-{key2}"] = {
                    'awake': awake_corr,
                    'unaware': unaware_corr,
                    'difference': awake_corr - unaware_corr
                }
        
        return results
    
    def print_summary(self) -> None:
        """Print detailed summary of correlation analysis."""
        if self.corr_awake is None or self.corr_unaware is None:
            self.compute_correlations()
        
        print('\n===== Cross-Validation Summary =====')
        
        # Key pair analysis
        key_analysis = self.analyze_key_correlations()
        
        for pair, results in key_analysis.items():
            print(f'{pair} correlation:')
            print(f'  Awake:   {results["awake"]:+.3f}')
            print(f'  Unaware: {results["unaware"]:+.3f}')
            print(f'  Δ:       {results["difference"]:+.3f}')
            print()
        
        # Overall statistics
        awake_mean_corr = np.mean(np.abs(self.corr_awake[np.triu_indices(self.n_keys, k=1)]))
        unaware_mean_corr = np.mean(np.abs(self.corr_unaware[np.triu_indices(self.n_keys, k=1)]))
        
        print(f'Mean absolute correlation:')
        print(f'  Awake:   {awake_mean_corr:.3f}')
        print(f'  Unaware: {unaware_mean_corr:.3f}')
    
    def save_data(self, 
                 output_dir: str = './',
                 save_raw_data: bool = True,
                 save_correlations: bool = True) -> List[str]:
        """Save generated data and correlation matrices.
        
        Args:
            output_dir: Directory to save files
            save_raw_data: Whether to save raw time-series data
            save_correlations: Whether to save correlation matrices
            
        Returns:
            List of saved file paths
        """
        if self.awake_data is None or self.unaware_data is None:
            self.generate_synthetic_data()
        if self.corr_awake is None or self.corr_unaware is None:
            self.compute_correlations()
        
        saved_files = []
        
        if save_raw_data:
            # Save raw time-series data
            awake_df = pd.DataFrame(self.awake_data, columns=self.keys)
            unaware_df = pd.DataFrame(self.unaware_data, columns=self.keys)
            
            awake_path = f"{output_dir}/awake_timeseries.csv"
            unaware_path = f"{output_dir}/unaware_timeseries.csv"
            
            awake_df.to_csv(awake_path, index=False)
            unaware_df.to_csv(unaware_path, index=False)
            
            saved_files.extend([awake_path, unaware_path])
        
        if save_correlations:
            # Save correlation matrices
            awake_corr_df, unaware_corr_df = self.get_correlation_dataframes()
            
            awake_corr_path = f"{output_dir}/awake_correlations.csv"
            unaware_corr_path = f"{output_dir}/unaware_correlations.csv"
            
            awake_corr_df.to_csv(awake_corr_path)
            unaware_corr_df.to_csv(unaware_corr_path)
            
            saved_files.extend([awake_corr_path, unaware_corr_path])
        
        return saved_files
    
    def generate_and_analyze(self, 
                           show_plots: bool = True,
                           save_files: bool = False,
                           output_dir: str = './') -> Tuple[plt.Figure, Dict]:
        """Complete workflow for cross-validation analysis.
        
        Args:
            show_plots: Whether to display plots
            save_files: Whether to save data and plots
            output_dir: Directory for output files
            
        Returns:
            Tuple of (figure, correlation_analysis_results)
        """
        # Generate data and compute correlations
        self.generate_synthetic_data()
        self.compute_correlations()
        
        # Create visualization
        fig = self.plot_correlation_heatmaps()
        
        # Analyze key correlations
        correlation_results = self.analyze_key_correlations()
        
        # Save files if requested
        if save_files:
            saved_files = self.save_data(output_dir)
            fig.savefig(f"{output_dir}/cross_validation_heatmap.png", 
                       dpi=300, bbox_inches='tight')
            print(f"\nFiles saved: {', '.join(saved_files)} & {output_dir}/cross_validation_heatmap.png")
        
        # Show plot if requested
        if show_plots:
            plt.show()
        
        # Print summary
        self.print_summary()
        
        return fig, correlation_results
    
    def update_parameters(self, 
                         awake_correlation: Optional[float] = None,
                         unaware_noise_factor: Optional[float] = None,
                         n_samples: Optional[int] = None) -> None:
        """Update analysis parameters and clear cached data.
        
        Args:
            awake_correlation: New correlation strength for awake state
            unaware_noise_factor: New noise factor for unaware state
            n_samples: New number of samples
        """
        if awake_correlation is not None:
            self.awake_correlation = awake_correlation
        if unaware_noise_factor is not None:
            self.unaware_noise_factor = unaware_noise_factor
        if n_samples is not None:
            self.n_samples = n_samples
        
        # Clear cached data to force regeneration
        self.awake_data = None
        self.unaware_data = None
        self.corr_awake = None
        self.corr_unaware = None


# Convenience function for quick usage
def quick_demo(show_plots: bool = True) -> None:
    """Quick demonstration of cross-validation analysis.
    
    Args:
        show_plots: Whether to display the plots
    """
    cv = CrossValidationAnalysis()
    cv.generate_and_analyze(show_plots=show_plots)


if __name__ == "__main__":
    # Run demo when script is executed directly
    quick_demo()