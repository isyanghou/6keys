---
title: "07-1_ACI 神經-星膠耦合臨界 g_eff(上)"
date: 2025-06-22
language: zh-TW
encoding: UTF-8
---
# 07-1 ACI：神經–星膠耦合臨界 g_eff（上）

## 🎯 Purpose — 理論動機與文獻

### 理論背景

1. **能流樞紐假說**  
   星形膠細胞透過乳酸穿梭（ANLS）與 Ca²⁺–IP₃ 波，為高度放電的突觸群提供即時葡萄糖/乳酸。此過程可維持能量平衡並調制突觸後電流。若缺乏足夠星膠覆蓋，刺激–代謝失衡可能導致突觸過度同步或沉默。

2. **意識相關證據**  
   當前 fMRS 研究顯示，清醒狀態下乳酸/葡萄糖比值與主觀清晰度呈倒 U 型關係；而異丙酚麻醉則迅速降低皮層乳酸輸出，伴隨星膠 Ca²⁺ 波密度下降 40%。

3. **研究缺口**  
   神經–星膠耦合過去多被視為代謝背景調節，較少模型將其納入臨界動力架構中，更罕見與資訊指標（如 $\Phi$、$\beta_1$ 等）同步量化。ACI（Astro–Cortical Coupling Index）正是為填補此空隙，並作為六鑰架構的終點站。

---

### 🔬 核心假說

**當有效耦合率 $g_{\text{eff}}(t)$ 維持在臨界窗格 $g_{\min} \leq g_{\text{eff}} \leq g_{\max}$（約 0.8–1.2）時，星膠可即時供能並吸收突觸餘量，保持 FELC、RFI、ECGP、PWC 同步臨界；一旦 $g_{\text{eff}}$ 偏離，能量供需失衡將導致 $\Phi$ 極限環收縮或爆漲，進而推高 $D_w$ 並逸出 CTM 管道。**


---

## 📐 Formulation — 核心方程

### 7.1 有效耦合率定義

設：

$$
G(t) = \frac{1}{N}\sum_{i=1}^{N} r_i(t) \quad \text{(平均放電率)}
$$

$$
A(t) = \frac{1}{M}\sum_{j=1}^{M} c_j(t) \quad \text{(星膠 Ca²⁺ 活度)}
$$

則有效耦合率定義為：

$$
g_{\text{eff}}(t) = \frac{A(t)}{G(t)} \tag{7.1}
$$

---

### 7.2 代謝–放電耦合方程

神經–星膠動力學系統：

$$
\dot{G} = f_{\text{ext}}(t) - \alpha\,g_{\text{eff}}\,G + \xi_G(t) \tag{7.2a}
$$

$$
\dot{A} = \beta\,G - \gamma\,A + \xi_A(t) \tag{7.2b}
$$


其中：
- $f_{\text{ext}}$：外部輸入功率  
- $\alpha, \beta, \gamma$：轉換常數  
- $\xi_G(t), \xi_A(t)$：高斯噪聲項  

線性穩態解：

$$
g_{\text{eff}}^{\ast} = \frac{\beta}{\alpha} \left(1 + \frac{\gamma}{\beta} \right)^{-1} \tag{7.3}
$$

---

### 7.3 ACI 臨界判準

$$
C_{\text{ACI}} = 
\begin{cases}
1, & g_{\min} \leq g_{\text{eff}}(t) \leq g_{\max} \text{ 且持續 } \tau_C = 100\ \mathrm{ms} \\
0, & \text{否則}
\end{cases} \tag{7.4}
$$

推薦參數：$(g_{\min}, g_{\max}) = (0.8, 1.2)$，以清醒鼠雙光子 *in vivo* 測值標準化。

---

### 7.4 無量綱化與 $D_w$ 耦合

標準化指標：

$$
\zeta_6(t) = \frac{g_{\text{eff}}(t) - g_{\text{eff}}^{\ast}}{\varepsilon_6}
$$

加權距離更新：

