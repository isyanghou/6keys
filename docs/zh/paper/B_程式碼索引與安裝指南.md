---
title: "B_程式碼索引與安裝指南"
date: 2025-06-28
language: zh-TW
encoding: UTF-8
---

# 附錄 B　程式碼索引與安裝指南

本附錄提供六鑰臨界框架的完整程式碼索引、安裝指南和使用說明。所有程式碼以 **BSD 3-Clause** 授權釋出，論文內容採用 **CC BY-NC 4.0** 授權。

**GitHub 倉庫**：https://github.com/isyanghou/6Keys  
**作者**：You Yang Hou (isyanghou@gmail.com)  
**ORCID**：0009-0000-7041-8574

## B.1 專案結構總覽

```
sixkeys/
│
├── sixkeys/                    # 核心 Python 套件
│   ├── __init__.py             # 套件初始化
│   ├── core/                   # 六個核心指標實現
│   │   ├── felc.py            # FELC (ζ₁) - 自由能極限環
│   │   ├── teb.py             # TEB (ζ₂) - 資訊-能耗效率
│   │   ├── rfi.py             # RFI (ζ₃) - Ricci曲率臨界流
│   │   ├── ecgp.py            # ECGP (ζ₄) - 因果滲流
│   │   ├── pwc.py             # PWC (ζ₅) - 相位拓撲環流
│   │   └── aci.py             # ACI (ζ₆) - 神經-星膠耦合臨界
│   ├── analysis/               # 分析工具
│   │   ├── analyzer.py        # 主要分析器類別
│   │   ├── cross_validation.py # 交叉驗證實現
│   │   └── public_data.py     # 公開資料重分析
│   ├── utils/                  # 工具函式庫
│   │   ├── data_io.py         # 數據輸入輸出
│   │   ├── preprocessing.py   # 數據預處理
│   │   ├── visualization.py   # 可視化工具
│   │   └── metrics.py         # 評估指標
│   └── demos/                  # 演示模組
│       ├── radar_chart.py     # 雷達圖可視化
│       ├── cross_validation.py # 交叉驗證演示
│       └── public_data_analysis.py # 公開數據分析演示
│
├── docs/                       # 文檔系統
│   ├── zh/                    # 中文文檔
│   │   ├── installation.md    # 安裝指南
│   │   ├── quickstart.md      # 快速開始
│   │   ├── theory.md          # 理論背景
│   │   └── faq.md             # 常見問題
│   ├── en/                    # 英文文檔
│   │   ├── installation.md    # Installation Guide
│   │   ├── quickstart.md      # Quick Start
│   │   ├── theory.md          # Theory Background
│   │   └── faq.md             # FAQ
│   └── api/                   # API 參考文檔
│
├── examples/                   # 使用範例
│   ├── basic_usage.py         # 基本使用示例
│   └── demo_visualization.py  # 可視化演示
│
├── notebooks/                  # Jupyter 筆記本
│   └── 01_basic_usage.ipynb   # 基本使用教程
│
├── scripts/                    # 腳本工具
│   └── analyze.py             # 分析腳本
│
├── tests/                      # 測試套件
│   └── test_core/             # 核心模組測試
│       ├── test_felc.py       # FELC 測試
│       └── test_all_indicators.py # 全指標測試
│
├── data/                       # 數據目錄
├── results/                    # 結果輸出目錄
│
├── pyproject.toml             # 專案配置
├── requirements.txt           # Python 依賴
├── environment.yml            # Conda 環境配置
├── Dockerfile                 # Docker 容器配置
├── docker-compose.yml         # Docker Compose 配置
├── setup.py                   # 安裝腳本
├── setup.cfg                  # 安裝配置
├── MANIFEST.in                # 打包清單
├── CITATION.cff               # 引用格式
├── CONTRIBUTING.md            # 貢獻指南
├── CHANGELOG.md               # 變更日誌
├── LICENSE                    # BSD 3-Clause 授權
├── LICENSE-PAPER              # CC BY-NC 4.0 授權
└── README.md                  # 專案說明
```

## B.2 安裝指南

### B.2.1 系統需求

- **Python**: 3.8 或更高版本
- **作業系統**: Windows, macOS, Linux
- **記憶體**: 建議 8GB 以上
- **硬碟空間**: 至少 2GB 可用空間

### B.2.2 安裝方式

#### 方法一：PyPI 安裝（推薦）

```bash
# 基本安裝
pip install sixkeys

# 完整安裝（包含所有可選依賴）
pip install "sixkeys[all]"

# 開發版本安裝
pip install "sixkeys[dev]"
```

#### 方法二：Conda 環境安裝

