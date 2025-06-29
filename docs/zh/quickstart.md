# 快速開始指南

歡迎使用六鑰臨界框架！本指南將在 5 分鐘內帶您了解基本功能。

## 🚀 第一個程序

### 1. 導入庫

```python
import sixkeys as sk
import numpy as np
import matplotlib.pyplot as plt

# 檢查版本
print(f"Six Keys 版本: {sk.__version__}")
```

### 2. 創建分析器

```python
# 初始化六鑰分析器
analyzer = sk.SixKeysAnalyzer(
    theta_c=1.0,  # 臨界閾值
    random_state=42  # 隨機種子，確保結果可重現
)

print("分析器初始化完成！")
```

### 3. 分析模擬數據

```python
# 分析不同意識狀態
states = ['awake', 'light_sedation', 'deep_anesthesia']
results = {}

for state in states:
    result = analyzer.analyze_simulated_data(
        consciousness_state=state,
        duration=5.0,  # 5秒數據
        dt=0.01       # 10ms 時間步長
    )
    results[state] = result
    print(f"{state}: D_w = {result.d_total:.3f}, 狀態 = {result.consciousness_state}")
```

### 4. 可視化結果

```python
# 繪製雷達圖
fig = analyzer.plot_radar_chart(results)
plt.show()

# 繪製相位圖
fig = analyzer.plot_phase_diagram(results)
plt.show()
```

## 📊 核心功能演示

### 單個指標分析

```python
from sixkeys.core import FELC, TEB, RFI

# FELC (自由能極限環) 分析
felc = FELC(sim_time=10.0, dt=0.01)
felc_results = felc.analyze_states()

# 繪製 FELC 結果
fig = felc.plot_results(felc_results)
plt.title('FELC 分析結果')
plt.show()

# TEB (資訊-能耗效率) 分析
teb = TEB(sim_time=10.0, dt=0.05)
teb_results = teb.analyze_states()

# 繪製 TEB 結果
fig = teb.plot_results(teb_results)
plt.title('TEB 分析結果')
plt.show()
```

### 批量數據處理

```python
# 模擬多個受試者的數據
subjects = ['subject_01', 'subject_02', 'subject_03']
batch_results = {}

for subject in subjects:
    # 為每個受試者設置不同的隨機種子
    analyzer.random_state = hash(subject) % 1000
    
    result = analyzer.analyze_simulated_data(
        consciousness_state='awake',
        duration=3.0
    )
    batch_results[subject] = result
    
    print(f"{subject}: D_w = {result.d_total:.3f}")

# 統計分析
d_values = [r.d_total for r in batch_results.values()]
print(f"平均 D_w: {np.mean(d_values):.3f} ± {np.std(d_values):.3f}")
```

## 🎯 實際數據分析

### 處理自定義數據

```python
# 假設您有 EEG 數據 (時間 × 通道)
# data.shape = (時間點數, 通道數)

# 生成示例數據
n_timepoints = 1000
n_channels = 64
sample_data = np.random.randn(n_timepoints, n_channels)

# 使用真實數據進行分析
# 注意：這需要實現數據預處理管道
# real_results = analyzer.analyze_real_data(sample_data)

print("實際數據分析功能正在開發中...")
```

### 自定義參數配置

```python
# 創建自定義權重的分析器
custom_weights = {
    'zeta1': 0.30,  # FELC 權重增加
    'zeta2': 0.20,  # TEB 權重增加
    'zeta3': 0.15,  # RFI
    'zeta4': 0.15,  # ECGP
    'zeta5': 0.10,  # PWC
    'zeta6': 0.10,  # ACI
}

custom_analyzer = sk.SixKeysAnalyzer(
    theta_c=0.8,  # 更嚴格的臨界閾值
    weights=custom_weights,
    enable_indicators=['FELC', 'TEB', 'RFI']  # 只啟用前三個指標
)

# 使用自定義分析器
custom_result = custom_analyzer.analyze_simulated_data('awake')
print(f"自定義分析: D_w = {custom_result.d_total:.3f}")
```

## 📈 高級可視化

### 時間序列分析

