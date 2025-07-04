---
title: "04-1_RFI Ricci Curvature Critical Flow (Part 1)"
date: 2025-06-22
language: en-US
encoding: UTF-8
---
# 04-1 RFI: Ricci Curvature Critical Flow (Part 1)

## 🎯 Purpose — Theoretical Motivation and Literature

### Core Motivation

1. **Geometric-Topological Bridge**
   - Ollivier–Ricci curvature $\kappa_{ij}$ provides a natural extension of metric geometry to discrete graphs
   - Simultaneously captures *local coupling strength* and *global information flow breadth*
   - In small-world networks, $\bar{\kappa} \approx 0$ corresponds to critical percolation thresholds

2. **Brain Network Resilience Indicator**
   - High positive curvature edges marginalize signal-to-noise attenuation
   - High negative curvature promotes burst propagation
   - fMRI and MEG studies indicate:
     - Average curvature $\bar{\kappa}$ in awake brain approaches zero with subtle dynamic fluctuations
     - Coma and deep anesthesia result in $\bar{\kappa} \ll 0$
     - Epileptic-like bursts briefly flip to $\bar{\kappa} > 0$

3. **Critical Flow Approach**
   - Treat $P(t)$ (energy consumption) as "curvature source"
   - Brain networks gradually approach critical flat surfaces $(\bar{\kappa} \to 0)$ through discrete Ricci flow $\partial_t g_{ij} = -2\,\kappa_{ij}$
   - Forms rapid dynamic softening mechanism

4. **Research Gap**
   - Most work only statically compares awake vs. anesthetized static curvature distributions
   - Quantitative indicators for *temporal evolution* and *critical flow dynamics* are lacking
   - Therefore, we propose "Ricci Curvature Critical Flow (RFI)" as the second key $\Psi$ in the six-key framework's **geometric criterion**

---
### 🔑 Core Hypothesis

> **Only when the brain network's average Ricci curvature $\bar{\kappa}(t)$ maintains within the critical window $[\kappa_{\min}, \kappa_{\max}]$ ($C_{\text{RFI}}=1$), can the system preserve optimal information transmission efficiency and noise resilience, corresponding to the geometric foundation of consciousness.**

---
## 📐 Mathematical Formulation and Core Equations

### Ollivier-Ricci Curvature

For brain network graph $G = (V, E)$, the Ollivier-Ricci curvature of edge $(i,j) \in E$ is defined as:

$$
\kappa_{ij} = 1 - \frac{W_1(\mu_i, \mu_j)}{d_{ij}}
$$

where:
- $W_1(\mu_i, \mu_j)$: Wasserstein-1 distance between neighborhood distributions of nodes $i$ and $j$  
- $d_{ij}$: Geodesic distance between nodes  
- $\mu_i$: Neighborhood probability distribution of node $i$  

### Average Curvature and Critical Flow

Define the network's average Ricci curvature:

$$
\bar{\kappa}(t) = \frac{1}{|E|} \sum_{(i,j) \in E} w_{ij}(t) \cdot \kappa_{ij}(t)
$$

where $w_{ij}(t)$ represents time-varying edge weights (e.g., functional connectivity strength).

### Discrete Ricci Flow Evolution

Brain network geometric evolution follows the discrete Ricci flow equation:

$$
\frac{\partial g_{ij}}{\partial t} = -2\kappa_{ij}(t) + \eta_{ij}(t)
$$

where:
- $g_{ij}(t)$: Time-varying metric tensor  
- $\eta_{ij}(t)$: External driving term (e.g., sensory input, cognitive load)  

### RFI Criterion Function

Define the Ricci curvature critical flow criterion:

$$
C_{\text{RFI}} = \begin{cases}
1 & \text{if } \kappa_{\min} \leq \bar{\kappa}(t) \leq \kappa_{\max} \text{ for all } t \in [T-\tau, T] \\
0 & \text{otherwise}
\end{cases}
$$

where:
- $\kappa_{\min}, \kappa_{\max}$: Critical window boundaries  
- $\tau$: Observation time window  

### Standardized Coordinates

Standardize the RFI state as the second dimension in the six-key framework:

$$
\zeta_2 = \frac{\bar{\kappa} - \kappa^\ast}{\varepsilon_2}
$$