```bash
# 下載專案
git clone https://github.com/isyanghou/6Keys.git
cd 6Keys

# 創建並啟用 Conda 環境
conda env create -f environment.yml
conda activate sixkeys

# 安裝套件
pip install -e .
```

#### 方法三：Docker 容器部署

```bash
# 拉取 Docker 鏡像
docker pull sixkeys/sixkeys:latest

# 或使用 Docker Compose
docker-compose up jupyter  # 啟動 Jupyter Lab
docker-compose up analysis  # 啟動分析服務
```

#### 方法四：源碼安裝

```bash
# 克隆倉庫
git clone https://github.com/isyanghou/6Keys.git
cd 6Keys

# 安裝依賴
pip install -r requirements.txt

# 開發模式安裝
pip install -e ".[dev]"
```

### B.2.3 安裝驗證

```python
import sixkeys as sk

# 檢查版本
print(f"Six Keys version: {sk.__version__}")

# 快速測試
analyzer = sk.SixKeysAnalyzer()
result = analyzer.analyze_simulated_data(duration=1.0)
print(f"安裝成功！測試結果 D_w = {result.d_total:.3f}")
```

## B.3 核心模組說明

### B.3.1 六個核心指標（sixkeys.core）

#### FELC - 自由能極限環 (ζ₁)
```python
from sixkeys.core import FELC

felc = FELC(theta_c=1.0)
zeta1 = felc.compute(neural_data, time_window=2.0)
```

#### TEB - 資訊-能耗效率 (ζ₂)
```python
from sixkeys.core import TEB

teb = TEB()
zeta2 = teb.compute(neural_data, metabolic_data)
```

#### RFI - Ricci曲率臨界流 (ζ₃)
```python
from sixkeys.core import RFI

rfi = RFI()
zeta3 = rfi.compute(connectivity_matrix)
```

#### ECGP - 因果滲流 (ζ₄)
```python
from sixkeys.core import ECGP

ecgp = ECGP()
zeta4 = ecgp.compute(time_series_data)
```

#### PWC - 相位拓撲環流 (ζ₅)
```python
from sixkeys.core import PWC

pwc = PWC()
zeta5 = pwc.compute(phase_data)
```

#### ACI - 神經-星膠耦合臨界 (ζ₆)
```python
from sixkeys.core import ACI

aci = ACI()
zeta6 = aci.compute(neural_data, astrocyte_data)
```

### B.3.2 分析工具（sixkeys.analysis）

#### 主要分析器
```python
from sixkeys.analysis import SixKeysAnalyzer

# 創建分析器
analyzer = SixKeysAnalyzer(
    theta_c=1.0,
    random_state=42,
    n_jobs=-1  # 使用所有CPU核心
)

# 分析真實數據
result = analyzer.analyze_real_data(
    data_path="path/to/data.npy",
    sampling_rate=1000,
    consciousness_state="awake"
)

# 分析模擬數據
result = analyzer.analyze_simulated_data(
    consciousness_state="light_sedation",
    duration=5.0,
    noise_level=0.1
)
```

#### 交叉驗證
```python
from sixkeys.analysis import CrossValidation

cv = CrossValidation(n_folds=5, random_state=42)
scores = cv.validate_model(data, labels)
```

#### 公開資料重分析
```python
from sixkeys.analysis import PublicDataAnalysis

pda = PublicDataAnalysis()
results = pda.analyze_dataset("ds002345")  # OpenNeuro 數據集
```

### B.3.3 工具函式（sixkeys.utils）

#### 數據處理
```python
from sixkeys.utils import preprocessing, data_io

# 數據預處理
clean_data = preprocessing.filter_signal(raw_data, fs=1000)
normalized_data = preprocessing.normalize(clean_data)

# 數據輸入輸出
data_io.save_results(results, "output.json")
loaded_results = data_io.load_results("output.json")
```

#### 可視化
```python
from sixkeys.utils import visualization

# 雷達圖
fig = visualization.plot_radar_chart(results)

# 時間序列圖
fig = visualization.plot_time_series(data, indicators)

# 相圖
fig = visualization.plot_phase_diagram(results)
```

### B.3.4 演示模組（sixkeys.demos）

```python
# 雷達圖演示
from sixkeys.demos import radar_chart
radar_chart.run_demo()

# 交叉驗證演示
from sixkeys.demos import cross_validation
cross_validation.run_demo()

# 公開數據分析演示
from sixkeys.demos import public_data_analysis
public_data_analysis.run_demo()
```

## B.4 使用範例

### B.4.1 基本使用流程

