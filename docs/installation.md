# ⚙️ 安裝指南 | Installation Guide

**📍 當前位置**: [🏠 首頁](../README.md) > [📚 文檔中心](README.md) > ⚙️ 安裝指南

本指南提供六鑰臨界框架的詳細安裝說明，適用於不同操作系統和使用場景。

**⏱️ 預計時間**: 5-15分鐘 | **💡 難度**: 新手友好 | **🎯 目標**: 成功安裝並驗證

---

## 🚨 **快速救援** | **Quick Help**

| 遇到問題？ | 解決方案 | 說明 |
|-----------|----------|------|
| 🚫 **安裝失敗** | [故障排除](#故障排除) | 常見安裝問題 |
| 🐍 **Python版本** | [系統要求](#系統要求) | 版本兼容性 |
| 💻 **系統不支援** | [Docker安裝](#docker-安裝) | 容器化解決方案 |
| ❓ **不知道選哪個** | [快速安裝](#快速安裝) | 推薦安裝方式 |

## 📋 系統要求 | System Requirements

### 最低要求 | Minimum Requirements

- **Python**: 3.8 或更高版本
- **記憶體**: 4GB RAM
- **硬碟空間**: 2GB 可用空間
- **操作系統**: Windows 10+, macOS 10.14+, Linux (Ubuntu 18.04+)

### 推薦配置 | Recommended Configuration

- **Python**: 3.10 或 3.11
- **記憶體**: 8GB+ RAM
- **硬碟空間**: 5GB+ 可用空間
- **GPU**: NVIDIA GPU (支援CUDA，可選)
- **處理器**: 多核心CPU (4核心以上)

## 🚀 快速安裝 | Quick Installation

### 使用 pip 安裝 | Install with pip

```bash
# 安裝最新穩定版本
pip install sixkeys

# 安裝特定版本
pip install sixkeys==1.0.0

# 升級到最新版本
pip install --upgrade sixkeys
```

### 使用 conda 安裝 | Install with conda

```bash
# 從 conda-forge 安裝
conda install -c conda-forge sixkeys

# 創建新環境並安裝
conda create -n sixkeys python=3.10
conda activate sixkeys
conda install -c conda-forge sixkeys
```

## 🔧 詳細安裝步驟 | Detailed Installation Steps

### Windows 系統 | Windows System

#### 1. 安裝 Python

如果尚未安裝 Python：

1. 訪問 [Python官網](https://www.python.org/downloads/)
2. 下載 Python 3.10 或更高版本
3. 運行安裝程序，**確保勾選「Add Python to PATH」**
4. 驗證安裝：
   ```cmd
   python --version
   pip --version
   ```

#### 2. 安裝六鑰臨界

```cmd
# 打開命令提示符或PowerShell
pip install sixkeys

# 驗證安裝
python -c "import sixkeys; print(sixkeys.__version__)"
```

#### 3. 安裝可選依賴

```cmd
# 安裝可視化增強包
pip install sixkeys[viz]

# 安裝GPU加速包
pip install sixkeys[gpu]

# 安裝完整功能包
pip install sixkeys[full]
```

### macOS 系統 | macOS System

#### 1. 安裝 Homebrew (如果尚未安裝)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### 2. 安裝 Python

```bash
# 使用 Homebrew 安裝 Python
brew install python@3.10

# 或使用 pyenv 管理多個 Python 版本
brew install pyenv
pyenv install 3.10.0
pyenv global 3.10.0
```

#### 3. 安裝六鑰臨界

```bash
# 安裝基本版本
pip3 install sixkeys

# 驗證安裝
python3 -c "import sixkeys; print(sixkeys.__version__)"
```

### Linux 系統 | Linux System

#### Ubuntu/Debian

```bash
# 更新套件列表
sudo apt update

# 安裝 Python 和 pip
sudo apt install python3.10 python3.10-pip python3.10-venv

# 創建虛擬環境
python3.10 -m venv sixkeys_env
source sixkeys_env/bin/activate

# 安裝六鑰臨界
pip install sixkeys
```

#### CentOS/RHEL/Fedora

```bash
# CentOS/RHEL
sudo yum install python3.10 python3.10-pip

# Fedora
sudo dnf install python3.10 python3.10-pip

# 安裝六鑰臨界
pip3.10 install sixkeys
```

## 🐳 Docker 安裝 | Docker Installation

### 使用預建映像 | Using Pre-built Image

```bash
# 拉取最新映像
docker pull sixkeys/sixkeys:latest

# 運行容器
docker run -it --rm -p 8888:8888 sixkeys/sixkeys:latest

# 運行帶有數據卷的容器
docker run -it --rm -v /path/to/your/data:/data -p 8888:8888 sixkeys/sixkeys:latest
```

### 自建映像 | Build Your Own Image

```bash
# 克隆儲存庫
git clone https://github.com/isyanghou/6Keys.git
cd 6Keys

# 構建映像
docker build -t my-sixkeys .

# 運行容器
docker run -it --rm -p 8888:8888 my-sixkeys
```

### Docker Compose

創建 `docker-compose.yml` 文件：

```yaml
version: '3.8'
services:
  sixkeys:
    image: sixkeys/sixkeys:latest
    ports:
      - "8888:8888"
      - "8050:8050"  # 儀表板端口
    volumes:
      - ./data:/data
      - ./results:/results
    environment:
      - JUPYTER_ENABLE_LAB=yes
```

運行：

```bash
docker-compose up
```

## 🔬 開發版本安裝 | Development Installation

### 從源碼安裝 | Install from Source

```bash
# 克隆儲存庫
git clone https://github.com/isyanghou/6Keys.git
cd 6Keys

# 創建虛擬環境
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate     # Windows

# 安裝開發依賴
pip install -e ".[dev]"

# 運行測試
pytest
```

### 安裝預發布版本 | Install Pre-release Version

```bash
# 安裝最新的預發布版本
pip install --pre sixkeys

# 從測試 PyPI 安裝
pip install -i https://test.pypi.org/simple/ sixkeys
```

## ⚙️ 依賴管理 | Dependency Management

### 核心依賴 | Core Dependencies

六鑰臨界的核心依賴包括：

```
numpy>=1.20.0
scipy>=1.7.0
scikit-learn>=1.0.0
matplotlib>=3.5.0
pandas>=1.3.0
```

### 可選依賴 | Optional Dependencies

```bash
# 可視化增強
pip install sixkeys[viz]
# 包含: plotly, bokeh, seaborn

# GPU 加速
pip install sixkeys[gpu]
# 包含: cupy, numba

# 神經科學工具
pip install sixkeys[neuro]
# 包含: mne, nibabel, nilearn

# 完整安裝
pip install sixkeys[full]
# 包含所有可選依賴
```

### 依賴衝突解決 | Dependency Conflict Resolution

如果遇到依賴衝突：

```bash
# 使用 pip-tools 管理依賴
pip install pip-tools
pip-compile requirements.in
pip-sync requirements.txt

# 或使用 conda 環境
conda env create -f environment.yml
conda activate sixkeys
```

## ✅ 安裝驗證 | Installation Verification

### 基本驗證 | Basic Verification

```python
# 檢查安裝
import sixkeys
print(f"Six Keys version: {sixkeys.__version__}")

# 檢查核心功能
from sixkeys.utils import data_loader
from sixkeys.analysis import metrics

# 載入範例數據
data = data_loader.load_sample_data()
print(f"Sample data shape: {data.shape}")

# 計算指標
results = metrics.compute_critical_fluctuation(data)
print(f"Critical fluctuation: {results:.4f}")

print("Installation verified successfully!")
```

### 完整功能測試 | Full Feature Test

```python
# 運行完整測試套件
import sixkeys.tests
sixkeys.tests.run_all_tests()

# 或使用命令行
# pytest --pyargs sixkeys
```

### 效能基準測試 | Performance Benchmark

```python
from sixkeys.utils import benchmark

# 運行效能測試
benchmark_results = benchmark.run_performance_test()
print("Benchmark results:")
for test, time in benchmark_results.items():
    print(f"{test}: {time:.3f} seconds")
```

## 🔧 故障排除 | Troubleshooting

### 常見問題 | Common Issues

#### 1. ImportError: No module named 'sixkeys'

**解決方案**:
```bash
# 確認 pip 安裝路徑
pip show sixkeys

# 重新安裝
pip uninstall sixkeys
pip install sixkeys

# 檢查 Python 路徑
python -c "import sys; print(sys.path)"
```

#### 2. 依賴版本衝突

**解決方案**:
```bash
# 創建新的虛擬環境
python -m venv fresh_env
source fresh_env/bin/activate
pip install sixkeys
```

#### 3. GPU 支援問題

**解決方案**:
```bash
# 檢查 CUDA 安裝
nvidia-smi

# 安裝對應的 CUDA 版本
pip install cupy-cuda11x  # 根據您的 CUDA 版本
```

#### 4. 記憶體不足

**解決方案**:
```python
# 使用分塊處理
from sixkeys.utils import memory_management
memory_management.enable_chunked_processing(chunk_size=1000)
```

### 獲取幫助 | Getting Help

如果遇到安裝問題：

1. **檢查文檔**: [常見問題](faq.md)
2. **搜索問題**: [GitHub Issues](https://github.com/isyanghou/6Keys/issues)
3. **提交新問題**: 包含錯誤信息和系統信息
4. **聯繫支援**: isyanghou@gmail.com

### 系統信息收集 | System Information Collection

提交問題時，請包含以下信息：

```python
import sixkeys
import sys
import platform
import numpy as np
import scipy

print("=== System Information ===")
print(f"Python version: {sys.version}")
print(f"Platform: {platform.platform()}")
print(f"Six Keys version: {sixkeys.__version__}")
print(f"NumPy version: {np.__version__}")
print(f"SciPy version: {scipy.__version__}")

# 保存到文件
with open('system_info.txt', 'w') as f:
    f.write(f"Python: {sys.version}\n")
    f.write(f"Platform: {platform.platform()}\n")
    f.write(f"Six Keys: {sixkeys.__version__}\n")
```

## 🔄 更新和卸載 | Update and Uninstall

### 更新 | Update

```bash
# 更新到最新版本
pip install --upgrade sixkeys

# 檢查可用更新
pip list --outdated | grep sixkeys

# 更新所有依賴
pip install --upgrade sixkeys[full]
```

### 卸載 | Uninstall

```bash
# 卸載六鑰臨界
pip uninstall sixkeys

# 清理依賴（可選）
pip autoremove  # 如果安裝了 pip-autoremove

# 刪除虛擬環境
rm -rf venv/  # Linux/macOS
# 或
rmdir /s venv  # Windows
```

---

## 🎉 **安裝完成！下一步做什麼？** | **Installation Complete! What's Next?**

### 🚀 **立即開始**
1. **🏃‍♂️ 快速體驗**: [快速開始指南](quickstart.md) - 5分鐘上手
2. **✅ 驗證安裝**: 運行測試代碼確認一切正常
3. **📚 學習理論**: [理論背景](theory.md) - 了解框架原理

### 📋 **驗證安裝**
```python
# 快速驗證代碼
import sixkeys
print(f"✅ 六鑰臨界框架 v{sixkeys.__version__} 安裝成功！")

# 載入範例數據測試
from sixkeys.utils import sample_data
data = sample_data.load_eeg_sample()
print(f"✅ 範例數據載入成功，形狀: {data.shape}")
```

---

## 🧭 **導航欄** | **Navigation**

**📍 當前位置**: [🏠 首頁](../README.md) > [📚 文檔中心](README.md) > ⚙️ **安裝指南**

### 🔄 **相關頁面**
- **➡️ 下一步**: [🚀 快速開始](quickstart.md) - 開始使用框架
- **❓ 遇到問題**: [常見問題](faq.md) - 安裝疑難排解
- **🧠 了解原理**: [理論背景](theory.md) - 框架理論基礎
- **🔙 返回**: [📚 文檔中心](README.md) - 瀏覽所有文檔

### 🆘 **需要幫助？**
- **💬 技術支援**: [isyanghou@gmail.com](mailto:isyanghou@gmail.com)
- **🐛 安裝問題**: [GitHub Issues](https://github.com/isyanghou/6Keys/issues)
- **💡 安裝建議**: [GitHub Discussions](https://github.com/isyanghou/6Keys/discussions)

---

**💡 提示**: 安裝遇到困難？查看 [❓ 常見問題](faq.md) 中的安裝疑難排解，或直接聯繫我們獲得幫助。