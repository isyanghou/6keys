---
title: "B_Code Index and Installation Guide"
date: 2025-06-28
language: en-US
encoding: UTF-8
---

# Appendix B　Code Index and Installation Guide

This appendix provides a complete code index, installation guide, and usage instructions for the Six Keys Criticality framework. All code is released under **BSD 3-Clause** license, and paper content is licensed under **CC BY-NC 4.0**.

**GitHub Repository**: https://github.com/isyanghou/6Keys  
**Author**: You Yang Hou (isyanghou@gmail.com)  
**ORCID**: 0009-0000-7041-8574

## B.1 Project Structure Overview

```
sixkeys/
│
├── sixkeys/                    # Core Python package
│   ├── __init__.py             # Package initialization
│   ├── core/                   # Six core indicators implementation
│   │   ├── felc.py            # FELC (ζ₁) - Free Energy Limit Cycle
│   │   ├── teb.py             # TEB (ζ₂) - Thermodynamic Efficiency Balance
│   │   ├── rfi.py             # RFI (ζ₃) - Ricci Flow Index
│   │   ├── ecgp.py            # ECGP (ζ₄) - Effective Causal Graph Percolation
│   │   ├── pwc.py             # PWC (ζ₅) - Phase-space Winding Circulation
│   │   └── aci.py             # ACI (ζ₆) - Astrocyte Coupling Index
│   ├── analysis/               # Analysis tools
│   │   ├── analyzer.py        # Main analyzer class
│   │   ├── cross_validation.py # Cross-validation implementation
│   │   └── public_data.py     # Public data reanalysis
│   ├── utils/                  # Utility functions
│   │   ├── data_io.py         # Data input/output
│   │   ├── preprocessing.py   # Data preprocessing
│   │   ├── visualization.py   # Visualization tools
│   │   └── metrics.py         # Evaluation metrics
│   └── demos/                  # Demo modules
│       ├── radar_chart.py     # Radar chart visualization
│       ├── cross_validation.py # Cross-validation demo
│       └── public_data_analysis.py # Public data analysis demo
│
├── docs/                       # Documentation system
│   ├── zh/                    # Chinese documentation
│   │   ├── installation.md    # Installation guide
│   │   ├── quickstart.md      # Quick start
│   │   ├── theory.md          # Theory background
│   │   └── faq.md             # FAQ
│   ├── en/                    # English documentation
│   │   ├── installation.md    # Installation Guide
│   │   ├── quickstart.md      # Quick Start
│   │   ├── theory.md          # Theory Background
│   │   └── faq.md             # FAQ
│   └── api/                   # API reference documentation
│
├── examples/                   # Usage examples
│   ├── basic_usage.py         # Basic usage example
│   └── demo_visualization.py  # Visualization demo
│
├── notebooks/                  # Jupyter notebooks
│   └── 01_basic_usage.ipynb   # Basic usage tutorial
│
├── scripts/                    # Script tools
│   └── analyze.py             # Analysis script
│
├── tests/                      # Test suite
│   └── test_core/             # Core module tests
│       ├── test_felc.py       # FELC tests
│       └── test_all_indicators.py # All indicators tests
│
├── data/                       # Data directory
├── results/                    # Results output directory
│
├── pyproject.toml             # Project configuration
├── requirements.txt           # Python dependencies
├── environment.yml            # Conda environment configuration
├── Dockerfile                 # Docker container configuration
├── docker-compose.yml         # Docker Compose configuration
├── setup.py                   # Installation script
├── setup.cfg                  # Installation configuration
├── MANIFEST.in                # Package manifest
├── CITATION.cff               # Citation format
├── CONTRIBUTING.md            # Contribution guide
├── CHANGELOG.md               # Change log
├── LICENSE                    # BSD 3-Clause license
├── LICENSE-PAPER              # CC BY-NC 4.0 license
└── README.md                  # Project description
```

## B.2 Installation Guide

### B.2.1 System Requirements

- **Python**: 3.8 or higher
- **Operating System**: Windows, macOS, Linux
- **Memory**: 8GB or more recommended
- **Disk Space**: At least 2GB available space

### B.2.2 Installation Methods

#### Method 1: PyPI Installation (Recommended)

```bash
# Basic installation
pip install sixkeys

# Full installation (including all optional dependencies)
pip install "sixkeys[all]"

# Development version installation
pip install "sixkeys[dev]"
```

#### Method 2: Conda Environment Installation

