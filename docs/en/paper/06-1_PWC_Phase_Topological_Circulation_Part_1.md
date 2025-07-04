---
title: "06-1_PWC Phase Topological Circulation β₁ (Part 1)"
date: 2025-06-22
language: en-US
encoding: UTF-8
---
# 06-1 PWC: Phase Topological Circulation β₁ (Part 1)

## 🎯 Purpose — Theoretical Motivation and Literature

### Theoretical Background

1. **From Synchronization to Circulation**  
   Critical brain involves not only spike synchronization, but also **connectivity and circulation in phase space**. TDA research shows that the first Betti number $β_1$ of awake EEG phase point clouds slowly drifts in the 2–6 range; while under deep anesthesia it drops sharply to $β_1 = 0$, indicating phase circulation collapse and topological fragmentation.

2. **Brain Rhythm Interactive Cycles**  
   Brain rhythm interaction mechanisms such as $\theta$–$\gamma$ nesting and $\beta$–$\alpha$ CFC rely on stable phase circulation channels. When topological circulation disappears, traditional CFC indicators (MI, PLV) also collapse synchronously.

3. **Research Gap**  
   Current work mostly uses average PLV and other indicators, but few people track time-varying connectivity from **topological structure of high-dimensional phase point clouds**. Therefore, we propose the "Phase–Winding Circulation (PWC)" module, using $β_1$ as the core topological quantity, incorporating it into the six-key framework and corresponding to dimensionless coordinate $\zeta_5$.
### 🔬 Core Hypothesis

**When phase point clouds maintain 2–6 consistent circulation paths ($β_1 \in [2,6]$), brain networks can support cross-frequency coupling and information loops without excessive synchronization. At this time, $\zeta_5$ maintains $|\zeta_5| \leq 1$ and helps $D_w$ stay within the CTM pipeline. Once $β_1$ falls to 0 or explodes >10, topological circulation collapses or disintegrates, $D_w$ immediately rises and leads to consciousness instability.**

---
## 📐 Formulation — Core Equations

### 6.1 Phase Reconstruction and Point Cloud

For each channel $\phi_k(t) = \arg(\mathcal{H}[x_k(t)])$ (Hilbert analytic phase), compose $d$-dimensional phase vector $\boldsymbol{\phi}(t) \in \mathbb{T}^d$.

Obtain point cloud by sliding sampling with embedding window $\Delta t = 100$ ms:

$$
\mathcal{P}(t) = \{\boldsymbol{\phi}(t - \tau_j)\}_{j=1}^{m}
$$

Using circulation window $m = 200$ points.

### 6.2 Constructing Vietoris–Rips Complex

Phase distance defined as:

$$
d_{\text{wrap}}(\phi_i, \phi_j) = \min_{k \in \mathbb{Z}} \lVert \boldsymbol{\phi}_i - \boldsymbol{\phi}_j + 2\pi k \rVert_2
$$

Set radius $\epsilon = 0.4$, obtain VR complex $\text{VR}_\epsilon(\mathcal{P})$; compute persistent homology $β_1(t)$ through Ripser GPU algorithm.

### 6.3 PWC Indicator and Binary Criterion

Define standardized indicator:

$$
β_1^{\text{norm}}(t) = \frac{β_1(t) - β_1^\ast}{\varepsilon_5}, \quad \zeta_5(t) = β_1^{\text{norm}}(t)
$$

PWC binary criterion:

$$
C_{\text{PWC}} =
\begin{cases}
1, & 2 \leq β_1(t) \leq 6 \text{ and } |\dot{β}_1| \leq 0.2 \text{ for } \tau_C\; (100\text{ ms}) \\
0, & \text{otherwise}
\end{cases} \tag{6.1}
$$

Where $β_1^\ast = 4$, $\varepsilon_5 = 1.5$ are estimates based on awake baseline.

### 6.4 Dimensionless Coupling to $D_w$

$$
D_w^2 = w_5\,\zeta_5^{2} + \sum_{i \neq 5} w_i\,\zeta_i^{2} \tag{6.2}
$$

If $C_{\text{PWC}} = 0$ (circulation channel collapse or fragmentation), then $|\zeta_5|$ increases, making $D_w$ easily break $\theta_c$. This phenomenon is common in deep sleep K-complex or propofol burst–suppression precursor stages.

---
## 💻 Implementation — Computational Process and Algorithms

### Core Algorithm Architecture (continued on next page)