where:
- $\kappa^\ast = \frac{\kappa_{\min} + \kappa_{\max}}{2}$: Critical window center  
- $\varepsilon_2 = \frac{\kappa_{\max} - \kappa_{\min}}{2}$: Standardization scale parameter  

---
## 🔬 Implementation Details and Computational Workflow

### Algorithm Steps (continued on next page)

```python
def compute_RFI_criterion(connectivity_matrix, kappa_min=-0.1, kappa_max=0.1, tau=100):
    """
    Compute Ricci curvature critical flow criterion
    
    Parameters:
    -----------
    connectivity_matrix : array
        Functional connectivity matrix time series (time, nodes, nodes)
    kappa_min, kappa_max : float
        Critical window boundaries
    tau : int
        Observation time window length
    
    Returns:
    --------
    C_RFI : int
        RFI criterion (0 or 1)
    zeta2 : float
        Standardized coordinate
    """
    import networkx as nx
    from GraphRicciCurvature.OllivierRicci import OllivierRicci
    
    kappa_series = []
    
    for t in range(connectivity_matrix.shape[0]):
        # Construct network graph
        G = nx.from_numpy_array(connectivity_matrix[t])
        
        # Compute Ollivier-Ricci curvature
        orc = OllivierRicci(G, alpha=0.5, verbose="ERROR")
        orc.compute_ricci_curvature()
        
        # Calculate average curvature
        kappa_values = [orc.G[u][v]['ricciCurvature'] for u, v in orc.G.edges()]
        kappa_mean = np.mean(kappa_values)
        kappa_series.append(kappa_mean)
    
    kappa_series = np.array(kappa_series)
    
    # Check recent tau time points
    recent_kappa = kappa_series[-tau:]
    
    # Determine if within critical window
    in_range = np.all((recent_kappa >= kappa_min) & (recent_kappa <= kappa_max))
    
    C_RFI = 1 if in_range else 0
    
    # Calculate standardized coordinate
    kappa_ast = (kappa_min + kappa_max) / 2
    epsilon2 = (kappa_max - kappa_min) / 2
    zeta2 = (np.mean(recent_kappa) - kappa_ast) / epsilon2
    
    return C_RFI, zeta2
```

### Parameter Setting Guidelines
| Parameter        | Recommended Range | Physical Meaning                    |
|------------------|-------------------|-------------------------------------|
| $\kappa_{\min}$  | -0.15             | Negative curvature lower bound, avoid excessive divergence |
| $\kappa_{\max}$  | +0.15             | Positive curvature upper bound, avoid excessive convergence |
| $\tau$           | 50–200 ms         | Corresponds to neural oscillation cycles |
| $\alpha$         | 0.3–0.7           | Ollivier parameter, controls locality |

---
## 📊 Coupling with CTM Pipeline

### Weighted Distance Contribution

In the CTM framework, RFI contributes to the overall pipeline distance through standardized coordinate $\zeta_2$:

$$
D_w^2 = w_1\,\zeta_1^{2} + w_2\,\zeta_2^{2} + \sum_{i=3}^{6} w_i\,\zeta_i^{2}
$$

### Geometric-Dynamical Coupling

Coupling relationship between RFI and FELC:

$$
\frac{d\bar{\kappa}}{dt} = -\gamma \cdot |\zeta_1|^2 + \beta \cdot \nabla^2 \bar{\kappa}
$$

where:
- $\gamma$: FELC–RFI coupling strength  
- $\beta$: Spatial diffusion coefficient  

Once $C_{\text{RFI}} = 0$, $|\zeta_2| \gg 1$ elevates $D_w$, often showing causal sequence with FELC collapse events.

---

## 📝 Summary

This section embeds Ricci curvature into the critical flow perspective, providing RFI criterion $C_{\text{RFI}}$ and dimensionless $\zeta_2$, offering the second (geometric layer) pillar for CTM weighted distance.  
The second half will demonstrate reanalysis of Bruno et al. MEG dataset, showing temporal evolution of $\bar{\kappa}$ during wakefulness and propofol anesthesia.

**Key Achievements:**
- ✅ Established dynamic criterion for brain network geometry  
- ✅ Integrated Ricci flow theory with consciousness research  
- ✅ Provided computable critical window indicators  
- ✅ Formed dynamical-geometric coupling with FELC  

---

**Next Chapter Preview:** 04-2 RFI: Ricci Curvature Critical Flow (Part 2) will demonstrate experimental validation and clinical application cases.