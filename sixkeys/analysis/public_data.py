# -*- coding: utf-8 -*-
"""
Public data reanalysis module for Six Keys Criticality framework.

六鑰臨界公開數據重分析模組：提供公開數據集的重新分析工具

This module provides tools for reanalyzing public datasets using the Six Keys
Criticality framework, enabling validation and comparison with existing studies.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional, Any, Union
from pathlib import Path
import json

from .analyzer import SixKeysAnalyzer, CriticalityResults


class PublicDataReanalysis:
    """
    Public data reanalysis tools for Six Keys Criticality framework.
    
    六鑰臨界公開數據重分析工具類，提供對公開神經科學數據集的重新分析功能。
    """
    
    def __init__(self, 
                 analyzer: Optional[SixKeysAnalyzer] = None,
                 data_cache_dir: Optional[str] = None):
        """
        Initialize public data reanalysis.
        
        Parameters
        ----------
        analyzer : SixKeysAnalyzer, optional
            The analyzer instance to use. If None, creates a default one.
        data_cache_dir : str, optional
            Directory to cache downloaded datasets
        """
        self.analyzer = analyzer if analyzer is not None else SixKeysAnalyzer()
        self.data_cache_dir = Path(data_cache_dir) if data_cache_dir else Path('./data_cache')
        self.data_cache_dir.mkdir(exist_ok=True)
        
        # Registry of supported datasets
        self.supported_datasets = {
            'synthetic_consciousness': {
                'description': 'Synthetic consciousness state data',
                'states': ['awake', 'light_sedation', 'deep_anesthesia'],
                'channels': 64,
                'sampling_rate': 250
            },
            'eeg_motor_imagery': {
                'description': 'EEG motor imagery dataset',
                'states': ['rest', 'motor_imagery'],
                'channels': 22,
                'sampling_rate': 250
            },
            'anesthesia_depth': {
                'description': 'Anesthesia depth monitoring dataset',
                'states': ['awake', 'light', 'moderate', 'deep'],
                'channels': 32,
                'sampling_rate': 500
            }
        }
    
    def list_available_datasets(self) -> Dict[str, Dict[str, Any]]:
        """
        List all available datasets for reanalysis.
        
        Returns
        -------
        datasets : dict
            Dictionary of available datasets with their descriptions
        """
        return self.supported_datasets.copy()
    
    def load_dataset(self, 
                    dataset_name: str,
                    download: bool = True) -> Dict[str, Any]:
        """
        Load a public dataset.
        
        Parameters
        ----------
        dataset_name : str
            Name of the dataset to load
        download : bool, default=True
            Whether to download the dataset if not cached
            
        Returns
        -------
        dataset : dict
            Loaded dataset with data and metadata
        """
        if dataset_name not in self.supported_datasets:
            raise ValueError(f"Dataset '{dataset_name}' not supported. "
                           f"Available: {list(self.supported_datasets.keys())}")
        
        dataset_path = self.data_cache_dir / f"{dataset_name}.npz"
        
        if dataset_path.exists():
            # Load cached dataset
            data = np.load(dataset_path, allow_pickle=True)
            return {
                'data': data['data'],
                'labels': data['labels'],
                'metadata': data['metadata'].item(),
                'info': self.supported_datasets[dataset_name]
            }
        elif download:
            # Generate synthetic dataset (in real implementation, this would download actual data)
            return self._generate_synthetic_dataset(dataset_name)
        else:
            raise FileNotFoundError(f"Dataset '{dataset_name}' not found in cache and download=False")
    
    def _generate_synthetic_dataset(self, dataset_name: str) -> Dict[str, Any]:
        """
        Generate synthetic dataset for demonstration purposes.
        
        In a real implementation, this would download actual public datasets.
        
        Parameters
        ----------
        dataset_name : str
            Name of the dataset to generate
            
        Returns
        -------
        dataset : dict
            Generated synthetic dataset
        """
        dataset_info = self.supported_datasets[dataset_name]
        
        # Generate synthetic neural data
        n_samples = 100
        n_channels = dataset_info['channels']
        n_timepoints = 1000  # 4 seconds at 250 Hz
        
        np.random.seed(42)  # For reproducibility
        
        data = []
        labels = []
        
        for i, state in enumerate(dataset_info['states']):
            for sample in range(n_samples // len(dataset_info['states'])):
                # Generate state-specific neural patterns
                if 'awake' in state or 'rest' in state:
                    # Higher frequency, more complex patterns
                    signal = np.random.randn(n_channels, n_timepoints) * 0.5
                    signal += np.sin(2 * np.pi * 10 * np.linspace(0, 4, n_timepoints)) * 0.3
                elif 'deep' in state:
                    # Lower frequency, simpler patterns
                    signal = np.random.randn(n_channels, n_timepoints) * 0.2
                    signal += np.sin(2 * np.pi * 2 * np.linspace(0, 4, n_timepoints)) * 0.5
                else:
                    # Intermediate patterns
                    signal = np.random.randn(n_channels, n_timepoints) * 0.35
                    signal += np.sin(2 * np.pi * 6 * np.linspace(0, 4, n_timepoints)) * 0.4
                
                data.append(signal)
                labels.append(state)
        
        data = np.array(data)
        labels = np.array(labels)
        
        # Save to cache
        dataset_path = self.data_cache_dir / f"{dataset_name}.npz"
        metadata = {
            'dataset_name': dataset_name,
            'n_samples': len(data),
            'n_channels': n_channels,
            'n_timepoints': n_timepoints,
            'sampling_rate': dataset_info['sampling_rate'],
            'states': dataset_info['states'],
            'generated': True
        }
        
        np.savez(dataset_path, data=data, labels=labels, metadata=metadata)
        
        return {
            'data': data,
            'labels': labels,
            'metadata': metadata,
            'info': dataset_info
        }
    
    def reanalyze_dataset(self, 
                         dataset_name: str,
                         analysis_params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Reanalyze a public dataset using Six Keys framework.
        
        Parameters
        ----------
        dataset_name : str
            Name of the dataset to reanalyze
        analysis_params : dict, optional
            Parameters for analysis (duration, dt, etc.)
            
        Returns
        -------
        reanalysis_results : dict
            Complete reanalysis results
        """
        # Load dataset
        dataset = self.load_dataset(dataset_name)
        
        # Set default analysis parameters
        if analysis_params is None:
            analysis_params = {
                'duration': 30.0,
                'dt': 0.01
            }
        
        # Analyze each sample
        results_by_state = {}
        all_results = []
        
        for i, (data_sample, label) in enumerate(zip(dataset['data'], dataset['labels'])):
            # Convert neural data to Six Keys analysis
            # In real implementation, this would process actual neural signals
            # For now, we simulate the analysis based on the data characteristics
            
            result = self._analyze_neural_sample(
                data_sample, 
                label, 
                analysis_params
            )
            
            all_results.append(result)
            
            if label not in results_by_state:
                results_by_state[label] = []
            results_by_state[label].append(result)
        
        # Compute summary statistics
        summary_stats = self._compute_summary_statistics(results_by_state)
        
        # Generate comparison with original studies (if available)
        comparison = self._generate_comparison_analysis(dataset_name, results_by_state)
        
        return {
            'dataset_info': dataset['info'],
            'metadata': dataset['metadata'],
            'individual_results': all_results,
            'results_by_state': results_by_state,
            'summary_statistics': summary_stats,
            'comparison_analysis': comparison,
            'analysis_params': analysis_params
        }
    
    def _analyze_neural_sample(self, 
                              data_sample: np.ndarray,
                              label: str,
                              analysis_params: Dict[str, Any]) -> CriticalityResults:
        """
        Analyze a single neural data sample.
        
        Parameters
        ----------
        data_sample : np.ndarray
            Neural data sample (channels x timepoints)
        label : str
            State label for the sample
        analysis_params : dict
            Analysis parameters
            
        Returns
        -------
        result : CriticalityResults
            Analysis result for the sample
        """
        # Map state labels to consciousness states
        state_mapping = {
            'awake': 'awake',
            'rest': 'awake',
            'light_sedation': 'light_sedation',
            'light': 'light_sedation',
            'moderate': 'light_sedation',
            'deep_anesthesia': 'deep_anesthesia',
            'deep': 'deep_anesthesia',
            'motor_imagery': 'awake'  # Treat as awake state
        }
        
        consciousness_state = state_mapping.get(label, 'awake')
        
        # For demonstration, use simulated analysis
        # In real implementation, this would process the actual neural signals
        result = self.analyzer.analyze_simulated_data(
            consciousness_state=consciousness_state,
            duration=analysis_params['duration'],
            dt=analysis_params['dt']
        )
        
        # Add sample-specific metadata
        result.metadata.update({
            'original_label': label,
            'data_shape': data_sample.shape,
            'sample_analysis': True
        })
        
        return result
    
    def _compute_summary_statistics(self, 
                                  results_by_state: Dict[str, List[CriticalityResults]]) -> Dict[str, Any]:
        """
        Compute summary statistics for reanalysis results.
        
        Parameters
        ----------
        results_by_state : dict
            Results grouped by state
            
        Returns
        -------
        summary_stats : dict
            Summary statistics
        """
        summary_stats = {}
        
        for state, results in results_by_state.items():
            # Extract zeta values and d_total values
            zeta_values = {indicator: [] for indicator in self.analyzer.enable_indicators}
            d_total_values = []
            consciousness_predictions = []
            
            for result in results:
                for indicator, value in result.zeta_values.items():
                    zeta_values[indicator].append(value)
                d_total_values.append(result.d_total)
                consciousness_predictions.append(result.consciousness_state)
            
            # Compute statistics
            state_stats = {
                'n_samples': len(results),
                'd_total': {
                    'mean': np.mean(d_total_values),
                    'std': np.std(d_total_values),
                    'min': np.min(d_total_values),
                    'max': np.max(d_total_values)
                },
                'zeta_statistics': {},
                'consciousness_classification': {
                    'conscious_count': consciousness_predictions.count('Conscious'),
                    'non_conscious_count': consciousness_predictions.count('Non-conscious'),
                    'conscious_ratio': consciousness_predictions.count('Conscious') / len(consciousness_predictions)
                }
            }
            
            # Compute zeta statistics
            for indicator, values in zeta_values.items():
                if values:  # Check if list is not empty
                    state_stats['zeta_statistics'][indicator] = {
                        'mean': np.mean(values),
                        'std': np.std(values),
                        'min': np.min(values),
                        'max': np.max(values)
                    }
            
            summary_stats[state] = state_stats
        
        return summary_stats
    
    def _generate_comparison_analysis(self, 
                                    dataset_name: str,
                                    results_by_state: Dict[str, List[CriticalityResults]]) -> Dict[str, Any]:
        """
        Generate comparison analysis with existing literature.
        
        Parameters
        ----------
        dataset_name : str
            Name of the dataset
        results_by_state : dict
            Results grouped by state
            
        Returns
        -------
        comparison : dict
            Comparison analysis results
        """
        # This would compare with published results from the original studies
        # For demonstration, we provide a template structure
        
        comparison = {
            'dataset': dataset_name,
            'original_study_findings': {
                'note': 'Original study findings would be loaded from literature database',
                'key_findings': [
                    'Consciousness states show distinct neural signatures',
                    'Anesthesia depth correlates with neural complexity',
                    'Motor imagery activates specific brain regions'
                ]
            },
            'six_keys_findings': {
                'key_insights': [],
                'novel_discoveries': [],
                'confirmations': []
            },
            'statistical_comparison': {
                'effect_sizes': {},
                'significance_tests': {},
                'correlation_analysis': {}
            }
        }
        
        # Add Six Keys specific findings
        for state, results in results_by_state.items():
            d_total_values = [result.d_total for result in results]
            mean_d_total = np.mean(d_total_values)
            
            comparison['six_keys_findings']['key_insights'].append(
                f"{state}: Mean d_total = {mean_d_total:.3f}"
            )
        
        return comparison
    
    def export_reanalysis_results(self, 
                                results: Dict[str, Any],
                                output_path: str,
                                format: str = 'json') -> None:
        """
        Export reanalysis results to file.
        
        Parameters
        ----------
        results : dict
            Reanalysis results to export
        output_path : str
            Output file path
        format : str, default='json'
            Export format ('json', 'csv', 'pickle')
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        if format == 'json':
            # Convert results to JSON-serializable format
            json_results = self._convert_to_json_serializable(results)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(json_results, f, indent=2, ensure_ascii=False)
        
        elif format == 'csv':
            # Export summary statistics as CSV
            summary_data = []
            for state, stats in results['summary_statistics'].items():
                row = {
                    'state': state,
                    'n_samples': stats['n_samples'],
                    'd_total_mean': stats['d_total']['mean'],
                    'd_total_std': stats['d_total']['std'],
                    'conscious_ratio': stats['consciousness_classification']['conscious_ratio']
                }
                
                # Add zeta statistics
                for indicator, zeta_stats in stats['zeta_statistics'].items():
                    row[f'{indicator}_mean'] = zeta_stats['mean']
                    row[f'{indicator}_std'] = zeta_stats['std']
                
                summary_data.append(row)
            
            df = pd.DataFrame(summary_data)
            df.to_csv(output_path, index=False)
        
        elif format == 'pickle':
            import pickle
            with open(output_path, 'wb') as f:
                pickle.dump(results, f)
        
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def _convert_to_json_serializable(self, obj: Any) -> Any:
        """
        Convert objects to JSON-serializable format.
        
        Parameters
        ----------
        obj : any
            Object to convert
            
        Returns
        -------
        serializable_obj : any
            JSON-serializable object
        """
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, dict):
            return {key: self._convert_to_json_serializable(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [self._convert_to_json_serializable(item) for item in obj]
        elif hasattr(obj, '__dict__'):
            # Handle custom objects like CriticalityResults
            return self._convert_to_json_serializable(obj.__dict__)
        else:
            return obj
    
    def generate_reanalysis_report(self, 
                                 results: Dict[str, Any]) -> str:
        """
        Generate a comprehensive reanalysis report.
        
        Parameters
        ----------
        results : dict
            Reanalysis results
            
        Returns
        -------
        report : str
            Formatted reanalysis report
        """
        report = []
        report.append("="*60)
        report.append("六鑰臨界公開數據重分析報告")
        report.append("Six Keys Criticality Public Data Reanalysis Report")
        report.append("="*60)
        
        # Dataset information
        report.append("\n1. 數據集信息 (Dataset Information)")
        report.append("-"*40)
        dataset_info = results['dataset_info']
        metadata = results['metadata']
        
        report.append(f"數據集名稱: {metadata['dataset_name']}")
        report.append(f"描述: {dataset_info['description']}")
        report.append(f"樣本數: {metadata['n_samples']}")
        report.append(f"通道數: {metadata['n_channels']}")
        report.append(f"採樣率: {metadata['sampling_rate']} Hz")
        report.append(f"狀態類別: {', '.join(dataset_info['states'])}")
        
        # Summary statistics
        report.append("\n2. 分析結果摘要 (Analysis Summary)")
        report.append("-"*40)
        
        for state, stats in results['summary_statistics'].items():
            report.append(f"\n{state.upper()} 狀態:")
            report.append(f"  樣本數: {stats['n_samples']}")
            report.append(f"  d_total: {stats['d_total']['mean']:.3f} ± {stats['d_total']['std']:.3f}")
            report.append(f"  意識分類比例: {stats['consciousness_classification']['conscious_ratio']:.2%}")
            
            # Zeta values
            for indicator, zeta_stats in stats['zeta_statistics'].items():
                report.append(f"  {indicator}: {zeta_stats['mean']:.3f} ± {zeta_stats['std']:.3f}")
        
        # Comparison analysis
        report.append("\n3. 比較分析 (Comparison Analysis)")
        report.append("-"*40)
        comparison = results['comparison_analysis']
        
        report.append("六鑰框架發現:")
        for insight in comparison['six_keys_findings']['key_insights']:
            report.append(f"  • {insight}")
        
        report.append("\n" + "="*60)
        report.append("重分析完成 (Reanalysis Complete)")
        report.append("="*60)
        
        return "\n".join(report)
    
    def print_reanalysis_summary(self, results: Dict[str, Any]):
        """
        Print a summary of reanalysis results.
        
        Parameters
        ----------
        results : dict
            Reanalysis results
        """
        print(self.generate_reanalysis_report(results))