```bash
# Download project
git clone https://github.com/isyanghou/6Keys.git
cd 6Keys

# Create and activate Conda environment
conda env create -f environment.yml
conda activate sixkeys

# Install package
pip install -e .
```

#### Method 3: Docker Container Deployment

```bash
# Pull Docker image
docker pull sixkeys/sixkeys:latest

# Or use Docker Compose
docker-compose up jupyter  # Start Jupyter Lab
docker-compose up analysis  # Start analysis service
```

#### Method 4: Source Code Installation

```bash
# Clone repository
git clone https://github.com/isyanghou/6Keys.git
cd 6Keys

# Install dependencies
pip install -r requirements.txt

# Development mode installation
pip install -e ".[dev]"
```

### B.2.3 Installation Verification

```python
import sixkeys as sk

# Check version
print(f"Six Keys version: {sk.__version__}")

# Quick test
analyzer = sk.SixKeysAnalyzer()
result = analyzer.analyze_simulated_data(duration=1.0)
print(f"Installation successful! Test result D_w = {result.d_total:.3f}")
```

## B.3 Core Module Description

### B.3.1 Six Core Indicators (sixkeys.core)

#### FELC - Free Energy Limit Cycle (ζ₁)
```python
from sixkeys.core import FELC

felc = FELC(theta_c=1.0)
zeta1 = felc.compute(neural_data, time_window=2.0)
```

#### TEB - Thermodynamic Efficiency Balance (ζ₂)
```python
from sixkeys.core import TEB

teb = TEB()
zeta2 = teb.compute(neural_data, metabolic_data)
```

#### RFI - Ricci Flow Index (ζ₃)
```python
from sixkeys.core import RFI

rfi = RFI()
zeta3 = rfi.compute(connectivity_matrix)
```

#### ECGP - Effective Causal Graph Percolation (ζ₄)
```python
from sixkeys.core import ECGP

ecgp = ECGP()
zeta4 = ecgp.compute(time_series_data)
```

#### PWC - Phase-space Winding Circulation (ζ₅)
```python
from sixkeys.core import PWC

pwc = PWC()
zeta5 = pwc.compute(phase_data)
```

#### ACI - Astrocyte Coupling Index (ζ₆)
```python
from sixkeys.core import ACI

aci = ACI()
zeta6 = aci.compute(neural_data, astrocyte_data)
```

### B.3.2 Analysis Tools (sixkeys.analysis)

#### Main Analyzer
```python
from sixkeys.analysis import SixKeysAnalyzer

# Create analyzer
analyzer = SixKeysAnalyzer(
    theta_c=1.0,
    random_state=42,
    n_jobs=-1  # Use all CPU cores
)

# Analyze real data
result = analyzer.analyze_real_data(
    data_path="path/to/data.npy",
    sampling_rate=1000,
    consciousness_state="awake"
)

# Analyze simulated data
result = analyzer.analyze_simulated_data(
    consciousness_state="light_sedation",
    duration=5.0,
    noise_level=0.1
)
```

#### Cross Validation
```python
from sixkeys.analysis import CrossValidation

cv = CrossValidation(n_folds=5, random_state=42)
scores = cv.validate_model(data, labels)
```

#### Public Data Reanalysis
```python
from sixkeys.analysis import PublicDataAnalysis

pda = PublicDataAnalysis()
results = pda.analyze_dataset("ds002345")  # OpenNeuro dataset
```

### B.3.3 Utility Functions (sixkeys.utils)

#### Data Processing
```python
from sixkeys.utils import preprocessing, data_io

# Data preprocessing
clean_data = preprocessing.filter_signal(raw_data, fs=1000)
normalized_data = preprocessing.normalize(clean_data)

# Data input/output
data_io.save_results(results, "output.json")
loaded_results = data_io.load_results("output.json")
```

#### Visualization
```python
from sixkeys.utils import visualization

# Radar chart
fig = visualization.plot_radar_chart(results)

# Time series plot
fig = visualization.plot_time_series(data, indicators)

# Phase diagram
fig = visualization.plot_phase_diagram(results)
```

### B.3.4 Demo Modules (sixkeys.demos)

```python
# Radar chart demo
from sixkeys.demos import radar_chart
radar_chart.run_demo()

# Cross validation demo
from sixkeys.demos import cross_validation
cross_validation.run_demo()

# Public data analysis demo
from sixkeys.demos import public_data_analysis
public_data_analysis.run_demo()
```

## B.4 Usage Examples

### B.4.1 Basic Usage Flow

