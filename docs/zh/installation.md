# 安裝指南

本指南將幫助您在不同環境中安裝和配置六鑰臨界框架。

## 📝 項目信息

**作者**: You Yang Hou  
**郵箱**: [isyanghou@gmail.com](mailto:isyanghou@gmail.com)  
**ORCID**: [0009-0000-7041-8574](https://orcid.org/0009-0000-7041-8574)  
**項目倉庫**: [https://github.com/isyanghou/6Keys](https://github.com/isyanghou/6Keys)  
**授權條款**: 論文內容採用 CC BY-NC 4.0，程式碼採用 BSD 3-Clause

## 📋 系統要求

### 基本要求
- **Python**: 3.8 或更高版本
- **操作系統**: Windows 10+, macOS 10.14+, Linux (Ubuntu 18.04+)
- **內存**: 建議 8GB 或以上
- **存儲空間**: 至少 2GB 可用空間

### 推薦配置
- **Python**: 3.9+ (最佳性能)
- **內存**: 16GB 或以上 (處理大型數據集)
- **GPU**: 支援 CUDA 的 NVIDIA GPU (可選，用於加速計算)

## 🚀 安裝方法

### 方法一：從 PyPI 安裝 (推薦)

```bash
# 基本安裝
pip install sixkeys

# 包含所有可選依賴的完整安裝
pip install "sixkeys[all]"

# 僅安裝開發依賴
pip install "sixkeys[dev]"
```

### 方法二：從源碼安裝

```bash
# 克隆倉庫
git clone https://github.com/yourusername/sixkeys.git
cd sixkeys

# 創建虛擬環境 (推薦)
python -m venv venv

# 激活虛擬環境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 安裝包
pip install -e .

# 或安裝開發版本
pip install -e ".[dev]"
```

### 方法三：使用 Conda

```bash
# 創建新的 conda 環境
conda create -n sixkeys python=3.9
conda activate sixkeys

# 安裝依賴
conda install numpy scipy matplotlib pandas scikit-learn
pip install sixkeys
```

## 🔧 環境配置

### 1. 虛擬環境設置 (強烈推薦)

```bash
# 使用 venv
python -m venv sixkeys_env
source sixkeys_env/bin/activate  # Linux/macOS
# 或
sixkeys_env\Scripts\activate     # Windows

# 使用 conda
conda create -n sixkeys python=3.9
conda activate sixkeys
```

### 2. 依賴管理

項目使用以下核心依賴：

```txt
numpy>=1.21.0          # 數值計算
scipy>=1.7.0           # 科學計算
matplotlib>=3.5.0      # 基礎繪圖
seaborn>=0.11.0        # 統計繪圖
pandas>=1.3.0          # 數據處理
scikit-learn>=1.0.0    # 機器學習
networkx>=2.6          # 網絡分析
numba>=0.56.0          # 數值優化
statsmodels>=0.13.0    # 統計分析
tqdm>=4.62.0           # 進度條
pyyaml>=6.0            # 配置文件
```

### 3. 可選依賴

```bash
# 神經影像數據支持
pip install nibabel mne

# 高級可視化
pip install plotly bokeh

# Jupyter 支持
pip install jupyter ipywidgets

# 測試和開發工具
pip install pytest pytest-cov black flake8 mypy
```

## ✅ 安裝驗證

### 基本功能測試

```python
# 測試導入
import sixkeys as sk
print(f"Six Keys version: {sk.__version__}")

# 測試核心模組
from sixkeys.core import FELC, TEB, RFI, ECGP, PWC, ACI
print("所有核心模組導入成功！")

# 快速功能測試
analyzer = sk.SixKeysAnalyzer()
results = analyzer.analyze_simulated_data(duration=1.0)
print(f"模擬分析完成，D_w = {results.d_total:.3f}")
```

### 運行測試套件

```bash
# 運行所有測試
pytest tests/

# 運行特定測試
pytest tests/test_felc.py -v

# 檢查代碼覆蓋率
pytest --cov=sixkeys tests/
```

## 🐛 常見問題

### 問題 1: ImportError: No module named 'sixkeys'

**解決方案:**
```bash
# 確認安裝
pip list | grep sixkeys

# 重新安裝
pip uninstall sixkeys
pip install sixkeys
```

### 問題 2: NumPy/SciPy 版本衝突

**解決方案:**
```bash
# 更新到兼容版本
pip install --upgrade numpy scipy

# 或使用 conda 管理科學計算包
conda install numpy scipy matplotlib
```

### 問題 3: Windows 上的編譯錯誤

**解決方案:**
```bash
# 安裝 Microsoft C++ Build Tools
# 或使用預編譯的 wheel
pip install --only-binary=all sixkeys
```

### 問題 4: 內存不足錯誤

**解決方案:**
- 減少數據集大小
- 使用批處理模式
- 增加虛擬內存
- 使用更高效的數據類型

## 🔄 更新和卸載

### 更新到最新版本

```bash
# 更新 sixkeys
pip install --upgrade sixkeys

# 檢查版本
python -c "import sixkeys; print(sixkeys.__version__)"
```

### 完全卸載

```bash
# 卸載包
pip uninstall sixkeys

# 清理緩存
pip cache purge

# 刪除虛擬環境 (如果使用)
rm -rf sixkeys_env  # Linux/macOS
# 或
rmdir /s sixkeys_env  # Windows
```

## 📞 獲取幫助

如果遇到安裝問題：

1. 查看 [常見問題](faq.md)
2. 搜索 [GitHub Issues](https://github.com/yourusername/sixkeys/issues)
3. 創建新的 issue 並提供：
   - 操作系統和版本
   - Python 版本
   - 完整的錯誤信息
   - 安裝命令和步驟

## 🎯 下一步

安裝完成後，建議：

1. 閱讀 [快速開始指南](quickstart.md)
2. 查看 [基礎教程](tutorials/basic_tutorial.md)
3. 運行 [示例代碼](examples/)
4. 探索 [API 文檔](api_reference.md)

---

**提示**: 建議在虛擬環境中安裝，避免與其他項目的依賴衝突。