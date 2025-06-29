# -*- coding: utf-8 -*-
"""
Preprocessing utilities for Six Keys Criticality framework.

六鑰臨界數據預處理工具模組：提供神經數據預處理和清理功能

This module provides utilities for preprocessing neural data, including
filtering, artifact removal, and standardization functions.
"""

import numpy as np
from typing import Dict, List, Tuple, Optional, Any, Union
import warnings
from scipy import signal
from scipy.signal import butter, filtfilt, hilbert
from sklearn.preprocessing import StandardScaler, RobustScaler


def preprocess_neural_data(data: np.ndarray,
                          sampling_rate: float,
                          filter_params: Optional[Dict[str, Any]] = None,
                          artifact_removal: bool = True,
                          standardize: bool = True,
                          **kwargs) -> Tuple[np.ndarray, Dict[str, Any]]:
    """
    Comprehensive preprocessing pipeline for neural data.
    
    Parameters
    ----------
    data : np.ndarray
        Neural data array (channels x time_points)
    sampling_rate : float
        Sampling rate in Hz
    filter_params : dict, optional
        Parameters for filtering (lowpass, highpass, bandpass)
    artifact_removal : bool, default=True
        Whether to perform artifact removal
    standardize : bool, default=True
        Whether to standardize the data
    **kwargs
        Additional preprocessing parameters
        
    Returns
    -------
    processed_data : np.ndarray
        Preprocessed neural data
    preprocessing_info : dict
        Information about preprocessing steps applied
        
    Examples
    --------
    >>> data = np.random.randn(64, 1000)  # 64 channels, 1000 time points
    >>> processed, info = preprocess_neural_data(data, sampling_rate=250)
    """
    if data.ndim != 2:
        raise ValueError("Data must be 2D array (channels x time_points)")
    
    n_channels, n_timepoints = data.shape
    processed_data = data.copy()
    preprocessing_info = {
        'original_shape': data.shape,
        'sampling_rate': sampling_rate,
        'steps_applied': []
    }
    
    # Step 1: Filtering
    if filter_params is not None:
        processed_data, filter_info = filter_data(
            processed_data, 
            sampling_rate, 
            **filter_params
        )
        preprocessing_info['steps_applied'].append('filtering')
        preprocessing_info['filter_info'] = filter_info
    
    # Step 2: Artifact removal
    if artifact_removal:
        processed_data, artifact_info = remove_artifacts(
            processed_data,
            method=kwargs.get('artifact_method', 'threshold'),
            **kwargs
        )
        preprocessing_info['steps_applied'].append('artifact_removal')
        preprocessing_info['artifact_info'] = artifact_info
    
    # Step 3: Standardization
    if standardize:
        processed_data, standardization_info = standardize_data(
            processed_data,
            method=kwargs.get('standardization_method', 'zscore'),
            **kwargs
        )
        preprocessing_info['steps_applied'].append('standardization')
        preprocessing_info['standardization_info'] = standardization_info
    
    preprocessing_info['final_shape'] = processed_data.shape
    preprocessing_info['data_quality'] = _assess_data_quality(processed_data)
    
    return processed_data, preprocessing_info