```python
import sixkeys as sk
import numpy as np
import matplotlib.pyplot as plt

# 1. Create analyzer
analyzer = sk.SixKeysAnalyzer(theta_c=1.0, random_state=42)

# 2. Analyze different consciousness states
states = ['awake', 'light_sedation', 'deep_anesthesia']
results = {}

for state in states:
    result = analyzer.analyze_simulated_data(
        consciousness_state=state,
        duration=5.0,  # 5 seconds of data
        sampling_rate=1000
    )
    results[state] = result
    print(f"{state}: D_w = {result.d_total:.3f}")

# 3. Visualize results
fig = analyzer.plot_radar_chart(results)
plt.title("Six Keys Criticality Analysis Results")
plt.show()

# 4. Save results
analyzer.save_results(results, "analysis_results.json")
```

### B.4.2 Advanced Analysis

```python
# Batch analysis
from sixkeys.analysis import BatchAnalyzer

batch = BatchAnalyzer()
results = batch.analyze_directory(
    data_dir="/path/to/data",
    output_dir="/path/to/results",
    file_pattern="*.npy"
)

# Statistical analysis
from sixkeys.utils import metrics

stats = metrics.compute_statistics(results)
print(f"Average D_w: {stats['d_total']['mean']:.3f}")
print(f"Standard deviation: {stats['d_total']['std']:.3f}")
```

## B.5 Testing and Validation

### B.5.1 Running Tests

```bash
# Run all tests
pytest tests/

# Run specific tests
pytest tests/test_core/test_felc.py -v

# Generate test coverage report
pytest --cov=sixkeys tests/
```

### B.5.2 Performance Benchmarks

```python
from sixkeys.utils import benchmarks

# Run performance tests
results = benchmarks.run_performance_tests()
print(f"Average processing time: {results['avg_time']:.2f} seconds")
```

## B.6 Development and Contribution

### B.6.1 Development Environment Setup

```bash
# Clone repository
git clone https://github.com/isyanghou/6Keys.git
cd 6Keys

# Install development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### B.6.2 Code Style

```bash
# Code formatting
black sixkeys/

# Code linting
ruff check sixkeys/

# Type checking
mypy sixkeys/
```

### B.6.3 Contribution Process

1. **Fork Project**: Fork this project on GitHub
2. **Create Branch**: `git checkout -b feature/new-feature`
3. **Develop Feature**: Implement new feature and add tests
4. **Run Tests**: Ensure all tests pass
5. **Commit Changes**: `git commit -m "Add new feature"`
6. **Push Branch**: `git push origin feature/new-feature`
7. **Create PR**: Create Pull Request on GitHub

## B.7 Troubleshooting

### B.7.1 Common Issues

**Q: Dependency conflicts during installation**
```bash
# Use virtual environment
python -m venv sixkeys_env
source sixkeys_env/bin/activate  # Linux/Mac
# or
sixkeys_env\Scripts\activate  # Windows
pip install sixkeys
```

**Q: Computation too slow**
```python
# Use multi-core processing
analyzer = sk.SixKeysAnalyzer(n_jobs=-1)

# Or reduce data length
result = analyzer.analyze_simulated_data(duration=1.0)  # Reduce to 1 second
```

**Q: Out of memory**
```python
# Process large data in batches
from sixkeys.utils import data_io

for batch in data_io.batch_loader(large_dataset, batch_size=1000):
    result = analyzer.analyze_batch(batch)
```

### B.7.2 Getting Help

- **GitHub Issues**: https://github.com/isyanghou/6Keys/issues
- **Documentation**: https://sixkeys.readthedocs.io/
- **Email**: isyanghou@gmail.com

## B.8 License and Citation

### B.8.1 License Terms

- **Code**: BSD 3-Clause License
- **Paper Content**: CC BY-NC 4.0 International License

### B.8.2 Citation Format

```bibtex
@software{hou2025sixkeys,
  title = {Six Keys Criticality: A Neural Consciousness Analysis Framework},
  author = {You Yang Hou},
  year = {2025},
  url = {https://github.com/isyanghou/6Keys},
  note = {Version 0.1.0}
}
```

---

## Conclusion

The Six Keys Criticality framework provides a unified, open analysis tool for neuroscience and consciousness research. We welcome participation and contributions from the research community to advance this field together.

**Start Your Exploration Journey**:
```bash
pip install sixkeys
python -c "import sixkeys; print('Welcome to Six Keys Criticality Framework!')"
```

For more detailed information, please refer to our [GitHub Repository](https://github.com/isyanghou/6Keys) and [Complete Documentation](https://sixkeys.readthedocs.io/).