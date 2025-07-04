# Quick Start Guide

**📍 Navigation**: [🏠 Home](../../README.md) > [📚 Documentation Hub](README.md) > **🚀 Quick Start**

**⏱️ Estimated Reading Time**: 10-15 minutes | **🎯 Difficulty**: Beginner | **🎯 Goal**: Get up and running with Six Keys Criticality

---

## 🎯 **What You'll Learn**

By the end of this guide, you'll be able to:
- ✅ Install and verify Six Keys Criticality
- ✅ Run your first analysis
- ✅ Understand the six core indicators
- ✅ Visualize results with charts
- ✅ Process your own neural data

---

## 🚨 **Quick Rescue**

**Need immediate help?**

| Problem | Quick Solution | Link |
|---------|----------------|------|
| 🔧 **Installation Issues** | Check installation guide | [Installation Guide](installation.md) |
| ❓ **Error Messages** | Check common problems | [FAQ](faq.md) |
| 📊 **Data Format** | See data requirements | [Data Processing Guide](../data-processing.md) |
| 🎨 **Visualization** | Learn plotting basics | [Visualization Tutorial](visualization.md) |

This guide will help you get started with the Six Keys Criticality framework quickly.

## Prerequisites

- Python 3.8 or higher
- Basic understanding of neural data analysis
- Familiarity with NumPy and Matplotlib (optional but helpful)

## Installation Verification

After installation, verify that everything works correctly:

```python
import sixkeys as sk
print(f"Six Keys version: {sk.__version__}")

# Quick functionality test
analyzer = sk.SixKeysAnalyzer()
result = analyzer.analyze_simulated_data(duration=1.0)
print(f"Test completed successfully: D_w = {result.d_total:.3f}")
```

## Basic Usage

### 1. Import the Library

```python
import sixkeys as sk
import matplotlib.pyplot as plt
import numpy as np
```

### 2. Create an Analyzer

```python
# Create analyzer with default parameters
analyzer = sk.SixKeysAnalyzer()

# Or with custom parameters
analyzer = sk.SixKeysAnalyzer(
    theta_c=1.0,        # Critical threshold
    random_state=42     # For reproducible results
)
```

### 3. Analyze Simulated Data

```python
# Analyze different consciousness states
states = ['awake', 'light_sedation', 'deep_anesthesia']
results = {}

for state in states:
    result = analyzer.analyze_simulated_data(
        consciousness_state=state,
        duration=5.0,  # 5 seconds of simulation
        dt=0.01        # Time step
    )
    results[state] = result
    print(f"{state}: D_w = {result.d_total:.3f}, State = {result.predicted_state}")
```

### 4. Visualize Results

#### Radar Chart
```python
# Create radar chart for all states
fig = analyzer.plot_radar_chart(results)
plt.title('Six Keys Criticality Analysis')
plt.show()
```

#### Phase Diagram
```python
# Create phase diagram
fig = analyzer.plot_phase_diagram(results)
plt.show()
```

## Individual Indicator Analysis

You can also analyze individual indicators:

### FELC (Free Energy Limit Cycle)
```python
from sixkeys.core import FELC

felc = FELC(sim_time=10.0, dt=0.01)
felc_results = felc.analyze_states()
felc.plot_results(felc_results)
plt.show()
```

### TEB (Thermodynamic Efficiency Balance)
```python
from sixkeys.core import TEB

teb = TEB(sim_time=10.0, dt=0.01)
teb_results = teb.analyze_states()
teb.plot_results(teb_results)
plt.show()
```

## Working with Real Data

### Data Format
Your neural data should be in the format:
- **Shape**: `(n_timepoints, n_channels)`
- **Type**: NumPy array or similar
- **Sampling rate**: Consistent with your analysis parameters

```python
# Example with your own data
# data = load_your_neural_data()  # Shape: (n_timepoints, n_channels)

# For demonstration, we'll use simulated data
data = np.random.randn(5000, 64)  # 5000 timepoints, 64 channels

# Analyze the data
result = analyzer.analyze_data(data, dt=0.001)  # 1ms time step
print(f"Analysis result: D_w = {result.d_total:.3f}")
print(f"Predicted state: {result.predicted_state}")
```

## Batch Processing

