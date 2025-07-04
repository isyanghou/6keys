# ❓ 常見問題 | Frequently Asked Questions

**📍 當前位置**: [🏠 首頁](../README.md) > [📚 文檔中心](README.md) > ❓ 常見問題

本文檔回答使用六鑰臨界框架時的常見問題和疑難解答。

**🔍 快速查找**: 使用 `Ctrl+F` (Windows) 或 `Cmd+F` (Mac) 搜索關鍵詞

---

## 🚨 **緊急救援** | **Emergency Help**

| 問題類型 | 快速解決方案 | 詳細說明 |
|---------|-------------|----------|
| 🚫 **無法安裝** | [安裝指南](installation.md) | 詳細安裝步驟 |
| 💥 **程式崩潰** | [錯誤排除](#技術問題) | 常見錯誤解決 |
| 📊 **數據問題** | [數據處理](#數據處理) | 數據格式說明 |
| 🤔 **不知道怎麼用** | [快速開始](quickstart.md) | 5分鐘上手指南 |

## 🚀 安裝和設置 | Installation and Setup

### Q1: 支援哪些 Python 版本？
**A**: 六鑰臨界支援 Python 3.8 及以上版本。推薦使用 Python 3.10 或 3.11 以獲得最佳性能和兼容性。

### Q2: 安裝時出現依賴衝突怎麼辦？
**A**: 建議使用虛擬環境：
```bash
python -m venv sixkeys_env
source sixkeys_env/bin/activate  # Linux/macOS
# 或 sixkeys_env\Scripts\activate  # Windows
pip install sixkeys
```

### Q3: 如何在 Jupyter Notebook 中使用？
**A**: 確保在正確的環境中安裝 Jupyter：
```bash
pip install jupyter
pip install sixkeys
jupyter notebook
```

### Q4: Docker 版本和本地安裝有什麼區別？
**A**: Docker 版本包含預配置的環境和範例數據，適合快速試用。本地安裝更靈活，適合開發和生產使用。

## 📊 數據處理 | Data Processing

### Q5: 支援哪些數據格式？
**A**: 支援多種格式：
- **EEG/MEG**: EDF, BDF, FIF, SET
- **通用格式**: MAT, CSV, HDF5, NPY
- **自定義格式**: 通過 NumPy 數組接口

```python
from sixkeys.utils import data_loader

# EDF 格式
data = data_loader.load_edf('data.edf')

# MAT 格式
data = data_loader.load_mat('data.mat', variable_name='eeg_data')

# CSV 格式
data = data_loader.load_csv('data.csv')
```

### Q6: 數據的最小長度要求是什麼？
**A**: 
- **最小長度**: 30秒（推薦60秒以上）
- **採樣率**: 不低於100Hz（推薦250Hz以上）
- **通道數**: 至少1個通道（推薦8個以上）

### Q7: 如何處理不同採樣率的數據？
**A**: 使用重採樣功能：
```python
from sixkeys.preprocessing import resampling

# 重採樣到目標頻率
resampled_data = resampling.resample(data, 
                                   original_fs=1000, 
                                   target_fs=250)
```

### Q8: 如何處理缺失數據？
**A**: 提供多種處理方法：
```python
from sixkeys.preprocessing import missing_data

# 線性插值
filled_data = missing_data.interpolate(data, method='linear')

# 移除包含缺失值的段落
clean_data = missing_data.remove_missing_segments(data)

# 使用均值填充
filled_data = missing_data.fill_with_mean(data)
```

## 🧠 指標計算 | Metrics Computation

### Q9: 六個核心指標的正常範圍是什麼？
**A**: 所有指標都標準化到 [0, 1] 範圍：
- **0.3-0.7**: 通常為正常範圍
- **< 0.3**: 可能表示功能減退
- **> 0.7**: 可能表示過度活躍

具體解釋因指標而異，詳見[理論背景](theory.md)。

### Q10: 如何選擇合適的窗口大小？
**A**: 窗口大小選擇指南：
- **短窗口 (1-2秒)**: 適合快速變化的分析
- **中窗口 (2-5秒)**: 一般用途，平衡時間解析度和穩定性
- **長窗口 (5-10秒)**: 適合穩定狀態分析

```python
# 不同窗口大小的比較
results_short = metrics.compute_all_metrics(data, window_size=1.0)
results_medium = metrics.compute_all_metrics(data, window_size=3.0)
results_long = metrics.compute_all_metrics(data, window_size=5.0)
```

### Q11: 計算速度很慢，如何優化？
**A**: 幾種優化方法：
```python
# 1. 使用並行處理
from sixkeys.analysis import parallel_processing
results = parallel_processing.compute_metrics_parallel(data, n_jobs=4)

# 2. 使用GPU加速（如果可用）
from sixkeys.analysis import gpu_acceleration
results = gpu_acceleration.compute_metrics_gpu(data)

# 3. 降低數據解析度
downsampled_data = data[::2]  # 降採樣到一半

# 4. 使用分塊處理
from sixkeys.utils import chunked_processing
results = chunked_processing.process_in_chunks(data, chunk_size=1000)
```

### Q12: 如何處理多通道數據？
**A**: 提供多種處理策略：
```python
# 1. 逐通道計算
results_per_channel = {}
for i, channel in enumerate(channel_names):
    results_per_channel[channel] = metrics.compute_all_metrics(data[:, i:i+1])

# 2. 全腦平均
average_results = metrics.compute_all_metrics(data.mean(axis=1, keepdims=True))

# 3. 區域分析
frontal_channels = [0, 1, 2]  # 前額區通道索引
frontal_results = metrics.compute_all_metrics(data[:, frontal_channels])
```

## 📈 可視化 | Visualization

### Q13: 圖表顯示不正常怎麼辦？
**A**: 常見解決方案：
```python
# 1. 設置後端
import matplotlib
matplotlib.use('TkAgg')  # 或 'Qt5Agg'

# 2. 調整圖形大小
import matplotlib.pyplot as plt
plt.figure(figsize=(12, 8))

# 3. 清除之前的圖形
plt.clf()
plt.close('all')
```

### Q14: 如何自定義圖表樣式？
**A**: 使用樣式配置：
```python
from sixkeys.visualization import style_config

# 設置科學出版物樣式
style_config.set_publication_style()

# 自定義顏色方案
style_config.set_color_palette('viridis')

# 設置字體大小
style_config.set_font_sizes(title=16, label=14, tick=12)
```

### Q15: 如何導出高質量圖片？
**A**: 使用適當的導出設置：
```python
# 導出為矢量格式
plt.savefig('figure.svg', format='svg', dpi=300, bbox_inches='tight')

# 導出為高解析度PNG
plt.savefig('figure.png', dpi=300, bbox_inches='tight', 
           facecolor='white', edgecolor='none')

# 導出為PDF
plt.savefig('figure.pdf', format='pdf', bbox_inches='tight')
```

## 🔬 統計分析 | Statistical Analysis

### Q16: 如何進行組間比較？
**A**: 使用內建的統計工具：
```python
from sixkeys.statistics import group_comparison

# t檢驗
t_result = group_comparison.independent_t_test(group1_data, group2_data)

# 非參數檢驗
mw_result = group_comparison.mann_whitney_u(group1_data, group2_data)

# 多組比較
anova_result = group_comparison.one_way_anova(group1_data, group2_data, group3_data)
```

### Q17: 如何處理多重比較問題？
**A**: 應用多重比較校正：
```python
from sixkeys.statistics import multiple_comparisons

# FDR校正
corrected_p = multiple_comparisons.fdr_correction(p_values)

# Bonferroni校正
corrected_p = multiple_comparisons.bonferroni_correction(p_values)

# Holm校正
corrected_p = multiple_comparisons.holm_correction(p_values)
```

### Q18: 如何計算效應大小？
**A**: 提供多種效應大小指標：
```python
from sixkeys.statistics import effect_size

# Cohen's d
cohen_d = effect_size.cohens_d(group1_data, group2_data)

# Glass's delta
glass_delta = effect_size.glass_delta(group1_data, group2_data)

# 相關係數
r_effect = effect_size.correlation_effect_size(correlation_value, n_samples)
```

## 🎯 實際應用 | Practical Applications

### Q19: 如何用於臨床診斷？
**A**: 建議的臨床應用流程：
```python
# 1. 數據預處理
from sixkeys.clinical import preprocessing
clean_data = preprocessing.clinical_preprocessing(raw_data)

# 2. 計算指標
from sixkeys.clinical import assessment
clinical_metrics = assessment.compute_clinical_metrics(clean_data)

# 3. 生成報告
from sixkeys.clinical import reporting
report = reporting.generate_clinical_report(clinical_metrics, patient_info)
```

### Q20: 如何建立自己的基準值？
**A**: 建立基準值的步驟：
```python
# 1. 收集正常對照組數據
control_results = []
for control_data in control_dataset:
    results = metrics.compute_all_metrics(control_data)
    control_results.append(results)

# 2. 計算統計量
from sixkeys.statistics import normative_data
norms = normative_data.compute_normative_statistics(control_results)

# 3. 保存基準值
normative_data.save_norms(norms, 'my_normative_data.json')

# 4. 使用基準值
z_scores = normative_data.compute_z_scores(patient_results, norms)
```

## 🔧 技術問題 | Technical Issues

### Q21: 記憶體使用量過大怎麼辦？
**A**: 記憶體優化策略：
```python
# 1. 使用分塊處理
from sixkeys.utils import memory_management
memory_management.enable_chunked_processing(max_memory_gb=4)

# 2. 降低精度
import numpy as np
data = data.astype(np.float32)  # 使用32位而非64位

# 3. 清理不需要的變量
del large_variable
import gc
gc.collect()
```

### Q22: 如何在服務器上運行？
**A**: 服務器部署建議：
```python
# 1. 使用無頭模式
import matplotlib
matplotlib.use('Agg')  # 無GUI後端

# 2. 批量處理
from sixkeys.batch import server_processing
server_processing.run_batch_analysis(input_dir, output_dir)

# 3. 使用配置文件
from sixkeys.config import load_config
config = load_config('server_config.yaml')
```

### Q23: 如何與其他工具整合？
**A**: 整合示例：
```python
# 與MNE整合
import mne
from sixkeys.integrations import mne_integration

raw = mne.io.read_raw_edf('data.edf')
sixkeys_data = mne_integration.mne_to_sixkeys(raw)

# 與scikit-learn整合
from sklearn.model_selection import cross_val_score
from sixkeys.integrations import sklearn_integration

X = sklearn_integration.metrics_to_features(metrics_results)
y = labels
scores = cross_val_score(classifier, X, y)
```

## 📚 學習和支援 | Learning and Support

### Q24: 如何學習六鑰臨界理論？
**A**: 推薦學習路徑：
1. 閱讀[理論背景](theory.md)
2. 查看[完整論文](zh/paper/)
3. 實踐[快速開始](quickstart.md)
4. 嘗試[實驗指南](experiments.md)
5. 參與社區討論

### Q25: 如何獲得技術支援？
**A**: 支援渠道：
- **文檔**: 查看完整文檔
- **GitHub Issues**: 報告問題和功能請求
- **郵件支援**: isyanghou@gmail.com
- **社區論壇**: 參與討論和交流

### Q26: 如何貢獻代碼？
**A**: 貢獻流程：
1. 閱讀[開發者指南](developers.md)
2. Fork 儲存庫
3. 創建功能分支
4. 提交拉取請求
5. 參與代碼審查

### Q27: 如何引用六鑰臨界？
**A**: 學術引用格式：
```
Yang, H. (2024). Six Keys Criticality: A Neural Manifold Path to Consciousness. 
GitHub repository. https://github.com/isyanghou/6Keys
```

BibTeX格式：
```bibtex
@software{yang2024sixkeys,
  author = {Yang, Hou},
  title = {Six Keys Criticality: A Neural Manifold Path to Consciousness},
  url = {https://github.com/isyanghou/6Keys},
  year = {2024}
}
```

## 🆘 故障排除 | Troubleshooting

### 常見錯誤信息 | Common Error Messages

#### "ModuleNotFoundError: No module named 'sixkeys'"
**解決方案**: 重新安裝或檢查環境
```bash
pip install --force-reinstall sixkeys
```

#### "ValueError: Input data shape is invalid"
**解決方案**: 檢查數據格式
```python
print(f"Data shape: {data.shape}")  # 應該是 (time_points, channels)
data = data.T if data.shape[0] < data.shape[1] else data
```

#### "RuntimeError: CUDA out of memory"
**解決方案**: 減少批次大小或使用CPU
```python
# 強制使用CPU
import os
os.environ['CUDA_VISIBLE_DEVICES'] = ''
```

### 性能問題 | Performance Issues

如果遇到性能問題，請檢查：
1. 數據大小和複雜度
2. 可用記憶體和CPU核心數
3. 是否啟用了並行處理
4. 參數設置是否合理

---

## 🧭 **導航欄** | **Navigation**

**📍 當前位置**: [🏠 首頁](../README.md) > [📚 文檔中心](README.md) > ❓ **常見問題**

### 🔄 **相關頁面**
- **🚀 快速開始**: [快速開始指南](quickstart.md) - 5分鐘上手
- **⚙️ 安裝問題**: [安裝指南](installation.md) - 詳細安裝步驟
- **🧠 理論疑問**: [理論背景](theory.md) - 理論基礎
- **🔙 返回**: [📚 文檔中心](README.md) - 瀏覽所有文檔

### 🆘 **仍需幫助？**
- **💬 直接聯繫**: [isyanghou@gmail.com](mailto:isyanghou@gmail.com) - 專業技術支援
- **🐛 問題回報**: [GitHub Issues](https://github.com/isyanghou/6Keys/issues) - 回報錯誤或建議
- **💡 功能請求**: [GitHub Discussions](https://github.com/isyanghou/6Keys/discussions) - 討論新功能

### 📚 **其他資源**
- **🎯 實用教程**: [實驗指南](experiments.md) - 實驗設計方法
- **🎨 可視化**: [可視化教程](visualization.md) - 圖表製作
- **👨‍💻 開發**: [開發者指南](developers.md) - 貢獻代碼

---

**💡 提示**: 沒找到答案？嘗試在 [📚 文檔中心](README.md) 搜索相關主題，或直接聯繫我們獲得幫助。