# Six Keys Criticality (六鑰臨界)

基於臨界轉換理論的神經意識狀態分析框架  
*A Neural Consciousness State Analysis Framework Based on Critical Transition Theory*

[![License: BSD 3-Clause](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Documentation Status](https://readthedocs.org/projects/sixkeys/badge/?version=latest)](https://sixkeys.readthedocs.io/en/latest/?badge=latest)
[![Docker](https://img.shields.io/badge/docker-supported-blue.svg)](https://hub.docker.com/r/sixkeys/sixkeys)
[![Conda](https://img.shields.io/badge/conda-supported-green.svg)](https://anaconda.org/conda-forge/sixkeys)

[🇨🇳 中文文檔](docs/zh/) | [🇺🇸 English Docs](docs/en/) | [📚 API Reference](docs/api/) | [🚀 Quick Start](docs/zh/quickstart.md)

## 🎯 項目概述

六鑰臨界是一個創新的神經科學理論框架，通過六個關鍵指標（ζ₁-ζ₆）來量化和分析神經系統的臨界狀態轉換。本項目提供了完整的Python實現，支持從理論建模到實際數據分析的全流程。

### 🔑 六個核心指標

1. **FELC (ζ₁)** - 自由能極限環 (Free Energy Limit Cycle)
2. **TEB (ζ₂)** - 資訊-能耗效率 (Thermodynamic Efficiency Balance)
3. **RFI (ζ₃)** - Ricci曲率臨界流 (Ricci Flow Index)
4. **ECGP (ζ₄)** - 因果滲流 (Effective Causal Graph Percolation)
5. **PWC (ζ₅)** - 相位拓撲環流 (Phase-Wrapped Circulation)
6. **ACI (ζ₆)** - 神經-星膠耦合臨界 (Astrocyte-Coupling Index)

## 🚀 快速開始 | Quick Start

### 📦 安裝方式 | Installation Options

#### 方法一：PyPI 安裝 (推薦)
```bash
# 基本安裝 | Basic installation
pip install sixkeys

# 完整安裝 (包含所有可選依賴) | Full installation
pip install "sixkeys[all]"
```

#### 方法二：Conda 安裝
```bash
# 創建環境並安裝 | Create environment and install
conda env create -f environment.yml
conda activate sixkeys
```

#### 方法三：Docker 部署
```bash
# 拉取鏡像 | Pull image
docker pull sixkeys/sixkeys:latest

# 或使用 Docker Compose | Or use Docker Compose
docker-compose up jupyter  # 啟動 Jupyter Lab
```

#### 方法四：源碼安裝
```bash
git clone https://github.com/yourusername/sixkeys.git
cd sixkeys
pip install -e ".[dev]"  # 開發版本
```

### ✅ 安裝驗證 | Installation Verification
```python
import sixkeys as sk
print(f"Six Keys version: {sk.__version__}")

# 快速測試 | Quick test
analyzer = sk.SixKeysAnalyzer()
result = analyzer.analyze_simulated_data(duration=1.0)
print(f"Test completed: D_w = {result.d_total:.3f}")
```

### 💡 基本使用 | Basic Usage

```python
import sixkeys as sk
import matplotlib.pyplot as plt

# 創建分析器 | Create analyzer
analyzer = sk.SixKeysAnalyzer(theta_c=1.0, random_state=42)

# 分析不同意識狀態 | Analyze different consciousness states
states = ['awake', 'light_sedation', 'deep_anesthesia']
results = {}

for state in states:
    result = analyzer.analyze_simulated_data(
        consciousness_state=state,
        duration=5.0  # 5 seconds
    )
    results[state] = result
    print(f"{state}: D_w = {result.d_total:.3f}")

# 可視化結果 | Visualize results
fig = analyzer.plot_radar_chart(results)
plt.show()
```

### 🔬 進階分析 | Advanced Analysis

```python
# 單個指標分析 | Individual indicator analysis
from sixkeys.core import FELC, TEB, RFI

felc = FELC(sim_time=10.0, dt=0.01)
felc_results = felc.analyze_states()
felc.plot_results(felc_results)

# 自定義參數 | Custom parameters
custom_analyzer = sk.SixKeysAnalyzer(
    theta_c=0.8,
    weights={'zeta1': 0.3, 'zeta2': 0.2, 'zeta3': 0.15, 
             'zeta4': 0.15, 'zeta5': 0.1, 'zeta6': 0.1}
)
```

### 🎨 可視化演示 | Visualization Demos

```python
# 快速演示 | Quick demos
from sixkeys.demos import (
    radar_demo,           # 六鑰雷達圖 | Six-key radar chart
    public_data_demo,     # 公開數據重分析 | Public data reanalysis
    cross_validation_demo # 交叉驗證分析 | Cross-validation analysis
)

radar_demo()
public_data_demo()
cross_validation_demo()
```

### 🐳 Docker 使用 | Docker Usage

```bash
# 啟動 Jupyter Lab | Start Jupyter Lab
docker-compose up jupyter
# 訪問 http://localhost:8888 (token: sixkeys)

# 開發模式 | Development mode
docker-compose run dev

# 運行測試 | Run tests
docker-compose run test
```

## 📊 主要功能 | Key Features

### 🔑 核心指標 | Core Indicators
- **FELC (ζ₁)**: 自由能極限環分析 | Free Energy Limit Cycle Analysis
- **TEB (ζ₂)**: 資訊-能耗效率平衡 | Thermodynamic Efficiency Balance
- **RFI (ζ₃)**: Ricci曲率臨界流 | Ricci Flow Index
- **ECGP (ζ₄)**: 有效因果圖滲透 | Effective Causal Graph Percolation
- **PWC (ζ₅)**: 相位拓撲環流 | Phase-Wrapped Circulation
- **ACI (ζ₆)**: 神經-星膠耦合指標 | Astrocyte-Coupling Index

### 🛠️ 分析工具 | Analysis Tools
- **統一框架**: 六鑰臨界管道流形 (CTM) | Unified framework with Critical Transition Manifold
- **多狀態分析**: 清醒、輕度鎮靜、深度麻醉 | Multi-state analysis (awake, sedation, anesthesia)
- **時間演化**: 動態臨界轉換追蹤 | Temporal evolution and critical transition tracking
- **統計驗證**: 交叉驗證和顯著性檢驗 | Statistical validation and significance testing

### 📈 可視化功能 | Visualization Features
- **雷達圖**: 六維指標空間可視化 | Radar charts for six-dimensional indicator space
- **相位圖**: 臨界狀態相位軌跡 | Phase diagrams for critical state trajectories
- **時間序列**: 動態演化分析 | Time series analysis for dynamic evolution
- **統計圖表**: 箱線圖、分布圖等 | Statistical plots (boxplots, distributions, etc.)

### 🔧 技術特性 | Technical Features
- **多平台支持**: Windows, macOS, Linux | Multi-platform support
- **容器化部署**: Docker 和 Docker Compose | Containerized deployment
- **批量處理**: 大規模數據集分析 | Batch processing for large datasets
- **可擴展性**: 模組化設計，易於擴展 | Extensible modular design
- **開源協議**: BSD 3-Clause 許可證 | Open source with BSD 3-Clause license

## 📁 項目結構 | Project Structure

```
sixkeys/
├── sixkeys/              # 主要Python包 | Main Python package
│   ├── core/            # 核心算法模組 | Core algorithm modules
│   │   ├── felc.py      # ζ₁ 自由能極限環 | Free Energy Limit Cycle
│   │   ├── teb.py       # ζ₂ 資訊-能耗效率 | Thermodynamic Efficiency
│   │   ├── rfi.py       # ζ₃ Ricci曲率流 | Ricci Flow Index
│   │   ├── ecgp.py      # ζ₄ 因果滲流 | Causal Graph Percolation
│   │   ├── pwc.py       # ζ₅ 相位環流 | Phase-Wrapped Circulation
│   │   └── aci.py       # ζ₆ 星膠耦合 | Astrocyte-Coupling Index
│   ├── analysis/        # 分析工具 | Analysis tools
│   ├── utils/           # 工具函數 | Utility functions
│   └── demos/           # 演示模組 | Demo modules
├── docs/                # 文檔 | Documentation
│   ├── zh/             # 中文文檔 | Chinese docs
│   ├── en/             # 英文文檔 | English docs
│   └── api/            # API文檔 | API reference
├── notebooks/           # Jupyter筆記本 | Jupyter notebooks
├── examples/            # 使用示例 | Usage examples
├── tests/              # 測試套件 | Test suite
├── environment.yml     # Conda環境 | Conda environment
├── Dockerfile          # Docker配置 | Docker configuration
└── docker-compose.yml  # Docker Compose配置
```

## 🔬 理論背景

六鑰臨界理論基於以下核心概念：

- **臨界轉換理論**：神經系統在不同意識狀態間的相變
- **自由能原理**：大腦的預測編碼和能量最小化
- **網絡拓撲學**：神經網絡的幾何和拓撲性質
- **資訊理論**：神經信號的熵和複雜性

## 🎨 可視化演示模組

`sixkeys.demos` 套件提供了三個可選的可視化演示模組：

### 1. 六鑰統合雷達圖 (SixKeysRadarChart)
- 模擬六個關鍵指標的無量綱化座標 ζ_i
- 生成二值臨界標誌 C_i 和加權距離 D_w_i
- 創建雷達圖和總距離條形圖
- 支援多種意識狀態比較

### 2. 公開資料重分析 (PublicDataAnalysis)
- 模擬五個公開數據集的 Dw 分佈
- 分析清醒與低意識狀態的差異
- 生成箱線圖和統計摘要
- 執行統計顯著性檢驗

### 3. 交叉驗證分析 (CrossValidationAnalysis)
- 生成六個指標的合成時間序列
- 計算不同意識狀態下的相關矩陣
- 創建並排熱力圖可視化
- 分析指標間的相關性變化

### 命令行界面
```bash
# 運行所有演示
python examples/demo_visualization.py

# 運行特定模組
python examples/demo_visualization.py --module radar

# 保存結果而不顯示圖形
python examples/demo_visualization.py --no-plots --save --output results/
```

### 依賴需求
演示模組需要額外的依賴：
```bash
pip install matplotlib seaborn scipy pandas
```

## 📚 文檔和教程

- [完整文檔](https://sixkeys.readthedocs.io/)
- [API參考](https://sixkeys.readthedocs.io/en/latest/api/)
- [教程筆記本](./notebooks/)
- [理論背景](./docs/theory/)

詳細的文檔和教程請參見 `docs/` 目錄和 `sixkeys/demos/README.md`。

## 🤝 貢獻指南

我們歡迎社群貢獻！請參閱 [CONTRIBUTING.md](CONTRIBUTING.md) 了解如何參與項目開發。

### 開發環境設置

```bash
# 克隆倉庫
git clone https://github.com/yourusername/sixkeys.git
cd sixkeys

# 創建虛擬環境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安裝開發依賴
pip install -e ".[dev]"

# 運行測試
pytest tests/
```

## 📄 授權條款

本項目採用 [BSD 3-Clause License](LICENSE) 授權。

## 📞 聯繫方式

- **作者**：You Yang Hou
- **Email**：[isyanghou@gmail.com]
- **GitHub**：[https://github.com/isyanghou/6keys]

## 🙏 致謝

感謝以下開源項目和社群的支持：

- NumPy, SciPy, Matplotlib
- NetworkX, scikit-learn
- Jupyter, Sphinx
- OpenNeuro, NeuroStars

## 📈 引用

如果您在研究中使用了本項目，請引用：

```bibtex
@software{sixkeys2025,
  title={Six Keys Criticality: A Framework for Neural Consciousness State Analysis},
  author={Hou, You Yang},
  year={2025},
  month={6},
  day={28},
  url={https://github.com/isyanghou/6Keys},
  note={ORCID: 0009-0000-7041-8574}
}
```

## 👤 作者信息

**You Yang Hou**  
📧 Email: [isyanghou@gmail.com](mailto:isyanghou@gmail.com)  
🆔 ORCID: [0009-0000-7041-8574](https://orcid.org/0009-0000-7041-8574)  
📅 論文日期: 2025-06-28

## 📄 授權條款

- **論文內容**: [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) - 創用CC 姓名標示-非商業性 4.0 國際授權條款
- **程式碼**: [BSD 3-Clause](LICENSE) - BSD 3條款授權

---

**注意**：本項目為研究性質，不適用於臨床診斷。使用前請詳閱相關文檔和免責聲明。