```python
# 分析時間演化
time_series_result = analyzer.analyze_time_evolution(
    consciousness_state='awake',
    duration=20.0,
    window_size=2.0,  # 2秒滑動窗口
    step_size=0.5     # 0.5秒步長
)

# 繪製時間演化圖
fig, axes = plt.subplots(2, 1, figsize=(12, 8))

# D_w 隨時間變化
axes[0].plot(time_series_result['time'], time_series_result['d_total'])
axes[0].axhline(y=analyzer.theta_c, color='r', linestyle='--', label='臨界閾值')
axes[0].set_ylabel('D_w')
axes[0].set_title('總距離隨時間變化')
axes[0].legend()
axes[0].grid(True)

# 各指標隨時間變化
for i, (key, values) in enumerate(time_series_result['zeta_values'].items()):
    axes[1].plot(time_series_result['time'], values, label=key)

axes[1].set_xlabel('時間 (秒)')
axes[1].set_ylabel('ζ 值')
axes[1].set_title('各指標隨時間變化')
axes[1].legend()
axes[1].grid(True)

plt.tight_layout()
plt.show()
```

### 統計比較

```python
# 比較不同狀態的統計特性
from sixkeys.utils import statistical_comparison

# 生成多次測量數據
n_trials = 20
comparison_data = {}

for state in ['awake', 'light_sedation', 'deep_anesthesia']:
    state_results = []
    for trial in range(n_trials):
        result = analyzer.analyze_simulated_data(
            consciousness_state=state,
            duration=2.0
        )
        state_results.append(result.d_total)
    comparison_data[state] = state_results

# 統計檢驗
stats_result = statistical_comparison(comparison_data)
print("統計比較結果:")
for comparison, p_value in stats_result.items():
    print(f"{comparison}: p = {p_value:.4f}")

# 箱線圖
plt.figure(figsize=(10, 6))
plt.boxplot(comparison_data.values(), labels=comparison_data.keys())
plt.ylabel('D_w')
plt.title('不同意識狀態的 D_w 分布')
plt.grid(True, alpha=0.3)
plt.show()
```

## 🔧 配置和設置

### 保存和載入配置

```python
# 保存分析器配置
config = analyzer.get_config()
sk.save_config(config, 'my_analysis_config.yaml')

# 載入配置
loaded_config = sk.load_config('my_analysis_config.yaml')
new_analyzer = sk.SixKeysAnalyzer.from_config(loaded_config)

print("配置保存和載入完成！")
```

### 結果導出

```python
# 導出結果到不同格式
result = analyzer.analyze_simulated_data('awake')

# 導出為 JSON
sk.export_results(result, 'analysis_result.json', format='json')

# 導出為 CSV
sk.export_results(result, 'analysis_result.csv', format='csv')

# 導出為 MATLAB 格式
sk.export_results(result, 'analysis_result.mat', format='matlab')

print("結果導出完成！")
```

## 📚 下一步學習

恭喜！您已經掌握了六鑰臨界框架的基本使用。接下來建議：

1. **深入學習**: 閱讀 [詳細教程](tutorials/basic_tutorial.md)
2. **理論背景**: 了解 [六鑰理論](../theory/overview.md)
3. **API 文檔**: 查看 [完整 API 參考](api_reference.md)
4. **實際應用**: 探索 [應用示例](examples/)
5. **進階功能**: 學習 [高級教程](tutorials/advanced_tutorial.md)

## 💡 提示和技巧

- **性能優化**: 對於大型數據集，考慮使用批處理模式
- **參數調優**: 根據您的具體應用調整權重和閾值
- **可視化**: 使用不同的繪圖選項來探索數據
- **驗證**: 始終在已知數據上驗證您的分析管道

## 🆘 需要幫助？

- 查看 [常見問題](faq.md)
- 瀏覽 [GitHub Issues](https://github.com/yourusername/sixkeys/issues)
- 參考 [API 文檔](api_reference.md)
- 聯繫開發團隊

---

**下一步**: [基礎教程](tutorials/basic_tutorial.md) - 深入了解每個指標的含義和應用