```python
import sixkeys as sk
import numpy as np
import matplotlib.pyplot as plt

# 1. 創建分析器
analyzer = sk.SixKeysAnalyzer(theta_c=1.0, random_state=42)

# 2. 分析不同意識狀態
states = ['awake', 'light_sedation', 'deep_anesthesia']
results = {}

for state in states:
    result = analyzer.analyze_simulated_data(
        consciousness_state=state,
        duration=5.0,  # 5秒數據
        sampling_rate=1000
    )
    results[state] = result
    print(f"{state}: D_w = {result.d_total:.3f}")

# 3. 可視化結果
fig = analyzer.plot_radar_chart(results)
plt.title("六鑰臨界分析結果")
plt.show()

# 4. 保存結果
analyzer.save_results(results, "analysis_results.json")
```

### B.4.2 進階分析

```python
# 批量分析
from sixkeys.analysis import BatchAnalyzer

batch = BatchAnalyzer()
results = batch.analyze_directory(
    data_dir="/path/to/data",
    output_dir="/path/to/results",
    file_pattern="*.npy"
)

# 統計分析
from sixkeys.utils import metrics

stats = metrics.compute_statistics(results)
print(f"平均 D_w: {stats['d_total']['mean']:.3f}")
print(f"標準差: {stats['d_total']['std']:.3f}")
```

## B.5 測試與驗證

### B.5.1 運行測試

```bash
# 運行所有測試
pytest tests/

# 運行特定測試
pytest tests/test_core/test_felc.py -v

# 生成測試覆蓋率報告
pytest --cov=sixkeys tests/
```

### B.5.2 性能基準測試

```python
from sixkeys.utils import benchmarks

# 運行性能測試
results = benchmarks.run_performance_tests()
print(f"平均處理時間: {results['avg_time']:.2f}秒")
```

## B.6 開發與貢獻

### B.6.1 開發環境設置

```bash
# 克隆倉庫
git clone https://github.com/isyanghou/6Keys.git
cd 6Keys

# 安裝開發依賴
pip install -e ".[dev]"

# 安裝 pre-commit hooks
pre-commit install
```

### B.6.2 代碼風格

```bash
# 代碼格式化
black sixkeys/

# 代碼檢查
ruff check sixkeys/

# 類型檢查
mypy sixkeys/
```

### B.6.3 貢獻流程

1. **Fork 專案**：在 GitHub 上 fork 本專案
2. **創建分支**：`git checkout -b feature/new-feature`
3. **開發功能**：實現新功能並添加測試
4. **運行測試**：確保所有測試通過
5. **提交變更**：`git commit -m "Add new feature"`
6. **推送分支**：`git push origin feature/new-feature`
7. **創建 PR**：在 GitHub 上創建 Pull Request

## B.7 故障排除

### B.7.1 常見問題

**Q: 安裝時出現依賴衝突**
```bash
# 使用虛擬環境
python -m venv sixkeys_env
source sixkeys_env/bin/activate  # Linux/Mac
# 或
sixkeys_env\Scripts\activate  # Windows
pip install sixkeys
```

**Q: 計算速度過慢**
```python
# 使用多核心處理
analyzer = sk.SixKeysAnalyzer(n_jobs=-1)

# 或減少數據長度
result = analyzer.analyze_simulated_data(duration=1.0)  # 減少到1秒
```

**Q: 記憶體不足**
```python
# 分批處理大數據
from sixkeys.utils import data_io

for batch in data_io.batch_loader(large_dataset, batch_size=1000):
    result = analyzer.analyze_batch(batch)
```

### B.7.2 獲取幫助

- **GitHub Issues**: https://github.com/isyanghou/6Keys/issues
- **文檔**: https://sixkeys.readthedocs.io/
- **電子郵件**: isyanghou@gmail.com

## B.8 授權與引用

### B.8.1 授權條款

- **程式碼**: BSD 3-Clause License
- **論文內容**: CC BY-NC 4.0 International License

### B.8.2 引用格式

```bibtex
@software{hou2025sixkeys,
  title = {Six Keys Criticality: A Neural Consciousness Analysis Framework},
  author = {You Yang Hou},
  year = {2025},
  url = {https://github.com/isyanghou/6Keys},
  note = {Version 0.1.0}
}
```

---

## 結語

六鑰臨界框架為神經科學和意識研究提供了一個統一、開放的分析工具。我們歡迎研究社群的參與和貢獻，共同推進這一領域的發展。

**開始您的探索之旅**：
```bash
pip install sixkeys
python -c "import sixkeys; print('歡迎使用六鑰臨界框架！')"
```

更多詳細信息請參考我們的 [GitHub 倉庫](https://github.com/isyanghou/6Keys) 和 [完整文檔](https://sixkeys.readthedocs.io/)。