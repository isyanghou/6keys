# 🚀 快速開始指南 | Quick Start Guide

**📍 當前位置**: [🏠 首頁](../README.md) > [📚 文檔中心](README.md) > 🚀 快速開始

本指南將幫助您在5分鐘內開始使用六鑰臨界框架進行神經數據分析。

**⏱️ 預計時間**: 5-10分鐘 | **💡 難度**: 新手友好 | **🎯 目標**: 成功運行第一個分析

## 🚀 安裝 | Installation

### 使用 pip 安裝 | Install with pip

```bash
pip install sixkeys
```

### 使用 conda 安裝 | Install with conda

```bash
conda install -c conda-forge sixkeys
```

### 驗證安裝 | Verify Installation

```python
import sixkeys
print(f"Six Keys version: {sixkeys.__version__}")
```

## 📊 基本使用 | Basic Usage

### 1. 載入數據 | Load Data

```python
from sixkeys.utils import data_loader

# 載入範例數據
data = data_loader.load_sample_data()
print(f"Data shape: {data.shape}")  # (time_points, channels)

# 或載入您自己的數據
# data = data_loader.load_edf('your_data.edf')
# data = data_loader.load_mat('your_data.mat')
```

### 2. 計算六個核心指標 | Compute Six Core Metrics

```python
from sixkeys.analysis import metrics

# 計算所有六個指標
results = metrics.compute_all_metrics(data)

print("Six Keys Metrics:")
for metric, value in results.items():
    print(f"{metric}: {value:.4f}")
```

### 3. 可視化結果 | Visualize Results

```python
from sixkeys.visualization import plots

# 繪製雷達圖
plots.plot_radar(results, title='Six Keys Metrics')

# 繪製時間序列
plots.plot_time_series(data, channels=['Fz', 'Cz', 'Pz'])

# 顯示圖表
import matplotlib.pyplot as plt
plt.show()
```

## 🧠 完整範例 | Complete Example

以下是一個完整的分析範例：

```python
import numpy as np
from sixkeys.utils import data_loader
from sixkeys.analysis import metrics
from sixkeys.visualization import plots
import matplotlib.pyplot as plt

# 1. 載入數據
print("Loading data...")
data = data_loader.load_sample_data()
print(f"Data loaded: {data.shape[0]} time points, {data.shape[1]} channels")

# 2. 數據預處理（可選）
from sixkeys.preprocessing import filters
filtered_data = filters.bandpass_filter(data, low_freq=0.5, high_freq=50)

# 3. 計算六個核心指標
print("\nComputing Six Keys metrics...")
results = metrics.compute_all_metrics(filtered_data)

# 4. 顯示結果
print("\n=== Six Keys Criticality Metrics ===")
metric_names = {
    'critical_fluctuation': '臨界波動性',
    'connectivity_complexity': '連接複雜度', 
    'information_integration': '信息整合度',
    'response_sensitivity': '響應敏感性',
    'synchronization_coordination': '同步協調性',
    'dynamic_stability': '動態穩定性'
}

for metric, value in results.items():
    chinese_name = metric_names.get(metric, metric)
    print(f"{chinese_name:12s}: {value:.4f}")

# 5. 創建可視化
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# 雷達圖
plots.plot_radar(results, ax=axes[0,0], title='Six Keys Metrics')

# 時間序列
plots.plot_time_series(data[:1000], channels=['Fz', 'Cz', 'Pz'], 
                      ax=axes[0,1], title='EEG Time Series')

# 功率譜
plots.plot_power_spectrum(data, channel='Cz', 
                         ax=axes[1,0], title='Power Spectrum')

# 指標分佈
plots.plot_metrics_distribution(results, 
                               ax=axes[1,1], title='Metrics Distribution')

plt.tight_layout()
plt.show()

print("\nAnalysis complete!")
```

## 🎯 進階使用 | Advanced Usage

### 批量分析 | Batch Analysis

```python
from sixkeys.analysis import batch_processing

# 批量處理多個文件
processor = batch_processing.BatchProcessor(
    metrics=['critical_fluctuation', 'information_integration'],
    window_size=2.0,
    overlap=0.5
)

# 處理文件列表
file_list = ['data1.edf', 'data2.edf', 'data3.edf']
results = processor.process_files(file_list)

# 保存結果
processor.save_results(results, 'batch_results.csv')
```

### 統計分析 | Statistical Analysis

```python
from sixkeys.statistics import analysis

# 比較兩組數據
control_results = metrics.compute_all_metrics(control_data)
patient_results = metrics.compute_all_metrics(patient_data)

# 統計檢驗
stats = analysis.StatisticalAnalyzer()
comparison = stats.compare_groups(control_results, patient_results)

print("Group comparison results:")
for metric, result in comparison.items():
    print(f"{metric}: p = {result.p_value:.4f}, effect size = {result.effect_size:.3f}")
```

### 實時分析 | Real-time Analysis

