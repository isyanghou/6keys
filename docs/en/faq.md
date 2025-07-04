# Frequently Asked Questions (FAQ)

**📍 Navigation**: [🏠 Home](../../README.md) > [📚 Documentation Hub](README.md) > **❓ FAQ**

---

## 🔍 **Quick Find**

**Looking for something specific?**

| Category | Quick Links |
|----------|-------------|
| 🔧 **Installation** | [Dependency Conflicts](#q1-how-to-resolve-dependency-conflicts-during-installation) \| [Conda Setup](#q2-how-to-install-in-a-conda-environment) \| [Import Issues](#q3-what-to-do-if-import-fails-after-installation) |
| 🎯 **Usage** | [Parameter Selection](#q4-how-to-choose-appropriate-parameters) \| [Data Format](#q5-what-are-the-data-format-requirements) \| [Missing Data](#q6-how-to-handle-missing-data) |
| 📊 **Results** | [Interpretation](#q7-how-to-interpret-analysis-results) \| [Visualization](#visualization-issues) \| [Export](#export-issues) |
| 🚨 **Troubleshooting** | [Performance](#performance-issues) \| [Memory](#memory-issues) \| [Errors](#common-errors) |

---

## 🚨 **Emergency Rescue**

**Stuck? Get immediate help:**

| Problem | Solution | Link |
|---------|----------|------|
| 🔧 **Can't Install** | Step-by-step installation guide | [Installation Guide](installation.md) |
| ❌ **Getting Errors** | Common error solutions | [Error Troubleshooting](#common-errors) |
| 📊 **Data Problems** | Data format and processing help | [Data Processing Guide](../data-processing.md) |
| 🚀 **Need Quick Start** | Get running in 5 minutes | [Quick Start Guide](quickstart.md) |

This document answers common questions when using the Six Keys Criticality framework.

## Installation Issues

### Q1: How to resolve dependency conflicts during installation?

**A:** We recommend using virtual environments to avoid dependency conflicts:

```bash
# Create virtual environment
python -m venv sixkeys_env

# Activate environment (Windows)
sixkeys_env\Scripts\activate

# Activate environment (macOS/Linux)
source sixkeys_env/bin/activate

# Install Six Keys
pip install sixkeys
```

### Q2: How to install in a Conda environment?

**A:** We recommend using the provided environment configuration file:

```bash
# Use environment configuration file
conda env create -f environment.yml
conda activate sixkeys

# Or manually create environment
conda create -n sixkeys python=3.9
conda activate sixkeys
pip install sixkeys
```

### Q3: What to do if import fails after installation?

**A:** Check if installation was successful:

```python
# Check installation
try:
    import sixkeys as sk
    print(f"✓ Installation successful, version: {sk.__version__}")
except ImportError as e:
    print(f"✗ Import failed: {e}")
    print("Try reinstalling: pip install --upgrade sixkeys")
```

## Usage Issues

### Q4: How to choose appropriate parameters?

**A:** Parameter selection recommendations:

```python
# For real-time analysis (speed priority)
fast_analyzer = sk.SixKeysAnalyzer(
    felc_params={'sim_time': 5.0, 'n_samples': 25},
    teb_params={'sim_time': 5.0, 'n_samples': 25}
)

# For accurate analysis (precision priority)
accurate_analyzer = sk.SixKeysAnalyzer(
    felc_params={'sim_time': 20.0, 'n_samples': 100},
    teb_params={'sim_time': 20.0, 'n_samples': 100}
)

# For specific application scenarios
clinical_analyzer = sk.SixKeysAnalyzer(
    theta_c=0.8,  # More sensitive threshold
    weights={'zeta1': 0.3, 'zeta2': 0.3, 'zeta3': 0.1, 
             'zeta4': 0.1, 'zeta5': 0.1, 'zeta6': 0.1}
)
```

### Q5: What are the data format requirements?

**A:** Data format requirements:

```python
import numpy as np

# Correct data format
# Shape: (n_timepoints, n_channels)
data = np.random.randn(5000, 64)  # 5000 timepoints, 64 channels

# Check data format
def check_data_format(data):
    if not isinstance(data, np.ndarray):
        raise TypeError("Data must be a NumPy array")
    
    if data.ndim != 2:
        raise ValueError("Data must be a 2D array (timepoints, channels)")
    
    if data.shape[0] < 100:
        print("Warning: Few timepoints may affect analysis precision")
    
    if data.shape[1] < 8:
        print("Warning: Few channels may affect analysis stability")
    
    print(f"✓ Data format correct: {data.shape[0]} timepoints, {data.shape[1]} channels")

check_data_format(data)
```

### Q6: How to handle missing data?

**A:** Missing data handling methods:

```python
import numpy as np
from scipy import interpolate

def handle_missing_data(data, method='interpolate'):
    """
    Handle missing data
    
    Parameters:
    -----------
    data : np.ndarray
        Original data, NaN indicates missing values
    method : str
        Handling method: 'interpolate', 'remove', 'zero_fill'
    """
    if method == 'interpolate':
        # Linear interpolation
        for ch in range(data.shape[1]):
            mask = ~np.isnan(data[:, ch])
            if np.sum(mask) > 1:
                f = interpolate.interp1d(
                    np.where(mask)[0], data[mask, ch], 
                    kind='linear', fill_value='extrapolate'
                )
                data[:, ch] = f(np.arange(len(data)))
    
    elif method == 'remove':
        # Remove timepoints with missing values
        mask = ~np.isnan(data).any(axis=1)
        data = data[mask]
    
    elif method == 'zero_fill':
        # Fill with zeros
        data = np.nan_to_num(data, nan=0.0)
    
    return data

# Usage example
data_with_nan = np.random.randn(1000, 32)
data_with_nan[100:110, 5] = np.nan  # Simulate missing data

clean_data = handle_missing_data(data_with_nan, method='interpolate')
analyzer = sk.SixKeysAnalyzer()
result = analyzer.analyze_data(clean_data)
```

### Q7: How to interpret analysis results?

**A:** Result interpretation guide:

```python
def interpret_results(result):
    """
    Interpret analysis results
    """
    print(f"=== Six Keys Criticality Analysis Results ===")
    print(f"Total Distance D_w: {result.d_total:.3f}")
    print(f"Predicted State: {result.predicted_state}")
    print(f"Critical Threshold: {result.theta_c:.3f}")
    print()
    
    # Indicator explanations
    indicators = {
        'zeta1': 'FELC (Free Energy Limit Cycle)',
        'zeta2': 'TEB (Thermodynamic Efficiency Balance)',
        'zeta3': 'RFI (Ricci Flow Index)',
        'zeta4': 'ECGP (Effective Causal Graph Percolation)',
        'zeta5': 'PWC (Phase-Wrapped Circulation)',
        'zeta6': 'ACI (Astrocyte-Coupling Index)'
    }
    
    print("Indicator Values:")
    for key, name in indicators.items():
        value = getattr(result, key)
        print(f"  {name}: {value:.3f}")
    print()
    
    # State interpretation
    if result.predicted_state == 'awake':
        print("Interpretation: System is in awake state, indicators near normal range")
    elif result.predicted_state == 'light_sedation':
        print("Interpretation: System is in light sedation, some indicators deviate from normal")
    elif result.predicted_state == 'deep_anesthesia':
        print("Interpretation: System is in deep anesthesia, most indicators significantly deviate")
    
    # Criticality assessment
    if result.d_total < result.theta_c * 0.5:
        print("Criticality: Low - System is stable")
    elif result.d_total < result.theta_c:
        print("Criticality: Medium - System approaching critical point")
    else:
        print("Criticality: High - System in critical transition state")

# Usage example
analyzer = sk.SixKeysAnalyzer()
result = analyzer.analyze_simulated_data('light_sedation')
interpret_results(result)
```

## Performance Issues

### Q8: What to do if analysis is too slow?

**A:** Performance optimization suggestions:

```python
# 1. Reduce simulation time
fast_params = {
    'sim_time': 5.0,    # Reduce from default 10.0 to 5.0
    'n_samples': 25,    # Reduce from default 50 to 25
    'dt': 0.02          # Increase from default 0.01 to 0.02
}

fast_analyzer = sk.SixKeysAnalyzer(
    felc_params=fast_params,
    teb_params=fast_params,
    rfi_params=fast_params,
    ecgp_params=fast_params,
    pwc_params=fast_params,
    aci_params=fast_params
)

# 2. Parallel processing for multiple datasets
from multiprocessing import Pool
import time

def analyze_single_dataset(data):
    analyzer = sk.SixKeysAnalyzer()
    return analyzer.analyze_data(data)

# Serial processing
start_time = time.time()
serial_results = [analyze_single_dataset(data) for data in datasets]
serial_time = time.time() - start_time

# Parallel processing
start_time = time.time()
with Pool() as pool:
    parallel_results = pool.map(analyze_single_dataset, datasets)
parallel_time = time.time() - start_time

print(f"Serial processing time: {serial_time:.2f} seconds")
print(f"Parallel processing time: {parallel_time:.2f} seconds")
print(f"Speedup: {serial_time/parallel_time:.2f}x")
```

### Q9: What to do about excessive memory usage?

**A:** Memory optimization strategies:

```python
import gc

def memory_efficient_analysis(large_data, chunk_size=1000):
    """
    Memory-efficient analysis for large data
    """
    analyzer = sk.SixKeysAnalyzer()
    results = []
    
    # Process in chunks
    for i in range(0, len(large_data), chunk_size):
        chunk = large_data[i:i+chunk_size]
        
        # Analyze current chunk
        result = analyzer.analyze_data(chunk)
        results.append(result)
        
        # Force garbage collection
        del chunk
        gc.collect()
        
        print(f"Progress: {min(i+chunk_size, len(large_data))}/{len(large_data)}")
    
    return results

# Monitor memory usage
import psutil
import os

def monitor_memory():
    process = psutil.Process(os.getpid())
    memory_mb = process.memory_info().rss / 1024 / 1024
    print(f"Current memory usage: {memory_mb:.1f} MB")

# Usage example
monitor_memory()
large_dataset = np.random.randn(50000, 64)  # Large dataset
results = memory_efficient_analysis(large_dataset)
monitor_memory()
```

## Error Handling

### Q10: Common errors and solutions?

**A:** Common error handling:

```python
from sixkeys.exceptions import (
    SixKeysError, DataFormatError, 
    ParameterError, AnalysisError
)

def robust_analysis(data, **kwargs):
    """
    Robust analysis function with error handling
    """
    try:
        analyzer = sk.SixKeysAnalyzer(**kwargs)
        result = analyzer.analyze_data(data)
        return result, None
        
    except DataFormatError as e:
        error_msg = f"Data format error: {e}"
        print(error_msg)
        print("Suggestion: Check data dimensions and type")
        return None, error_msg
        
    except ParameterError as e:
        error_msg = f"Parameter error: {e}"
        print(error_msg)
        print("Suggestion: Check parameter ranges and types")
        return None, error_msg
        
    except AnalysisError as e:
        error_msg = f"Analysis computation error: {e}"
        print(error_msg)
        print("Suggestion: Check data quality or adjust parameters")
        return None, error_msg
        
    except Exception as e:
        error_msg = f"Unknown error: {e}"
        print(error_msg)
        print("Suggestion: Contact technical support")
        return None, error_msg

# Usage example
data = np.random.randn(1000, 32)
result, error = robust_analysis(data)

if result is not None:
    print(f"Analysis successful: D_w = {result.d_total:.3f}")
else:
    print(f"Analysis failed: {error}")
```

## Visualization Issues

### Q11: How to customize visualizations?

**A:** Custom visualization examples:

```python
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle

def custom_radar_chart(results, title="Custom Radar Chart"):
    """
    Create custom radar chart
    """
    # Indicator names
    labels = ['FELC\n(ζ₁)', 'TEB\n(ζ₂)', 'RFI\n(ζ₃)', 
              'ECGP\n(ζ₄)', 'PWC\n(ζ₅)', 'ACI\n(ζ₆)']
    
    # Angle settings
    angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]  # Close the plot
    
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
    
    # Plot multiple results
    colors = ['red', 'blue', 'green', 'orange', 'purple']
    
    for i, (name, result) in enumerate(results.items()):
        values = [getattr(result, f'zeta{j+1}') for j in range(6)]
        values += values[:1]  # Close the plot
        
        ax.plot(angles, values, 'o-', linewidth=2, 
                label=name, color=colors[i % len(colors)])
        ax.fill(angles, values, alpha=0.25, color=colors[i % len(colors)])
    
    # Set labels
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    ax.set_ylim(0, max([max([getattr(r, f'zeta{j+1}') for j in range(6)]) 
                       for r in results.values()]) * 1.1)
    
    # Add grid
    ax.grid(True)
    ax.set_title(title, size=16, fontweight='bold', pad=20)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
    
    plt.tight_layout()
    return fig

def custom_time_series_plot(time_results, title="Time Series Analysis"):
    """
    Create time series plot
    """
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()
    
    indicators = ['zeta1', 'zeta2', 'zeta3', 'zeta4', 'zeta5', 'zeta6']
    names = ['FELC', 'TEB', 'RFI', 'ECGP', 'PWC', 'ACI']
    
    time_points = np.arange(len(time_results))
    
    for i, (indicator, name) in enumerate(zip(indicators, names)):
        values = [getattr(result, indicator) for result in time_results]
        
        axes[i].plot(time_points, values, 'o-', linewidth=2, markersize=4)
        axes[i].set_title(f'{name} (ζ{i+1})', fontweight='bold')
        axes[i].set_xlabel('Time Point')
        axes[i].set_ylabel('Indicator Value')
        axes[i].grid(True, alpha=0.3)
    
    plt.suptitle(title, size=16, fontweight='bold')
    plt.tight_layout()
    return fig

# Usage example
analyzer = sk.SixKeysAnalyzer()
results = {
    'Awake': analyzer.analyze_simulated_data('awake'),
    'Light Sedation': analyzer.analyze_simulated_data('light_sedation'),
    'Deep Anesthesia': analyzer.analyze_simulated_data('deep_anesthesia')
}

fig1 = custom_radar_chart(results)
plt.show()
```

### Q12: How to save high-quality images?

**A:** High-quality image saving:

```python
def save_high_quality_figure(fig, filename, dpi=300, format='png'):
    """
    Save high-quality images
    """
    # Supported formats
    supported_formats = ['png', 'pdf', 'svg', 'eps', 'jpg']
    
    if format not in supported_formats:
        raise ValueError(f"Unsupported format: {format}")
    
    # Set save parameters
    save_kwargs = {
        'dpi': dpi,
        'bbox_inches': 'tight',
        'pad_inches': 0.1,
        'facecolor': 'white',
        'edgecolor': 'none'
    }
    
    # Adjust parameters by format
    if format in ['jpg', 'jpeg']:
        save_kwargs['quality'] = 95
    
    # Save image
    full_filename = f"{filename}.{format}"
    fig.savefig(full_filename, format=format, **save_kwargs)
    print(f"Image saved: {full_filename}")
    
    return full_filename

# Usage example
analyzer = sk.SixKeysAnalyzer()
result = analyzer.analyze_simulated_data()
fig = analyzer.plot_radar_chart({'Test': result})

# Save in different formats
save_high_quality_figure(fig, 'radar_chart', dpi=300, format='png')
save_high_quality_figure(fig, 'radar_chart', dpi=300, format='pdf')
save_high_quality_figure(fig, 'radar_chart', dpi=300, format='svg')
```

## Advanced Applications

### Q13: How to perform batch analysis and statistical comparison?

**A:** Batch analysis example:

```python
import pandas as pd
from scipy import stats
import seaborn as sns

def batch_analysis_with_statistics(datasets, labels, n_bootstrap=100):
    """
    Batch analysis with statistical comparison
    """
    analyzer = sk.SixKeysAnalyzer()
    all_results = []
    
    # Batch analysis
    for dataset, label in zip(datasets, labels):
        for i in range(n_bootstrap):
            # Add different random seeds for bootstrap
            analyzer_boot = sk.SixKeysAnalyzer(random_state=i)
            result = analyzer_boot.analyze_data(dataset)
            
            result_dict = {
                'label': label,
                'bootstrap_id': i,
                'D_w': result.d_total,
                'state': result.predicted_state
            }
            
            # Add individual indicators
            for j in range(1, 7):
                result_dict[f'zeta{j}'] = getattr(result, f'zeta{j}')
            
            all_results.append(result_dict)
    
    # Convert to DataFrame
    df = pd.DataFrame(all_results)
    
    # Statistical analysis
    print("=== Descriptive Statistics ===")
    print(df.groupby('label')['D_w'].describe())
    print()
    
    # Between-group comparison
    groups = [group['D_w'].values for name, group in df.groupby('label')]
    
    if len(groups) == 2:
        # t-test
        t_stat, p_value = stats.ttest_ind(groups[0], groups[1])
        print(f"t-test results: t={t_stat:.3f}, p={p_value:.3f}")
    else:
        # ANOVA
        f_stat, p_value = stats.f_oneway(*groups)
        print(f"ANOVA results: F={f_stat:.3f}, p={p_value:.3f}")
    
    # Visualization
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    # Box plot
    sns.boxplot(data=df, x='label', y='D_w', ax=axes[0])
    axes[0].set_title('D_w Distribution Comparison')
    axes[0].set_ylabel('Weighted Distance (D_w)')
    
    # Violin plot
    sns.violinplot(data=df, x='label', y='D_w', ax=axes[1])
    axes[1].set_title('D_w Density Distribution')
    axes[1].set_ylabel('Weighted Distance (D_w)')
    
    plt.tight_layout()
    plt.show()
    
    return df

# Usage example
# Generate simulated data
datasets = [
    np.random.randn(1000, 32),  # Dataset 1
    np.random.randn(1000, 32),  # Dataset 2
    np.random.randn(1000, 32)   # Dataset 3
]
labels = ['Group A', 'Group B', 'Group C']

results_df = batch_analysis_with_statistics(datasets, labels)
```

### Q14: How to perform real-time analysis?

**A:** Real-time analysis implementation:

```python
import threading
import queue
import time
from collections import deque

class RealTimeAnalyzer:
    """
    Real-time Six Keys analyzer
    """
    
    def __init__(self, window_size=1000, update_interval=1.0):
        self.analyzer = sk.SixKeysAnalyzer()
        self.window_size = window_size
        self.update_interval = update_interval
        
        self.data_buffer = deque(maxlen=window_size)
        self.result_queue = queue.Queue()
        self.is_running = False
        self.analysis_thread = None
    
    def add_data(self, new_data):
        """
        Add new data point
        
        Parameters:
        -----------
        new_data : np.ndarray
            New data, shape (n_channels,)
        """
        self.data_buffer.append(new_data)
    
    def _analysis_worker(self):
        """
        Analysis worker thread
        """
        while self.is_running:
            if len(self.data_buffer) >= self.window_size:
                # Get current window data
                current_data = np.array(list(self.data_buffer))
                
                try:
                    # Perform analysis
                    result = self.analyzer.analyze_data(current_data)
                    
                    # Put result in queue
                    self.result_queue.put({
                        'timestamp': time.time(),
                        'result': result,
                        'status': 'success'
                    })
                    
                except Exception as e:
                    self.result_queue.put({
                        'timestamp': time.time(),
                        'error': str(e),
                        'status': 'error'
                    })
            
            time.sleep(self.update_interval)
    
    def start(self):
        """
        Start real-time analysis
        """
        if not self.is_running:
            self.is_running = True
            self.analysis_thread = threading.Thread(target=self._analysis_worker)
            self.analysis_thread.start()
            print("Real-time analysis started")
    
    def stop(self):
        """
        Stop real-time analysis
        """
        if self.is_running:
            self.is_running = False
            if self.analysis_thread:
                self.analysis_thread.join()
            print("Real-time analysis stopped")
    
    def get_latest_result(self):
        """
        Get latest analysis result
        """
        try:
            return self.result_queue.get_nowait()
        except queue.Empty:
            return None

# Usage example
def simulate_real_time_data():
    """
    Simulate real-time data stream
    """
    rt_analyzer = RealTimeAnalyzer(window_size=500, update_interval=0.5)
    rt_analyzer.start()
    
    try:
        # Simulate data stream
        for i in range(1000):
            # Generate new data point
            new_data = np.random.randn(32)  # 32 channels
            rt_analyzer.add_data(new_data)
            
            # Check for new results
            latest_result = rt_analyzer.get_latest_result()
            if latest_result:
                if latest_result['status'] == 'success':
                    result = latest_result['result']
                    print(f"Time {i}: D_w = {result.d_total:.3f}, "
                          f"State = {result.predicted_state}")
                else:
                    print(f"Time {i}: Analysis error - {latest_result['error']}")
            
            time.sleep(0.1)  # Simulate data acquisition interval
    
    finally:
        rt_analyzer.stop()

# Run real-time analysis example
# simulate_real_time_data()
```

## Technical Support

### Q15: How to report issues or request features?

**A:** Issue reporting process:

1. **Check existing issues**: First check [GitHub Issues](https://github.com/yourusername/sixkeys/issues)
2. **Prepare information**: Include error messages, system environment, reproduction steps
3. **Create Issue**: Use provided templates to create new issues

```python
# Collect system information for issue reporting
import sys
import platform
import numpy as np
import scipy
import matplotlib

def collect_system_info():
    """
    Collect system information for issue reporting
    """
    info = {
        'Python Version': sys.version,
        'Operating System': platform.platform(),
        'NumPy Version': np.__version__,
        'SciPy Version': scipy.__version__,
        'Matplotlib Version': matplotlib.__version__
    }
    
    try:
        import sixkeys
        info['SixKeys Version'] = sixkeys.__version__
    except:
        info['SixKeys Version'] = 'Not installed or import failed'
    
    print("=== System Information ===")
    for key, value in info.items():
        print(f"{key}: {value}")
    
    return info

# Usage example
system_info = collect_system_info()
```

### Q16: How to get more help?

**A:** Ways to get help:

1. **Documentation**: Check complete documentation [docs/](../)
2. **Examples**: Refer to [examples/](../../examples/) directory
3. **Community**: Join [GitHub Discussions](https://github.com/yourusername/sixkeys/discussions)
4. **Email**: Contact maintainers [maintainer@sixkeys.org](mailto:maintainer@sixkeys.org)

```python
# Quick help function
def get_help(topic=None):
    """
    Get help information
    """
    help_topics = {
        'installation': 'Installation Guide: docs/en/installation.md',
        'quickstart': 'Quick Start: docs/en/quickstart.md',
        'api': 'API Reference: docs/api/',
        'theory': 'Theory Background: docs/en/theory.md',
        'examples': 'Usage Examples: examples/',
        'faq': 'FAQ: docs/en/faq.md'
    }
    
    if topic is None:
        print("Available help topics:")
        for key, desc in help_topics.items():
            print(f"  {key}: {desc}")
        print("\nUsage: get_help('topic_name')")
    elif topic in help_topics:
        print(f"Help: {help_topics[topic]}")
    else:
        print(f"Unknown topic: {topic}")
        print("Available topics:", list(help_topics.keys()))

# Usage example
get_help()  # Show all topics
get_help('installation')  # Get installation help
```

---

**Note**: If your question is not answered in this FAQ, please don't hesitate to contact us. We continuously update this document to include more common questions.

---

## 📚 **Navigation Bar**

### 📍 **Current Location**
**Documentation Hub** > **Frequently Asked Questions**

### 🔗 **Related Pages**
- [🚀 Quick Start Guide](quickstart.md) - Get started in 5 minutes
- [⚙️ Installation Guide](installation.md) - Detailed setup instructions
- [🧠 Theory Background](theory.md) - Understand the foundations
- [📚 Documentation Hub](README.md) - Return to main documentation

### 🆘 **Help & Support**
- [🔧 **Installation Issues**](installation.md) - Setup troubleshooting
- [💬 **Technical Support**](mailto:isyanghou@gmail.com) - Direct assistance
- [🐛 **GitHub Issues**](https://github.com/isyanghou/6Keys/issues) - Report bugs or request features
- [💭 **GitHub Discussions**](https://github.com/isyanghou/6Keys/discussions) - Community forum

### 🌐 **Other Resources**
- [🇨🇳 **Chinese Version**](../zh/faq.md) - 中文版常见问题
- [🏠 **Project Home**](../../README.md) - Main project page
- [📚 **Complete Documentation**](../) - Full documentation index
- [🎮 **Interactive Examples**](../../examples/) - Hands-on demonstrations