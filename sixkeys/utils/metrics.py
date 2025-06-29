# -*- coding: utf-8 -*-
"""
Metrics utilities for Six Keys Criticality framework.

六鑰臨界指標工具模組：提供指標計算、標準化和評估功能

This module provides utility functions for calculating criticality metrics,
normalizing indicators, and assessing consciousness states.
"""

import numpy as np
from typing import Dict, List, Tuple, Optional, Any, Union
import warnings
from scipy import stats
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.metrics import euclidean_distances


def calculate_criticality_metrics(zeta_values: Dict[str, float],
                                 weights: Optional[Dict[str, float]] = None) -> Dict[str, float]:
    """
    Calculate comprehensive criticality metrics from zeta values.
    
    Parameters
    ----------
    zeta_values : dict
        Dictionary of indicator names and their zeta values
    weights : dict, optional
        Weights for each indicator. If None, uses equal weights
        
    Returns
    -------
    metrics : dict
        Dictionary of calculated metrics
        
    Examples
    --------
    >>> zeta_values = {'FELC': 0.8, 'TEB': 0.6, 'RFI': 0.7}
    >>> metrics = calculate_criticality_metrics(zeta_values)
    >>> print(metrics['d_total'])
    """
    if not zeta_values:
        raise ValueError("zeta_values cannot be empty")
    
    # Set default weights if not provided
    if weights is None:
        weights = {indicator: 1.0 for indicator in zeta_values.keys()}
    
    # Ensure all indicators have weights
    for indicator in zeta_values.keys():
        if indicator not in weights:
            weights[indicator] = 1.0
    
    # Normalize weights
    total_weight = sum(weights.values())
    normalized_weights = {k: v / total_weight for k, v in weights.items()}
    
    # Calculate weighted distance from criticality
    weighted_distances = []
    for indicator, zeta in zeta_values.items():
        weight = normalized_weights.get(indicator, 0.0)
        distance = abs(zeta - 1.0)  # Distance from critical point (zeta = 1)
        weighted_distances.append(weight * distance)
    
    d_total = sum(weighted_distances)
    
    # Calculate additional metrics
    zeta_array = np.array(list(zeta_values.values()))
    
    metrics = {
        'd_total': d_total,
        'mean_zeta': np.mean(zeta_array),
        'std_zeta': np.std(zeta_array),
        'min_zeta': np.min(zeta_array),
        'max_zeta': np.max(zeta_array),
        'range_zeta': np.max(zeta_array) - np.min(zeta_array),
        'median_zeta': np.median(zeta_array),
        'variance_zeta': np.var(zeta_array),
        'skewness_zeta': stats.skew(zeta_array) if len(zeta_array) > 2 else 0.0,
        'kurtosis_zeta': stats.kurtosis(zeta_array) if len(zeta_array) > 3 else 0.0,
        'criticality_score': 1.0 / (1.0 + d_total),  # Inverse relationship with distance
        'coherence_index': 1.0 - np.std(zeta_array),  # Higher when zetas are similar
        'balance_index': 1.0 - abs(np.mean(zeta_array) - 1.0)  # Higher when mean is near 1
    }
    
    # Calculate indicator-specific metrics
    for indicator, zeta in zeta_values.items():
        metrics[f'{indicator}_distance'] = abs(zeta - 1.0)
        metrics[f'{indicator}_criticality'] = 1.0 / (1.0 + abs(zeta - 1.0))
    
    return metrics


