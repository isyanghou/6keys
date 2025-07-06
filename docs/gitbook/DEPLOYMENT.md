# GitBook 部署指南

本指南說明如何將「六鑰臨界」理論文檔部署到 GitBook 和 GitHub Pages。

## 📁 目錄結構

```
docs/gitbook/
├── README.md              # 書籍簡介
├── SUMMARY.md             # 目錄結構
├── book.json              # GitBook 配置
├── package.json           # 依賴管理
├── .gitignore            # 忽略文件
├── .markdownlint.json    # Markdown 格式檢查
├── DEPLOYMENT.md         # 本文件
├── quick-navigation.md   # 快速導航
├── core-concepts/        # 核心概念章節
│   ├── README.md
│   ├── q1-1.md
│   ├── q1-2.md
│   └── q1-3.md
└── .github/
    └── workflows/
        ├── gitbook.yml           # 自動部署工作流
        └── mlc_config.json       # 連結檢查配置
```

## 🚀 部署方法

### 方法一：新版 GitBook 平台（推薦）

1. **登入 GitBook**
   - 訪問 [GitBook.com](https://www.gitbook.com/)
   - 使用 GitHub 帳號登入

2. **創建新書籍**
   - 點擊「New Space」
   - 選擇「Import from GitHub」
   - 選擇你的倉庫和 `docs/gitbook` 資料夾

3. **配置同步**
   - 設定 GitHub 同步
   - 選擇主分支（main 或 master）
   - 設定自動同步

4. **發佈**
   - 設定書籍為公開
   - 獲得 GitBook 網址

### 方法二：GitHub Pages + GitBook CLI

1. **本地安裝**
   ```bash
   cd docs/gitbook
   npm install -g gitbook-cli
   npm install
   gitbook install
   ```

2. **本地預覽**
   ```bash
   gitbook serve
   # 訪問 http://localhost:4000
   ```

3. **構建靜態網站**
   ```bash
   gitbook build
   ```

4. **推送到 GitHub**
   ```bash
   git add .
   git commit -m "Add GitBook content"
   git push origin main
   ```

5. **啟用 GitHub Pages**
   - 進入倉庫設定
   - 找到 Pages 設定
   - 選擇 `gh-pages` 分支
   - 設定路徑為 `/gitbook`

## 🤖 自動化部署

### GitHub Actions 工作流

已配置的 `.github/workflows/gitbook.yml` 會自動：

1. **觸發條件**
   - 推送到 main/master 分支
   - `docs/gitbook/` 路徑有變更
   - 手動觸發

2. **執行步驟**
   - 安裝 Node.js 和 GitBook CLI
   - 安裝依賴和插件
   - 構建 GitBook
   - 部署到 GitHub Pages
   - 生成 PDF（可選）

3. **品質檢查**
   - Markdown 格式檢查
   - 連結有效性檢查

### 啟用自動部署

1. **確保工作流文件存在**
   ```bash
   ls .github/workflows/gitbook.yml
   ```

2. **推送到 GitHub**
   ```bash
   git add .github/
   git commit -m "Add GitBook auto-deployment"
   git push origin main
   ```

3. **檢查 Actions**
   - 進入 GitHub 倉庫
   - 點擊 "Actions" 標籤
   - 查看工作流執行狀態

## 📝 內容管理

### 添加新章節

1. **創建 Markdown 文件**
   ```bash
   # 例如添加新的核心概念問題
   touch core-concepts/q1-4.md
   ```

2. **更新 SUMMARY.md**
   ```markdown
   * [核心概念](core-concepts/README.md)
     * [問題 1.1](core-concepts/q1-1.md)
     * [問題 1.2](core-concepts/q1-2.md)
     * [問題 1.3](core-concepts/q1-3.md)
     * [問題 1.4](core-concepts/q1-4.md)  # 新增
   ```

3. **編寫內容**
   - 使用 Markdown 語法
   - 支援 LaTeX 數學公式（$...$ 和 $$...$$）
   - 添加內部連結

### 數學公式支援

使用 KaTeX 插件，支援：

```markdown
行內公式：$E = mc^2$

塊級公式：
$$
D_w = \sqrt{\sum_{i=1}^{6} w_i (\zeta_i - \zeta_i^{\text{critical}})^2}
$$
```

### 內部連結

```markdown
[相對連結](../other-chapter/file.md)
[錨點連結](file.md#section)
[外部連結](https://example.com)
```

## 🔧 配置說明

### book.json 主要配置

- **插件**：數學公式、搜尋、導航等
- **主題**：自定義外觀
- **PDF**：生成設定
- **變數**：版本號等

### package.json 腳本

```bash
npm run serve    # 本地預覽
npm run build    # 構建
npm run install  # 安裝插件
npm run pdf      # 生成 PDF
npm run clean    # 清理構建文件
```

## 🌐 訪問網址

部署成功後，可通過以下網址訪問：

- **GitBook 平台**：`https://your-org.gitbook.io/sixkeys-criticality/`
- **GitHub Pages**：`https://your-username.github.io/sixkeys/gitbook/`

## 🔍 故障排除

### 常見問題

1. **構建失敗**
   - 檢查 `book.json` 語法
   - 確認所有連結有效
   - 查看 Actions 日誌

2. **數學公式不顯示**
   - 確認 KaTeX 插件已安裝
   - 檢查公式語法

3. **GitHub Pages 404**
   - 確認 Pages 設定正確
   - 檢查分支和路徑

### 調試命令

```bash
# 檢查 GitBook 版本
gitbook --version

# 詳細構建日誌
gitbook build --debug

# 檢查插件
gitbook ls

# 重新安裝插件
gitbook install
```

## 📚 進階功能

### 多語言支援

可以創建多語言版本：

```
docs/gitbook/
├── zh/          # 中文版
├── en/          # 英文版
└── LANGS.md     # 語言配置
```

### 自定義域名

1. **GitHub Pages**
   - 添加 `CNAME` 文件
   - 配置 DNS

2. **GitBook 平台**
   - 升級到付費方案
   - 在設定中配置域名

### PDF 自動生成

工作流會自動生成 PDF 版本，可在 Actions 的 Artifacts 中下載。

## 📞 支援

如有問題，請：

1. 查看 [GitBook 官方文檔](https://docs.gitbook.com/)
2. 檢查 GitHub Issues
3. 聯繫項目維護者

---

**提示**：建議先在本地測試，確認無誤後再推送到 GitHub！