```python
from sixkeys.realtime import analyzer

# 創建實時分析器
rt_analyzer = analyzer.RealTimeAnalyzer(
    metrics=['critical_fluctuation', 'information_integration'],
    window_size=2.0,
    update_interval=0.5
)

# 開始實時分析
rt_analyzer.start()

# 添加新數據
for new_data_chunk in data_stream:
    rt_analyzer.add_data(new_data_chunk)
    current_metrics = rt_analyzer.get_current_metrics()
    print(f"Current metrics: {current_metrics}")
```

## 🎮 互動式演示 | Interactive Demo

啟動互動式演示界面：

```bash
# 命令行啟動
sixkeys-demo --data sample

# 或在Python中啟動
from sixkeys.visualization import dashboard
dash = dashboard.SixKeysDashboard()
dash.run(port=8050)
```

然後在瀏覽器中打開 `http://localhost:8050` 查看互動式界面。

## 📚 學習資源 | Learning Resources

### 教程和範例 | Tutorials and Examples

- **[完整教程](../examples/notebooks/)**: Jupyter筆記本教程
- **[API參考](api/)**: 詳細的API文檔
- **[理論背景](theory.md)**: 六鑰臨界理論介紹
- **[實驗指南](experiments.md)**: 實驗設計和分析指南

### 範例數據 | Sample Data

```python
# 載入不同類型的範例數據
from sixkeys.utils import data_loader

# EEG數據
eeg_data = data_loader.load_sample_eeg()

# MEG數據
meg_data = data_loader.load_sample_meg()

# 模擬數據
sim_data = data_loader.generate_synthetic_data(
    n_channels=64, 
    duration=60, 
    sampling_rate=250
)
```

## ❓ 常見問題 | Common Questions

### Q: 支援哪些數據格式？
**A**: 支援 EDF、BDF、MAT、CSV、NumPy 等多種格式。

### Q: 最小數據長度要求？
**A**: 建議至少30秒的數據，採樣率不低於100Hz。

### Q: 如何處理偽影？
**A**: 使用內建的預處理工具：
```python
from sixkeys.preprocessing import artifact_removal
clean_data = artifact_removal.remove_artifacts(data)
```

### Q: 如何解釋結果？
**A**: 每個指標範圍為0-1，值越高表示該特性越明顯。詳見[理論背景](theory.md)。

---

## 🎉 **完成了！下一步做什麼？** | **What's Next?**

### 🎯 **根據您的需求選擇**:

<details>
<summary><strong>🧠 我想深入了解理論</strong></summary>

**推薦路徑**:
1. [🧠 理論背景](theory.md) - 六鑰臨界理論基礎
2. [📚 完整論文](zh/paper/) - 深入理論細節
3. [🧮 數學推導](zh/paper/A-0_數學推導詳解.md) - 數學證明

</details>

<details>
<summary><strong>👨‍💻 我要開發和定制</strong></summary>

**推薦路徑**:
1. [📚 API文檔](api/) - 完整API參考
2. [🔧 開發者指南](developers.md) - 開發環境設置
3. [🏗️ 項目結構](project-structure.md) - 代碼架構

</details>

<details>
<summary><strong>🔬 我要設計實驗</strong></summary>

**推薦路徑**:
1. [🧪 實驗指南](experiments.md) - 實驗設計方法
2. [📊 可視化教程](visualization.md) - 結果展示
3. [🎯 特性說明](features.md) - 功能詳解

</details>

### 📚 **學習資源** | **Learning Resources**

| 資源類型 | 連結 | 說明 |
|---------|------|------|
| 🎯 **範例數據** | [載入範例](api/sample_data.md) | 測試用數據集 |
| 📖 **教程筆記本** | [Jupyter教程](../notebooks/) | 互動式學習 |
| 🎨 **可視化範例** | [可視化教程](visualization.md) | 圖表製作 |
| ❓ **問題解答** | [常見問題](faq.md) | 疑難排解 |

---

## 🧭 **導航欄** | **Navigation**

**📍 當前位置**: [🏠 首頁](../README.md) > [📚 文檔中心](README.md) > 🚀 **快速開始**

### 🔄 **相關頁面**
- **⬅️ 上一步**: [⚙️ 安裝指南](installation.md) - 詳細安裝說明
- **➡️ 下一步**: [🧠 理論背景](theory.md) - 了解理論基礎
- **🔙 返回**: [📚 文檔中心](README.md) - 瀏覽所有文檔

### 🆘 **需要幫助？**
- **❓ 常見問題**: [FAQ](faq.md) - 快速解決問題
- **💬 聯繫我們**: [isyanghou@gmail.com](mailto:isyanghou@gmail.com)
- **🐛 問題回報**: [GitHub Issues](https://github.com/isyanghou/6Keys/issues)

---

**💡 提示**: 迷路了？隨時點擊頁面頂部的麵包屑導航返回 [📚 文檔中心](README.md)。