def normalize_indicators(indicator_values: Dict[str, Union[float, np.ndarray]],
                        method: str = 'minmax',
                        target_range: Tuple[float, float] = (0.0, 2.0)) -> Dict[str, Union[float, np.ndarray]]:
    """
    Normalize indicator values to a specified range.
    
    Parameters
    ----------
    indicator_values : dict
        Dictionary of indicator names and their values
    method : str, default='minmax'
        Normalization method ('minmax', 'zscore', 'robust')
    target_range : tuple, default=(0.0, 2.0)
        Target range for normalization
        
    Returns
    -------
    normalized_values : dict
        Dictionary of normalized indicator values
        
    Examples
    --------
    >>> values = {'FELC': [0.5, 1.0, 1.5], 'TEB': [0.8, 1.2, 0.9]}
    >>> normalized = normalize_indicators(values)
    """
    if not indicator_values:
        raise ValueError("indicator_values cannot be empty")
    
    normalized_values = {}
    
    for indicator, values in indicator_values.items():
        if isinstance(values, (int, float)):
            # Single value - normalize based on expected range
            if method == 'minmax':
                # Assume typical range is [0, 2] for zeta values
                normalized = (values - 0.0) / (2.0 - 0.0) * (target_range[1] - target_range[0]) + target_range[0]
            elif method == 'zscore':
                # For single values, just return as is (can't calculate z-score)
                normalized = values
            else:
                normalized = values
            
            normalized_values[indicator] = normalized
        
        else:
            # Array of values
            values_array = np.array(values)
            
            if method == 'minmax':
                scaler = MinMaxScaler(feature_range=target_range)
                normalized = scaler.fit_transform(values_array.reshape(-1, 1)).flatten()
            
            elif method == 'zscore':
                normalized = stats.zscore(values_array)
                # Scale to target range
                if np.std(normalized) > 0:
                    normalized = (normalized - np.min(normalized)) / (np.max(normalized) - np.min(normalized))
                    normalized = normalized * (target_range[1] - target_range[0]) + target_range[0]
                else:
                    normalized = np.full_like(normalized, np.mean(target_range))
            
            elif method == 'robust':
                # Robust scaling using median and IQR
                median = np.median(values_array)
                q75, q25 = np.percentile(values_array, [75, 25])
                iqr = q75 - q25
                
                if iqr > 0:
                    normalized = (values_array - median) / iqr
                    # Scale to target range
                    normalized = (normalized - np.min(normalized)) / (np.max(normalized) - np.min(normalized))
                    normalized = normalized * (target_range[1] - target_range[0]) + target_range[0]
                else:
                    normalized = np.full_like(values_array, np.mean(target_range))
            
            else:
                raise ValueError(f"Unknown normalization method: {method}")
            
            normalized_values[indicator] = normalized
    
    return normalized_values


def calculate_pipeline_distance(zeta_values: Dict[str, float],
                              reference_state: str = 'critical',
                              distance_metric: str = 'euclidean') -> float:
    """
    Calculate distance from a reference state in the criticality pipeline.
    
    Parameters
    ----------
    zeta_values : dict
        Dictionary of indicator names and their zeta values
    reference_state : str, default='critical'
        Reference state ('critical', 'subcritical', 'supercritical')
    distance_metric : str, default='euclidean'
        Distance metric to use
        
    Returns
    -------
    distance : float
        Distance from reference state
        
    Examples
    --------
    >>> zeta_values = {'FELC': 0.8, 'TEB': 1.2, 'RFI': 0.9}
    >>> distance = calculate_pipeline_distance(zeta_values, 'critical')
    """
    if not zeta_values:
        raise ValueError("zeta_values cannot be empty")
    
    # Define reference points for different states
    reference_points = {
        'critical': 1.0,
        'subcritical': 0.5,
        'supercritical': 1.5
    }
    
    if reference_state not in reference_points:
        raise ValueError(f"Unknown reference state: {reference_state}")
    
    reference_point = reference_points[reference_state]
    zeta_array = np.array(list(zeta_values.values()))
    reference_array = np.full_like(zeta_array, reference_point)
    
    if distance_metric == 'euclidean':
        distance = np.sqrt(np.sum((zeta_array - reference_array) ** 2))
    elif distance_metric == 'manhattan':
        distance = np.sum(np.abs(zeta_array - reference_array))
    elif distance_metric == 'chebyshev':
        distance = np.max(np.abs(zeta_array - reference_array))
    elif distance_metric == 'cosine':
        # Cosine distance
        dot_product = np.dot(zeta_array, reference_array)
        norm_product = np.linalg.norm(zeta_array) * np.linalg.norm(reference_array)
        if norm_product > 0:
            cosine_similarity = dot_product / norm_product
            distance = 1.0 - cosine_similarity
        else:
            distance = 1.0
    else:
        raise ValueError(f"Unknown distance metric: {distance_metric}")
    
    return distance


