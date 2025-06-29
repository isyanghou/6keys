"""Public Data Re-analysis Module

This module provides synthetic Dw distribution analysis for demonstrating
consciousness state differences across multiple public datasets. It generates
synthetic data mimicking real public datasets and visualizes the distribution
of Dw values between awake and low consciousness states.

Example:
    >>> from sixkeys.demos import PublicDataAnalysis
    >>> analyzer = PublicDataAnalysis()
    >>> analyzer.generate_and_analyze()
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from typing import Dict, Tuple, Optional, List
try:
    import seaborn as sns
    HAS_SEABORN = True
except ImportError:
    HAS_SEABORN = False


class PublicDataAnalysis:
    """Public Data Re-analysis for Dw Distribution.
    
    This class generates synthetic Dw distribution data mimicking five public
    datasets and analyzes the differences between awake and low consciousness states.
    """
    
    def __init__(self, 
                 datasets: Optional[Dict] = None,
                 n_samples: int = 25,
                 random_seed: int = 2025,
                 theta_c: float = 0.55):
        """Initialize the public data analyzer.
        
        Args:
            datasets: Dictionary of dataset configurations. Uses default if None.
            n_samples: Number of samples per state per dataset.
            random_seed: Random seed for reproducible results.
            theta_c: Critical threshold for Dw.
        """
        self.datasets = datasets or {
            'ds002345 (MEG)': {'mu_awake': 0.40, 'mu_low': 0.60},
            'ds002770 (NeuPix)': {'mu_awake': 0.42, 'mu_low': 0.65},
            'HCP-7T (fMRI+MEG)': {'mu_awake': 0.38, 'mu_low': 0.58},
            'CamCAN-StageII (MEG)': {'mu_awake': 0.43, 'mu_low': 0.63},
            'Zenodo-8965432 (Mouse)': {'mu_awake': 0.41, 'mu_low': 0.62},
        }
        self.n_samples = n_samples
        self.random_seed = random_seed
        self.theta_c = theta_c
        self.sigma = 0.04  # Standard deviation for synthetic data
        
        # Set random seed
        np.random.seed(self.random_seed)
        
        # Data storage
        self.df = None
        self.summary = None
    
    def generate_synthetic_data(self) -> pd.DataFrame:
        """Generate synthetic Dw distribution data.
        
        Returns:
            DataFrame containing synthetic Dw values for all datasets and states
        """
        rows = []
        
        for dataset_name, config in self.datasets.items():
            for state, mu in [('Awake', config['mu_awake']), 
                             ('Low', config['mu_low'])]:
                values = np.random.normal(mu, self.sigma, self.n_samples)
                for value in values:
                    rows.append({
                        'dataset': dataset_name,
                        'state': state,
                        'Dw': value
                    })
        
        self.df = pd.DataFrame(rows)
        return self.df
    
    def calculate_summary_statistics(self) -> pd.DataFrame:
        """Calculate summary statistics for each dataset and state.
        
        Returns:
            DataFrame containing mean and standard deviation for each group
        """
        if self.df is None:
            self.generate_synthetic_data()
        
        self.summary = (self.df.groupby(['dataset', 'state'])['Dw']
                       .agg(['mean', 'std', 'count'])
                       .reset_index())
        return self.summary
    
    def plot_boxplot(self, 
                    figsize: Tuple[int, int] = (10, 4.5),
                    use_seaborn: bool = None) -> plt.Figure:
        """Create boxplot visualization of Dw distributions.
        
        Args:
            figsize: Figure size tuple
            use_seaborn: Whether to use seaborn. Auto-detects if None.
            
        Returns:
            Matplotlib figure object
        """
        if self.df is None:
            self.generate_synthetic_data()
        
        if use_seaborn is None:
            use_seaborn = HAS_SEABORN
        
        fig, ax = plt.subplots(figsize=figsize)
        
        if use_seaborn and HAS_SEABORN:
            sns.set(style='whitegrid', font_scale=1.0)
            ax = sns.boxplot(x='dataset', y='Dw', hue='state',
                           data=self.df, palette=['tab:green', 'tab:red'], ax=ax)
        else:
            # Fallback to matplotlib boxplot
            datasets = list(self.datasets.keys())
            awake_data = []
            low_data = []
            
            for dataset in datasets:
                awake_vals = self.df[(self.df['dataset'] == dataset) & 
                                   (self.df['state'] == 'Awake')]['Dw'].values
                low_vals = self.df[(self.df['dataset'] == dataset) & 
                                 (self.df['state'] == 'Low')]['Dw'].values
                awake_data.append(awake_vals)
                low_data.append(low_vals)
            
            positions_awake = np.arange(len(datasets)) - 0.2
            positions_low = np.arange(len(datasets)) + 0.2
            
            bp1 = ax.boxplot(awake_data, positions=positions_awake, widths=0.3,
                           patch_artist=True, boxprops=dict(facecolor='tab:green', alpha=0.7))
            bp2 = ax.boxplot(low_data, positions=positions_low, widths=0.3,
                           patch_artist=True, boxprops=dict(facecolor='tab:red', alpha=0.7))
            
            ax.set_xticks(range(len(datasets)))
            ax.set_xticklabels(datasets, rotation=18)
            
            # Add legend
            ax.legend([bp1['boxes'][0], bp2['boxes'][0]], ['Awake', 'Low'], 
                     loc='upper right')
        
        # Add critical threshold line
        ax.axhline(self.theta_c, ls='--', lw=1, color='gray',
                  label=f'θ_c = {self.theta_c}')
        
        ax.set_title('Synthetic Dw Distribution (Awake vs Low Consciousness)')
        ax.set_ylabel('D_w')
        ax.set_xlabel('')
        
        if not (use_seaborn and HAS_SEABORN):
            plt.xticks(rotation=18)
        
        plt.tight_layout()
        return fig
    
    def save_data(self, 
                 csv_filename: str = 'summary_Dw_demo.csv',
                 output_dir: str = './') -> str:
        """Save synthetic data to CSV file.
        
        Args:
            csv_filename: Name of the CSV file
            output_dir: Directory to save the file
            
        Returns:
            Full path of the saved file
        """
        if self.df is None:
            self.generate_synthetic_data()
        
        filepath = f"{output_dir.rstrip('/')}/{csv_filename}"
        self.df.to_csv(filepath, index=False)
        return filepath
    
    def print_summary(self) -> None:
        """Print detailed summary of Dw statistics."""
        if self.summary is None:
            self.calculate_summary_statistics()
        
        print('\n===== Dw Summary (mean ± SD) =====')
        for _, row in self.summary.iterrows():
            print(f"{row['dataset']:<28s} {row['state']}: "
                  f"{row['mean']:.3f} ± {row['std']:.3f} (n={row['count']})")
    
    def analyze_significance(self) -> Dict[str, Dict]:
        """Analyze statistical significance between awake and low states.
        
        Returns:
            Dictionary containing statistical test results for each dataset
        """
        if self.df is None:
            self.generate_synthetic_data()
        
        try:
            from scipy import stats
            HAS_SCIPY = True
        except ImportError:
            HAS_SCIPY = False
            print("Warning: scipy not available. Cannot perform statistical tests.")
            return {}
        
        results = {}
        for dataset in self.datasets.keys():
            awake_data = self.df[(self.df['dataset'] == dataset) & 
                               (self.df['state'] == 'Awake')]['Dw'].values
            low_data = self.df[(self.df['dataset'] == dataset) & 
                             (self.df['state'] == 'Low')]['Dw'].values
            
            if HAS_SCIPY:
                t_stat, p_value = stats.ttest_ind(awake_data, low_data)
                effect_size = (np.mean(low_data) - np.mean(awake_data)) / \
                             np.sqrt((np.var(awake_data) + np.var(low_data)) / 2)
                
                results[dataset] = {
                    't_statistic': t_stat,
                    'p_value': p_value,
                    'effect_size': effect_size,
                    'significant': p_value < 0.05
                }
        
        return results
    
    def generate_and_analyze(self, 
                           show_plots: bool = True,
                           save_files: bool = False,
                           output_dir: str = './') -> Tuple[plt.Figure, pd.DataFrame]:
        """Complete workflow for data generation and analysis.
        
        Args:
            show_plots: Whether to display plots
            save_files: Whether to save data and plots
            output_dir: Directory for output files
            
        Returns:
            Tuple of (figure, summary_dataframe)
        """
        # Generate data
        self.generate_synthetic_data()
        
        # Calculate statistics
        self.calculate_summary_statistics()
        
        # Create visualization
        fig = self.plot_boxplot()
        
        # Save files if requested
        if save_files:
            csv_path = self.save_data(output_dir=output_dir)
            fig.savefig(f"{output_dir}/public_data_dw_boxplot.png", 
                       dpi=300, bbox_inches='tight')
            print(f"\nFiles saved: {csv_path} & {output_dir}/public_data_dw_boxplot.png")
        
        # Show plot if requested
        if show_plots:
            plt.show()
        
        # Print summary
        self.print_summary()
        
        # Analyze significance
        sig_results = self.analyze_significance()
        if sig_results:
            print('\n===== Statistical Significance =====')
            for dataset, results in sig_results.items():
                sig_marker = '***' if results['p_value'] < 0.001 else \
                           '**' if results['p_value'] < 0.01 else \
                           '*' if results['p_value'] < 0.05 else 'ns'
                print(f"{dataset:<28s}: p={results['p_value']:.4f} {sig_marker}, "
                      f"d={results['effect_size']:.3f}")
        
        return fig, self.summary
    
    def add_dataset(self, name: str, mu_awake: float, mu_low: float) -> None:
        """Add a new dataset configuration.
        
        Args:
            name: Dataset name
            mu_awake: Mean Dw value for awake state
            mu_low: Mean Dw value for low consciousness state
        """
        self.datasets[name] = {'mu_awake': mu_awake, 'mu_low': mu_low}
        # Clear previous data to force regeneration
        self.df = None
        self.summary = None


# Convenience function for quick usage
def quick_demo(show_plots: bool = True) -> None:
    """Quick demonstration of public data analysis.
    
    Args:
        show_plots: Whether to display the plots
    """
    analyzer = PublicDataAnalysis()
    analyzer.generate_and_analyze(show_plots=show_plots)


if __name__ == "__main__":
    # Run demo when script is executed directly
    quick_demo()