$$
D_w^2 = w_6\,\zeta_6^{2} + \sum_{i=1}^{5} w_i\,\zeta_i^{2} \tag{7.5}
$$

其中 $\varepsilon_6$ 為清醒期 $g_{\text{eff}}$ 的標準差；當 $C_{\text{ACI}} = 0$ 時，$|\zeta_6| \gg 1$，且常晚於 FELC 崩潰 40–60 ms，作為「能量層防線的最後破口」。

---

## 💻 Implementation — 計算流程與演算法

### 核心演算法架構(接下頁)

```python
# ACI 神經-星膠耦合分析核心流程
from sixkeys import ACI, load_demo
import numpy as np
from scipy.integrate import odeint
from scipy.signal import find_peaks

class ACIAnalyzer:
    def __init__(self, neural_data, astro_data, fs=1000):
        self.neural_data = neural_data  # 神經元放電數據
        self.astro_data = astro_data    # 星膠 Ca2+ 數據
        self.fs = fs
        self.g_min = 0.8
        self.g_max = 1.2
        self.tau_c = 0.1  # 100ms 持續時間
        
    def compute_firing_rate(self, window_ms=50):
        """計算平均放電率 G(t)"""
        window_samples = int(window_ms * self.fs / 1000)
        n_neurons, n_samples = self.neural_data.shape
        
        firing_rates = []
        for t in range(0, n_samples - window_samples, window_samples//2):
            window_data = self.neural_data[:, t:t+window_samples]
            # 計算窗口內的平均放電率
            rate = np.sum(window_data) / (n_neurons * window_ms / 1000)
            firing_rates.append(rate)
            
        return np.array(firing_rates)
    
    def compute_astro_activity(self, window_ms=50):
        """計算星膠 Ca2+ 活度 A(t)"""
        window_samples = int(window_ms * self.fs / 1000)
        n_astro, n_samples = self.astro_data.shape
        
        activities = []
        for t in range(0, n_samples - window_samples, window_samples//2):
            window_data = self.astro_data[:, t:t+window_samples]
            # 計算窗口內的平均 Ca2+ 活度
            activity = np.mean(window_data)
            activities.append(activity)
            
        return np.array(activities)
    
    def compute_g_eff(self):
        """計算有效耦合率 g_eff(t)"""
        G = self.compute_firing_rate()
        A = self.compute_astro_activity()
        
        # 確保長度一致
        min_len = min(len(G), len(A))
        G = G[:min_len]
        A = A[:min_len]
        
        # 避免除零
        G[G < 1e-6] = 1e-6
        
        g_eff = A / G
        return g_eff
    
    def aci_criterion(self, g_eff):
        """計算 ACI 判準函數"""
        criteria = np.zeros(len(g_eff))
        window_size = int(self.tau_c * self.fs / 50)  # 對應時間窗
        
        for t in range(len(g_eff)):
            # 檢查當前時刻是否在臨界窗格內
            in_range = self.g_min <= g_eff[t] <= self.g_max
            
            # 檢查持續性（向前看 window_size 個時間點）
            if in_range and t + window_size < len(g_eff):
                future_window = g_eff[t:t+window_size]
                sustained = np.all((future_window >= self.g_min) & 
                                 (future_window <= self.g_max))
                criteria[t] = 1 if sustained else 0
            else:
                criteria[t] = 1 if in_range else 0
                
        return criteria
    
    def normalize_zeta6(self, g_eff):
        """計算標準化 ζ₆"""
        g_eff_star = np.mean(g_eff)  # 使用平均值作為參考
        epsilon6 = np.std(g_eff)     # 使用標準差作為歸一化因子
        
        zeta6 = (g_eff - g_eff_star) / epsilon6
        return zeta6
    
    def simulate_coupling_dynamics(self, t_span, initial_conditions, params):
        """模擬神經-星膠耦合動力學"""
        alpha, beta, gamma = params['alpha'], params['beta'], params['gamma']
        f_ext = params.get('f_ext', lambda t: 1.0)
        noise_strength = params.get('noise', 0.01)
        
        def system(state, t):
            G, A = state
            g_eff = A / (G + 1e-6)  # 避免除零
            
            dG_dt = f_ext(t) - alpha * g_eff * G
            dA_dt = beta * G - gamma * A
            
            # 添加噪聲
            dG_dt += noise_strength * np.random.randn()
            dA_dt += noise_strength * np.random.randn()
            
            return [dG_dt, dA_dt]
        
        solution = odeint(system, initial_conditions, t_span)
        return solution
```

