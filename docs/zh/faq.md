# 常見問題 (FAQ)

本文檔回答使用六鑰臨界框架時的常見問題。

## 安裝相關問題

### Q1: 安裝時出現依賴衝突怎麼辦？

**A:** 建議使用虛擬環境來避免依賴衝突：

```bash
# 創建虛擬環境
python -m venv sixkeys_env

# 激活環境 (Windows)
sixkeys_env\Scripts\activate

# 激活環境 (macOS/Linux)
source sixkeys_env/bin/activate

# 安裝六鑰
pip install sixkeys
```

### Q2: 在 Conda 環境中如何安裝？

**A:** 推薦使用提供的環境配置文件：

```bash
# 使用環境配置文件
conda env create -f environment.yml
conda activate sixkeys

# 或手動創建環境
conda create -n sixkeys python=3.9
conda activate sixkeys
pip install sixkeys
```

### Q3: 安裝後導入失敗怎麼辦？

**A:** 檢查安裝是否成功：

```python
# 檢查安裝
try:
    import sixkeys as sk
    print(f"✓ 安裝成功，版本: {sk.__version__}")
except ImportError as e:
    print(f"✗ 導入失敗: {e}")
    print("請嘗試重新安裝: pip install --upgrade sixkeys")
```

## 使用相關問題

### Q4: 如何選擇合適的參數？

**A:** 參數選擇建議：

```python
# 對於實時分析（速度優先）
fast_analyzer = sk.SixKeysAnalyzer(
    felc_params={'sim_time': 5.0, 'n_samples': 25},
    teb_params={'sim_time': 5.0, 'n_samples': 25}
)

# 對於精確分析（精度優先）
accurate_analyzer = sk.SixKeysAnalyzer(
    felc_params={'sim_time': 20.0, 'n_samples': 100},
    teb_params={'sim_time': 20.0, 'n_samples': 100}
)

# 對於特定應用場景
clinical_analyzer = sk.SixKeysAnalyzer(
    theta_c=0.8,  # 更敏感的閾值
    weights={'zeta1': 0.3, 'zeta2': 0.3, 'zeta3': 0.1, 
             'zeta4': 0.1, 'zeta5': 0.1, 'zeta6': 0.1}
)
```

### Q5: 數據格式要求是什麼？

**A:** 數據格式要求：

```python
import numpy as np

# 正確的數據格式
# 形狀: (時間點數, 通道數)
data = np.random.randn(5000, 64)  # 5000個時間點，64個通道

# 檢查數據格式
def check_data_format(data):
    if not isinstance(data, np.ndarray):
        raise TypeError("數據必須是 NumPy 數組")
    
    if data.ndim != 2:
        raise ValueError("數據必須是二維數組 (時間點, 通道)")
    
    if data.shape[0] < 100:
        print("警告: 時間點數量較少，可能影響分析精度")
    
    if data.shape[1] < 8:
        print("警告: 通道數量較少，可能影響分析穩定性")
    
    print(f"✓ 數據格式正確: {data.shape[0]} 時間點, {data.shape[1]} 通道")

check_data_format(data)
```

### Q6: 如何處理缺失數據？

**A:** 缺失數據處理方法：

```python
import numpy as np
from scipy import interpolate

def handle_missing_data(data, method='interpolate'):
    """
    處理缺失數據
    
    Parameters:
    -----------
    data : np.ndarray
        原始數據，NaN 表示缺失值
    method : str
        處理方法: 'interpolate', 'remove', 'zero_fill'
    """
    if method == 'interpolate':
        # 線性插值
        for ch in range(data.shape[1]):
            mask = ~np.isnan(data[:, ch])
            if np.sum(mask) > 1:
                f = interpolate.interp1d(
                    np.where(mask)[0], data[mask, ch], 
                    kind='linear', fill_value='extrapolate'
                )
                data[:, ch] = f(np.arange(len(data)))
    
    elif method == 'remove':
        # 移除包含缺失值的時間點
        mask = ~np.isnan(data).any(axis=1)
        data = data[mask]
    
    elif method == 'zero_fill':
        # 用零填充
        data = np.nan_to_num(data, nan=0.0)
    
    return data

# 使用示例
data_with_nan = np.random.randn(1000, 32)
data_with_nan[100:110, 5] = np.nan  # 模擬缺失數據

clean_data = handle_missing_data(data_with_nan, method='interpolate')
analyzer = sk.SixKeysAnalyzer()
result = analyzer.analyze_data(clean_data)
```

