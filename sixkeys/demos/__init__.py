"""SixKeys Demonstration Modules

This package contains demonstration scripts and visualization tools for the SixKeys framework.
These modules are optional and can be used independently to showcase various aspects
of the six key indicators for consciousness analysis.

Modules:
    radar_chart: Integrated radar chart visualization for all six indicators
    public_data_analysis: Re-analysis of public datasets with Dw distribution
    cross_validation: Cross-validation analysis with correlation matrices
"""

__version__ = "1.0.0"
__author__ = "SixKeys Team"

# Optional imports - gracefully handle missing dependencies
try:
    from .radar_chart import SixKeysRadarChart, quick_demo as radar_demo
except ImportError:
    SixKeysRadarChart = None
    radar_demo = None

try:
    from .public_data_analysis import PublicDataAnalysis, quick_demo as public_data_demo
except ImportError:
    PublicDataAnalysis = None
    public_data_demo = None

try:
    from .cross_validation import CrossValidationAnalysis, quick_demo as cross_validation_demo
except ImportError:
    CrossValidationAnalysis = None
    cross_validation_demo = None

__all__ = [
    'SixKeysRadarChart',
    'PublicDataAnalysis', 
    'CrossValidationAnalysis',
    'radar_demo',
    'public_data_demo',
    'cross_validation_demo',
    'check_demo_dependencies'
]

def check_demo_dependencies():
    """Check if all required dependencies for demos are available."""
    missing = []
    
    try:
        import matplotlib.pyplot as plt
        import numpy as np
    except ImportError as e:
        missing.append(f"matplotlib/numpy: {e}")
    
    try:
        import seaborn as sns
    except ImportError:
        missing.append("seaborn (optional for enhanced visualizations)")
    
    if missing:
        print("Missing dependencies for demos:")
        for dep in missing:
            print(f"  - {dep}")
        print("\nInstall with: pip install matplotlib seaborn")
        return False
    
    return True