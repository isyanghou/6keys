# 可視化教程 | Visualization Tutorial

本文檔詳細介紹六鑰臨界框架的可視化功能、使用方法和最佳實踐。

## 🎨 可視化模組概述 | Visualization Module Overview

六鑰臨界框架提供了強大的可視化工具，幫助研究者和臨床工作者直觀地理解和分析神經數據。可視化模組設計為易用、靈活且高度可定制，支援從基礎圖表到複雜的互動式儀表板。

### 主要功能 | Key Features

- **多維數據可視化**: 支援高維數據的降維和可視化
- **實時數據流**: 支援實時數據的動態可視化
- **互動式探索**: 提供參數調整和數據篩選功能
- **多模態整合**: 整合多種數據源和分析結果
- **報告生成**: 自動生成高質量的分析報告

## 📊 基礎可視化 | Basic Visualization

### 時間序列可視化 | Time Series Visualization

```python
from sixkeys.visualization import plots

# 載入範例數據
from sixkeys.utils import data_loader
data = data_loader.load_sample_data()

# 繪製多通道時間序列
plots.plot_time_series(data, channels=['Fz', 'Cz', 'Pz'], 
                      title='EEG Channels', 
                      time_range=[0, 10])

# 繪製時頻圖
plots.plot_spectrogram(data, channel='Cz', 
                      freq_range=[0, 50], 
                      colormap='viridis')
```

### 指標可視化 | Metrics Visualization

```python
from sixkeys.analysis import metrics
from sixkeys.visualization import plots

# 計算六個核心指標
results = metrics.compute_all_metrics(data)

# 繪製雷達圖
plots.plot_radar(results, title='Six Keys Metrics')

# 繪製時間變化趨勢
plots.plot_metrics_trend(results, time_window=5, 
                        overlap=0.5, 
                        smoothing=True)
```

### 統計可視化 | Statistical Visualization

```python
from sixkeys.visualization import stats_plots

# 繪製分佈圖
stats_plots.plot_distribution(results['critical_fluctuation'], 
                             kde=True, 
                             title='Critical Fluctuation Distribution')

# 繪製箱形圖比較
stats_plots.plot_boxplot(results, 
                        groups=['control', 'patient'], 
                        title='Group Comparison')

# 繪製相關矩陣
stats_plots.plot_correlation_matrix(results, 
                                   method='pearson', 
                                   cmap='coolwarm')
```

## 🌐 網絡可視化 | Network Visualization

### 腦網絡圖 | Brain Network Graph

```python
from sixkeys.visualization import network_plots

# 計算功能連接
from sixkeys.analysis import connectivity
conn_matrix = connectivity.compute_connectivity(data, method='plv')

# 繪製腦網絡圖
network_plots.plot_brain_network(conn_matrix, 
                               threshold=0.7, 
                               view='top', 
                               node_size='degree')

# 繪製連接矩陣
network_plots.plot_connectivity_matrix(conn_matrix, 
                                     labels=data.channel_names, 
                                     colormap='Reds')
```

### 動態網絡 | Dynamic Networks

```python
from sixkeys.visualization import dynamic_plots

# 計算時變連接
time_conn = connectivity.compute_time_varying_connectivity(data, 
                                                       window=2, 
                                                       step=0.5)

# 繪製動態網絡
dynamic_plots.plot_dynamic_network(time_conn, 
                                 frame_duration=200, 
                                 save_gif='dynamic_network.gif')

# 繪製網絡指標變化
dynamic_plots.plot_network_metrics_evolution(time_conn, 
                                          metrics=['clustering', 'path_length', 'efficiency'])
```

## 🎮 互動式可視化 | Interactive Visualization

### 互動式儀表板 | Interactive Dashboard

```python
from sixkeys.visualization import dashboard

# 創建儀表板
dash = dashboard.SixKeysDashboard(data)

# 添加組件
dash.add_time_series_panel()
dash.add_spectrogram_panel()
dash.add_metrics_panel()
dash.add_network_panel()

# 啟動儀表板
dash.run(port=8050)
```

### 參數探索 | Parameter Exploration