def assess_consciousness_state(zeta_values: Dict[str, float],
                             d_total: Optional[float] = None,
                             threshold: float = 0.5,
                             method: str = 'threshold') -> Dict[str, Any]:
    """
    Assess consciousness state based on criticality indicators.
    
    Parameters
    ----------
    zeta_values : dict
        Dictionary of indicator names and their zeta values
    d_total : float, optional
        Total distance from criticality. If None, calculated from zeta_values
    threshold : float, default=0.5
        Threshold for consciousness classification
    method : str, default='threshold'
        Assessment method ('threshold', 'probabilistic', 'fuzzy')
        
    Returns
    -------
    assessment : dict
        Dictionary containing consciousness assessment results
        
    Examples
    --------
    >>> zeta_values = {'FELC': 0.9, 'TEB': 1.1, 'RFI': 0.8}
    >>> assessment = assess_consciousness_state(zeta_values)
    >>> print(assessment['state'])
    """
    if not zeta_values:
        raise ValueError("zeta_values cannot be empty")
    
    # Calculate d_total if not provided
    if d_total is None:
        metrics = calculate_criticality_metrics(zeta_values)
        d_total = metrics['d_total']
    
    assessment = {
        'd_total': d_total,
        'threshold': threshold,
        'method': method
    }
    
    if method == 'threshold':
        # Simple threshold-based classification
        if d_total <= threshold:
            state = 'Conscious'
            confidence = 1.0 - (d_total / threshold)
        else:
            state = 'Non-conscious'
            confidence = min(1.0, (d_total - threshold) / threshold)
        
        assessment.update({
            'state': state,
            'confidence': confidence,
            'probability_conscious': 1.0 - confidence if state == 'Non-conscious' else confidence
        })
    
    elif method == 'probabilistic':
        # Probabilistic assessment using sigmoid function
        # P(conscious) = 1 / (1 + exp(k * (d_total - threshold)))
        k = 10.0  # Steepness parameter
        prob_conscious = 1.0 / (1.0 + np.exp(k * (d_total - threshold)))
        
        state = 'Conscious' if prob_conscious > 0.5 else 'Non-conscious'
        confidence = max(prob_conscious, 1.0 - prob_conscious)
        
        assessment.update({
            'state': state,
            'confidence': confidence,
            'probability_conscious': prob_conscious
        })
    
    elif method == 'fuzzy':
        # Fuzzy logic assessment
        # Define membership functions for different states
        def conscious_membership(d):
            if d <= 0.2:
                return 1.0
            elif d <= 0.6:
                return 1.0 - (d - 0.2) / 0.4
            else:
                return 0.0
        
        def non_conscious_membership(d):
            if d <= 0.4:
                return 0.0
            elif d <= 0.8:
                return (d - 0.4) / 0.4
            else:
                return 1.0
        
        conscious_degree = conscious_membership(d_total)
        non_conscious_degree = non_conscious_membership(d_total)
        
        if conscious_degree > non_conscious_degree:
            state = 'Conscious'
            confidence = conscious_degree
        else:
            state = 'Non-conscious'
            confidence = non_conscious_degree
        
        assessment.update({
            'state': state,
            'confidence': confidence,
            'conscious_degree': conscious_degree,
            'non_conscious_degree': non_conscious_degree,
            'probability_conscious': conscious_degree / (conscious_degree + non_conscious_degree)
        })
    
    else:
        raise ValueError(f"Unknown assessment method: {method}")
    
    # Add detailed indicator analysis
    indicator_analysis = {}
    for indicator, zeta in zeta_values.items():
        distance_from_critical = abs(zeta - 1.0)
        criticality_score = 1.0 / (1.0 + distance_from_critical)
        
        indicator_analysis[indicator] = {
            'zeta': zeta,
            'distance_from_critical': distance_from_critical,
            'criticality_score': criticality_score,
            'state': 'Critical' if 0.9 <= zeta <= 1.1 else ('Subcritical' if zeta < 0.9 else 'Supercritical')
        }
    
    assessment['indicator_analysis'] = indicator_analysis
    
    return assessment