### Q7: 如何解釋分析結果？

**A:** 結果解釋指南：

```python
def interpret_results(result):
    """
    解釋分析結果
    """
    print(f"=== 六鑰臨界分析結果 ===")
    print(f"總距離 D_w: {result.d_total:.3f}")
    print(f"預測狀態: {result.predicted_state}")
    print(f"臨界閾值: {result.theta_c:.3f}")
    print()
    
    # 各指標解釋
    indicators = {
        'zeta1': 'FELC (自由能極限環)',
        'zeta2': 'TEB (資訊-能耗效率)',
        'zeta3': 'RFI (Ricci曲率流)',
        'zeta4': 'ECGP (因果圖滲透)',
        'zeta5': 'PWC (相位環流)',
        'zeta6': 'ACI (星膠耦合)'
    }
    
    print("各指標值:")
    for key, name in indicators.items():
        value = getattr(result, key)
        print(f"  {name}: {value:.3f}")
    print()
    
    # 狀態解釋
    if result.predicted_state == 'awake':
        print("解釋: 系統處於清醒狀態，各指標接近正常範圍")
    elif result.predicted_state == 'light_sedation':
        print("解釋: 系統處於輕度鎮靜狀態，部分指標偏離正常範圍")
    elif result.predicted_state == 'deep_anesthesia':
        print("解釋: 系統處於深度麻醉狀態，多數指標顯著偏離正常範圍")
    
    # 臨界性評估
    if result.d_total < result.theta_c * 0.5:
        print("臨界性: 低 - 系統穩定")
    elif result.d_total < result.theta_c:
        print("臨界性: 中等 - 系統接近臨界點")
    else:
        print("臨界性: 高 - 系統處於臨界轉換狀態")

# 使用示例
analyzer = sk.SixKeysAnalyzer()
result = analyzer.analyze_simulated_data('light_sedation')
interpret_results(result)
```

## 性能相關問題

### Q8: 分析速度太慢怎麼辦？

**A:** 性能優化建議：

```python
# 1. 減少模擬時間
fast_params = {
    'sim_time': 5.0,    # 從默認的 10.0 減少到 5.0
    'n_samples': 25,    # 從默認的 50 減少到 25
    'dt': 0.02          # 從默認的 0.01 增加到 0.02
}

fast_analyzer = sk.SixKeysAnalyzer(
    felc_params=fast_params,
    teb_params=fast_params,
    rfi_params=fast_params,
    ecgp_params=fast_params,
    pwc_params=fast_params,
    aci_params=fast_params
)

# 2. 並行處理多個數據集
from multiprocessing import Pool
import time

def analyze_single_dataset(data):
    analyzer = sk.SixKeysAnalyzer()
    return analyzer.analyze_data(data)

# 串行處理
start_time = time.time()
serial_results = [analyze_single_dataset(data) for data in datasets]
serial_time = time.time() - start_time

# 並行處理
start_time = time.time()
with Pool() as pool:
    parallel_results = pool.map(analyze_single_dataset, datasets)
parallel_time = time.time() - start_time

print(f"串行處理時間: {serial_time:.2f} 秒")
print(f"並行處理時間: {parallel_time:.2f} 秒")
print(f"加速比: {serial_time/parallel_time:.2f}x")
```

### Q9: 內存使用過多怎麼辦？

**A:** 內存優化策略：

```python
import gc

def memory_efficient_analysis(large_data, chunk_size=1000):
    """
    內存高效的大數據分析
    """
    analyzer = sk.SixKeysAnalyzer()
    results = []
    
    # 分塊處理
    for i in range(0, len(large_data), chunk_size):
        chunk = large_data[i:i+chunk_size]
        
        # 分析當前塊
        result = analyzer.analyze_data(chunk)
        results.append(result)
        
        # 強制垃圾回收
        del chunk
        gc.collect()
        
        print(f"處理進度: {min(i+chunk_size, len(large_data))}/{len(large_data)}")
    
    return results

# 監控內存使用
import psutil
import os

def monitor_memory():
    process = psutil.Process(os.getpid())
    memory_mb = process.memory_info().rss / 1024 / 1024
    print(f"當前內存使用: {memory_mb:.1f} MB")

# 使用示例
monitor_memory()
large_dataset = np.random.randn(50000, 64)  # 大數據集
results = memory_efficient_analysis(large_dataset)
monitor_memory()
```

