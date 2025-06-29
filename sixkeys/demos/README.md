# SixKeys Demonstration Modules

This package contains optional demonstration modules for the SixKeys framework. These modules provide integrated visualizations and analysis tools to showcase various aspects of the six key indicators for consciousness analysis.

## Overview

The demos package includes three main modules:

1. **Radar Chart** (`radar_chart.py`) - Integrated radar chart visualization for all six indicators
2. **Public Data Analysis** (`public_data_analysis.py`) - Re-analysis of public datasets with Dw distribution
3. **Cross-Validation** (`cross_validation.py`) - Cross-validation analysis with correlation matrices

## Installation

The demos modules require additional dependencies beyond the core SixKeys package:

```bash
pip install matplotlib seaborn scipy pandas
```

You can check if all dependencies are available:

```python
from sixkeys.demos import check_demo_dependencies
check_demo_dependencies()
```

## Quick Start

### Option 1: Quick Demonstrations

```python
# Run individual demos
from sixkeys.demos import radar_demo, public_data_demo, cross_validation_demo

radar_demo()           # Six Keys Radar Chart
public_data_demo()     # Public Data Re-analysis  
cross_validation_demo() # Cross-Validation Analysis
```

### Option 2: Using Classes Directly

```python
from sixkeys.demos import SixKeysRadarChart, PublicDataAnalysis, CrossValidationAnalysis

# Radar Chart
radar = SixKeysRadarChart()
fig_radar, fig_bar = radar.simulate_and_plot()

# Public Data Analysis
analyzer = PublicDataAnalysis()
fig, summary = analyzer.generate_and_analyze()

# Cross-Validation
cv = CrossValidationAnalysis()
fig, results = cv.generate_and_analyze()
```

### Option 3: Command Line Interface

```bash
# Run all demonstrations
python examples/demo_visualization.py

# Run specific module
python examples/demo_visualization.py --module radar

# Save outputs without displaying plots
python examples/demo_visualization.py --no-plots --save --output results/
```

## Module Details

### 1. SixKeysRadarChart

Visualizes the six key indicators using radar charts and bar plots to demonstrate consciousness state transitions.

**Features:**
- Simulates dimensionless coordinates ζ_i for different consciousness states
- Generates binary critical flags C_i and weighted distances D_w_i
- Creates radar charts showing |ζ| values
- Displays total distance D_total vs critical threshold θ_c

**Example:**
```python
from sixkeys.demos import SixKeysRadarChart

radar = SixKeysRadarChart(
    theta_c=1.0,  # Critical threshold
    random_seed=2025
)

# Customize consciousness states
radar.update_state_parameters({
    "Custom_State": -0.3
})

fig_radar, fig_bar = radar.simulate_and_plot(save_plots=True)
radar.print_summary()
```

### 2. PublicDataAnalysis

Generates synthetic Dw distribution data mimicking real public datasets and analyzes differences between consciousness states.

**Features:**
- Simulates five public datasets (MEG, fMRI, Mouse data, etc.)
- Generates Dw distributions for awake vs low consciousness states
- Creates boxplot visualizations
- Performs statistical significance testing
- Exports data to CSV format

**Example:**
```python
from sixkeys.demos import PublicDataAnalysis

analyzer = PublicDataAnalysis(
    n_samples=50,  # Samples per state per dataset
    theta_c=0.55   # Critical threshold
)

# Add custom dataset
analyzer.add_dataset("Custom_Dataset", mu_awake=0.35, mu_low=0.70)

fig, summary = analyzer.generate_and_analyze(save_files=True)
sig_results = analyzer.analyze_significance()
```

### 3. CrossValidationAnalysis

Analyzes correlations between the six key indicators under different consciousness states.

**Features:**
- Generates synthetic time-series data for all six indicators
- Computes correlation matrices for awake vs unaware states
- Creates side-by-side correlation heatmaps
- Analyzes specific key pair relationships (e.g., FELC-RFI)
- Exports correlation matrices and raw data

**Example:**
```python
from sixkeys.demos import CrossValidationAnalysis

cv = CrossValidationAnalysis(
    n_samples=500,        # Time samples
    awake_correlation=0.8, # FELC-RFI correlation in awake state
    random_seed=42
)

# Update parameters
cv.update_parameters(awake_correlation=0.9, unaware_noise_factor=1.5)

fig, results = cv.generate_and_analyze(save_files=True)

# Analyze specific correlations
key_analysis = cv.analyze_key_correlations([
    ('FELC', 'RFI'), 
    ('ECGP', 'PWC')
])
```

## Customization

All modules support extensive customization:

### Consciousness States
```python
# Radar Chart - Add custom states
radar.add_custom_state("Meditation", mu=-0.2)

# Public Data - Add custom datasets
analyzer.add_dataset("EEG_Study", mu_awake=0.40, mu_low=0.65)
```

### Visualization Options
```python
# Control plot display and saving
fig = module.plot_method(
    show_plots=False,  # Don't display
    save_files=True,   # Save to disk
    output_dir="./results/"
)

# Customize figure size
fig = module.plot_method(figsize=(12, 8))
```

### Data Export
```python
# Save raw data
saved_files = analyzer.save_data(
    output_dir="./data/",
    save_raw_data=True,
    save_correlations=True
)

# Get data as DataFrames
awake_df, unaware_df = cv.get_correlation_dataframes()
```

## Integration with Core SixKeys

These demonstration modules are designed to complement the core SixKeys analysis framework:

```python
# Use with real SixKeys analysis
from sixkeys.analysis import SixKeysAnalyzer
from sixkeys.demos import SixKeysRadarChart

# Analyze real data
analyzer = SixKeysAnalyzer()
results = analyzer.analyze_simulated_data(duration=10.0)

# Visualize with demo tools
radar = SixKeysRadarChart()
# ... customize radar with real results
```

## Dependencies

- **Required:** `numpy`, `matplotlib`
- **Optional:** `seaborn` (enhanced visualizations), `scipy` (statistical tests), `pandas` (data handling)

## Notes

- All modules use reproducible random seeds for consistent results
- Graceful fallbacks are provided when optional dependencies are missing
- Modules can be used independently or together
- All visualizations are publication-ready with high DPI output

## Troubleshooting

### Missing Dependencies
```python
from sixkeys.demos import check_demo_dependencies
if not check_demo_dependencies():
    print("Install missing dependencies with: pip install matplotlib seaborn scipy pandas")
```

### Import Errors
If you encounter import errors, ensure the SixKeys package is properly installed:
```bash
pip install -e .  # If installing from source
```

### Display Issues
For headless environments or when plots don't display:
```python
# Use non-interactive backend
import matplotlib
matplotlib.use('Agg')

# Or disable plot display
module.generate_and_analyze(show_plots=False, save_files=True)
```