# 項目結構詳解 | Project Structure Details

本文檔詳細介紹六鑰臨界項目的完整結構和組織方式。

## 📁 完整項目結構 | Complete Project Structure

```
sixkeys/
├── 📁 sixkeys/                    # 核心程式庫
│   ├── 📄 __init__.py             # 套件初始化
│   ├── 📁 core/                   # 核心演算法
│   │   ├── 📄 criticality.py     # 臨界性計算
│   │   ├── 📄 manifold.py        # 流形分析
│   │   └── 📄 consciousness.py   # 意識指標
│   ├── 📁 analysis/               # 分析工具
│   │   ├── 📄 metrics.py         # 六個核心指標
│   │   ├── 📄 statistics.py      # 統計分析
│   │   └── 📄 validation.py      # 驗證工具
│   ├── 📁 visualization/          # 可視化模組
│   │   ├── 📄 plots.py           # 基礎繪圖
│   │   ├── 📄 interactive.py     # 互動式圖表
│   │   └── 📄 dashboard.py       # 儀表板
│   └── 📁 utils/                  # 工具函數
│       ├── 📄 data_loader.py     # 資料載入
│       ├── 📄 preprocessing.py   # 資料預處理
│       └── 📄 helpers.py         # 輔助函數
├── 📁 docs/                       # 文檔系統
│   ├── 📄 README.md              # 文檔導航
│   ├── 📁 zh/                    # 中文文檔
│   │   ├── 📁 paper/             # 完整論文章節
│   │   ├── 📄 quickstart.md      # 快速開始
│   │   ├── 📄 installation.md    # 安裝指南
│   │   └── 📄 faq.md             # 常見問題
│   ├── 📁 en/                    # 英文文檔
│   │   ├── 📁 paper/             # Complete paper sections
│   │   ├── 📄 quickstart.md      # Quick start
│   │   ├── 📄 installation.md    # Installation guide
│   │   └── 📄 faq.md             # FAQ
│   ├── 📁 api/                   # API文檔
│   │   ├── 📄 core.md            # 核心API
│   │   ├── 📄 analysis.md        # 分析API
│   │   └── 📄 visualization.md   # 可視化API
│   ├── 📄 theory.md              # 理論背景
│   ├── 📄 developers.md          # 開發者指南
│   ├── 📄 experiments.md         # 實驗指南
│   └── 📄 visualization.md       # 可視化教程
├── 📁 examples/                   # 使用範例
│   ├── 📄 basic_usage.py         # 基礎使用
│   ├── 📄 advanced_analysis.py   # 進階分析
│   ├── 📄 visualization_demo.py  # 可視化演示
│   └── 📁 notebooks/             # Jupyter筆記本
│       ├── 📄 tutorial_01.ipynb  # 教程1
│       ├── 📄 tutorial_02.ipynb  # 教程2
│       └── 📄 case_study.ipynb   # 案例研究
├── 📁 tests/                      # 測試套件
│   ├── 📄 test_core.py           # 核心測試
│   ├── 📄 test_analysis.py       # 分析測試
│   ├── 📄 test_visualization.py  # 可視化測試
│   └── 📁 data/                  # 測試資料
├── 📁 data/                       # 範例資料
│   ├── 📁 sample/                # 範例資料集
│   ├── 📁 benchmarks/            # 基準測試資料
│   └── 📄 README.md              # 資料說明
├── 📁 scripts/                    # 工具腳本
│   ├── 📄 setup_env.py           # 環境設置
│   ├── 📄 run_tests.py           # 執行測試
│   └── 📄 generate_docs.py       # 生成文檔
├── 📄 README.md                   # 主要說明文件
├── 📄 requirements.txt            # Python依賴
├── 📄 setup.py                    # 安裝配置
├── 📄 pyproject.toml             # 專案配置
├── 📄 LICENSE                     # 授權條款
├── 📄 CONTRIBUTING.md             # 貢獻指南
├── 📄 CHANGELOG.md                # 更新日誌
└── 📄 .gitignore                  # Git忽略文件
```

## 🏗️ 架構設計原則 | Architecture Design Principles

### 1. 模組化設計 | Modular Design
- **核心分離**: 核心演算法與應用層分離
- **功能獨立**: 每個模組功能獨立，可單獨使用
- **介面統一**: 統一的API介面設計

### 2. 可擴展性 | Extensibility
- **插件架構**: 支援自定義分析方法
- **開放介面**: 提供擴展點供第三方開發
- **版本兼容**: 向後兼容的API設計

### 3. 易用性 | Usability
- **簡潔API**: 簡單直觀的函數介面
- **豐富範例**: 完整的使用範例和教程
- **詳細文檔**: 全面的文檔和說明

## 📦 核心模組詳解 | Core Modules Details

### `sixkeys.core` - 核心演算法
- **criticality.py**: 實現六鑰臨界性的核心計算
- **manifold.py**: 神經流形分析和維度計算
- **consciousness.py**: 意識指標的量化方法

### `sixkeys.analysis` - 分析工具
- **metrics.py**: 六個核心指標的實現
- **statistics.py**: 統計分析和假設檢驗
- **validation.py**: 結果驗證和交叉驗證

### `sixkeys.visualization` - 可視化
- **plots.py**: 基礎圖表繪製
- **interactive.py**: 互動式可視化
- **dashboard.py**: 整合式儀表板

### `sixkeys.utils` - 工具函數
- **data_loader.py**: 支援多種資料格式載入
- **preprocessing.py**: 資料清理和預處理
- **helpers.py**: 常用輔助函數

## 🔧 開發工具 | Development Tools

### 測試框架 | Testing Framework
- 使用 `pytest` 進行單元測試
- 覆蓋率報告和持續整合
- 效能基準測試

### 文檔系統 | Documentation System
- 使用 `Sphinx` 生成API文檔
- Markdown格式的用戶文檔
- 自動化文檔更新

### 程式碼品質 | Code Quality
- `black` 程式碼格式化
- `flake8` 程式碼檢查
- `mypy` 類型檢查

## 📊 資料流程 | Data Flow

```
原始資料 → 預處理 → 核心分析 → 指標計算 → 可視化 → 結果輸出
   ↓         ↓        ↓        ↓        ↓        ↓
data/    utils/   core/   analysis/ visual/  reports/
```

## 🚀 部署結構 | Deployment Structure

### PyPI套件 | PyPI Package
```
sixkeys-x.x.x/
├── sixkeys/          # 核心程式庫
├── docs/            # 文檔
├── examples/        # 範例
└── tests/           # 測試
```

### Docker容器 | Docker Container
```
/app/
├── sixkeys/         # 安裝的套件
├── notebooks/       # Jupyter環境
├── data/           # 掛載的資料目錄
└── outputs/        # 結果輸出目錄
```

---

**返回**: [文檔導航](README.md) | **下一步**: [開發者指南](developers.md)