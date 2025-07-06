---
title: "03-1_FELC 自由能極限環(上)"
date: 2025-06-22
language: zh-TW
encoding: UTF-8
---
# 03-1 FELC：自由能極限環（上）

## 🎯 Purpose — 理論動機與文獻

### 核心動機

1. **從「極小」到「極限環」**
   - Friston 等人提出的自由能原理（FEP）僅聲稱系統應最小化變分自由能 $F$
   - 然而活體腦並非永遠停於靜態極小，而是保持 *低振幅、週期性波動*
   - 對應約 80–150 ms 的感知更新窗口與 $\gamma$–$\beta$ 交互振盪

2. **神經生理證據**
   - *清醒*時，自由能相關振幅呈現週期性下限
   - *深麻醉*則單調衰減並鎖死於零
   - 雙皮層雪崩實驗亦顯示臨界附近出現阻尼震盪，與「極限環」概念一致

3. **增益與意識狀態**
   - 腦幹膽鹼與 NE 系統調節神經增益 $\lambda$
   - 增益下降 $\Rightarrow$ 極限環收斂為固定點，行為上對應意識喪失

4. **研究缺口**
   - 既有自由能文獻多聚焦於平均值或趨勢
   - 缺乏 *時域形貌* 與 *臨界振幅* 之量化指標
   - 因此提出「自由能極限環（FELC）」作為六鑰中的第一鑰 $\Phi$ 之 **動態判準**
   - 並將其標準化為 $\zeta_1=\frac{\Phi-\Phi^\ast}{\varepsilon_1}$，進一步併入 CTM 的加權距離 $D_w$

---
### 🔑 核心假說

> **只有當自由能軌跡落在半徑 $r_0$、振幅 $\Delta r$ 受限的穩定極限環內（$C_{\text{FELC}}=1$），系統才可能進入 CTM 管道 $\pi(\Sigma_{\mathrm{CT}})$ 並維持 $D_w \leq \theta_c$。**

---
## 📐 數學定式與核心方程

### 極限環動力學

考慮二維相空間中的自由能動力系統：

$$\begin{cases}
\dot{F} = \lambda F - \alpha F^3 + \beta G \\
\dot{G} = -\omega F + \gamma G - \delta G^3
\end{cases}$$

其中：
- $F$：變分自由能
- $G$：輔助動力變數（對應預測誤差梯度）
- $\lambda$：線性增益參數
- $\alpha, \delta$：非線性阻尼係數
- $\beta, \gamma$：耦合強度
- $\omega$：特徵頻率

### FELC 判準函數

定義極限環穩定性判準：

$$
C_{\text{FELC}} = \begin{cases}
1 & \text{if } r_0 - \Delta r \leq |\mathbf{x}(t)| \leq r_0 + \Delta r \text{ for all } t \in [T-\tau, T] \\
0 & \text{otherwise}
\end{cases}
$$
其中：
- $\mathbf{x}(t) = (F(t), G(t))^T$：系統狀態向量  
- $r_0$：極限環標準半徑  
- $\Delta r$：允許振幅偏差  
- $\tau$：觀測時間窗  

### 標準化座標

將 FELC 狀態標準化為六鑰框架中的第一維：

$$
\zeta_1 = \frac{\Phi - \Phi^\ast}{\varepsilon_1}
$$

其中：
- $\Phi = \langle |\mathbf{x}(t)| \rangle_\tau$：時間窗內的平均軌道半徑  
- $\Phi^\ast = r_0$：理想極限環半徑  
- $\varepsilon_1$：標準化尺度參數  
### 臨界通過判準

$$
C_{\text{FELC}} = \begin{cases}
1 & \text{if } r_0 - \Delta r \leq |\mathbf{x}(t)| \leq r_0 + \Delta r \text{ for all } t \in [T-\tau, T] \\
0 & \text{otherwise}
\end{cases}
$$
---
## 🔬 實作細節與計算流程

### 參數設定指引：

| 參數         | 建議範圍     | 物理意義                           |
|--------------|--------------|------------------------------------|
| $r_0$        | 0.5–2.0      | 健康意識狀態的標準軌道半徑         |
| $\Delta r$   | 0.1–0.5      | 允許的生理變異範圍                 |
| $\tau$       | 50–200 ms    | 對應神經振盪週期                   |
| $\lambda$    | 0.1–1.0      | 神經增益，與覺醒度相關             |
| $\omega$     | 10–100 Hz    | 特徵頻率，對應 $\gamma$ 波段       |
### 演算法步驟：(接下頁)

```python
def compute_FELC_criterion(F_trajectory, G_trajectory, r0, delta_r, tau):
    """
    計算自由能極限環判準
    
    Parameters:
    -----------
    F_trajectory : array
        自由能時間序列
    G_trajectory : array  
        輔助變數時間序列
    r0 : float
        標準極限環半徑
    delta_r : float
        允許振幅偏差
    tau : int
        觀測時間窗長度
    
    Returns:
    --------
    C_FELC : int
        極限環判準 (0 或 1)
    zeta1 : float
        標準化座標
    """
    # 計算軌道半徑
    radius = np.sqrt(F_trajectory**2 + G_trajectory**2)
    
    # 檢查最近 tau 個時間點
    recent_radius = radius[-tau:]
    
    # 判斷是否在極限環範圍內
    in_range = np.all((recent_radius >= r0 - delta_r) & 
                     (recent_radius <= r0 + delta_r))
    
    C_FELC = 1 if in_range else 0
    
    # 計算標準化座標
    phi = np.mean(recent_radius)
    zeta1 = (phi - r0) / delta_r  # 使用 delta_r 作為標準化尺度
    
    return C_FELC, zeta1
```

---
## 📊 與 CTM 管道的耦合

### 加權距離貢獻

在 CTM 框架中，FELC 通過標準化座標 $\zeta_1$ 貢獻於總體管道距離：

$$
D_w^2 = w_1\,\zeta_1^{2} + \sum_{i=2}^{6}w_i\,\zeta_i^{2}
$$
當極限環崩潰（$C_{\text{FELC}} = 0$）時，$|\zeta_1| \uparrow$，$D_w$ 通常率先突破 $\theta_c$，驗證「多鑰同步崩離」敘事。

---
## 📝 小結

本節將「自由能極限環」正式定式為 Hopf 動力系統，並給出可操作的意識判準 $C_{\text{FELC}}$，同時確立與 CTM 管道距離 $D_w$ 的耦合關係。

**關鍵成果：**
- ✅ 建立了自由能的動態判準，超越靜態極小化
- ✅ 提供了可計算的極限環穩定性指標
- ✅ 整合進六鑰統一框架，支持多維度意識評估
- ✅ 為後續章節的實驗驗證奠定理論基礎
---
**下一章預告：** 03-2 FELC：自由能極限環（下） 將深入探討實驗驗證、臨床應用與侷限性分析。