def filter_data(data: np.ndarray,
               sampling_rate: float,
               lowpass: Optional[float] = None,
               highpass: Optional[float] = None,
               bandpass: Optional[Tuple[float, float]] = None,
               filter_order: int = 4,
               filter_type: str = 'butterworth') -> Tuple[np.ndarray, Dict[str, Any]]:
    """
    Apply frequency filtering to neural data.
    
    Parameters
    ----------
    data : np.ndarray
        Neural data array (channels x time_points)
    sampling_rate : float
        Sampling rate in Hz
    lowpass : float, optional
        Lowpass filter cutoff frequency in Hz
    highpass : float, optional
        Highpass filter cutoff frequency in Hz
    bandpass : tuple of float, optional
        Bandpass filter cutoff frequencies (low, high) in Hz
    filter_order : int, default=4
        Filter order
    filter_type : str, default='butterworth'
        Type of filter ('butterworth', 'chebyshev', 'elliptic')
        
    Returns
    -------
    filtered_data : np.ndarray
        Filtered neural data
    filter_info : dict
        Information about filtering applied
        
    Examples
    --------
    >>> data = np.random.randn(64, 1000)
    >>> filtered, info = filter_data(data, 250, lowpass=40, highpass=1)
    """
    if data.ndim != 2:
        raise ValueError("Data must be 2D array (channels x time_points)")
    
    filtered_data = data.copy()
    nyquist = sampling_rate / 2
    
    filter_info = {
        'filter_type': filter_type,
        'filter_order': filter_order,
        'sampling_rate': sampling_rate,
        'nyquist_frequency': nyquist,
        'filters_applied': []
    }
    
    # Apply bandpass filter if specified
    if bandpass is not None:
        low_freq, high_freq = bandpass
        if low_freq >= high_freq:
            raise ValueError("Bandpass low frequency must be less than high frequency")
        if high_freq >= nyquist:
            raise ValueError(f"Bandpass high frequency ({high_freq}) must be less than Nyquist frequency ({nyquist})")
        
        sos = butter(filter_order, [low_freq, high_freq], btype='band', fs=sampling_rate, output='sos')
        
        for ch in range(filtered_data.shape[0]):
            filtered_data[ch, :] = filtfilt(sos, filtered_data[ch, :], method='gust')
        
        filter_info['filters_applied'].append({
            'type': 'bandpass',
            'frequencies': [low_freq, high_freq]
        })
    
    else:
        # Apply highpass filter if specified
        if highpass is not None:
            if highpass >= nyquist:
                raise ValueError(f"Highpass frequency ({highpass}) must be less than Nyquist frequency ({nyquist})")
            
            sos = butter(filter_order, highpass, btype='high', fs=sampling_rate, output='sos')
            
            for ch in range(filtered_data.shape[0]):
                filtered_data[ch, :] = filtfilt(sos, filtered_data[ch, :], method='gust')
            
            filter_info['filters_applied'].append({
                'type': 'highpass',
                'frequency': highpass
            })
        
        # Apply lowpass filter if specified
        if lowpass is not None:
            if lowpass >= nyquist:
                raise ValueError(f"Lowpass frequency ({lowpass}) must be less than Nyquist frequency ({nyquist})")
            
            sos = butter(filter_order, lowpass, btype='low', fs=sampling_rate, output='sos')
            
            for ch in range(filtered_data.shape[0]):
                filtered_data[ch, :] = filtfilt(sos, filtered_data[ch, :], method='gust')
            
            filter_info['filters_applied'].append({
                'type': 'lowpass',
                'frequency': lowpass
            })
    
    if not filter_info['filters_applied']:
        warnings.warn("No filters were applied. Specify lowpass, highpass, or bandpass parameters.")
    
    return filtered_data, filter_info