```python
# PWC topological analysis core process
from sixkeys import PWC, load_demo
import numpy as np
from ripser import ripser
from scipy.signal import hilbert

class PWCAnalyzer:
    def __init__(self, data, fs=1000, embed_win=0.1, epsilon=0.4):
        self.data = data
        self.fs = fs
        self.embed_win = int(embed_win * fs)  # 100ms window
        self.epsilon = epsilon
        self.beta1_target = 4
        self.epsilon5 = 1.5
    
    def extract_phases(self):
        """Extract multi-channel Hilbert phases"""
        phases = np.zeros_like(self.data)
        for ch in range(self.data.shape[1]):
            analytic = hilbert(self.data[:, ch])
            phases[:, ch] = np.angle(analytic)
        return phases
    
    def sliding_point_cloud(self, phases):
        """Construct phase point cloud with sliding window"""
        n_samples, n_channels = phases.shape
        point_clouds = []
        
        for t in range(self.embed_win, n_samples):
            # Extract phase vectors within time window
            window_phases = phases[t-self.embed_win:t, :]
            point_clouds.append(window_phases)
        
        return point_clouds
    
    def compute_betti1(self, point_cloud):
        """Compute first Betti number"""
        # Compute phase distance matrix (considering periodicity)
        distances = self._phase_distance_matrix(point_cloud)
        
        # Use Ripser to compute persistent homology
        result = ripser(distances, metric='precomputed', maxdim=1)
        
        # Extract β₁ (number of 1-dimensional holes)
        h1_bars = result['dgms'][1]
        beta1 = len(h1_bars[h1_bars[:, 1] - h1_bars[:, 0] > 0.1])
        
        return beta1
    
    def _phase_distance_matrix(self, phases):
        """Compute wrapped distance between phase points"""
        n_points = len(phases)
        distances = np.zeros((n_points, n_points))
        
        for i in range(n_points):
            for j in range(i+1, n_points):
                # Compute wrapped phase distance
                diff = phases[i] - phases[j]
                wrapped_diff = np.angle(np.exp(1j * diff))
                distances[i, j] = distances[j, i] = np.linalg.norm(wrapped_diff)
        
        return distances
    
    def pwc_criterion(self, beta1_series):
        """Compute PWC criterion function"""
        criteria = np.zeros(len(beta1_series))
        
        for t in range(len(beta1_series)):
            # Check β₁ range
            in_range = 2 <= beta1_series[t] <= 6
            
            # Check rate of change (if sufficient historical data)
            if t > 0:
                rate_stable = abs(beta1_series[t] - beta1_series[t-1]) <= 0.2
            else:
                rate_stable = True
            
            criteria[t] = 1 if (in_range and rate_stable) else 0
        
        return criteria
    
    def normalize_zeta5(self, beta1_series):
        """Compute standardized ζ₅"""
        return (beta1_series - self.beta1_target) / self.epsilon5
```

### 🔧 Parameter Setting Guidelines

| Parameter             | Recommended Value | Description                                 |
|----------------------|-------------------|---------------------------------------------|
| **Embedding Window** | 100 ms            | Balance time resolution and topological stability |
| **VR Radius**        | 0.4               | Based on typical distance scale in phase space |
| **Target $β_1$**     | 4                 | Typical circulation count in awake state   |
| **Tolerance $\varepsilon_5$** | 1.5               | Allowed $β_1$ fluctuation range           |
| **Stability Threshold** | 0.2               | Stability requirement for $β_1$ rate of change |

### 🚀 Computational Optimization Strategies

1. **GPU Acceleration**: Use Ripser++ or GUDHI GPU version
2. **Parallel Processing**: Multi-threading for different time windows
3. **Memory Management**: Sliding window avoids redundant computation
4. **Approximation Algorithms**: Use landmark sampling for large-scale data

---
## 🔗 Coupling Relationship with CTM Pipeline

### Topological Layer Contribution

PWC serves as the fifth component of the six-key system, specifically responsible for **topological level** consciousness state monitoring:

- **FELC** (Energy Layer) → Free Energy Limit Cycle
- **RFI** (Geometric Layer) → Ricci Curvature Flow
- **ECGP** (Information Layer) → Causal Percolation
- **PWC** (Topological Layer) → Phase Circulation
- **To be continued** (Integration Layer) → Sixth Key
### Multi-Key Synergistic Mechanism (continued on next page)

```python
# Multi-key synchronous analysis example
def multi_key_analysis(data):
    # Compute each key indicator
    felc_score = compute_felc(data)
    rfi_score = compute_rfi(data)
    ecgp_score = compute_ecgp(data)
    pwc_score = compute_pwc(data)
    
    # Compute weighted distance
    weights = [0.25, 0.25, 0.25, 0.25]  # Equal weights
    zetas = [felc_score, rfi_score, ecgp_score, pwc_score]
    
    Dw_squared = sum(w * z**2 for w, z in zip(weights, zetas))
    Dw = np.sqrt(Dw_squared)
    
    # Determine pipeline state
    in_manifold = Dw < 0.5  # Threshold example
    
    return {
        'Dw': Dw,
        'in_manifold': in_manifold,
        'individual_scores': dict(zip(['FELC', 'RFI', 'ECGP', 'PWC'], zetas))
    }
```

---
## 📝 Section Summary

**This section formally formulates phase topological circulation as Betti$_1$ dynamics of sliding embedded point clouds, and proposes PWC criterion $C_{\text{PWC}}$ and dimensionless $\zeta_5$, filling the topological layer of CTM pipeline distance $D_w$.**
### 🎯 Key Achievements
- ✅ **Topological Theory**: Established mathematical framework for phase space topological analysis
- ✅ **Computational Methods**: Provided efficient β₁ calculation algorithms
- ✅ **Criterion Function**: Designed robust PWC binary criterion
- ✅ **System Integration**: Achieved seamless coupling with the other four keys