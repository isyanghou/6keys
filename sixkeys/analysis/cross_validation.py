# -*- coding: utf-8 -*-
"""
Cross-validation module for Six Keys Criticality framework.

六鑰臨界交叉驗證模組：提供交叉驗證和模型評估工具

This module provides cross-validation tools for validating the Six Keys
Criticality framework across different datasets and conditions.
"""

import numpy as np
from typing import Dict, List, Tuple, Optional, Any
from sklearn.model_selection import KFold, StratifiedKFold
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

from .analyzer import SixKeysAnalyzer, CriticalityResults


class CrossValidation:
    """
    Cross-validation tools for Six Keys Criticality framework.
    
    六鑰臨界交叉驗證工具類，提供多種驗證方法來評估框架的穩定性和準確性。
    """
    
    def __init__(self, 
                 analyzer: Optional[SixKeysAnalyzer] = None,
                 n_splits: int = 5,
                 random_state: int = 42):
        """
        Initialize cross-validation.
        
        Parameters
        ----------
        analyzer : SixKeysAnalyzer, optional
            The analyzer instance to use. If None, creates a default one.
        n_splits : int, default=5
            Number of folds for cross-validation
        random_state : int, default=42
            Random state for reproducibility
        """
        self.analyzer = analyzer if analyzer is not None else SixKeysAnalyzer()
        self.n_splits = n_splits
        self.random_state = random_state
        
        # Initialize cross-validation splitters
        self.kfold = KFold(n_splits=n_splits, shuffle=True, random_state=random_state)
        self.stratified_kfold = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=random_state)
    
    def validate_simulated_states(self, 
                                states: List[str] = None,
                                n_trials: int = 10) -> Dict[str, Any]:
        """
        Cross-validate using simulated data for different consciousness states.
        
        Parameters
        ----------
        states : list of str, optional
            Consciousness states to validate. Default: ['awake', 'light_sedation', 'deep_anesthesia']
        n_trials : int, default=10
            Number of trials per state
            
        Returns
        -------
        validation_results : dict
            Cross-validation results including accuracy, precision, recall, F1-score
        """
        if states is None:
            states = ['awake', 'light_sedation', 'deep_anesthesia']
        
        # Generate simulated data
        all_results = []
        all_labels = []
        
        for state in states:
            for trial in range(n_trials):
                # Add some randomness to each trial
                np.random.seed(self.random_state + trial)
                
                result = self.analyzer.analyze_simulated_data(
                    consciousness_state=state,
                    duration=30.0  # Shorter duration for faster validation
                )
                
                all_results.append(result)
                # Binary classification: conscious vs non-conscious
                all_labels.append(1 if result.consciousness_state == 'Conscious' else 0)
        
        # Perform cross-validation
        cv_scores = self._cross_validate_results(all_results, all_labels)
        
        return {
            'cv_scores': cv_scores,
            'mean_accuracy': np.mean(cv_scores['accuracy']),
            'std_accuracy': np.std(cv_scores['accuracy']),
            'mean_f1': np.mean(cv_scores['f1']),
            'std_f1': np.std(cv_scores['f1']),
            'states_tested': states,
            'n_trials_per_state': n_trials,
            'total_samples': len(all_results)
        }
    
    def _cross_validate_results(self, 
                              results: List[CriticalityResults], 
                              labels: List[int]) -> Dict[str, List[float]]:
        """
        Perform cross-validation on analysis results.
        
        Parameters
        ----------
        results : list of CriticalityResults
            Analysis results to validate
        labels : list of int
            True labels (0: non-conscious, 1: conscious)
            
        Returns
        -------
        cv_scores : dict
            Cross-validation scores for each fold
        """
        # Extract features (d_total values) and convert to array
        X = np.array([result.d_total for result in results]).reshape(-1, 1)
        y = np.array(labels)
        
        cv_scores = {
            'accuracy': [],
            'precision': [],
            'recall': [],
            'f1': []
        }
        
        # Perform k-fold cross-validation
        for train_idx, test_idx in self.kfold.split(X, y):
            X_train, X_test = X[train_idx], X[test_idx]
            y_train, y_test = y[train_idx], y[test_idx]
            
            # Simple threshold-based classifier using d_total
            # Threshold is learned from training data
            threshold = self._learn_threshold(X_train, y_train)
            
            # Make predictions
            y_pred = (X_test.flatten() < threshold).astype(int)
            
            # Calculate metrics
            cv_scores['accuracy'].append(accuracy_score(y_test, y_pred))
            cv_scores['precision'].append(precision_score(y_test, y_pred, zero_division=0))
            cv_scores['recall'].append(recall_score(y_test, y_pred, zero_division=0))
            cv_scores['f1'].append(f1_score(y_test, y_pred, zero_division=0))
        
        return cv_scores
    
    def _learn_threshold(self, X_train: np.ndarray, y_train: np.ndarray) -> float:
        """
        Learn optimal threshold from training data.
        
        Parameters
        ----------
        X_train : np.ndarray
            Training features (d_total values)
        y_train : np.ndarray
            Training labels
            
        Returns
        -------
        threshold : float
            Optimal threshold for classification
        """
        # Simple approach: use mean of conscious and non-conscious samples
        conscious_samples = X_train[y_train == 1]
        non_conscious_samples = X_train[y_train == 0]
        
        if len(conscious_samples) > 0 and len(non_conscious_samples) > 0:
            threshold = (np.mean(conscious_samples) + np.mean(non_conscious_samples)) / 2
        else:
            # Fallback to default threshold
            threshold = self.analyzer.theta_c
        
        return threshold
    
    def validate_indicator_stability(self, 
                                   n_runs: int = 20,
                                   duration: float = 30.0) -> Dict[str, Any]:
        """
        Validate the stability of individual indicators across multiple runs.
        
        Parameters
        ----------
        n_runs : int, default=20
            Number of independent runs
        duration : float, default=30.0
            Simulation duration for each run
            
        Returns
        -------
        stability_results : dict
            Stability metrics for each indicator
        """
        indicator_values = {indicator: [] for indicator in self.analyzer.enable_indicators}
        
        for run in range(n_runs):
            # Use different random seed for each run
            np.random.seed(self.random_state + run)
            
            result = self.analyzer.analyze_simulated_data(
                consciousness_state='awake',
                duration=duration
            )
            
            for indicator, value in result.zeta_values.items():
                indicator_values[indicator].append(value)
        
        # Calculate stability metrics
        stability_metrics = {}
        for indicator, values in indicator_values.items():
            values = np.array(values)
            stability_metrics[indicator] = {
                'mean': np.mean(values),
                'std': np.std(values),
                'cv': np.std(values) / np.abs(np.mean(values)) if np.mean(values) != 0 else np.inf,
                'min': np.min(values),
                'max': np.max(values),
                'range': np.max(values) - np.min(values)
            }
        
        return {
            'stability_metrics': stability_metrics,
            'n_runs': n_runs,
            'duration': duration,
            'overall_stability': np.mean([metrics['cv'] for metrics in stability_metrics.values()])
        }
    
    def validate_parameter_sensitivity(self, 
                                     parameter_ranges: Dict[str, List[float]] = None) -> Dict[str, Any]:
        """
        Validate sensitivity to parameter changes.
        
        Parameters
        ----------
        parameter_ranges : dict, optional
            Parameter ranges to test. Default tests theta_c values.
            
        Returns
        -------
        sensitivity_results : dict
            Sensitivity analysis results
        """
        if parameter_ranges is None:
            parameter_ranges = {
                'theta_c': [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
            }
        
        sensitivity_results = {}
        
        for param_name, param_values in parameter_ranges.items():
            param_results = []
            
            for param_value in param_values:
                # Create analyzer with modified parameter
                if param_name == 'theta_c':
                    test_analyzer = SixKeysAnalyzer(
                        theta_c=param_value,
                        enable_indicators=self.analyzer.enable_indicators,
                        weights=self.analyzer.weights
                    )
                else:
                    # For other parameters, modify accordingly
                    test_analyzer = self.analyzer
                
                # Test with different consciousness states
                state_results = {}
                for state in ['awake', 'light_sedation', 'deep_anesthesia']:
                    result = test_analyzer.analyze_simulated_data(
                        consciousness_state=state,
                        duration=20.0
                    )
                    state_results[state] = {
                        'd_total': result.d_total,
                        'classification': result.consciousness_state
                    }
                
                param_results.append({
                    'parameter_value': param_value,
                    'state_results': state_results
                })
            
            sensitivity_results[param_name] = param_results
        
        return sensitivity_results
    
    def generate_validation_report(self) -> str:
        """
        Generate a comprehensive validation report.
        
        Returns
        -------
        report : str
            Formatted validation report
        """
        report = []
        report.append("="*60)
        report.append("六鑰臨界框架交叉驗證報告")
        report.append("Six Keys Criticality Framework Cross-Validation Report")
        report.append("="*60)
        
        # State validation
        report.append("\n1. 意識狀態驗證 (Consciousness State Validation)")
        report.append("-"*40)
        state_validation = self.validate_simulated_states()
        report.append(f"平均準確率 (Mean Accuracy): {state_validation['mean_accuracy']:.3f} ± {state_validation['std_accuracy']:.3f}")
        report.append(f"平均F1分數 (Mean F1-Score): {state_validation['mean_f1']:.3f} ± {state_validation['std_f1']:.3f}")
        report.append(f"測試樣本數 (Total Samples): {state_validation['total_samples']}")
        
        # Indicator stability
        report.append("\n2. 指標穩定性驗證 (Indicator Stability Validation)")
        report.append("-"*40)
        stability_validation = self.validate_indicator_stability()
        report.append(f"整體穩定性 (Overall Stability CV): {stability_validation['overall_stability']:.3f}")
        
        for indicator, metrics in stability_validation['stability_metrics'].items():
            report.append(f"{indicator}: μ={metrics['mean']:.3f}, σ={metrics['std']:.3f}, CV={metrics['cv']:.3f}")
        
        # Parameter sensitivity
        report.append("\n3. 參數敏感性分析 (Parameter Sensitivity Analysis)")
        report.append("-"*40)
        sensitivity_validation = self.validate_parameter_sensitivity()
        
        for param_name, param_results in sensitivity_validation.items():
            report.append(f"\n{param_name} 敏感性:")
            for result in param_results:
                param_val = result['parameter_value']
                awake_class = result['state_results']['awake']['classification']
                anesthesia_class = result['state_results']['deep_anesthesia']['classification']
                report.append(f"  {param_val}: 清醒={awake_class}, 麻醉={anesthesia_class}")
        
        report.append("\n" + "="*60)
        report.append("驗證完成 (Validation Complete)")
        report.append("="*60)
        
        return "\n".join(report)
    
    def print_validation_summary(self):
        """
        Print a summary of validation results.
        """
        print(self.generate_validation_report())