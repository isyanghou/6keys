# 📊 Visualization Tutorial

**📍 Current Location**: [🏠 Home](../../README.md) > [📚 Documentation Hub](README.md) > 📊 Visualization Tutorial

This document provides detailed guidance on visualization features, usage methods, and best practices for the Six Keys Criticality framework.

**⏱️ Reading Time**: 15-30 minutes | **💡 Difficulty**: Beginner-Intermediate | **🎯 Goal**: Master visualization tools

---

## 🆘 **Quick Rescue**

**Having visualization issues?** Get immediate help:

- **🚨 Setup Problems**: [Installation Guide](installation.md) - Environment setup
- **❓ Common Issues**: [FAQ](faq.md) - Troubleshooting
- **📊 Basic Usage**: [Quick Start](quickstart.md) - Getting started
- **🧪 Experiments**: [Experiment Guide](experiments.md) - Research design

---

## 🎨 Visualization Module Overview

The Six Keys Criticality framework provides powerful visualization tools to help researchers and clinicians intuitively understand and analyze neural data. The visualization module is designed to be user-friendly, flexible, and highly customizable, supporting everything from basic charts to complex interactive dashboards.

### Key Features

- **Multi-dimensional Data Visualization**: Support for dimensionality reduction and visualization of high-dimensional data
- **Real-time Data Streaming**: Support for dynamic visualization of real-time data
- **Interactive Exploration**: Provides parameter adjustment and data filtering capabilities
- **Multi-modal Integration**: Integrates multiple data sources and analysis results
- **Report Generation**: Automatically generates high-quality analysis reports

## 📊 Basic Visualization

### Time Series Visualization

```python
from sixkeys.visualization import plots

# Load sample data
from sixkeys.utils import data_loader
data = data_loader.load_sample_data()

# Plot multi-channel time series
plots.plot_time_series(data, channels=['Fz', 'Cz', 'Pz'], 
                      title='EEG Channels', 
                      time_range=[0, 10])

# Plot spectrogram
plots.plot_spectrogram(data, channel='Cz', 
                      freq_range=[0, 50], 
                      colormap='viridis')
```

### Metrics Visualization

```python
from sixkeys.analysis import metrics
from sixkeys.visualization import plots

# Compute six core metrics
results = metrics.compute_all_metrics(data)

# Plot radar chart
plots.plot_radar(results, title='Six Keys Metrics')

# Plot temporal trends
plots.plot_metrics_trend(results, time_window=5, 
                        overlap=0.5, 
                        smoothing=True)
```

### Statistical Visualization

```python
from sixkeys.visualization import stats_plots

# Plot distribution
stats_plots.plot_distribution(results['critical_fluctuation'], 
                             kde=True, 
                             title='Critical Fluctuation Distribution')

# Plot boxplot comparison
stats_plots.plot_boxplot(results, 
                        groups=['control', 'patient'], 
                        title='Group Comparison')

# Plot correlation matrix
stats_plots.plot_correlation_matrix(results, 
                                   method='pearson', 
                                   cmap='coolwarm')
```

## 🌐 Network Visualization

### Brain Network Graph

```python
from sixkeys.visualization import network_plots

# Compute functional connectivity
from sixkeys.analysis import connectivity
conn_matrix = connectivity.compute_connectivity(data, method='plv')

# Plot brain network graph
network_plots.plot_brain_network(conn_matrix, 
                               threshold=0.7, 
                               view='top', 
                               node_size='degree')

# Plot connectivity matrix
network_plots.plot_connectivity_matrix(conn_matrix, 
                                     labels=data.channel_names, 
                                     colormap='Reds')
```

### Dynamic Networks

```python
from sixkeys.visualization import dynamic_plots

# Compute time-varying connectivity
time_conn = connectivity.compute_time_varying_connectivity(data, 
                                                       window=2, 
                                                       step=0.5)

# Plot dynamic network
dynamic_plots.plot_dynamic_network(time_conn, 
                                 frame_duration=200, 
                                 save_gif='dynamic_network.gif')

# Plot network metrics evolution
dynamic_plots.plot_network_metrics_evolution(time_conn, 
                                          metrics=['clustering', 'path_length', 'efficiency'])
```

## 🎮 Interactive Visualization

### Interactive Dashboard

```python
from sixkeys.visualization import dashboard

# Create dashboard
dash = dashboard.SixKeysDashboard(data)

# Add components
dash.add_time_series_panel()
dash.add_spectrogram_panel()
dash.add_metrics_panel()
dash.add_network_panel()

# Launch dashboard
dash.run(port=8050)
```

### Parameter Exploration

```python
from sixkeys.visualization import interactive

# Create parameter exploration interface
explorer = interactive.ParameterExplorer(data)

# Add parameter sliders
explorer.add_slider('window_size', 1, 10, 2, step=0.5)
explorer.add_slider('threshold', 0, 1, 0.5, step=0.05)
explorer.add_dropdown('metric', ['CF', 'CC', 'II', 'RS', 'SC', 'DS'])

# Set callback function
def update_plot(params):
    # Use parameters to compute results and update charts
    pass

explorer.set_callback(update_plot)

# Launch interface
explorer.run()
```

