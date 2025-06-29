# API Reference

Complete API documentation for the Six Keys Criticality framework.

## Core Modules

### Analysis Framework
- [`SixKeysAnalyzer`](analyzer.md) - Main analysis class
- [`CriticalityResults`](results.md) - Results data structure

### Core Indicators
- [`FELC`](felc.md) - Free Energy Limit Cycle (ζ₁)
- [`TEB`](teb.md) - Thermodynamic Efficiency Balance (ζ₂)
- [`RFI`](rfi.md) - Ricci Flow Index (ζ₃)
- [`ECGP`](ecgp.md) - Effective Causal Graph Percolation (ζ₄)
- [`PWC`](pwc.md) - Phase-Wrapped Circulation (ζ₅)
- [`ACI`](aci.md) - Astrocyte-Coupling Index (ζ₆)

### Utilities
- [`utils.data`](utils_data.md) - Data processing utilities
- [`utils.visualization`](utils_viz.md) - Visualization functions
- [`utils.statistics`](utils_stats.md) - Statistical analysis tools

### Demos
- [`demos.radar`](demos_radar.md) - Radar chart demonstrations
- [`demos.analysis`](demos_analysis.md) - Analysis demonstrations
- [`demos.validation`](demos_validation.md) - Validation demonstrations

## Quick Reference

### Main Classes

```python
# Primary analysis interface
from sixkeys import SixKeysAnalyzer

# Individual indicators
from sixkeys.core import FELC, TEB, RFI, ECGP, PWC, ACI

# Results handling
from sixkeys.analysis import CriticalityResults

# Utilities
from sixkeys.utils import plot_radar_chart, plot_phase_diagram
```

### Key Methods

| Method | Description | Returns |
|--------|-------------|----------|
| `analyze_simulated_data()` | Analyze simulated consciousness states | `CriticalityResults` |
| `analyze_data()` | Analyze real neural data | `CriticalityResults` |
| `plot_radar_chart()` | Create radar visualization | `matplotlib.Figure` |
| `plot_phase_diagram()` | Create phase space plot | `matplotlib.Figure` |
| `save_config()` | Save analyzer configuration | `None` |
| `from_config()` | Load analyzer from config | `SixKeysAnalyzer` |

### Key Properties

| Property | Type | Description |
|----------|------|-------------|
| `theta_c` | `float` | Critical threshold for state classification |
| `weights` | `dict` | Weights for combining the six indicators |
| `random_state` | `int` | Random seed for reproducible results |

## Data Structures

### CriticalityResults

```python
@dataclass
class CriticalityResults:
    zeta1: float          # FELC indicator value
    zeta2: float          # TEB indicator value  
    zeta3: float          # RFI indicator value
    zeta4: float          # ECGP indicator value
    zeta5: float          # PWC indicator value
    zeta6: float          # ACI indicator value
    d_total: float        # Weighted total distance
    theta_c: float        # Critical threshold used
    predicted_state: str  # Predicted consciousness state
    
    def to_dict(self) -> dict
    def to_json(self, filepath: str) -> None
    def __str__(self) -> str
```

## Parameter Specifications

### Common Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `sim_time` | `float` | `10.0` | Simulation duration (seconds) |
| `dt` | `float` | `0.01` | Time step (seconds) |
| `noise_level` | `float` | `0.1` | Noise amplitude |
| `random_state` | `int` | `None` | Random seed |

### Consciousness State Parameters

| State | Noise Level | Coupling | Description |
|-------|-------------|----------|-------------|
| `'awake'` | `0.05` | `1.0` | Normal conscious state |
| `'light_sedation'` | `0.15` | `0.7` | Light anesthesia/sedation |
| `'deep_anesthesia'` | `0.25` | `0.3` | Deep anesthetic state |

## Error Handling

### Common Exceptions

```python
from sixkeys.exceptions import (
    SixKeysError,           # Base exception
    DataFormatError,        # Invalid data format
    ParameterError,         # Invalid parameters
    AnalysisError,          # Analysis computation error
    VisualizationError      # Plotting error
)
```

### Error Examples

```python
try:
    result = analyzer.analyze_data(invalid_data)
except DataFormatError as e:
    print(f"Data format error: {e}")
except AnalysisError as e:
    print(f"Analysis failed: {e}")
```

## Configuration

### YAML Configuration Format

```yaml
# sixkeys_config.yaml
analyzer:
  theta_c: 1.0
  random_state: 42
  
weights:
  zeta1: 0.2
  zeta2: 0.2
  zeta3: 0.15
  zeta4: 0.15
  zeta5: 0.15
  zeta6: 0.15

felc_params:
  sim_time: 10.0
  dt: 0.01
  n_samples: 50
  inband_threshold: 0.1
  cv_threshold: 0.05

teb_params:
  sim_time: 10.0
  dt: 0.01
  n_samples: 50
  efficiency_min: 0.1
  efficiency_max: 0.9

# ... other indicator parameters
```

## Performance Considerations

### Memory Usage
- Each indicator analysis requires ~10-50 MB for default parameters
- Batch processing scales linearly with number of datasets
- Consider chunking for very large datasets (>10GB)

### Computation Time
- Single analysis: ~1-5 seconds (depending on parameters)
- Batch analysis: scales with number of samples
- GPU acceleration available for some indicators (experimental)

### Optimization Tips

```python
# Reduce simulation time for faster analysis
fast_analyzer = SixKeysAnalyzer(
    felc_params={'sim_time': 5.0},
    teb_params={'sim_time': 5.0},
    # ... other params
)

# Use multiprocessing for batch analysis
from multiprocessing import Pool
with Pool() as pool:
    results = pool.map(analyzer.analyze_data, datasets)
```

## Version Compatibility

| Six Keys Version | Python | NumPy | SciPy | Matplotlib |
|------------------|--------|-------|-------|------------|
| 1.0.x | 3.8+ | 1.19+ | 1.6+ | 3.3+ |
| 1.1.x | 3.8+ | 1.20+ | 1.7+ | 3.4+ |
| 2.0.x | 3.9+ | 1.21+ | 1.8+ | 3.5+ |

## Migration Guide

### From v1.0 to v1.1
- No breaking changes
- New optional parameters added
- Enhanced visualization options

### From v1.1 to v2.0
- `analyze_criticality()` renamed to `analyze_data()`
- New `CriticalityResults` data structure
- Updated parameter names for consistency

## See Also

- [Installation Guide](../zh/installation.md)
- [Quick Start Guide](../zh/quickstart.md)
- [Theory Documentation](../zh/theory.md)
- [Examples](../../examples/)
- [Contributing Guide](../../CONTRIBUTING.md)