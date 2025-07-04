---
title: "04-1_RFI Ricci 曲率臨界流(上)"
date: 2025-06-22
language: zh-TW
encoding: UTF-8
---
# 04-1 RFI：Ricci 曲率臨界流（上）

## 🎯 Purpose — 理論動機與文獻

### 核心動機

1. **幾何—拓撲橋樑**
   - Ollivier–Ricci 曲率 $\kappa_{ij}$ 為離散圖上度量幾何的自然推廣
   - 能同時捕捉 *局部耦合強度* 與 *全域資訊流廣度*
   - 在小世界網路中，$\bar{\kappa} \approx 0$ 對應臨界穿通閾值

2. **腦網路韌性指標**
   - 高正曲率邊緣化訊號對噪衰減
   - 高負曲率則增促爆發傳播
   - fMRI 與 MEG 研究指出：
     - 清醒腦的平均曲率 $\bar{\kappa}$ 接近零但帶細微動態起伏
     - 昏迷與深麻醉使 $\bar{\kappa} \ll 0$
     - 類癲癇爆發則短暫翻成 $\bar{\kappa} > 0$

3. **臨界流思路**
   - 把 $P(t)$（能量耗功）視為「彎曲源」
   - 腦網格會逐步經離散 Ricci flow $\partial_t g_{ij} = -2\,\kappa_{ij}$ 逼近臨界平坦面 $(\bar{\kappa} \to 0)$
   - 形成快速動態柔化機制

4. **研究缺口**
   - 多數工作只靜態比較清醒 vs. 麻醉的靜態曲率分布
   - *時間演化* 與 *臨界流動* 的量化指標付之闕如
   - 因此提出「Ricci 曲率臨界流（RFI）」作為六鑰中的第二鑰 $\Psi$ 之 **幾何判準**

---
### 🔑 核心假說

> **只有當腦網路的平均 Ricci 曲率 $\bar{\kappa}(t)$ 維持在臨界窗格 $[\kappa_{\min}, \kappa_{\max}]$ 內（$C_{\text{RFI}}=1$），系統才能保持最佳的資訊傳輸效率與抗噪韌性，對應意識的幾何基礎。**

---
## 📐 數學定式與核心方程

### Ollivier-Ricci 曲率

對於腦網路圖 $G = (V, E)$，邊 $(i,j) \in E$ 的 Ollivier-Ricci 曲率定義為：

$$
\kappa_{ij} = 1 - \frac{W_1(\mu_i, \mu_j)}{d_{ij}}
$$

其中：
- $W_1(\mu_i, \mu_j)$：節點 $i$ 和 $j$ 的鄰域分布間的 Wasserstein-1 距離  
- $d_{ij}$：節點間的測地距離  
- $\mu_i$：節點 $i$ 的鄰域概率分布  

### 平均曲率與臨界流

定義網路的平均 Ricci 曲率：

$$
\bar{\kappa}(t) = \frac{1}{|E|} \sum_{(i,j) \in E} w_{ij}(t) \cdot \kappa_{ij}(t)
$$

其中 $w_{ij}(t)$ 為時變邊權重（如功能連接強度）。

### 離散 Ricci 流演化

腦網路的幾何演化遵循離散 Ricci 流方程：

$$
\frac{\partial g_{ij}}{\partial t} = -2\kappa_{ij}(t) + \eta_{ij}(t)
$$

其中：
- $g_{ij}(t)$：時變度量張量  
- $\eta_{ij}(t)$：外部驅動項（如感覺輸入、認知負荷）  

### RFI 判準函數

定義 Ricci 曲率臨界流判準：

$$
C_{\text{RFI}} = \begin{cases}
1 & \text{if } \kappa_{\min} \leq \bar{\kappa}(t) \leq \kappa_{\max} \text{ for all } t \in [T-\tau, T] \\
0 & \text{otherwise}
\end{cases}
$$

其中：
- $\kappa_{\min}, \kappa_{\max}$：臨界窗格邊界  
- $\tau$：觀測時間窗  

### 標準化座標

將 RFI 狀態標準化為六鑰框架中的第二維：

$$
\zeta_2 = \frac{\bar{\kappa} - \kappa^\ast}{\varepsilon_2}
$$