```python
# Process multiple datasets
datasets = {
    'subject_1': data1,
    'subject_2': data2,
    'subject_3': data3
}

batch_results = {}
for subject, data in datasets.items():
    result = analyzer.analyze_data(data)
    batch_results[subject] = result
    print(f"{subject}: D_w = {result.d_total:.3f}")

# Visualize batch results
fig = analyzer.plot_radar_chart(batch_results)
plt.show()
```

## Custom Parameter Configuration

### Adjusting Weights
```python
# Custom weights for the six indicators
custom_weights = {
    'zeta1': 0.25,  # FELC
    'zeta2': 0.20,  # TEB
    'zeta3': 0.15,  # RFI
    'zeta4': 0.15,  # ECGP
    'zeta5': 0.15,  # PWC
    'zeta6': 0.10   # ACI
}

analyzer = sk.SixKeysAnalyzer(
    theta_c=0.8,
    weights=custom_weights
)
```

### Adjusting Individual Indicators
```python
# Custom FELC parameters
felc_params = {
    'sim_time': 20.0,
    'dt': 0.005,
    'n_samples': 100,
    'inband_threshold': 0.1,
    'cv_threshold': 0.05
}

analyzer = sk.SixKeysAnalyzer(felc_params=felc_params)
```

## Advanced Visualization

### Time Series Analysis
```python
# Analyze temporal evolution
time_results = []
for t in np.linspace(0, 10, 21):  # 21 time points over 10 seconds
    result = analyzer.analyze_simulated_data(
        consciousness_state='light_sedation',
        duration=1.0,
        noise_level=0.1 + 0.05 * t  # Increasing noise over time
    )
    time_results.append(result)

# Plot temporal evolution
d_values = [r.d_total for r in time_results]
plt.figure(figsize=(10, 6))
plt.plot(np.linspace(0, 10, 21), d_values, 'o-')
plt.axhline(y=analyzer.theta_c, color='r', linestyle='--', label='Critical threshold')
plt.xlabel('Time (s)')
plt.ylabel('D_w')
plt.title('Temporal Evolution of Criticality')
plt.legend()
plt.grid(True)
plt.show()
```

### Statistical Comparison
```python
import seaborn as sns

# Generate multiple samples for statistical analysis
n_samples = 50
states = ['awake', 'light_sedation', 'deep_anesthesia']
statistical_data = []

for state in states:
    for i in range(n_samples):
        result = analyzer.analyze_simulated_data(
            consciousness_state=state,
            duration=2.0,
            random_state=i  # Different random seed for each sample
        )
        statistical_data.append({
            'state': state,
            'D_w': result.d_total,
            'zeta1': result.zeta1,
            'zeta2': result.zeta2,
            'zeta3': result.zeta3,
            'zeta4': result.zeta4,
            'zeta5': result.zeta5,
            'zeta6': result.zeta6
        })

# Convert to DataFrame for easy plotting
import pandas as pd
df = pd.DataFrame(statistical_data)

# Box plot comparison
plt.figure(figsize=(12, 8))
sns.boxplot(data=df, x='state', y='D_w')
plt.title('Statistical Comparison of D_w Across States')
plt.ylabel('Weighted Distance (D_w)')
plt.show()
```

## Saving and Loading Configurations

### Save Configuration
```python
# Save current analyzer configuration
analyzer.save_config('my_analysis_config.yaml')
```

### Load Configuration
```python
# Load saved configuration
analyzer = sk.SixKeysAnalyzer.from_config('my_analysis_config.yaml')
```

## Exporting Results

### JSON Export
```python
# Export results to JSON
result.to_json('analysis_results.json')
```

### CSV Export
```python
# Export batch results to CSV
results_df = pd.DataFrame([
    {
        'subject': name,
        'D_w': result.d_total,
        'state': result.predicted_state,
        **{f'zeta{i+1}': getattr(result, f'zeta{i+1}') for i in range(6)}
    }
    for name, result in batch_results.items()
])
results_df.to_csv('batch_analysis_results.csv', index=False)
```

### MATLAB Export
```python
from scipy.io import savemat

# Export for MATLAB analysis
matlab_data = {
    'D_w': [result.d_total for result in batch_results.values()],
    'zeta_values': np.array([[getattr(result, f'zeta{i+1}') for i in range(6)] 
                            for result in batch_results.values()]),
    'states': [result.predicted_state for result in batch_results.values()]
}
savemat('sixkeys_results.mat', matlab_data)
```