## 錯誤處理問題

### Q10: 常見錯誤及解決方法？

**A:** 常見錯誤處理：

```python
from sixkeys.exceptions import (
    SixKeysError, DataFormatError, 
    ParameterError, AnalysisError
)

def robust_analysis(data, **kwargs):
    """
    穩健的分析函數，包含錯誤處理
    """
    try:
        analyzer = sk.SixKeysAnalyzer(**kwargs)
        result = analyzer.analyze_data(data)
        return result, None
        
    except DataFormatError as e:
        error_msg = f"數據格式錯誤: {e}"
        print(error_msg)
        print("建議: 檢查數據維度和類型")
        return None, error_msg
        
    except ParameterError as e:
        error_msg = f"參數錯誤: {e}"
        print(error_msg)
        print("建議: 檢查參數範圍和類型")
        return None, error_msg
        
    except AnalysisError as e:
        error_msg = f"分析計算錯誤: {e}"
        print(error_msg)
        print("建議: 檢查數據質量或調整參數")
        return None, error_msg
        
    except Exception as e:
        error_msg = f"未知錯誤: {e}"
        print(error_msg)
        print("建議: 聯繫技術支持")
        return None, error_msg

# 使用示例
data = np.random.randn(1000, 32)
result, error = robust_analysis(data)

if result is not None:
    print(f"分析成功: D_w = {result.d_total:.3f}")
else:
    print(f"分析失敗: {error}")
```

## 可視化問題

### Q11: 如何自定義可視化？

**A:** 自定義可視化示例：

```python
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle

def custom_radar_chart(results, title="自定義雷達圖"):
    """
    創建自定義雷達圖
    """
    # 設置中文字體
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    
    # 指標名稱
    labels = ['FELC\n(ζ₁)', 'TEB\n(ζ₂)', 'RFI\n(ζ₃)', 
              'ECGP\n(ζ₄)', 'PWC\n(ζ₅)', 'ACI\n(ζ₆)']
    
    # 角度設置
    angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]  # 閉合圖形
    
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
    
    # 繪製多個結果
    colors = ['red', 'blue', 'green', 'orange', 'purple']
    
    for i, (name, result) in enumerate(results.items()):
        values = [getattr(result, f'zeta{j+1}') for j in range(6)]
        values += values[:1]  # 閉合圖形
        
        ax.plot(angles, values, 'o-', linewidth=2, 
                label=name, color=colors[i % len(colors)])
        ax.fill(angles, values, alpha=0.25, color=colors[i % len(colors)])
    
    # 設置標籤
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    ax.set_ylim(0, max([max([getattr(r, f'zeta{j+1}') for j in range(6)]) 
                       for r in results.values()]) * 1.1)
    
    # 添加網格線
    ax.grid(True)
    ax.set_title(title, size=16, fontweight='bold', pad=20)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
    
    plt.tight_layout()
    return fig

def custom_time_series_plot(time_results, title="時間序列分析"):
    """
    創建時間序列圖
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
        axes[i].set_xlabel('時間點')
        axes[i].set_ylabel('指標值')
        axes[i].grid(True, alpha=0.3)
    
    plt.suptitle(title, size=16, fontweight='bold')
    plt.tight_layout()
    return fig

# 使用示例
analyzer = sk.SixKeysAnalyzer()
results = {
    '清醒': analyzer.analyze_simulated_data('awake'),
    '輕度鎮靜': analyzer.analyze_simulated_data('light_sedation'),
    '深度麻醉': analyzer.analyze_simulated_data('deep_anesthesia')
}

fig1 = custom_radar_chart(results)
plt.show()
```

### Q12: 如何保存高質量圖片？

**A:** 高質量圖片保存：

