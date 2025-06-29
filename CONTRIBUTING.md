# Contributing to Six Keys Criticality

感謝您對六鑰臨界項目的興趣！我們歡迎各種形式的貢獻，包括代碼、文檔、測試、問題報告和功能建議。

## 🤝 如何貢獻

### 報告問題 (Issues)

如果您發現了錯誤或有功能建議，請：

1. 檢查 [現有問題](https://github.com/isyanghou/6Keys/issues) 是否已有相關報告
2. 如果沒有，請創建新的 issue，包含：
   - 清晰的標題和描述
   - 重現步驟（如果是錯誤報告）
   - 預期行為和實際行為
   - 系統環境信息（Python版本、操作系統等）
   - 相關的錯誤信息或截圖

### 提交代碼 (Pull Requests)

1. **Fork 倉庫**
   ```bash
   git clone https://github.com/isyanghou/6Keys.git
   cd sixkeys
   ```

2. **創建開發環境**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -e ".[dev]"
   ```

3. **創建功能分支**
   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **進行開發**
   - 遵循代碼風格指南
   - 添加適當的測試
   - 更新相關文檔

5. **運行測試**
   ```bash
   pytest tests/
   flake8 sixkeys/
   black sixkeys/
   ```

6. **提交更改**
   ```bash
   git add .
   git commit -m "Add: your descriptive commit message"
   git push origin feature/your-feature-name
   ```

7. **創建 Pull Request**
   - 提供清晰的標題和描述
   - 引用相關的 issues
   - 確保所有檢查通過

## 📝 代碼風格指南

### Python 代碼風格

我們使用以下工具來維護代碼質量：

- **Black**: 代碼格式化
- **Flake8**: 代碼檢查
- **isort**: 導入排序
- **mypy**: 類型檢查（可選）

### 代碼規範

1. **命名規範**
   - 類名：`PascalCase`
   - 函數和變量：`snake_case`
   - 常量：`UPPER_CASE`
   - 私有成員：`_leading_underscore`

2. **文檔字符串**
   ```python
   def function_name(param1: type, param2: type) -> return_type:
       """
       Brief description of the function.
       
       Parameters
       ----------
       param1 : type
           Description of param1
       param2 : type
           Description of param2
           
       Returns
       -------
       return_type
           Description of return value
       """
   ```

3. **類型提示**
   - 使用類型提示來提高代碼可讀性
   - 導入類型：`from typing import Dict, List, Optional, Tuple`

4. **錯誤處理**
   - 使用適當的異常類型
   - 提供有意義的錯誤信息
   - 避免裸露的 `except:` 語句

## 🧪 測試指南

### 編寫測試

1. **測試文件結構**
   ```
   tests/
   ├── test_core/
   │   ├── test_felc.py
   │   ├── test_teb.py
   │   └── ...
   ├── test_analysis/
   │   └── test_analyzer.py
   └── test_utils/
       └── test_visualization.py
   ```

2. **測試命名**
   - 測試函數：`test_function_name_condition`
   - 測試類：`TestClassName`

3. **測試內容**
   - 單元測試：測試單個函數或方法
   - 集成測試：測試組件間的交互
   - 回歸測試：確保修復的錯誤不再出現

### 運行測試

```bash
# 運行所有測試
pytest

# 運行特定測試文件
pytest tests/test_core/test_felc.py

# 運行帶覆蓋率報告的測試
pytest --cov=sixkeys tests/

# 運行特定標記的測試
pytest -m "not slow"
```

## 📚 文檔貢獻

### 文檔類型

1. **API 文檔**：自動從代碼生成
2. **用戶指南**：`docs/` 目錄中的 Markdown 文件
3. **示例**：`examples/` 和 `notebooks/` 目錄
4. **README**：項目主頁面

### 文檔風格

- 使用清晰、簡潔的語言
- 提供實際的代碼示例
- 包含適當的數學公式（使用 LaTeX）
- 添加圖表和可視化說明

### 構建文檔

```bash
cd docs/
make html
# 或
sphinx-build -b html . _build/html
```

## 🔬 開發指南

### 項目結構

```
sixkeys/
├── sixkeys/              # 主要Python包
│   ├── core/            # 核心指標實現
│   ├── analysis/        # 分析工具
│   ├── utils/           # 工具函數
│   └── examples/        # 使用示例
├── tests/               # 測試文件
├── docs/                # 文檔
├── notebooks/           # Jupyter筆記本
├── scripts/             # 腳本工具
└── data/                # 示例數據
```

### 添加新指標

如果您想添加新的ζ指標（如ζ₃-ζ₆），請：

1. 在 `sixkeys/core/` 中創建新模組
2. 實現指標類，遵循現有的 `FELC` 和 `TEB` 模式
3. 在 `sixkeys/core/__init__.py` 中導入
4. 更新 `SixKeysAnalyzer` 以支持新指標
5. 添加相應的測試
6. 更新文檔

### 版本控制

我們使用 [語義化版本](https://semver.org/)：

- `MAJOR.MINOR.PATCH`
- MAJOR：不兼容的API更改
- MINOR：向後兼容的功能添加
- PATCH：向後兼容的錯誤修復

## 🎯 開發優先級

當前開發重點：

1. **高優先級**
   - 實現剩餘的ζ指標（ζ₃-ζ₆）
   - 真實神經數據處理功能
   - 性能優化

2. **中優先級**
   - 批量分析工具
   - 更多可視化選項
   - 交叉驗證功能

3. **低優先級**
   - GUI界面
   - 雲端部署支持
   - 額外的數據格式支持

## 🏷️ 標籤和里程碑

### Issue 標籤

- `bug`: 錯誤報告
- `enhancement`: 功能增強
- `documentation`: 文檔相關
- `good first issue`: 適合新貢獻者
- `help wanted`: 需要幫助
- `priority-high/medium/low`: 優先級

### 里程碑

- `v0.2.0`: 實現所有六個指標
- `v0.3.0`: 真實數據處理
- `v1.0.0`: 穩定版本發布

## 📞 聯繫方式

如果您有任何問題或需要幫助：

- 創建 [GitHub Issue](https://github.com/yourusername/sixkeys/issues)
- 發送郵件至：[your.email@example.com]
- 加入我們的討論：[GitHub Discussions](https://github.com/yourusername/sixkeys/discussions)

## 🙏 致謝

感謝所有貢獻者的努力！您的貢獻使這個項目變得更好。

### 貢獻者列表

- You Yang Hou - 項目創始人和主要開發者
- [您的名字] - 歡迎成為貢獻者！

---

**注意**：通過貢獻代碼，您同意您的貢獻將在 BSD 3-Clause 許可證下發布。