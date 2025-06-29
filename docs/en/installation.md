# Installation Guide

This guide will help you install and configure the Six Keys Criticality framework in different environments.

## 📝 Project Information

**Author**: You Yang Hou  
**Email**: [isyanghou@gmail.com](mailto:isyanghou@gmail.com)  
**ORCID**: [0009-0000-7041-8574](https://orcid.org/0009-0000-7041-8574)  
**Repository**: [https://github.com/isyanghou/6Keys](https://github.com/isyanghou/6Keys)  
**License**: Paper content under CC BY-NC 4.0, Code under BSD 3-Clause

## 📋 System Requirements

### Basic Requirements
- **Python**: 3.8 or higher
- **Operating System**: Windows 10+, macOS 10.14+, Linux (Ubuntu 18.04+)
- **Memory**: 8GB or more recommended
- **Storage**: At least 2GB available space

### Recommended Configuration
- **Python**: 3.9+ (optimal performance)
- **Memory**: 16GB or more (for large datasets)
- **GPU**: CUDA-compatible NVIDIA GPU (optional, for accelerated computing)

## 🚀 Installation Methods

### Method 1: Install from PyPI (Recommended)

```bash
# Basic installation
pip install sixkeys

# Full installation with all optional dependencies
pip install "sixkeys[all]"

# Development installation only
pip install "sixkeys[dev]"
```

### Method 2: Install from Source

```bash
# Clone repository
git clone https://github.com/yourusername/sixkeys.git
cd sixkeys

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install package
pip install -e .

# Or install development version
pip install -e ".[dev]"
```

### Method 3: Using Conda

```bash
# Create new conda environment
conda create -n sixkeys python=3.9
conda activate sixkeys

# Install dependencies
conda install numpy scipy matplotlib pandas scikit-learn
pip install sixkeys
```

## 🔧 Environment Configuration

### 1. Virtual Environment Setup (Highly Recommended)

```bash
# Using venv
python -m venv sixkeys_env
source sixkeys_env/bin/activate  # Linux/macOS
# or
sixkeys_env\Scripts\activate     # Windows

# Using conda
conda create -n sixkeys python=3.9
conda activate sixkeys
```

### 2. Dependency Management

The project uses the following core dependencies:

```txt
numpy>=1.21.0          # Numerical computing
scipy>=1.7.0           # Scientific computing
matplotlib>=3.5.0      # Basic plotting
seaborn>=0.11.0        # Statistical plotting
pandas>=1.3.0          # Data manipulation
scikit-learn>=1.0.0    # Machine learning
networkx>=2.6          # Network analysis
numba>=0.56.0          # Numerical optimization
statsmodels>=0.13.0    # Statistical analysis
tqdm>=4.62.0           # Progress bars
pyyaml>=6.0            # Configuration files
```

### 3. Optional Dependencies

```bash
# Neuroimaging data support
pip install nibabel mne

# Advanced visualization
pip install plotly bokeh

# Jupyter support
pip install jupyter ipywidgets

# Testing and development tools
pip install pytest pytest-cov black flake8 mypy
```

## ✅ Installation Verification

### Basic Functionality Test

```python
# Test import
import sixkeys as sk
print(f"Six Keys version: {sk.__version__}")

# Test core modules
from sixkeys.core import FELC, TEB, RFI, ECGP, PWC, ACI
print("All core modules imported successfully!")

# Quick functionality test
analyzer = sk.SixKeysAnalyzer()
results = analyzer.analyze_simulated_data(duration=1.0)
print(f"Simulation analysis completed, D_w = {results.d_total:.3f}")
```

### Run Test Suite

```bash
# Run all tests
pytest tests/

# Run specific tests
pytest tests/test_felc.py -v

# Check code coverage
pytest --cov=sixkeys tests/
```

## 🐛 Common Issues

### Issue 1: ImportError: No module named 'sixkeys'

**Solution:**
```bash
# Confirm installation
pip list | grep sixkeys

# Reinstall
pip uninstall sixkeys
pip install sixkeys
```

### Issue 2: NumPy/SciPy Version Conflicts

**Solution:**
```bash
# Update to compatible versions
pip install --upgrade numpy scipy

# Or use conda to manage scientific packages
conda install numpy scipy matplotlib
```

### Issue 3: Compilation Errors on Windows

**Solution:**
```bash
# Install Microsoft C++ Build Tools
# Or use pre-compiled wheels
pip install --only-binary=all sixkeys
```

### Issue 4: Out of Memory Errors

**Solutions:**
- Reduce dataset size
- Use batch processing mode
- Increase virtual memory
- Use more efficient data types

## 🔄 Updates and Uninstallation

### Update to Latest Version

```bash
# Update sixkeys
pip install --upgrade sixkeys

# Check version
python -c "import sixkeys; print(sixkeys.__version__)"
```

### Complete Uninstallation

```bash
# Uninstall package
pip uninstall sixkeys

# Clear cache
pip cache purge

# Remove virtual environment (if used)
rm -rf sixkeys_env  # Linux/macOS
# or
rmdir /s sixkeys_env  # Windows
```

## 📞 Getting Help

If you encounter installation issues:

1. Check [FAQ](faq.md)
2. Search [GitHub Issues](https://github.com/yourusername/sixkeys/issues)
3. Create a new issue with:
   - Operating system and version
   - Python version
   - Complete error message
   - Installation commands and steps

## 🎯 Next Steps

After installation, we recommend:

1. Read the [Quick Start Guide](quickstart.md)
2. Check out [Basic Tutorial](tutorials/basic_tutorial.md)
3. Run [Example Code](examples/)
4. Explore [API Documentation](api_reference.md)

---

**Tip**: We recommend installing in a virtual environment to avoid conflicts with other projects' dependencies.