# Six Keys Criticality (六鑰臨界)

基於臨界轉換理論的神經意識狀態分析框架  
*A Neural Consciousness State Analysis Framework Based on Critical Transition Theory*

[![License: BSD 3-Clause](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Documentation Status](https://readthedocs.org/projects/sixkeys/badge/?version=latest)](https://sixkeys.readthedocs.io/en/latest/?badge=latest)
[![Docker](https://img.shields.io/badge/docker-supported-blue.svg)](https://hub.docker.com/r/sixkeys/sixkeys)
[![Conda](https://img.shields.io/badge/conda-supported-green.svg)](https://anaconda.org/conda-forge/sixkeys)

## 📥 **論文下載** | **Paper Download**

> **🔥 [📄 完整論文PDF下載 (中文)](https://github.com/isyanghou/6Keys/releases/latest/download/Six-Key_Criticality_Neural_Manifold_Path_to_Consciousness_ZH.pdf)**  
> **🔥 [📄 Complete Paper PDF (English)](https://github.com/isyanghou/6Keys/releases/latest/download/Six-Key_Criticality_Neural_Manifold_Path_to_Consciousness_EN.pdf)**

## 🧭 **快速導航** | **Quick Navigation**

| 用戶類型 | 推薦路徑 | 說明 |
|---------|---------|------|
| 🆕 **新手用戶** | [🚀 快速開始](docs/quickstart.md) → [❓ 常見問題](docs/faq.md) | 5分鐘上手指南 |
| 🧠 **理論研究者** | [📚 完整論文](docs/zh/paper/) → [🧮 數學推導](docs/zh/paper/A-0_數學推導詳解.md) | 深入理論背景 |
| 👨‍💻 **程式開發者** | [📚 API文檔](docs/api/) → [🔧 開發者指南](docs/developers.md) | 技術實現細節 |
| 🔬 **實驗驗證者** | [🧪 實驗指南](docs/experiments.md) → [📊 可視化教程](docs/visualization.md) | 實驗設計方法 |

**🌐 語言版本**: [🇨🇳 中文文檔](docs/zh/) | [🇺🇸 English Docs](docs/en/) | **📖 完整導航**: [📚 文檔中心](docs/)

---

## 🇺🇸 **For English Visitors**

**Welcome! This project provides comprehensive English documentation.**

| User Type | Recommended Path | Description |
|-----------|------------------|-------------|
| 🆕 **New Users** | [🚀 Quick Start](docs/en/quickstart.md) → [❓ FAQ](docs/en/faq.md) | 5-minute getting started guide |
| 🧠 **Researchers** | [📚 Complete Paper](docs/en/paper/) → [🧮 Mathematical Derivations](docs/en/paper/A_Mathematical_Derivations_Detailed.md) | In-depth theoretical background |
| 👨‍💻 **Developers** | [📚 API Docs](docs/api/) → [🔧 Developer Guide](docs/developers.md) | Technical implementation details |
| 🔬 **Experimenters** | [🧪 Experiment Guide](docs/en/experiments.md) → [📊 Visualization Tutorial](docs/en/visualization.md) | Experimental design methods |

**📖 English Documentation Hub**: [📚 English Docs Center](docs/en/) | **🏠 Main Navigation**: [📚 All Documentation](docs/)

## 🎯 項目概述

**Six Keys Criticality** 是一個基於臨界轉換理論的神經意識狀態分析框架。通過六個核心指標（ζ₁-ζ₆）量化神經網絡的臨界性特徵，為意識研究提供理論視角和實用工具。

### 🔑 六個核心指標

| 指標 | 名稱 | 描述 |
|------|------|------|
| **ζ₁** | **FELC** | 自由能極限環 (Free Energy Limit Cycle) |
| **ζ₂** | **TEB** | 資訊-能耗效率 (Thermodynamic Efficiency Balance) |
| **ζ₃** | **RFI** | Ricci曲率臨界流 (Ricci Flow Index) |
| **ζ₄** | **ECGP** | 因果滲流 (Effective Causal Graph Percolation) |
| **ζ₅** | **PWC** | 相位拓撲環流 (Phase-Wrapped Circulation) |
| **ζ₆** | **ACI** | 神經-星膠耦合臨界 (Astrocyte-Coupling Index) |

## 🚀 快速開始 | Quick Start

### 📦 安裝

```bash
# 推薦方式：pip 安裝
pip install sixkeys

# 或從源碼安裝
git clone https://github.com/isyanghou/6Keys.git
cd 6Keys && pip install -e .
```

### 🎮 基本使用

```python
import numpy as np
from sixkeys import SixKeysAnalyzer

# 創建分析器並分析數據
analyzer = SixKeysAnalyzer()
data = np.random.randn(1000, 64)  # 示例神經數據
results = analyzer.analyze(data)

# 查看六個核心指標
for key, value in results.items():
    print(f"{key}: {value:.4f}")
```

> 📖 **詳細教程**: [完整安裝指南](docs/installation.md) | [使用教程](docs/tutorials/) | [API文檔](docs/api/)

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
├── sixkeys/              # 核心Python包
│   ├── core/            # 六個核心指標算法 (ζ₁-ζ₆)
│   ├── analysis/        # 分析工具
│   └── demos/           # 演示模組
├── docs/                # 完整文檔系統
│   ├── zh/paper/       # 中文完整論文
│   ├── en/paper/       # English complete paper
│   └── api/            # API參考文檔
├── examples/            # 使用示例
└── tests/              # 測試套件
```

> 📖 **詳細結構**: [完整項目結構說明](docs/project-structure.md)

## 🔬 理論背景 | Theoretical Background

六鑰臨界理論基於臨界轉換理論、自由能原理、網絡拓撲學和資訊理論，通過六個核心指標量化神經系統的臨界狀態轉換。

> 📖 **深入了解**: [理論背景詳解](docs/theory.md) | [數學推導](docs/mathematical-foundations.md)

## 🎨 可視化演示 | Visualization Demos

```bash
# 運行可視化演示
python examples/demo_visualization.py

# 安裝可視化依賴
pip install matplotlib seaborn scipy pandas
```

**演示內容**:
- **六鑰雷達圖** - 六個指標的可視化比較
- **公開數據重分析** - 現有數據集的重新分析
- **交叉驗證分析** - 指標間相關性分析

> 📖 **詳細說明**: [可視化教程](docs/visualization.md)

## 📚 文檔和教程 | Documentation & Tutorials

### 🎯 按需求快速定位 | Quick Access by Needs

<details>
<summary><strong>🆕 我是新手，想快速上手</strong></summary>

**推薦學習路徑**:
1. [🚀 快速開始](docs/quickstart.md) - 5分鐘上手
2. [⚙️ 安裝指南](docs/installation.md) - 詳細安裝步驟
3. [❓ 常見問題](docs/faq.md) - 解決常見疑問
4. [📊 可視化教程](docs/visualization.md) - 學習結果展示

**🔗 遇到問題？** → [❓ FAQ](docs/faq.md) | [💬 聯繫我們](mailto:isyanghou@gmail.com)
</details>

<details>
<summary><strong>🧠 我想深入了解理論</strong></summary>

**推薦學習路徑**:
1. [🧠 理論背景](docs/theory.md) - 理論基礎概述
2. [📚 完整論文](docs/zh/paper/) - 中文完整論文
3. [🧮 數學推導](docs/zh/paper/A-0_數學推導詳解.md) - 詳細數學證明
4. [🔬 實驗驗證](docs/experiments.md) - 實驗設計方法

**🌐 其他語言**: [🇺🇸 English Paper](docs/en/paper/)
</details>

<details>
<summary><strong>👨‍💻 我要開發和集成</strong></summary>

**推薦學習路徑**:
1. [📚 API文檔](docs/api/) - 完整API參考
2. [🔧 開發者指南](docs/developers.md) - 開發環境設置
3. [🏗️ 項目結構](docs/project-structure.md) - 代碼組織架構
4. [🧪 測試指南](docs/developers.md#測試指南) - 測試和驗證

**🔗 開發資源**: [GitHub](https://github.com/isyanghou/6Keys) | [Issues](https://github.com/isyanghou/6Keys/issues)
</details>

### 🌟 核心文檔入口 | Core Documentation

| 文檔類型 | 連結 | 適合對象 |
|---------|------|----------|
| 📖 **快速開始** | [開始使用](docs/quickstart.md) | 所有用戶 |
| 📚 **完整論文** | [中文](docs/zh/paper/) \| [English](docs/en/paper/) | 研究者 |
| 🔧 **API文檔** | [技術文檔](docs/api/) | 開發者 |
| ❓ **常見問題** | [FAQ](docs/faq.md) | 所有用戶 |

> 📖 **完整導航**: [📚 文檔中心](docs/) - 包含所有文檔的詳細索引和導航

## 🤝 貢獻指南 | Contributing

我們歡迎社群貢獻！請參閱 [CONTRIBUTING.md](CONTRIBUTING.md) 了解詳細信息。

```bash
# 開發環境設置
git clone https://github.com/isyanghou/6Keys.git
cd 6Keys && pip install -e ".[dev]"
pytest tests/  # 運行測試
```

## 📈 引用 | Citation

如果您在研究中使用了本項目，請引用：

```bibtex
@software{sixkeys2025,
  title={Six Keys Criticality: A Framework for Neural Consciousness State Analysis},
  author={Hou, You Yang},
  year={2025},
  url={https://github.com/isyanghou/6Keys},
  note={ORCID: 0009-0000-7041-8574}
}
```

## 📄 授權條款 | License

- **論文內容**: [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/)
- **程式碼**: [BSD 3-Clause](LICENSE)

## 👤 作者 | Author

**You Yang Hou**  
📧 [isyanghou@gmail.com](mailto:isyanghou@gmail.com) | 🆔 ORCID: [0009-0000-7041-8574](https://orcid.org/0009-0000-7041-8574)

---

**注意**：本項目為研究性質，不適用於臨床診斷。使用前請詳閱相關文檔和免責聲明。