## Next Steps

1. **Explore the API Reference**: Check out the [API documentation](../api/) for detailed parameter descriptions
2. **Try the Examples**: Look at the [examples](../../examples/) directory for more complex use cases
3. **Read the Theory**: Understand the mathematical foundation in our [theory documentation](theory.md)
4. **Join the Community**: Contribute to the project or ask questions on our [GitHub repository](https://github.com/yourusername/sixkeys)

## Getting Help

- **Documentation**: Browse the full documentation at [docs/](../)
- **Examples**: Check practical examples in [examples/](../../examples/)
- **Issues**: Report bugs or request features on [GitHub Issues](https://github.com/yourusername/sixkeys/issues)
- **Discussions**: Join community discussions on [GitHub Discussions](https://github.com/yourusername/sixkeys/discussions)

## Common Troubleshooting

### Import Errors
```python
# If you get import errors, check your installation
try:
    import sixkeys
    print("✓ Six Keys imported successfully")
except ImportError as e:
    print(f"✗ Import error: {e}")
    print("Try: pip install --upgrade sixkeys")
```

### Memory Issues
```python
# For large datasets, process in chunks
def analyze_large_dataset(data, chunk_size=1000):
    results = []
    for i in range(0, len(data), chunk_size):
        chunk = data[i:i+chunk_size]
        result = analyzer.analyze_data(chunk)
        results.append(result)
    return results
```

### Performance Optimization
```python
# Use multiprocessing for batch analysis
from multiprocessing import Pool

def analyze_single(args):
    data, params = args
    analyzer = sk.SixKeysAnalyzer(**params)
    return analyzer.analyze_data(data)

# Parallel processing
with Pool() as pool:
    args = [(data, params) for data in datasets]
    results = pool.map(analyze_single, args)
```

---

## 🎉 **Quick Start Complete! What's Next?**

**Choose your path based on your needs:**

### 🧠 **Dive Deeper into Theory**
- [📖 Theoretical Background](theory.md) - Understand the science behind the six indicators
- [📚 Complete Academic Paper](paper/) - Read the full research paper
- [🧮 Mathematical Foundations](paper/A-0_Mathematical_Derivations.md) - Explore detailed mathematical proofs

### 👨‍💻 **Develop Custom Solutions**
- [📚 API Reference](../api/) - Complete technical documentation
- [🔧 Developer Guide](../developers.md) - Set up development environment
- [🏗️ Project Structure](../project-structure.md) - Understand the codebase

### 🔬 **Design Experiments**
- [🧪 Experiment Guide](experiments.md) - Research methodology and design
- [📊 Visualization Tutorial](visualization.md) - Advanced plotting techniques
- [📈 Statistical Analysis](paper/08_Statistical_Analysis_and_Validation.md) - Validation methods

### 📚 **Learning Resources**
- [❓ FAQ](faq.md) - Common questions and troubleshooting
- [🎮 Interactive Examples](../../examples/) - Hands-on demonstrations
- [📖 Best Practices](../best-practices.md) - Tips for effective analysis

---

## 📚 **Navigation Bar**

### 📍 **Current Location**
**Documentation Hub** > **Quick Start Guide**

### 🔗 **Related Pages**
- [⚙️ Installation Guide](installation.md) - Detailed setup instructions
- [❓ FAQ](faq.md) - Common questions and solutions
- [🧠 Theory Background](theory.md) - Understand the foundations
- [📚 Documentation Hub](README.md) - Return to main documentation

### 🆘 **Help & Support**
- [❓ **Common Questions**](faq.md) - Quick answers to frequent issues
- [💬 **Technical Support**](mailto:isyanghou@gmail.com) - Direct assistance
- [🐛 **GitHub Issues**](https://github.com/isyanghou/6Keys/issues) - Report bugs or request features
- [💭 **GitHub Discussions**](https://github.com/isyanghou/6Keys/discussions) - Community forum

### 🌐 **Other Resources**
- [🇨🇳 **Chinese Version**](../zh/quickstart.md) - 中文版快速开始
- [🏠 **Project Home**](../../README.md) - Main project page
- [📚 **Complete Documentation**](../) - Full documentation index