# 👨‍💻 開發者指南 | Developer Guide

**📍 當前位置**: [🏠 首頁](../README.md) > [📚 文檔中心](README.md) > 👨‍💻 開發者指南

本指南為希望參與六鑰臨界框架開發的開發者提供詳細的開發環境設置、工作流程和貢獻指南。

**⏱️ 設置時間**: 30-60分鐘 | **💡 難度**: 中高級 | **🎯 目標**: 完成開發環境設置

---

## 🗺️ **開發導航** | **Development Navigation**

| 階段 | 內容 | 適合對象 |
|------|------|----------|
| [⚙️ 環境設置](#開發環境設置) | 開發環境配置 | 新手開發者 |
| [🔄 工作流程](#開發工作流程) | Git和協作流程 | 所有開發者 |
| [🧪 測試指南](#測試指南) | 測試編寫和運行 | 所有開發者 |
| [📝 代碼規範](#程式碼規範) | 編碼標準 | 所有開發者 |

## 🛠️ 開發環境設置 | Development Environment Setup

### 基本要求 | Basic Requirements

- Python 3.8+ (建議使用 Python 3.10)
- Git
- 適合的IDE (推薦 PyCharm 或 VS Code)

### 克隆儲存庫 | Clone Repository

```bash
# 克隆儲存庫
git clone https://github.com/isyanghou/6Keys.git
cd 6Keys

# 創建並激活虛擬環境
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 安裝開發依賴 | Install Development Dependencies

```bash
# 安裝開發依賴
pip install -e ".[dev]"

# 或手動安裝
pip install -e .
pip install pytest pytest-cov black flake8 mypy sphinx sphinx-rtd-theme
```

### 設置預提交鉤子 | Setup Pre-commit Hooks

```bash
pip install pre-commit
pre-commit install
```

## 🔄 開發工作流程 | Development Workflow

### 分支策略 | Branching Strategy

- `main`: 穩定版本分支
- `develop`: 開發分支，所有功能分支合併到此
- `feature/*`: 新功能分支
- `bugfix/*`: 錯誤修復分支
- `release/*`: 發布準備分支

### 創建功能分支 | Create Feature Branch

```bash
# 確保從最新的develop分支創建
git checkout develop
git pull origin develop

# 創建功能分支
git checkout -b feature/your-feature-name
```

### 提交變更 | Commit Changes

```bash
# 添加變更
git add .

# 提交變更 (使用約定式提交格式)
git commit -m "feat: add new visualization component"
```

### 提交拉取請求 | Submit Pull Request

1. 將分支推送到遠端儲存庫
   ```bash
   git push origin feature/your-feature-name
   ```

2. 在GitHub上創建拉取請求到`develop`分支
3. 等待代碼審查和CI檢查
4. 根據反饋進行修改
5. 合併拉取請求

## 🧪 測試指南 | Testing Guidelines

### 運行測試 | Run Tests

```bash
# 運行所有測試
pytest

# 運行特定測試模組
pytest tests/test_core.py

# 運行帶覆蓋率報告的測試
pytest --cov=sixkeys tests/
```

### 編寫測試 | Writing Tests

```python
# tests/test_metrics.py
import pytest
from sixkeys.analysis import metrics
import numpy as np

def test_critical_fluctuation():
    # 準備測試數據
    data = np.random.randn(1000, 10)
    
    # 調用被測函數
    result = metrics.compute_critical_fluctuation(data)
    
    # 驗證結果
    assert isinstance(result, float)
    assert 0 <= result <= 1
```

### 測試覆蓋率目標 | Test Coverage Goals

- 核心模組: 95%+
- 分析模組: 90%+
- 可視化模組: 85%+
- 工具函數: 90%+

## 📝 程式碼規範 | Code Style Guidelines

### Python 風格 | Python Style

- 遵循 [PEP 8](https://www.python.org/dev/peps/pep-0008/) 風格指南
- 使用 [Google Python 風格指南](https://google.github.io/styleguide/pyguide.html) 的文檔字符串格式
- 最大行長度: 88 字符
- 使用 4 空格縮進

### 自動格式化 | Automatic Formatting

```bash
# 使用 black 格式化代碼
black sixkeys/ tests/

# 使用 flake8 檢查風格
flake8 sixkeys/ tests/

# 使用 mypy 進行類型檢查
mypy sixkeys/
```

### 命名約定 | Naming Conventions

- **模組**: 小寫，單詞用下劃線分隔 (e.g., `data_loader.py`)
- **類**: 駝峰式命名法 (e.g., `CriticalityAnalyzer`)
- **函數/方法**: 小寫，單詞用下劃線分隔 (e.g., `compute_metrics`)
- **常量**: 全大寫，單詞用下劃線分隔 (e.g., `MAX_ITERATIONS`)
- **變量**: 小寫，單詞用下劃線分隔 (e.g., `result_data`)

## 📚 文檔指南 | Documentation Guidelines

### 文檔字符串 | Docstrings

```python
def compute_critical_fluctuation(data, window_size=1.0, overlap=0.5):
    """
    計算時間序列的臨界波動性指標。
    
    臨界波動性量化系統在臨界點附近的動態波動特徵，基於功率譜密度的標度行為。
    
    Args:
        data (np.ndarray): 形狀為 (time_points, channels) 的時間序列數據
        window_size (float): 分析窗口大小，單位為秒
        overlap (float): 相鄰窗口的重疊比例，範圍 [0, 1)
    
    Returns:
        float: 臨界波動性指標，範圍 [0, 1]
    
    Raises:
        ValueError: 如果數據維度不正確或參數無效
    
    Examples:
        >>> import numpy as np
        >>> data = np.random.randn(1000, 10)
        >>> cf = compute_critical_fluctuation(data)
        >>> print(f"Critical Fluctuation: {cf:.4f}")
    """
```

### 生成API文檔 | Generate API Documentation

```bash
# 安裝Sphinx和主題
pip install sphinx sphinx-rtd-theme

# 生成API文檔
cd docs
make html
```

### 更新文檔 | Update Documentation

當添加新功能或修改現有功能時，請確保：

1. 更新相關函數/類的文檔字符串
2. 更新API參考文檔
3. 如果需要，添加或更新教程和示例
4. 更新CHANGELOG.md文件

## 🚀 發布流程 | Release Process

### 版本控制 | Versioning

遵循[語義化版本控制](https://semver.org/)：

- **主版本號 (X.0.0)**: 不兼容的API變更
- **次版本號 (0.X.0)**: 向後兼容的功能新增
- **修訂號 (0.0.X)**: 向後兼容的問題修正

### 準備發布 | Prepare Release

```bash
# 從develop創建發布分支
git checkout develop
git pull origin develop
git checkout -b release/vX.Y.Z

# 更新版本號
# 編輯 sixkeys/__init__.py 和 pyproject.toml

# 更新CHANGELOG.md

# 提交變更
git add .
git commit -m "chore: prepare release vX.Y.Z"
```

### 完成發布 | Finalize Release

```bash
# 合併到main
git checkout main
git pull origin main
git merge --no-ff release/vX.Y.Z
git tag -a vX.Y.Z -m "Release vX.Y.Z"

# 合併回develop
git checkout develop
git pull origin develop
git merge --no-ff release/vX.Y.Z

# 推送變更
git push origin main develop --tags
```

### 發布到PyPI | Publish to PyPI

```bash
# 構建分發包
python -m pip install --upgrade build
python -m build

# 上傳到PyPI
python -m pip install --upgrade twine
python -m twine upload dist/*
```

## 🔍 代碼審查 | Code Review

### 審查清單 | Review Checklist

- 代碼是否遵循項目的風格指南？
- 是否有適當的測試覆蓋率？
- 文檔是否完整且準確？
- 性能是否可接受？
- 是否有潛在的安全問題？
- 代碼是否可維護和可擴展？

### 審查流程 | Review Process

1. 審查者應在2個工作日內回應拉取請求
2. 使用GitHub的審查功能提供具體的行級評論
3. 批准前確保所有問題都已解決
4. 合併前需要至少一個批准

## 🌐 社區貢獻 | Community Contributions

### 貢獻類型 | Types of Contributions

- **代碼**: 新功能、錯誤修復、性能改進
- **文檔**: 改進文檔、添加教程、修正錯誤
- **測試**: 添加測試、改進測試覆蓋率
- **示例**: 添加使用示例和案例研究
- **問題**: 報告錯誤、提出功能請求

### 貢獻流程 | Contribution Process

1. 在GitHub上創建問題，描述你想要貢獻的內容
2. 等待維護者的反饋和確認
3. 按照上述開發工作流程進行開發
4. 提交拉取請求並參與代碼審查

---

## 🎉 **開發環境完成！準備貢獻？** | **Development Setup Complete! Ready to Contribute?**

### 🚀 **開始貢獻**
1. **🔍 尋找任務**: 查看 [Good First Issues](https://github.com/isyanghou/6Keys/labels/good%20first%20issue)
2. **💬 討論想法**: 在 [GitHub Discussions](https://github.com/isyanghou/6Keys/discussions) 中交流
3. **🛠️ 開始開發**: 按照工作流程進行開發

### 📚 **開發資源**
- **🏗️ 項目架構**: [項目結構](project-structure.md) - 了解代碼組織
- **🎯 功能說明**: [特性說明](features.md) - 理解現有功能
- **🧪 測試範例**: [測試目錄](../tests/) - 學習測試編寫

---

## 🧭 **導航欄** | **Navigation**

**📍 當前位置**: [🏠 首頁](../README.md) > [📚 文檔中心](README.md) > 👨‍💻 **開發者指南**

### 🔄 **相關頁面**
- **🏗️ 項目結構**: [項目結構](project-structure.md) - 代碼架構
- **🎯 功能詳解**: [特性說明](features.md) - 功能說明
- **❓ 開發問題**: [FAQ-開發部分](faq.md#技術問題) - 開發常見問題
- **🔙 返回**: [📚 文檔中心](README.md) - 瀏覽所有文檔

### 🆘 **開發問題？**
- **💬 技術討論**: [GitHub Discussions](https://github.com/isyanghou/6Keys/discussions) - 開發者社群
- **🐛 問題回報**: [GitHub Issues](https://github.com/isyanghou/6Keys/issues) - 回報錯誤
- **📧 直接聯繫**: [isyanghou@gmail.com](mailto:isyanghou@gmail.com) - 開發諮詢

### 🎯 **貢獻機會**
- **🌟 新手友好**: [Good First Issues](https://github.com/isyanghou/6Keys/labels/good%20first%20issue)
- **🚀 功能開發**: [Feature Requests](https://github.com/isyanghou/6Keys/labels/enhancement)
- **📝 文檔改進**: [Documentation](https://github.com/isyanghou/6Keys/labels/documentation)

---

**💡 提示**: 準備開始貢獻？先查看 [Good First Issues](https://github.com/isyanghou/6Keys/labels/good%20first%20issue) 找到適合的任務，或在 [Discussions](https://github.com/isyanghou/6Keys/discussions) 中提出你的想法。