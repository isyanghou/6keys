# 🧪 實驗指南 | Experimental Guide

**📍 當前位置**: [🏠 首頁](../README.md) > [📚 文檔中心](README.md) > 🧪 實驗指南

本文檔提供使用六鑰臨界框架進行實驗設計、數據分析和結果驗證的詳細指南。

**⏱️ 閱讀時間**: 20-40分鐘 | **💡 難度**: 中高級 | **🎯 目標**: 設計完整實驗

---

## 🗺️ **實驗導航** | **Experiment Navigation**

| 階段 | 內容 | 適合對象 |
|------|------|----------|
| [📋 實驗設計](#實驗設計原則) | 設計原則和方法 | 研究人員 |
| [🔧 數據處理](#數據預處理) | 預處理和清理 | 分析師 |
| [📊 指標分析](#指標計算與分析) | 計算和統計 | 所有用戶 |
| [📈 結果展示](#結果可視化) | 可視化和報告 | 所有用戶 |

## 🧪 實驗設計原則 | Experimental Design Principles

### 基本要求 | Basic Requirements

1. **數據質量**: 確保數據採集的質量和一致性
2. **樣本大小**: 根據統計功效分析確定適當的樣本大小
3. **對照組設計**: 設置適當的對照組和實驗組
4. **隨機化**: 實施適當的隨機化策略
5. **盲法**: 在可能的情況下實施單盲或雙盲設計

### 實驗類型 | Experiment Types

#### 1. 橫斷面研究 | Cross-sectional Studies

適用於比較不同群體或狀態下的六鑰指標差異：

```python
from sixkeys.experiments import cross_sectional

# 設計橫斷面實驗
experiment = cross_sectional.CrossSectionalExperiment(
    groups=['control', 'patient'],
    metrics=['all'],  # 計算所有六個指標
    statistical_tests=['t_test', 'mann_whitney']
)

# 添加數據
experiment.add_group_data('control', control_data)
experiment.add_group_data('patient', patient_data)

# 執行分析
results = experiment.run_analysis()
```

#### 2. 縱向研究 | Longitudinal Studies

適用於追蹤個體或群體隨時間的變化：

```python
from sixkeys.experiments import longitudinal

# 設計縱向實驗
experiment = longitudinal.LongitudinalExperiment(
    time_points=['baseline', 'week_1', 'week_4', 'week_12'],
    subjects=range(1, 21),  # 20個受試者
    metrics=['critical_fluctuation', 'information_integration']
)

# 添加時間點數據
for time_point in experiment.time_points:
    for subject in experiment.subjects:
        data = load_subject_data(subject, time_point)
        experiment.add_data(subject, time_point, data)

# 執行分析
results = experiment.run_analysis()
```

#### 3. 干預研究 | Intervention Studies

適用於評估治療或干預措施的效果：

```python
from sixkeys.experiments import intervention

# 設計干預實驗
experiment = intervention.InterventionExperiment(
    design='randomized_controlled',
    intervention_groups=['treatment', 'placebo'],
    time_points=['pre', 'post', 'follow_up'],
    primary_outcome='information_integration'
)

# 隨機分組
experiment.randomize_subjects(subjects_list, stratify_by='age_group')

# 執行分析
results = experiment.run_analysis()
```

## 📊 數據預處理 | Data Preprocessing

### 數據質量檢查 | Data Quality Assessment

```python
from sixkeys.preprocessing import quality_control

# 創建質量控制檢查器
qc = quality_control.QualityController()

# 檢查數據完整性
completeness = qc.check_completeness(data)
print(f"Data completeness: {completeness:.2%}")

# 檢查信號質量
signal_quality = qc.assess_signal_quality(data)
print(f"Signal quality score: {signal_quality:.3f}")

# 檢測偽影
artifacts = qc.detect_artifacts(data, methods=['amplitude', 'gradient', 'frequency'])
print(f"Artifacts detected: {len(artifacts)} segments")
```

### 數據清理 | Data Cleaning

```python
from sixkeys.preprocessing import cleaning

# 創建數據清理管道
cleaner = cleaning.DataCleaner()

# 移除偽影
clean_data = cleaner.remove_artifacts(data, artifacts)

# 濾波處理
filtered_data = cleaner.apply_filter(clean_data, 
                                   filter_type='bandpass', 
                                   low_freq=0.5, 
                                   high_freq=50)

# 重新參考
rereferenced_data = cleaner.rereference(filtered_data, method='average')
```

### 數據標準化 | Data Standardization

```python
from sixkeys.preprocessing import standardization

# 創建標準化器
standardizer = standardization.DataStandardizer()

# Z-score標準化
standardized_data = standardizer.z_score_normalize(data)

# 基於基線的標準化
baseline_normalized = standardizer.baseline_normalize(data, 
                                                    baseline_period=[0, 60])

# 跨受試者標準化
cross_subject_normalized = standardizer.cross_subject_normalize(all_subjects_data)
```

## 🔬 指標計算與分析 | Metrics Computation and Analysis

### 批量計算 | Batch Computation

```python
from sixkeys.analysis import batch_processing

# 創建批量處理器
processor = batch_processing.BatchProcessor(
    metrics=['all'],
    window_size=2.0,
    overlap=0.5,
    n_jobs=4  # 並行處理
)

# 處理多個文件
results = processor.process_files(file_list, output_dir='results/')

# 處理多個受試者
subject_results = processor.process_subjects(subject_data_dict)
```

### 統計分析 | Statistical Analysis

```python
from sixkeys.statistics import analysis

# 創建統計分析器
stats = analysis.StatisticalAnalyzer()

# 描述性統計
descriptive = stats.descriptive_statistics(results)

# 組間比較
group_comparison = stats.compare_groups(control_results, patient_results)

# 相關性分析
correlations = stats.correlation_analysis(results, method='spearman')

# 多重比較校正
corrected_p = stats.multiple_comparison_correction(p_values, method='fdr_bh')
```

## 📈 結果可視化 | Results Visualization

### 統計圖表 | Statistical Plots

```python
from sixkeys.visualization import statistical_plots

# 組間比較圖
statistical_plots.plot_group_comparison(results, 
                                      groups=['control', 'patient'],
                                      test_results=group_comparison)

# 效應大小圖
statistical_plots.plot_effect_sizes(group_comparison, 
                                   metrics=['CF', 'CC', 'II', 'RS', 'SC', 'DS'])

# 相關性熱力圖
statistical_plots.plot_correlation_heatmap(correlations, 
                                          significance_mask=True)
```

### 時間序列分析 | Time Series Analysis

```python
from sixkeys.visualization import time_series_plots

# 縱向變化圖
time_series_plots.plot_longitudinal_changes(longitudinal_results,
                                           time_points=['baseline', 'week_1', 'week_4'],
                                           metrics=['II', 'CF'])

# 個體軌跡圖
time_series_plots.plot_individual_trajectories(subject_trajectories,
                                              highlight_mean=True)
```

## 🎯 實驗驗證 | Experimental Validation

### 可靠性分析 | Reliability Analysis

```python
from sixkeys.validation import reliability

# 測試-重測可靠性
test_retest = reliability.test_retest_reliability(session1_data, session2_data)
print(f"Test-retest ICC: {test_retest.icc:.3f}")

# 內部一致性
internal_consistency = reliability.internal_consistency(data)
print(f"Cronbach's alpha: {internal_consistency.alpha:.3f}")

# 評分者間可靠性
inter_rater = reliability.inter_rater_reliability(rater1_scores, rater2_scores)
print(f"Inter-rater correlation: {inter_rater.correlation:.3f}")
```

### 效度分析 | Validity Analysis

```python
from sixkeys.validation import validity

# 構念效度
construct_validity = validity.construct_validity(sixkeys_scores, 
                                               related_measures)

# 判別效度
discriminant_validity = validity.discriminant_validity(control_scores, 
                                                     patient_scores)

# 預測效度
predictive_validity = validity.predictive_validity(baseline_scores, 
                                                  outcome_measures)
```

### 敏感性分析 | Sensitivity Analysis

```python
from sixkeys.validation import sensitivity

# 參數敏感性
param_sensitivity = sensitivity.parameter_sensitivity(
    data, 
    parameter_ranges={
        'window_size': [1.0, 2.0, 3.0],
        'overlap': [0.25, 0.5, 0.75]
    }
)

# 樣本大小敏感性
sample_sensitivity = sensitivity.sample_size_sensitivity(
    data, 
    sample_sizes=[10, 20, 50, 100]
)
```

## 📋 實驗報告 | Experimental Reporting

### 自動報告生成 | Automatic Report Generation

```python
from sixkeys.reporting import experiment_report

# 創建實驗報告
report = experiment_report.ExperimentReport(
    experiment_type='cross_sectional',
    title='Six Keys Metrics in Depression',
    authors=['Dr. Smith', 'Dr. Johnson']
)

# 添加方法部分
report.add_methods_section(
    participants=participant_info,
    data_acquisition=acquisition_params,
    preprocessing=preprocessing_steps,
    analysis=analysis_methods
)

# 添加結果部分
report.add_results_section(
    descriptive_stats=descriptive,
    statistical_tests=group_comparison,
    figures=figure_list
)

# 生成報告
report.generate_pdf('experiment_report.pdf')
```

### 結果表格 | Results Tables

```python
from sixkeys.reporting import tables

# 生成描述性統計表
descriptive_table = tables.descriptive_statistics_table(
    results, 
    groups=['control', 'patient'],
    format='apa'
)

# 生成統計檢驗表
statistical_table = tables.statistical_tests_table(
    group_comparison,
    include_effect_size=True,
    format='scientific'
)

# 生成相關性表
correlation_table = tables.correlation_table(
    correlations,
    significance_stars=True
)
```

## 🔍 常見問題與解決方案 | Common Issues and Solutions

### 數據質量問題 | Data Quality Issues

**問題**: 信號中包含大量偽影
**解決方案**:
```python
# 使用自動偽影檢測和移除
from sixkeys.preprocessing import artifact_removal

artifact_remover = artifact_removal.AutomaticArtifactRemover()
clean_data = artifact_remover.remove_artifacts(data, 
                                             methods=['ica', 'regression'])
```

**問題**: 數據長度不一致
**解決方案**:
```python
# 統一數據長度
from sixkeys.preprocessing import alignment

aligner = alignment.DataAligner()
aligned_data = aligner.align_to_shortest(data_list)
# 或
aligned_data = aligner.align_to_length(data_list, target_length=1000)
```

### 統計分析問題 | Statistical Analysis Issues

**問題**: 數據不符合正態分佈
**解決方案**:
```python
# 使用非參數檢驗
from sixkeys.statistics import nonparametric

# Mann-Whitney U檢驗
result = nonparametric.mann_whitney_u(group1, group2)

# Kruskal-Wallis檢驗
result = nonparametric.kruskal_wallis(group1, group2, group3)
```

**問題**: 多重比較問題
**解決方案**:
```python
# 應用多重比較校正
from sixkeys.statistics import multiple_comparisons

corrected_p = multiple_comparisons.fdr_correction(p_values)
# 或
corrected_p = multiple_comparisons.bonferroni_correction(p_values)
```

## 📚 實驗範例 | Experimental Examples

### 範例1: 意識狀態分類 | Example 1: Consciousness State Classification

```python
# 完整的意識狀態分類實驗
from sixkeys.experiments.examples import consciousness_classification

# 載入範例實驗
experiment = consciousness_classification.ConsciousnessClassificationExperiment()

# 執行實驗
results = experiment.run()

# 查看結果
print(f"Classification accuracy: {results.accuracy:.3f}")
print(f"Sensitivity: {results.sensitivity:.3f}")
print(f"Specificity: {results.specificity:.3f}")
```

### 範例2: 治療效果評估 | Example 2: Treatment Effect Assessment

```python
# 治療效果評估實驗
from sixkeys.experiments.examples import treatment_assessment

# 設置實驗
experiment = treatment_assessment.TreatmentAssessmentExperiment(
    treatment_type='meditation',
    duration_weeks=8,
    assessment_points=['baseline', 'mid', 'post', 'follow_up']
)

# 執行實驗
results = experiment.run()

# 生成報告
experiment.generate_report('treatment_effect_report.pdf')
```

---

## 🎉 **實驗設計完成！下一步做什麼？** | **Experiment Design Complete! What's Next?**

### 🚀 **開始實驗**
1. **📊 數據收集**: 按照設計方案收集數據
2. **🔧 數據分析**: 使用框架進行分析
3. **📈 結果展示**: 創建專業的可視化報告

### 📚 **深入資源**
- **📊 可視化**: [可視化教程](visualization.md) - 專業圖表製作
- **🧠 理論深入**: [理論背景](theory.md) - 理解分析原理
- **❓ 問題解決**: [常見問題](faq.md) - 實驗疑難排解

---

## 🧭 **導航欄** | **Navigation**

**📍 當前位置**: [🏠 首頁](../README.md) > [📚 文檔中心](README.md) > 🧪 **實驗指南**

### 🔄 **相關頁面**
- **⬅️ 上一步**: [🧠 理論背景](theory.md) - 理論基礎
- **➡️ 下一步**: [📊 可視化教程](visualization.md) - 結果展示
- **🎯 功能詳解**: [特性說明](features.md) - 框架功能
- **🔙 返回**: [📚 文檔中心](README.md) - 瀏覽所有文檔

### 🆘 **實驗問題？**
- **❓ 實驗疑問**: [FAQ-實驗部分](faq.md#實際應用) - 實驗常見問題
- **📧 學術討論**: [isyanghou@gmail.com](mailto:isyanghou@gmail.com) - 實驗設計諮詢
- **💡 方法建議**: [GitHub Discussions](https://github.com/isyanghou/6Keys/discussions) - 社群討論

---

**💡 提示**: 實驗遇到困難？查看 [❓ 常見問題](faq.md) 中的實驗部分，或參考 [案例研究](zh/paper/B-0_案例研究.md) 獲得靈感。