```python
from sixkeys.visualization import interactive

# 創建參數探索界面
explorer = interactive.ParameterExplorer(data)

# 添加參數滑塊
explorer.add_slider('window_size', 1, 10, 2, step=0.5)
explorer.add_slider('threshold', 0, 1, 0.5, step=0.05)
explorer.add_dropdown('metric', ['CF', 'CC', 'II', 'RS', 'SC', 'DS'])

# 設置回調函數
def update_plot(params):
    # 使用參數計算結果並更新圖表
    pass

explorer.set_callback(update_plot)

# 啟動界面
explorer.run()
```

## 📱 可視化演示模組 | Visualization Demo Module

六鑰臨界框架提供了一個獨立的可視化演示模組，可以快速展示和探索分析結果，無需編寫代碼。

### 命令行界面 | Command Line Interface

```bash
# 啟動基本演示
sixkeys-demo --data sample_data.edf

# 啟動網絡可視化
sixkeys-demo --mode network --data sample_data.edf

# 啟動完整儀表板
sixkeys-demo --mode dashboard --data sample_data.edf --port 8050

# 批量分析模式
sixkeys-demo --mode batch --data data_folder/ --output results/
```

### 配置選項 | Configuration Options

可以通過配置文件自定義演示模組的行為：

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

network:
  threshold_method: 'percentile'
  threshold_value: 90
  layout_algorithm: 'force'
```

使用配置文件：

```bash
sixkeys-demo --config demo_config.yaml --data sample_data.edf
```

## 🎯 高級技巧 | Advanced Techniques

### 自定義可視化 | Custom Visualization

```python
from sixkeys.visualization import base
import matplotlib.pyplot as plt
import numpy as np

# 創建自定義可視化類
class CustomPlot(base.BasePlot):
    def __init__(self, data):
        super().__init__(data)
    
    def plot(self, **kwargs):
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # 自定義繪圖邏輯
        x = np.linspace(0, 10, 100)
        y = np.sin(x) * self.data.mean(axis=0)
        ax.plot(x, y, **kwargs)
        
        return fig

# 使用自定義可視化
custom_plot = CustomPlot(data)
fig = custom_plot.plot(color='red', linewidth=2)
fig.savefig('custom_plot.png')
```

### 導出和共享 | Export and Sharing

```python
from sixkeys.visualization import export

# 導出為互動式HTML
export.to_html(fig, 'interactive_plot.html', include_js=True)

# 導出為儀表板應用
export.to_dashboard(results, 'dashboard_app', include_data=True)

# 生成完整報告
export.generate_report(results, 'analysis_report.pdf', 
                     template='scientific', 
                     include_code=True)
```

## 🖼️ 視覺化資源 | Visualization Resources

### 顏色方案 | Color Schemes

六鑰臨界框架提供了專門設計的顏色方案，適合科學可視化：

```python
from sixkeys.visualization import colors

# 使用預設顏色方案
cmap = colors.get_colormap('sixkeys')

# 使用特定指標的顏色
metric_colors = colors.get_metric_colors()
ax.plot(data, color=metric_colors['critical_fluctuation'])

# 獲取對比色方案
contrast_colors = colors.get_contrast_palette(n_colors=6)
```

### 模板庫 | Template Library

```python
from sixkeys.visualization import templates

# 使用科學出版物模板
fig = templates.scientific_figure(data, title='Analysis Results')

# 使用臨床報告模板
report = templates.clinical_report(patient_data, metrics_results)

# 使用演示模板
presentation = templates.presentation_slides(results, template='modern')
```

## 📋 最佳實踐 | Best Practices

### 可視化建議 | Visualization Tips

1. **保持簡潔**: 避免過度裝飾，專注於數據
2. **一致性**: 在整個分析中使用一致的顏色和風格
3. **適當標籤**: 確保所有軸和圖例都有清晰的標籤
4. **色盲友好**: 使用色盲友好的調色板
5. **互動性**: 對於複雜數據，提供互動式探索功能

### 效能優化 | Performance Optimization

1. **數據降採樣**: 對於大型數據集，使用降採樣提高繪圖速度
2. **惰性加載**: 使用惰性加載技術處理大型數據集
3. **GPU加速**: 啟用GPU加速渲染
4. **向量格式**: 使用SVG等向量格式保存高質量圖表

---

**返回**: [文檔導航](README.md) | **相關**: [API參考](api/) | **下一步**: [實驗指南](experiments.md)