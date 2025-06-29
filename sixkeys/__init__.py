#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Six Keys Criticality - A Framework for Neural Consciousness State Analysis

六鑰臨界：基於臨界轉換理論的神經意識狀態分析框架

This package provides tools for analyzing neural criticality through six key indicators:
- FELC (ζ₁): Free Energy Limit Cycle
- TEB (ζ₂): Thermodynamic Efficiency Balance  
- RFI (ζ₃): Ricci Flow Index
- ECGP (ζ₄): Effective Causal Graph Percolation
- PWC (ζ₅): Phase-Wrapped Circulation
- ACI (ζ₆): Astrocyte-Coupling Index
"""

__version__ = '0.1.0'
__author__ = 'You Yang Hou'
__email__ = 'your.email@example.com'
__license__ = 'BSD 3-Clause'

# Core modules
from .core import (
    FELC,
    TEB, 
    RFI,
    ECGP,
    PWC,
    ACI,
)

# Analysis tools
from .analysis import (
    SixKeysAnalyzer,
    CrossValidation,
    PublicDataReanalysis,
)

# Utility functions
from .utils import (
    load_data,
    save_results,
    plot_radar_chart,
    plot_phase_diagram,
    calculate_criticality_metrics,
)

# Main analysis function
def analyze_criticality(data, **kwargs):
    """
    Perform complete six-keys criticality analysis.
    
    Parameters
    ----------
    data : array-like, shape (n_timepoints, n_channels)
        Neural time series data
    **kwargs : dict
        Additional parameters for analysis
        
    Returns
    -------
    results : dict
        Dictionary containing all six key indicators and derived metrics
    """
    analyzer = SixKeysAnalyzer(**kwargs)
    return analyzer.fit_transform(data)

# Package metadata
__all__ = [
    # Version info
    '__version__',
    '__author__',
    '__email__',
    '__license__',
    
    # Core classes
    'FELC',
    'TEB',
    'RFI', 
    'ECGP',
    'PWC',
    'ACI',
    
    # Analysis classes
    'SixKeysAnalyzer',
    'CrossValidation',
    'PublicDataReanalysis',
    
    # Utility functions
    'load_data',
    'save_results',
    'plot_radar_chart',
    'plot_phase_diagram',
    'calculate_criticality_metrics',
    
    # Main function
    'analyze_criticality',
]

# Package configuration
import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())

# Optional: Set up package-level configuration
try:
    import numpy as np
    np.seterr(divide='ignore', invalid='ignore')
except ImportError:
    pass