## 📱 Visualization Demo Module

The Six Keys Criticality framework provides a standalone visualization demo module that can quickly display and explore analysis results without writing code.

### Command Line Interface

```bash
# Launch basic demo
sixkeys-demo --data sample_data.edf

# Launch network visualization
sixkeys-demo --mode network --data sample_data.edf

# Launch full dashboard
sixkeys-demo --mode dashboard --data sample_data.edf --port 8050

# Batch analysis mode
sixkeys-demo --mode batch --data data_folder/ --output results/
```

### Configuration Options

You can customize the demo module behavior through configuration files:

```yaml
# demo_config.yaml
visualization:
  theme: 'dark'  # 'light' or 'dark'
  colormap: 'viridis'
  layout: 'grid'  # 'grid', 'tabs', or 'flow'
  export_format: 'png'  # 'png', 'svg', or 'pdf'

metrics:
  compute_all: true
  window_size: 2.0
  overlap: 0.5
```

## 🖼️ Visualization Resources

### Template Library

```python
from sixkeys.visualization import templates

# Use scientific publication template
fig = templates.scientific_figure(data, title='Analysis Results')

# Use clinical report template
report = templates.clinical_report(patient_data, metrics_results)

# Use presentation template
presentation = templates.presentation_slides(results, template='modern')
```

### Export and Sharing

```python
from sixkeys.visualization import export

# Export high-resolution figures
export.save_figure(fig, 'results.png', dpi=300)

# Export interactive HTML
export.save_interactive(dashboard, 'interactive_report.html')

# Generate PDF report
export.generate_pdf_report(results, 'analysis_report.pdf')
```

## 📋 Best Practices

### Visualization Tips

1. **Keep it Simple**: Avoid over-decoration, focus on the data
2. **Consistency**: Use consistent colors and styles throughout analysis
3. **Accessibility**: Consider color-blind friendly palettes
4. **Context**: Always provide appropriate titles, labels, and legends
5. **Interactivity**: Use interactive elements to enhance exploration

### Performance Optimization

```python
# For large datasets, use data sampling
from sixkeys.utils import sampling
sampled_data = sampling.downsample(data, factor=10)

# Use efficient plotting backends
import matplotlib
matplotlib.use('Agg')  # For non-interactive environments

# Enable caching for repeated computations
from sixkeys.visualization import cache
cache.enable_caching()
```

## 🎉 **Visualization Mastery Complete! What's Next?**

### 🚀 **Apply Your Skills**

1. **🧪 Design Experiments**: Use visualizations in research design
2. **📊 Create Reports**: Generate professional analysis reports
3. **🎨 Customize Plots**: Develop your own visualization styles

### 📚 **Advanced Resources**
- **🧪 Experiments**: [Experiment Guide](experiments.md) - Research methodology
- **🧠 Theory Deep Dive**: [Theory Background](theory.md) - Understand principles
- **❓ Problem Solving**: [FAQ](faq.md) - Visualization troubleshooting

---

## 🧭 **Navigation**

**📍 Current Location**: [🏠 Home](../../README.md) > [📚 Documentation Hub](README.md) > 📊 **Visualization Tutorial**

### 🔄 **Related Pages**
- **⬅️ Previous**: [🧪 Experiment Guide](experiments.md) - Research design
- **➡️ Next**: [🧠 Theory Background](theory.md) - Theoretical foundation
- **🎯 Feature Details**: [Features](../features.md) - Framework capabilities
- **🔙 Back**: [📚 Documentation Hub](README.md) - Browse all documentation

### 🆘 **Visualization Issues?**
- **❓ Plotting Problems**: [FAQ-Visualization](faq.md#visualization) - Common plotting issues
- **📧 Technical Support**: [isyanghou@gmail.com](mailto:isyanghou@gmail.com) - Visualization consultation
- **💡 Feature Requests**: [GitHub Issues](https://github.com/isyanghou/6Keys/issues) - Request new features
- **🎨 Gallery**: [GitHub Discussions](https://github.com/isyanghou/6Keys/discussions) - Share your visualizations

### 🌍 **Other Resources**
- **🇨🇳 Chinese Version**: [中文版](../visualization.md) - 中文可視化教程
- **🏠 Project Home**: [Main Repository](https://github.com/isyanghou/6Keys) - Source code
- **📚 Complete Documentation**: [All Docs](../README.md) - Full documentation index
- **🎨 Interactive Examples**: [Live Demos](https://sixkeys-demo.herokuapp.com) - Try online

---

**💡 Tip**: Want to create stunning visualizations? Start with the [📊 Quick Start](quickstart.md) examples, then explore the [🎮 Interactive Dashboard](#interactive-dashboard) for advanced features.