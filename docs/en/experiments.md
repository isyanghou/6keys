# 🧪 Experimental Guide

**📍 Current Location**: [🏠 Home](../../README.md) > [📚 Documentation Hub](README.md) > 🧪 Experimental Guide

This document provides detailed guidance for experimental design, data analysis, and result validation using the Six Keys Criticality framework.

**⏱️ Reading Time**: 20-40 minutes | **💡 Difficulty**: Intermediate-Advanced | **🎯 Goal**: Design complete experiments

---

## 🆘 **Quick Rescue**

**Having experimental issues?** Get immediate help:

- **🚨 Setup Problems**: [Installation Guide](installation.md) - Environment setup
- **❓ Common Issues**: [FAQ](faq.md) - Troubleshooting
- **📊 Data Processing**: [Quick Start](quickstart.md) - Basic usage
- **📈 Visualization**: [Visualization Tutorial](visualization.md) - Result presentation

---

## 🗺️ **Experiment Navigation**

| Stage | Content | Target Users |
|-------|---------|-------------|
| [📋 Experimental Design](#experimental-design-principles) | Design principles and methods | Researchers |
| [🔧 Data Processing](#data-preprocessing) | Preprocessing and cleaning | Analysts |
| [📊 Metrics Analysis](#metrics-computation-and-analysis) | Computation and statistics | All users |
| [📈 Result Presentation](#results-visualization) | Visualization and reporting | All users |

## 🧪 Experimental Design Principles

### Basic Requirements

1. **Data Quality**: Ensure quality and consistency of data collection
2. **Sample Size**: Determine appropriate sample size based on statistical power analysis
3. **Control Group Design**: Set up appropriate control and experimental groups
4. **Randomization**: Implement proper randomization strategies
5. **Blinding**: Implement single or double blinding when possible

### Experiment Types

#### 1. Cross-sectional Studies

Suitable for comparing Six Keys indicators across different groups or states:

```python
from sixkeys.experiments import cross_sectional

# Design cross-sectional experiment
experiment = cross_sectional.CrossSectionalExperiment(
    groups=['control', 'patient'],
    metrics=['all'],  # Calculate all six indicators
    statistical_tests=['t_test', 'mann_whitney']
)

# Add data
experiment.add_group_data('control', control_data)
experiment.add_group_data('patient', patient_data)

# Run analysis
results = experiment.run_analysis()
```

#### 2. Longitudinal Studies

Suitable for tracking changes in individuals or groups over time:

```python
from sixkeys.experiments import longitudinal

# Design longitudinal experiment
experiment = longitudinal.LongitudinalExperiment(
    time_points=['baseline', 'week_1', 'week_4', 'week_12'],
    subjects=range(1, 21),  # 20 subjects
    metrics=['critical_fluctuation', 'information_integration']
)

# Add time point data
for time_point in experiment.time_points:
    for subject in experiment.subjects:
        data = load_subject_data(subject, time_point)
        experiment.add_data(subject, time_point, data)

# Run analysis
results = experiment.run_analysis()
```

#### 3. Intervention Studies

Suitable for evaluating the effects of treatments or interventions:

```python
from sixkeys.experiments import intervention

# Design intervention experiment
experiment = intervention.InterventionExperiment(
    design='randomized_controlled',
    intervention_groups=['treatment', 'placebo'],
    time_points=['pre', 'post', 'follow_up'],
    primary_outcome='information_integration'
)

# Randomize subjects
experiment.randomize_subjects(subjects_list, stratify_by='age_group')

# Run analysis
results = experiment.run_analysis()
```

## 📊 Data Preprocessing

### Data Quality Assessment

```python
from sixkeys.preprocessing import quality_control

# Create quality control checker
qc = quality_control.QualityController()

# Check data completeness
completeness = qc.check_completeness(data)
print(f"Data completeness: {completeness:.2%}")

# Assess signal quality
signal_quality = qc.assess_signal_quality(data)
print(f"Signal quality score: {signal_quality:.3f}")

# Detect artifacts
artifacts = qc.detect_artifacts(data, methods=['amplitude', 'gradient', 'frequency'])
print(f"Artifacts detected: {len(artifacts)} segments")
```

### Data Cleaning

```python
from sixkeys.preprocessing import cleaning

# Create data cleaning pipeline
cleaner = cleaning.DataCleaner()

# Remove artifacts
clean_data = cleaner.remove_artifacts(data, artifacts)

# Apply filtering
filtered_data = cleaner.apply_filter(clean_data, 
                                   filter_type='bandpass', 
                                   low_freq=0.5, 
                                   high_freq=50)

# Re-reference
rereferenced_data = cleaner.rereference(filtered_data, method='average')
```

### Data Standardization

```python
from sixkeys.preprocessing import standardization

# Create standardizer
standardizer = standardization.DataStandardizer()

# Z-score normalization
standardized_data = standardizer.z_score_normalize(data)

# Baseline normalization
baseline_normalized = standardizer.baseline_normalize(data, 
                                                    baseline_period=[0, 60])

# Cross-subject normalization
cross_subject_normalized = standardizer.cross_subject_normalize(all_subjects_data)
```

## 🔬 Metrics Computation and Analysis

### Batch Computation

```python
from sixkeys.analysis import batch_processing

# Create batch processor
processor = batch_processing.BatchProcessor(
    metrics=['all'],
    window_size=2.0,
    overlap=0.5,
    n_jobs=4  # Parallel processing
)

# Process multiple files
results = processor.process_files(file_list, output_dir='results/')

# Process multiple subjects
subject_results = processor.process_subjects(subject_data_dict)
```

### Statistical Analysis

```python
from sixkeys.statistics import analysis

# Create statistical analyzer
stats = analysis.StatisticalAnalyzer()

# Descriptive statistics
descriptive = stats.descriptive_statistics(results)

# Group comparison
group_comparison = stats.compare_groups(control_results, patient_results)

# Correlation analysis
correlations = stats.correlation_analysis(results, method='spearman')
```

## 📈 Results Visualization

### Statistical Plots

```python
from sixkeys.visualization import statistical_plots

# Group comparison plot
statistical_plots.plot_group_comparison(results, 
                                      groups=['control', 'patient'],
                                      test_results=group_comparison)

# Effect size plot
statistical_plots.plot_effect_sizes(group_comparison, 
                                   metrics=['CF', 'CC', 'II', 'RS', 'SC', 'DS'])

# Correlation heatmap
statistical_plots.plot_correlation_heatmap(correlations)
```

### Time Series Analysis

```python
from sixkeys.visualization import time_series_plots

# Longitudinal changes plot
time_series_plots.plot_longitudinal_changes(longitudinal_results,
                                           time_points=['baseline', 'week_1', 'week_4'],
                                           metrics=['II', 'CF'])

# Individual trajectory plot
time_series_plots.plot_individual_trajectories(subject_trajectories,
                                              highlight_subjects=[1, 5, 10])
```

## 🎉 **Experiment Design Complete! What's Next?**

### 🚀 **Start Experiments**

1. **📊 Data Collection**: Collect data according to design protocol
2. **🔧 Data Analysis**: Use framework for analysis
3. **📈 Result Presentation**: Create professional visualization reports

### 📚 **Deep Dive Resources**
- **📊 Visualization**: [Visualization Tutorial](visualization.md) - Professional chart creation
- **🧠 Theory Deep Dive**: [Theory Background](theory.md) - Understand analysis principles
- **❓ Problem Solving**: [FAQ](faq.md) - Experimental troubleshooting

---

## 🧭 **Navigation**

**📍 Current Location**: [🏠 Home](../../README.md) > [📚 Documentation Hub](README.md) > 🧪 **Experimental Guide**

### 🔄 **Related Pages**
- **⬅️ Previous**: [🧠 Theory Background](theory.md) - Theoretical foundation
- **➡️ Next**: [📊 Visualization Tutorial](visualization.md) - Result presentation
- **🎯 Feature Details**: [Features](../features.md) - Framework capabilities
- **🔙 Back**: [📚 Documentation Hub](README.md) - Browse all documentation

### 🆘 **Experimental Issues?**
- **❓ Experimental Questions**: [FAQ-Experiments](faq.md#practical-applications) - Common experimental issues
- **📧 Academic Discussion**: [isyanghou@gmail.com](mailto:isyanghou@gmail.com) - Experimental design consultation
- **💡 Method Suggestions**: [GitHub Discussions](https://github.com/isyanghou/6Keys/discussions) - Community discussion

### 🌍 **Other Resources**
- **🇨🇳 Chinese Version**: [中文版](../experiments.md) - 中文實驗指南
- **🏠 Project Home**: [Main Repository](https://github.com/isyanghou/6Keys) - Source code
- **📚 Complete Documentation**: [All Docs](../README.md) - Full documentation index

---

**💡 Tip**: Having experimental difficulties? Check the [❓ FAQ](faq.md) experimental section, or refer to [Case Studies](paper/D_Experimental_Details_Reference_Blueprint.md) for inspiration.