```python
def save_high_quality_figure(fig, filename, dpi=300, format='png'):
    """
    保存高質量圖片
    """
    # 支持的格式
    supported_formats = ['png', 'pdf', 'svg', 'eps', 'jpg']
    
    if format not in supported_formats:
        raise ValueError(f"不支持的格式: {format}")
    
    # 設置保存參數
    save_kwargs = {
        'dpi': dpi,
        'bbox_inches': 'tight',
        'pad_inches': 0.1,
        'facecolor': 'white',
        'edgecolor': 'none'
    }
    
    # 根據格式調整參數
    if format in ['jpg', 'jpeg']:
        save_kwargs['quality'] = 95
    
    # 保存圖片
    full_filename = f"{filename}.{format}"
    fig.savefig(full_filename, format=format, **save_kwargs)
    print(f"圖片已保存: {full_filename}")
    
    return full_filename

# 使用示例
analyzer = sk.SixKeysAnalyzer()
result = analyzer.analyze_simulated_data()
fig = analyzer.plot_radar_chart({'測試': result})

# 保存不同格式
save_high_quality_figure(fig, 'radar_chart', dpi=300, format='png')
save_high_quality_figure(fig, 'radar_chart', dpi=300, format='pdf')
save_high_quality_figure(fig, 'radar_chart', dpi=300, format='svg')
```

## 高級應用問題

### Q13: 如何進行批量分析和統計比較？

**A:** 批量分析示例：

```python
import pandas as pd
from scipy import stats
import seaborn as sns

def batch_analysis_with_statistics(datasets, labels, n_bootstrap=100):
    """
    批量分析並進行統計比較
    """
    analyzer = sk.SixKeysAnalyzer()
    all_results = []
    
    # 批量分析
    for dataset, label in zip(datasets, labels):
        for i in range(n_bootstrap):
            # 添加不同的隨機種子進行bootstrap
            analyzer_boot = sk.SixKeysAnalyzer(random_state=i)
            result = analyzer_boot.analyze_data(dataset)
            
            result_dict = {
                'label': label,
                'bootstrap_id': i,
                'D_w': result.d_total,
                'state': result.predicted_state
            }
            
            # 添加各個指標
            for j in range(1, 7):
                result_dict[f'zeta{j}'] = getattr(result, f'zeta{j}')
            
            all_results.append(result_dict)
    
    # 轉換為DataFrame
    df = pd.DataFrame(all_results)
    
    # 統計分析
    print("=== 描述性統計 ===")
    print(df.groupby('label')['D_w'].describe())
    print()
    
    # 組間比較
    groups = [group['D_w'].values for name, group in df.groupby('label')]
    
    if len(groups) == 2:
        # t檢驗
        t_stat, p_value = stats.ttest_ind(groups[0], groups[1])
        print(f"t檢驗結果: t={t_stat:.3f}, p={p_value:.3f}")
    else:
        # 方差分析
        f_stat, p_value = stats.f_oneway(*groups)
        print(f"ANOVA結果: F={f_stat:.3f}, p={p_value:.3f}")
    
    # 可視化
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    # 箱線圖
    sns.boxplot(data=df, x='label', y='D_w', ax=axes[0])
    axes[0].set_title('D_w 分布比較')
    axes[0].set_ylabel('加權距離 (D_w)')
    
    # 小提琴圖
    sns.violinplot(data=df, x='label', y='D_w', ax=axes[1])
    axes[1].set_title('D_w 密度分布')
    axes[1].set_ylabel('加權距離 (D_w)')
    
    plt.tight_layout()
    plt.show()
    
    return df

# 使用示例
# 生成模擬數據
datasets = [
    np.random.randn(1000, 32),  # 數據集1
    np.random.randn(1000, 32),  # 數據集2
    np.random.randn(1000, 32)   # 數據集3
]
labels = ['組別A', '組別B', '組別C']

results_df = batch_analysis_with_statistics(datasets, labels)
```

### Q14: 如何進行實時分析？

**A:** 實時分析實現：