def calculate_state_transitions(zeta_time_series: Dict[str, np.ndarray],
                              window_size: int = 10,
                              threshold: float = 0.5) -> Dict[str, Any]:
    """
    Calculate state transitions over time.
    
    Parameters
    ----------
    zeta_time_series : dict
        Dictionary of indicator names and their time series of zeta values
    window_size : int, default=10
        Window size for calculating transitions
    threshold : float, default=0.5
        Threshold for state classification
        
    Returns
    -------
    transitions : dict
        Dictionary containing transition analysis results
        
    Examples
    --------
    >>> zeta_series = {'FELC': np.random.rand(100), 'TEB': np.random.rand(100)}
    >>> transitions = calculate_state_transitions(zeta_series)
    """
    if not zeta_time_series:
        raise ValueError("zeta_time_series cannot be empty")
    
    # Get time series length (assume all indicators have same length)
    first_indicator = list(zeta_time_series.keys())[0]
    time_length = len(zeta_time_series[first_indicator])
    
    # Calculate d_total time series
    d_total_series = []
    state_series = []
    
    for t in range(time_length):
        zeta_values_t = {indicator: series[t] for indicator, series in zeta_time_series.items()}
        metrics_t = calculate_criticality_metrics(zeta_values_t)
        d_total_t = metrics_t['d_total']
        
        d_total_series.append(d_total_t)
        state_series.append('Conscious' if d_total_t <= threshold else 'Non-conscious')
    
    d_total_series = np.array(d_total_series)
    
    # Calculate transitions
    transitions = []
    for i in range(1, len(state_series)):
        if state_series[i] != state_series[i-1]:
            transitions.append({
                'time': i,
                'from_state': state_series[i-1],
                'to_state': state_series[i],
                'd_total_before': d_total_series[i-1],
                'd_total_after': d_total_series[i]
            })
    
    # Calculate transition statistics
    conscious_to_non = sum(1 for t in transitions if t['from_state'] == 'Conscious' and t['to_state'] == 'Non-conscious')
    non_to_conscious = sum(1 for t in transitions if t['from_state'] == 'Non-conscious' and t['to_state'] == 'Conscious')
    
    # Calculate state durations
    conscious_durations = []
    non_conscious_durations = []
    
    current_state = state_series[0]
    current_duration = 1
    
    for i in range(1, len(state_series)):
        if state_series[i] == current_state:
            current_duration += 1
        else:
            if current_state == 'Conscious':
                conscious_durations.append(current_duration)
            else:
                non_conscious_durations.append(current_duration)
            
            current_state = state_series[i]
            current_duration = 1
    
    # Add final duration
    if current_state == 'Conscious':
        conscious_durations.append(current_duration)
    else:
        non_conscious_durations.append(current_duration)
    
    results = {
        'd_total_series': d_total_series,
        'state_series': state_series,
        'transitions': transitions,
        'n_transitions': len(transitions),
        'conscious_to_non_conscious': conscious_to_non,
        'non_conscious_to_conscious': non_to_conscious,
        'conscious_durations': conscious_durations,
        'non_conscious_durations': non_conscious_durations,
        'mean_conscious_duration': np.mean(conscious_durations) if conscious_durations else 0,
        'mean_non_conscious_duration': np.mean(non_conscious_durations) if non_conscious_durations else 0,
        'conscious_ratio': state_series.count('Conscious') / len(state_series),
        'transition_rate': len(transitions) / time_length
    }
    
    return results


def calculate_indicator_correlations(zeta_values_dict: Dict[str, Dict[str, float]]) -> Dict[str, Any]:
    """
    Calculate correlations between indicators across multiple samples.
    
    Parameters
    ----------
    zeta_values_dict : dict
        Dictionary where keys are sample IDs and values are dicts of indicator zeta values
        
    Returns
    -------
    correlations : dict
        Dictionary containing correlation analysis results
        
    Examples
    --------
    >>> samples = {
    ...     'sample1': {'FELC': 0.8, 'TEB': 0.9},
    ...     'sample2': {'FELC': 1.2, 'TEB': 1.1}
    ... }
    >>> correlations = calculate_indicator_correlations(samples)
    """
    if not zeta_values_dict:
        raise ValueError("zeta_values_dict cannot be empty")
    
    # Extract indicator names
    first_sample = list(zeta_values_dict.values())[0]
    indicators = list(first_sample.keys())
    
    # Create data matrix
    data_matrix = []
    for sample_id, zeta_values in zeta_values_dict.items():
        row = [zeta_values.get(indicator, np.nan) for indicator in indicators]
        data_matrix.append(row)
    
    data_matrix = np.array(data_matrix)
    
    # Calculate correlation matrix
    correlation_matrix = np.corrcoef(data_matrix.T)
    
    # Create correlation dictionary
    correlations = {}
    for i, indicator1 in enumerate(indicators):
        for j, indicator2 in enumerate(indicators):
            if i != j:
                corr_key = f"{indicator1}_{indicator2}"
                correlations[corr_key] = correlation_matrix[i, j]
    
    # Calculate summary statistics
    mean_correlations = {}
    for indicator in indicators:
        indicator_correlations = []
        for other_indicator in indicators:
            if indicator != other_indicator:
                corr_key = f"{indicator}_{other_indicator}"
                if not np.isnan(correlations[corr_key]):
                    indicator_correlations.append(abs(correlations[corr_key]))
        
        if indicator_correlations:
            mean_correlations[indicator] = np.mean(indicator_correlations)
        else:
            mean_correlations[indicator] = 0.0
    
    results = {
        'correlation_matrix': correlation_matrix,
        'correlations': correlations,
        'mean_correlations': mean_correlations,
        'indicators': indicators,
        'n_samples': len(zeta_values_dict),
        'strongest_correlation': max(correlations.items(), key=lambda x: abs(x[1])) if correlations else None,
        'weakest_correlation': min(correlations.items(), key=lambda x: abs(x[1])) if correlations else None
    }
    
    return results