其中：
- $\kappa^\ast = \frac{\kappa_{\min} + \kappa_{\max}}{2}$：臨界窗格中心  
- $\varepsilon_2 = \frac{\kappa_{\max} - \kappa_{\min}}{2}$：標準化尺度參數  


---
## 🔬 實作細節與計算流程

### 演算法步驟(接下頁)

```python
def compute_RFI_criterion(connectivity_matrix, kappa_min=-0.1, kappa_max=0.1, tau=100):
    """
    計算 Ricci 曲率臨界流判準
    
    Parameters:
    -----------
    connectivity_matrix : array
        功能連接矩陣時間序列 (time, nodes, nodes)
    kappa_min, kappa_max : float
        臨界窗格邊界
    tau : int
        觀測時間窗長度
    
    Returns:
    --------
    C_RFI : int
        RFI 判準 (0 或 1)
    zeta2 : float
        標準化座標
    """
    import networkx as nx
    from GraphRicciCurvature.OllivierRicci import OllivierRicci
    
    kappa_series = []
    
    for t in range(connectivity_matrix.shape[0]):
        # 構建網路圖
        G = nx.from_numpy_array(connectivity_matrix[t])
        
        # 計算 Ollivier-Ricci 曲率
        orc = OllivierRicci(G, alpha=0.5, verbose="ERROR")
        orc.compute_ricci_curvature()
        
        # 計算平均曲率
        kappa_values = [orc.G[u][v]['ricciCurvature'] for u, v in orc.G.edges()]
        kappa_mean = np.mean(kappa_values)
        kappa_series.append(kappa_mean)
    
    kappa_series = np.array(kappa_series)
    
    # 檢查最近 tau 個時間點
    recent_kappa = kappa_series[-tau:]
    
    # 判斷是否在臨界窗格內
    in_range = np.all((recent_kappa >= kappa_min) & (recent_kappa <= kappa_max))
    
    C_RFI = 1 if in_range else 0
    
    # 計算標準化座標
    kappa_ast = (kappa_min + kappa_max) / 2
    epsilon2 = (kappa_max - kappa_min) / 2
    zeta2 = (np.mean(recent_kappa) - kappa_ast) / epsilon2
    
    return C_RFI, zeta2
```

### 參數設定指引
| 參數             | 建議範圍     | 物理意義                       |
|------------------|--------------|--------------------------------|
| $\kappa_{\min}$  | -0.15        | 負曲率下界，避免過度發散       |
| $\kappa_{\max}$  | +0.15        | 正曲率上界，避免過度收斂       |
| $\tau$           | 50–200 ms    | 對應神經振盪週期               |
| $\alpha$         | 0.3–0.7      | Ollivier 參數，控制局部性      |

---
## 📊 與 CTM 管道的耦合

### 加權距離貢獻

在 CTM 框架中，RFI 通過標準化座標 $\zeta_2$ 貢獻於總體管道距離：

$$
D_w^2 = w_1\,\zeta_1^{2} + w_2\,\zeta_2^{2} + \sum_{i=3}^{6} w_i\,\zeta_i^{2}
$$

### 幾何—動力學耦合

RFI 與 FELC 的耦合關係：

$$
\frac{d\bar{\kappa}}{dt} = -\gamma \cdot |\zeta_1|^2 + \beta \cdot \nabla^2 \bar{\kappa}
$$

其中：
- $\gamma$：FELC–RFI 耦合強度  
- $\beta$：空間擴散係數  

一旦 $C_{\text{RFI}} = 0$，$|\zeta_2| \gg 1$ 拉高 $D_w$，與 FELC 崩潰事件常呈因果先後。

---

## 📝 小結

本節把 Ricci 曲率嵌入臨界流視角，給出 RFI 判準 $C_{\text{RFI}}$ 與無量綱化 $\zeta_2$，為 CTM 加權距離提供第二個（幾何層）支柱。  
下半章將示範 Bruno et al. MEG 資料集重分析，展示 $\bar{\kappa}$ 於清醒與異丙酚麻醉的時間演化。

**關鍵成果：**
- ✅ 建立了腦網路幾何的動態判準  
- ✅ 整合 Ricci 流理論與意識研究  
- ✅ 提供了可計算的臨界窗格指標  
- ✅ 與 FELC 形成動力學—幾何耦合  


---

**下一章預告：** 04-2 RFI：Ricci 曲率臨界流（下）將展示實驗驗證與臨床應用案例。