```python
import threading
import queue
import time
from collections import deque

class RealTimeAnalyzer:
    """
    實時六鑰分析器
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
        添加新數據點
        
        Parameters:
        -----------
        new_data : np.ndarray
            新數據，形狀為 (n_channels,)
        """
        self.data_buffer.append(new_data)
    
    def _analysis_worker(self):
        """
        分析工作線程
        """
        while self.is_running:
            if len(self.data_buffer) >= self.window_size:
                # 獲取當前窗口數據
                current_data = np.array(list(self.data_buffer))
                
                try:
                    # 執行分析
                    result = self.analyzer.analyze_data(current_data)
                    
                    # 將結果放入隊列
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
        開始實時分析
        """
        if not self.is_running:
            self.is_running = True
            self.analysis_thread = threading.Thread(target=self._analysis_worker)
            self.analysis_thread.start()
            print("實時分析已開始")
    
    def stop(self):
        """
        停止實時分析
        """
        if self.is_running:
            self.is_running = False
            if self.analysis_thread:
                self.analysis_thread.join()
            print("實時分析已停止")
    
    def get_latest_result(self):
        """
        獲取最新分析結果
        """
        try:
            return self.result_queue.get_nowait()
        except queue.Empty:
            return None

# 使用示例
def simulate_real_time_data():
    """
    模擬實時數據流
    """
    rt_analyzer = RealTimeAnalyzer(window_size=500, update_interval=0.5)
    rt_analyzer.start()
    
    try:
        # 模擬數據流
        for i in range(1000):
            # 生成新數據點
            new_data = np.random.randn(32)  # 32個通道
            rt_analyzer.add_data(new_data)
            
            # 檢查是否有新結果
            latest_result = rt_analyzer.get_latest_result()
            if latest_result:
                if latest_result['status'] == 'success':
                    result = latest_result['result']
                    print(f"時間 {i}: D_w = {result.d_total:.3f}, "
                          f"狀態 = {result.predicted_state}")
                else:
                    print(f"時間 {i}: 分析錯誤 - {latest_result['error']}")
            
            time.sleep(0.1)  # 模擬數據採集間隔
    
    finally:
        rt_analyzer.stop()

# 運行實時分析示例
# simulate_real_time_data()
```

## 技術支持

### Q15: 如何報告問題或請求功能？

**A:** 問題報告流程：

1. **檢查現有問題**: 首先查看 [GitHub Issues](https://github.com/yourusername/sixkeys/issues)
2. **準備信息**: 包括錯誤信息、系統環境、重現步驟
3. **創建Issue**: 使用提供的模板創建新問題

```python
# 收集系統信息用於問題報告
import sys
import platform
import numpy as np
import scipy
import matplotlib

def collect_system_info():
    """
    收集系統信息用於問題報告
    """
    info = {
        'Python版本': sys.version,
        '操作系統': platform.platform(),
        'NumPy版本': np.__version__,
        'SciPy版本': scipy.__version__,
        'Matplotlib版本': matplotlib.__version__
    }
    
    try:
        import sixkeys
        info['SixKeys版本'] = sixkeys.__version__
    except:
        info['SixKeys版本'] = '未安裝或導入失敗'
    
    print("=== 系統信息 ===")
    for key, value in info.items():
        print(f"{key}: {value}")
    
    return info

# 使用示例
system_info = collect_system_info()
```

### Q16: 如何獲得更多幫助？

**A:** 獲取幫助的途徑：

1. **文檔**: 查看完整文檔 [docs/](../)
2. **示例**: 參考 [examples/](../../examples/) 目錄
3. **社區**: 加入 [GitHub Discussions](https://github.com/yourusername/sixkeys/discussions)
4. **郵件**: 聯繫維護者 [maintainer@sixkeys.org](mailto:maintainer@sixkeys.org)

```python
# 快速幫助函數
def get_help(topic=None):
    """
    獲取幫助信息
    """
    help_topics = {
        'installation': '安裝指南: docs/zh/installation.md',
        'quickstart': '快速開始: docs/zh/quickstart.md',
        'api': 'API參考: docs/api/',
        'theory': '理論背景: docs/zh/theory.md',
        'examples': '使用示例: examples/',
        'faq': '常見問題: docs/zh/faq.md'
    }
    
    if topic is None:
        print("可用的幫助主題:")
        for key, desc in help_topics.items():
            print(f"  {key}: {desc}")
        print("\n使用方法: get_help('topic_name')")
    elif topic in help_topics:
        print(f"幫助: {help_topics[topic]}")
    else:
        print(f"未知主題: {topic}")
        print("可用主題:", list(help_topics.keys()))

# 使用示例
get_help()  # 顯示所有主題
get_help('installation')  # 獲取安裝幫助
```

---

**注意**: 如果您的問題在此FAQ中沒有找到答案，請不要猶豫聯繫我們。我們會持續更新此文檔以包含更多常見問題。