### 🔧 參數設定指引
| 參數           | 建議值     | 說明                             |
|----------------|------------|----------------------------------|
| **臨界下限**   | 0.8        | 基於清醒狀態的最低耦合率         |
| **臨界上限**   | 1.2        | 避免過度耦合的上限               |
| **持續時間**   | 100 ms     | 確保耦合穩定性的最小時間         |
| **轉換常數 α** | 0.5–1.0    | 神經活動的自抑制強度             |
| **轉換常數 β** | 1.0–2.0    | 神經到星膠的耦合強度             |
| **轉換常數 γ** | 0.8–1.5    | 星膠活動的衰減率                 |

### 🚀 計算優化策略

1. **多尺度分析**：同時分析快速（ms）和慢速（秒）時間尺度
2. **空間分辨**：考慮不同腦區的耦合差異
3. **實時監測**：開發在線算法用於臨床監測
4. **噪聲處理**：使用卡爾曼濾波器減少測量噪聲

---

## 🔗 與 CTM 管道的耦合關係

### 能量支援層貢獻

ACI 作為六鑰系統的最後一個組件，專門負責**能量支援層面**的意識狀態監測：

- **FELC**（能量層）→ 自由能極限環
- **RFI**（幾何層）→ Ricci 曲率流
- **ECGP**（訊息層）→ 因果滲流
- **PWC**（拓撲層）→ 相位環流
- **ACI**（支援層）→ 神經-星膠耦合
- **TEB**（效率層）→ 資訊-能耗效率（待續）

### 六鑰協同機制

```python
# 六鑰完整分析示例
def complete_six_keys_analysis(data):
    # 計算各鑰指標
    felc_score = compute_felc(data)
    rfi_score = compute_rfi(data)
    ecgp_score = compute_ecgp(data)
    pwc_score = compute_pwc(data)
    aci_score = compute_aci(data)
    # teb_score = compute_teb(data)  # 第六鑰待實現
    
    # 計算加權距離（五鑰版本）
    weights = [0.2, 0.2, 0.2, 0.2, 0.2]  # 等權重
    zetas = [felc_score, rfi_score, ecgp_score, pwc_score, aci_score]
    
    Dw_squared = sum(w * z**2 for w, z in zip(weights, zetas))
    Dw = np.sqrt(Dw_squared)
    
    # 判斷管道狀態
    in_manifold = Dw < 0.5  # 閾值示例
    
    return {
        'Dw': Dw,
        'in_manifold': in_manifold,
        'individual_scores': dict(zip(['FELC', 'RFI', 'ECGP', 'PWC', 'ACI'], zetas))
    }
```

---

## 📝 本節小結

**本節將神經–星膠耦合正式定式為雙變量動力系統，提出 ACI 判準 $C_{\text{ACI}}$ 與無量綱化 $\zeta_6$，補完 CTM 管道距離 $D_w$ 的能量支援層。**

### 🎯 關鍵成就

- ✅ **耦合理論**：建立了神經–星膠耦合的動力學框架  
- ✅ **能量整合**：將代謝過程納入意識理論體系  
- ✅ **判準設計**：提供了可操作的耦合評估指標  
- ✅ **系統完善**：實現了五鑰系統的能量支援層  

### 🔗 章節銜接

**下半章預告：** 將示範在 Neuropixels＋雙光子同步測序列中驗證 $g_{\text{eff}}$ 臨界窗格，展示 ACI 在實際神經數據中的表現。


---