def remove_artifacts(data: np.ndarray,
                    method: str = 'threshold',
                    threshold_std: float = 3.0,
                    window_size: Optional[int] = None,
                    **kwargs) -> Tuple[np.ndarray, Dict[str, Any]]:
    """
    Remove artifacts from neural data.
    
    Parameters
    ----------
    data : np.ndarray
        Neural data array (channels x time_points)
    method : str, default='threshold'
        Artifact removal method ('threshold', 'ica', 'robust')
    threshold_std : float, default=3.0
        Threshold in standard deviations for artifact detection
    window_size : int, optional
        Window size for sliding window artifact detection
    **kwargs
        Additional parameters for specific methods
        
    Returns
    -------
    cleaned_data : np.ndarray
        Data with artifacts removed
    artifact_info : dict
        Information about artifacts detected and removed
        
    Examples
    --------
    >>> data = np.random.randn(64, 1000)
    >>> cleaned, info = remove_artifacts(data, method='threshold')
    """
    if data.ndim != 2:
        raise ValueError("Data must be 2D array (channels x time_points)")
    
    cleaned_data = data.copy()
    n_channels, n_timepoints = data.shape
    
    artifact_info = {
        'method': method,
        'original_shape': data.shape,
        'artifacts_detected': [],
        'channels_affected': [],
        'timepoints_affected': []
    }
    
    if method == 'threshold':
        # Threshold-based artifact detection
        artifacts_mask = np.zeros_like(data, dtype=bool)
        
        for ch in range(n_channels):
            channel_data = data[ch, :]
            channel_std = np.std(channel_data)
            channel_mean = np.mean(channel_data)
            
            # Detect outliers
            outliers = np.abs(channel_data - channel_mean) > (threshold_std * channel_std)
            artifacts_mask[ch, :] = outliers
            
            if np.any(outliers):
                artifact_info['channels_affected'].append(ch)
                artifact_timepoints = np.where(outliers)[0]
                artifact_info['timepoints_affected'].extend(artifact_timepoints.tolist())
                
                # Replace artifacts with interpolated values
                if window_size is not None:
                    # Use sliding window interpolation
                    for tp in artifact_timepoints:
                        start_idx = max(0, tp - window_size // 2)
                        end_idx = min(n_timepoints, tp + window_size // 2 + 1)
                        
                        # Get clean data points in window
                        window_mask = ~outliers[start_idx:end_idx]
                        if np.any(window_mask):
                            window_data = channel_data[start_idx:end_idx][window_mask]
                            cleaned_data[ch, tp] = np.mean(window_data)
                        else:
                            # If no clean data in window, use channel mean
                            cleaned_data[ch, tp] = channel_mean
                else:
                    # Simple replacement with channel mean
                    cleaned_data[ch, outliers] = channel_mean
    
    elif method == 'robust':
        # Robust artifact detection using median and MAD
        artifacts_mask = np.zeros_like(data, dtype=bool)
        
        for ch in range(n_channels):
            channel_data = data[ch, :]
            channel_median = np.median(channel_data)
            mad = np.median(np.abs(channel_data - channel_median))
            
            # Modified z-score using MAD
            modified_z_scores = 0.6745 * (channel_data - channel_median) / mad
            outliers = np.abs(modified_z_scores) > threshold_std
            artifacts_mask[ch, :] = outliers
            
            if np.any(outliers):
                artifact_info['channels_affected'].append(ch)
                artifact_timepoints = np.where(outliers)[0]
                artifact_info['timepoints_affected'].extend(artifact_timepoints.tolist())
                
                # Replace artifacts with median
                cleaned_data[ch, outliers] = channel_median
    
    elif method == 'ica':
        # Placeholder for ICA-based artifact removal
        # In a full implementation, this would use FastICA or similar
        warnings.warn("ICA artifact removal not fully implemented. Using threshold method instead.")
        return remove_artifacts(data, method='threshold', threshold_std=threshold_std, **kwargs)
    
    else:
        raise ValueError(f"Unknown artifact removal method: {method}")
    
    # Calculate artifact statistics
    total_artifacts = len(set(artifact_info['timepoints_affected']))
    artifact_info['total_artifacts'] = total_artifacts
    artifact_info['artifact_percentage'] = (total_artifacts / n_timepoints) * 100
    artifact_info['channels_affected'] = list(set(artifact_info['channels_affected']))
    artifact_info['n_channels_affected'] = len(artifact_info['channels_affected'])
    
    return cleaned_data, artifact_info


def standardize_data(data: np.ndarray,
                    method: str = 'zscore',
                    axis: int = 1,
                    robust: bool = False) -> Tuple[np.ndarray, Dict[str, Any]]:
    """
    Standardize neural data.
    
    Parameters
    ----------
    data : np.ndarray
        Neural data array (channels x time_points)
    method : str, default='zscore'
        Standardization method ('zscore', 'minmax', 'robust')
    axis : int, default=1
        Axis along which to standardize (0=channels, 1=time)
    robust : bool, default=False
        Whether to use robust statistics
        
    Returns
    -------
    standardized_data : np.ndarray
        Standardized neural data
    standardization_info : dict
        Information about standardization applied
        
    Examples
    --------
    >>> data = np.random.randn(64, 1000)
    >>> standardized, info = standardize_data(data, method='zscore')
    """
    if data.ndim != 2:
        raise ValueError("Data must be 2D array (channels x time_points)")
    
    standardized_data = data.copy()
    
    standardization_info = {
        'method': method,
        'axis': axis,
        'robust': robust,
        'original_shape': data.shape
    }
    
    if method == 'zscore':
        if robust:
            # Use median and MAD for robust z-score
            if axis == 1:  # Standardize across time for each channel
                for ch in range(data.shape[0]):
                    channel_data = data[ch, :]
                    median = np.median(channel_data)
                    mad = np.median(np.abs(channel_data - median))
                    if mad > 0:
                        standardized_data[ch, :] = (channel_data - median) / (1.4826 * mad)
                    else:
                        standardized_data[ch, :] = channel_data - median
            else:  # Standardize across channels for each time point
                for tp in range(data.shape[1]):
                    timepoint_data = data[:, tp]
                    median = np.median(timepoint_data)
                    mad = np.median(np.abs(timepoint_data - median))
                    if mad > 0:
                        standardized_data[:, tp] = (timepoint_data - median) / (1.4826 * mad)
                    else:
                        standardized_data[:, tp] = timepoint_data - median
        else:
            # Standard z-score normalization
            mean = np.mean(standardized_data, axis=axis, keepdims=True)
            std = np.std(standardized_data, axis=axis, keepdims=True)
            
            # Avoid division by zero
            std[std == 0] = 1
            
            standardized_data = (standardized_data - mean) / std
            
            standardization_info['mean'] = mean
            standardization_info['std'] = std
    
    elif method == 'minmax':
        # Min-max normalization to [0, 1]
        min_val = np.min(standardized_data, axis=axis, keepdims=True)
        max_val = np.max(standardized_data, axis=axis, keepdims=True)
        
        # Avoid division by zero
        range_val = max_val - min_val
        range_val[range_val == 0] = 1
        
        standardized_data = (standardized_data - min_val) / range_val
        
        standardization_info['min'] = min_val
        standardization_info['max'] = max_val
        standardization_info['range'] = range_val
    
    elif method == 'robust':
        # Robust standardization using median and IQR
        if axis == 1:  # Standardize across time for each channel
            for ch in range(data.shape[0]):
                channel_data = data[ch, :]
                median = np.median(channel_data)
                q75, q25 = np.percentile(channel_data, [75, 25])
                iqr = q75 - q25
                if iqr > 0:
                    standardized_data[ch, :] = (channel_data - median) / iqr
                else:
                    standardized_data[ch, :] = channel_data - median
        else:  # Standardize across channels for each time point
            for tp in range(data.shape[1]):
                timepoint_data = data[:, tp]
                median = np.median(timepoint_data)
                q75, q25 = np.percentile(timepoint_data, [75, 25])
                iqr = q75 - q25
                if iqr > 0:
                    standardized_data[:, tp] = (timepoint_data - median) / iqr
                else:
                    standardized_data[:, tp] = timepoint_data - median
    
    else:
        raise ValueError(f"Unknown standardization method: {method}")
    
    # Calculate standardization statistics
    standardization_info['final_mean'] = np.mean(standardized_data)
    standardization_info['final_std'] = np.std(standardized_data)
    standardization_info['final_min'] = np.min(standardized_data)
    standardization_info['final_max'] = np.max(standardized_data)
    
    return standardized_data, standardization_info


def _assess_data_quality(data: np.ndarray) -> Dict[str, Any]:
    """
    Assess the quality of preprocessed neural data.
    
    Parameters
    ----------
    data : np.ndarray
        Neural data array (channels x time_points)
        
    Returns
    -------
    quality_metrics : dict
        Dictionary containing data quality metrics
    """
    quality_metrics = {
        'shape': data.shape,
        'n_channels': data.shape[0],
        'n_timepoints': data.shape[1],
        'has_nan': np.any(np.isnan(data)),
        'has_inf': np.any(np.isinf(data)),
        'n_nan': np.sum(np.isnan(data)),
        'n_inf': np.sum(np.isinf(data)),
        'mean': np.mean(data),
        'std': np.std(data),
        'min': np.min(data),
        'max': np.max(data),
        'dynamic_range': np.max(data) - np.min(data)
    }
    
    # Channel-wise quality metrics
    channel_means = np.mean(data, axis=1)
    channel_stds = np.std(data, axis=1)
    
    quality_metrics['channel_statistics'] = {
        'mean_across_channels': np.mean(channel_means),
        'std_of_channel_means': np.std(channel_means),
        'mean_of_channel_stds': np.mean(channel_stds),
        'std_of_channel_stds': np.std(channel_stds),
        'min_channel_std': np.min(channel_stds),
        'max_channel_std': np.max(channel_stds)
    }
    
    # Detect potential issues
    issues = []
    if quality_metrics['has_nan']:
        issues.append(f"Contains {quality_metrics['n_nan']} NaN values")
    if quality_metrics['has_inf']:
        issues.append(f"Contains {quality_metrics['n_inf']} infinite values")
    if np.any(channel_stds == 0):
        flat_channels = np.where(channel_stds == 0)[0]
        issues.append(f"Flat channels detected: {flat_channels.tolist()}")
    if quality_metrics['dynamic_range'] == 0:
        issues.append("No dynamic range in data")
    
    quality_metrics['issues'] = issues
    quality_metrics['quality_score'] = _calculate_quality_score(quality_metrics)
    
    return quality_metrics


def _calculate_quality_score(quality_metrics: Dict[str, Any]) -> float:
    """
    Calculate an overall quality score for the data.
    
    Parameters
    ----------
    quality_metrics : dict
        Quality metrics dictionary
        
    Returns
    -------
    quality_score : float
        Quality score between 0 and 1 (higher is better)
    """
    score = 1.0
    
    # Penalize for NaN and infinite values
    if quality_metrics['has_nan']:
        nan_ratio = quality_metrics['n_nan'] / (quality_metrics['n_channels'] * quality_metrics['n_timepoints'])
        score -= min(0.5, nan_ratio * 2)  # Max penalty of 0.5
    
    if quality_metrics['has_inf']:
        inf_ratio = quality_metrics['n_inf'] / (quality_metrics['n_channels'] * quality_metrics['n_timepoints'])
        score -= min(0.3, inf_ratio * 2)  # Max penalty of 0.3
    
    # Penalize for lack of dynamic range
    if quality_metrics['dynamic_range'] == 0:
        score -= 0.5
    
    # Penalize for flat channels
    channel_stds = quality_metrics['channel_statistics']['mean_of_channel_stds']
    if channel_stds == 0:
        score -= 0.3
    
    # Ensure score is between 0 and 1
    score = max(0.0, min(1.0, score))
    
    return score


def detect_bad_channels(data: np.ndarray,
                       method: str = 'variance',
                       threshold: float = 3.0) -> Tuple[List[int], Dict[str, Any]]:
    """
    Detect bad channels in neural data.
    
    Parameters
    ----------
    data : np.ndarray
        Neural data array (channels x time_points)
    method : str, default='variance'
        Detection method ('variance', 'correlation', 'kurtosis')
    threshold : float, default=3.0
        Threshold for bad channel detection
        
    Returns
    -------
    bad_channels : list of int
        Indices of detected bad channels
    detection_info : dict
        Information about bad channel detection
        
    Examples
    --------
    >>> data = np.random.randn(64, 1000)
    >>> bad_channels, info = detect_bad_channels(data)
    """
    if data.ndim != 2:
        raise ValueError("Data must be 2D array (channels x time_points)")
    
    n_channels, n_timepoints = data.shape
    bad_channels = []
    
    detection_info = {
        'method': method,
        'threshold': threshold,
        'n_channels': n_channels,
        'channel_metrics': {}
    }
    
    if method == 'variance':
        # Detect channels with abnormal variance
        channel_variances = np.var(data, axis=1)
        median_variance = np.median(channel_variances)
        mad_variance = np.median(np.abs(channel_variances - median_variance))
        
        for ch in range(n_channels):
            if mad_variance > 0:
                z_score = abs(channel_variances[ch] - median_variance) / (1.4826 * mad_variance)
            else:
                z_score = 0
            
            detection_info['channel_metrics'][ch] = {
                'variance': channel_variances[ch],
                'z_score': z_score
            }
            
            if z_score > threshold:
                bad_channels.append(ch)
    
    elif method == 'correlation':
        # Detect channels with low correlation to other channels
        correlation_matrix = np.corrcoef(data)
        
        for ch in range(n_channels):
            # Calculate mean correlation with other channels
            other_channels = [i for i in range(n_channels) if i != ch]
            if other_channels:
                mean_correlation = np.mean(np.abs(correlation_matrix[ch, other_channels]))
            else:
                mean_correlation = 0
            
            detection_info['channel_metrics'][ch] = {
                'mean_correlation': mean_correlation
            }
            
            # Channels with very low correlation are considered bad
            if mean_correlation < (1.0 / threshold):  # Inverse threshold for correlation
                bad_channels.append(ch)
    
    elif method == 'kurtosis':
        # Detect channels with abnormal kurtosis
        from scipy.stats import kurtosis
        
        channel_kurtosis = [kurtosis(data[ch, :]) for ch in range(n_channels)]
        median_kurtosis = np.median(channel_kurtosis)
        mad_kurtosis = np.median(np.abs(np.array(channel_kurtosis) - median_kurtosis))
        
        for ch in range(n_channels):
            if mad_kurtosis > 0:
                z_score = abs(channel_kurtosis[ch] - median_kurtosis) / (1.4826 * mad_kurtosis)
            else:
                z_score = 0
            
            detection_info['channel_metrics'][ch] = {
                'kurtosis': channel_kurtosis[ch],
                'z_score': z_score
            }
            
            if z_score > threshold:
                bad_channels.append(ch)
    
    else:
        raise ValueError(f"Unknown bad channel detection method: {method}")
    
    detection_info['bad_channels'] = bad_channels
    detection_info['n_bad_channels'] = len(bad_channels)
    detection_info['bad_channel_percentage'] = (len(bad_channels) / n_channels) * 100
    
    return bad_channels, detection_info


def interpolate_bad_channels(data: np.ndarray,
                           bad_channels: List[int],
                           method: str = 'spline') -> Tuple[np.ndarray, Dict[str, Any]]:
    """
    Interpolate bad channels using neighboring good channels.
    
    Parameters
    ----------
    data : np.ndarray
        Neural data array (channels x time_points)
    bad_channels : list of int
        Indices of bad channels to interpolate
    method : str, default='spline'
        Interpolation method ('spline', 'linear', 'nearest')
        
    Returns
    -------
    interpolated_data : np.ndarray
        Data with bad channels interpolated
    interpolation_info : dict
        Information about interpolation performed
        
    Examples
    --------
    >>> data = np.random.randn(64, 1000)
    >>> bad_channels = [5, 23, 45]
    >>> interpolated, info = interpolate_bad_channels(data, bad_channels)
    """
    if data.ndim != 2:
        raise ValueError("Data must be 2D array (channels x time_points)")
    
    n_channels, n_timepoints = data.shape
    interpolated_data = data.copy()
    
    interpolation_info = {
        'method': method,
        'bad_channels': bad_channels,
        'n_bad_channels': len(bad_channels),
        'interpolated_channels': []
    }
    
    good_channels = [ch for ch in range(n_channels) if ch not in bad_channels]
    
    if not good_channels:
        warnings.warn("No good channels available for interpolation")
        return interpolated_data, interpolation_info
    
    for bad_ch in bad_channels:
        if method == 'spline':
            # Use spline interpolation based on neighboring channels
            # For simplicity, use average of nearest good channels
            distances = [abs(bad_ch - good_ch) for good_ch in good_channels]
            nearest_indices = np.argsort(distances)[:min(4, len(good_channels))]  # Use up to 4 nearest
            nearest_channels = [good_channels[i] for i in nearest_indices]
            
            # Weight by inverse distance
            weights = [1.0 / (abs(bad_ch - ch) + 1) for ch in nearest_channels]
            weights = np.array(weights) / np.sum(weights)
            
            interpolated_signal = np.zeros(n_timepoints)
            for i, ch in enumerate(nearest_channels):
                interpolated_signal += weights[i] * data[ch, :]
            
            interpolated_data[bad_ch, :] = interpolated_signal
        
        elif method == 'linear':
            # Simple linear interpolation using nearest neighbors
            if bad_ch == 0:
                # First channel - use next good channel
                next_good = next((ch for ch in good_channels if ch > bad_ch), good_channels[0])
                interpolated_data[bad_ch, :] = data[next_good, :]
            elif bad_ch == n_channels - 1:
                # Last channel - use previous good channel
                prev_good = next((ch for ch in reversed(good_channels) if ch < bad_ch), good_channels[-1])
                interpolated_data[bad_ch, :] = data[prev_good, :]
            else:
                # Middle channel - interpolate between neighbors
                prev_good = next((ch for ch in reversed(good_channels) if ch < bad_ch), None)
                next_good = next((ch for ch in good_channels if ch > bad_ch), None)
                
                if prev_good is not None and next_good is not None:
                    # Linear interpolation
                    weight_next = (bad_ch - prev_good) / (next_good - prev_good)
                    weight_prev = 1.0 - weight_next
                    interpolated_data[bad_ch, :] = (weight_prev * data[prev_good, :] + 
                                                  weight_next * data[next_good, :])
                elif prev_good is not None:
                    interpolated_data[bad_ch, :] = data[prev_good, :]
                elif next_good is not None:
                    interpolated_data[bad_ch, :] = data[next_good, :]
        
        elif method == 'nearest':
            # Use nearest good channel
            distances = [abs(bad_ch - good_ch) for good_ch in good_channels]
            nearest_ch = good_channels[np.argmin(distances)]
            interpolated_data[bad_ch, :] = data[nearest_ch, :]
        
        else:
            raise ValueError(f"Unknown interpolation method: {method}")
        
        interpolation_info['interpolated_channels'].append(bad_ch)
    
    return interpolated_data, interpolation_info