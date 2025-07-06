---
title: "05-1_ECGP Effective Causal Gradient Percolation (Part 1)"
date: 2025-06-22
language: en-US
encoding: UTF-8
---
# 05-1 ECGP: Effective Causal Gradient Percolation σ→1 (Part 1)

## 🎯 Purpose — Theoretical Motivation and Literature

### Core Motivation

1. **Ignition and Reproduction Number**  
   If one spike can trigger an average of $\sigma$ subsequent spikes, then $\sigma$ is the "branching ratio" or effective reproduction number $R_e$.  
   When $\sigma < 1$ ⇒ activity extinction; $\sigma > 1$ ⇒ explosive runaway;  
   *Only* $\sigma \approx 1$ simultaneously satisfies long-range propagation and energy consumption control, consistent with GNW "global ignition".

2. **Empirical Evidence**  
   Cortical avalanches exhibit $P(L) \propto L^{-1.5}$ (Beggs & Plenz 2003; Petermann 2009).  
   Resting Neuropixels show $\hat{\sigma} \approx 0.97$–1.03 during wakefulness, dropping to 0.8–0.9 under propofol anesthesia (Priesemann 2014–2022).  
   Before consciousness loss, $\sigma(t)$ transitions from 0.99 → 0.85 with loss of reportability (Taghia 2021).

3. **Research Gap**  
   Previous studies mostly focused on static spike avalanches, without integrating time-varying effective connectivity $A_{ij}(t)$ and synchronous estimation with other keys ($\bar{\kappa}, \Phi$), also lacking construction of closed flow equations.

---

### 🔑 Core Hypothesis

> **Only when $\sigma(t)$, avalanche indicator $\tau(t)$, and macroscopic causal cluster coverage $f_{\text{GCC}}(t)$ simultaneously approach critical windows does the system enter the CTM pipeline $\pi(\Sigma_{\mathrm{CT}})$; where $\sigma$ corresponds to the fourth component of CTM, dimensionalized as $\zeta_4 = \frac{\sigma - 1}{\varepsilon_4}$, and contributes to weighted distance $D_w$.**

---

## 📐 Mathematical Formulation and Core Equations

### Branching Ratio Dynamics

Considering spike propagation processes in neural networks, define branching ratio $\sigma(t)$ as:

$$
\sigma(t) = \frac{\langle N_{\text{offspring}}(t) \rangle}{\langle N_{\text{parent}}(t) \rangle}
$$

where:
- $N_{\text{offspring}}(t)$: Number of offspring spikes at time $t$  
- $N_{\text{parent}}(t)$: Number of parent spikes at time $t$  

### Effective Connectivity Matrix

Time-varying effective connectivity strength is defined as:

$$
A_{ij}(t) = \frac{\text{TE}_{i \to j}(t)}{\sum_k \text{TE}_{k \to j}(t)}
$$

where $\text{TE}_{i \to j}(t)$ is the transfer entropy from node $i$ to node $j$.

### Causal Percolation Equation

Combining branching ratio and effective connectivity, establish causal percolation dynamics:

$$
\frac{d\sigma}{dt} = \alpha \cdot \left(\sum_{i,j} A_{ij}(t) \cdot w_{ij} - \sigma(t)\right) - \beta \cdot \sigma(t)^3
$$

where:
- $\alpha$: Linear recovery coefficient  
- $\beta$: Nonlinear damping coefficient  
- $w_{ij}$: Structural connectivity weights  

### Avalanche Indicator

Define the critical indicator of avalanche size distribution:

$$
\tau(t) = -\frac{d \log P(L,t)}{d \log L}\bigg|_{L=L_{\text{ref}}}
$$

where $P(L,t)$ is the avalanche size distribution at time $t$, and $L_{\text{ref}}$ is the reference avalanche size.

### Macroscopic Causal Cluster Coverage

Define the coverage of whole-brain causal connections:

$$
f_{\text{GCC}}(t) = \frac{|\{(i,j) : A_{ij}(t) > \theta_{\text{causal}}\}|}{N(N-1)}
$$

where:
- $\theta_{\text{causal}}$: Causal connection threshold  
- $N$: Total number of brain regions  

### ECGP Criterion Function

Define the causal percolation criterion:

$$
C_{\text{ECGP}} = \begin{cases}
1 & \text{if } |\sigma(t) - 1| \leq \delta_{\sigma} \text{ and } |\tau(t) - 1.5| \leq \delta_{\tau} \text{ and } f_{\text{GCC}}(t) \geq f_{\min} \\
0 & \text{otherwise}
\end{cases}
$$

where:
- $\delta_{\sigma}$: Branching ratio tolerance  
- $\delta_{\tau}$: Avalanche indicator tolerance  
- $f_{\min}$: Minimum causal coverage  

### Standardized Coordinates

Standardize the ECGP state as the fourth dimension in the six-key framework:

$$
\zeta_4 = \frac{\sigma - 1}{\varepsilon_4}
$$

where $\varepsilon_4$ is the standardization scale parameter.

---

## 🔬 Implementation Details and Computational Workflow

### Algorithm Steps (continued on next page)

```python
def compute_ECGP_criterion(spike_data, connectivity_matrix, 
                           delta_sigma=0.05, delta_tau=0.2, f_min=0.3):
    """
    Compute causal percolation criterion
    
    Parameters:
    -----------
    spike_data : array
        Spike time series (time, neurons)
    connectivity_matrix : array
        Structural connectivity matrix
    delta_sigma, delta_tau : float
        Critical window tolerance
    f_min : float
        Minimum causal coverage
    
    Returns:
    --------
    C_ECGP : int
        ECGP criterion (0 or 1)
    zeta4 : float
        Standardized coordinate
    """
    import numpy as np
    from scipy import stats
    
    # Compute branching ratio
    sigma_t = compute_branching_ratio(spike_data)
    
    # Compute avalanche indicator
    avalanche_sizes = detect_avalanches(spike_data)
    tau_t = compute_avalanche_exponent(avalanche_sizes)
    
    # Compute effective connectivity
    A_ij = compute_transfer_entropy_matrix(spike_data)
    
    # Compute causal coverage
    f_gcc = np.sum(A_ij > 0.1) / (A_ij.shape[0] * (A_ij.shape[1] - 1))
    
    # Determine if critical conditions are met
    sigma_crit = abs(sigma_t - 1) <= delta_sigma
    tau_crit = abs(tau_t - 1.5) <= delta_tau
    gcc_crit = f_gcc >= f_min
    
    C_ECGP = 1 if (sigma_crit and tau_crit and gcc_crit) else 0
    
    # Calculate standardized coordinate
    epsilon4 = delta_sigma  # Use tolerance as standardization scale
    zeta4 = (sigma_t - 1) / epsilon4
    
    return C_ECGP, zeta4

def compute_branching_ratio(spike_data, window_size=50):
    """Compute branching ratio within sliding window"""
    n_time, n_neurons = spike_data.shape
    sigma_series = []
    
    for t in range(window_size, n_time - window_size):
        window = spike_data[t-window_size:t+window_size]
        
        # Detect avalanche events
        avalanches = detect_avalanche_events(window)
        
        if len(avalanches) > 1:
            # Calculate average branching ratio
            branching_ratios = []
            for av in avalanches[:-1]:
                offspring = count_triggered_spikes(av, window)
                if av['size'] > 0:
                    branching_ratios.append(offspring / av['size'])
            
            sigma_t = np.mean(branching_ratios) if branching_ratios else 0
        else:
            sigma_t = 0
            
        sigma_series.append(sigma_t)
    
    return np.mean(sigma_series)
```

### Parameter Setting Guidelines
| Parameter                | Recommended Range | Physical Meaning                    |
|--------------------------|-------------------|-------------------------------------|
| $\delta_{\sigma}$        | 0.03–0.08         | Branching ratio critical window width |
| $\delta_{\tau}$          | 0.1–0.3           | Avalanche indicator tolerance       |
| $f_{\min}$               | 0.2–0.5           | Minimum causal coverage             |
| $\theta_{\text{causal}}$ | 0.05–0.15         | Causal connection significance threshold |

---
## 📊 Coupling with CTM Pipeline

### Weighted Distance Contribution

In the CTM framework, ECGP contributes to the overall pipeline distance through standardized coordinate $\zeta_4$:

$$
D_w^2 = w_4\,\zeta_4^{2} + \sum_{i \neq 4} w_i\,\zeta_i^{2}
$$

When $C_{\text{ECGP}} = 1$ is satisfied, $|\zeta_4| \leq 1$, and the total distance is updated.

### Multi-Key Coupling Dynamics

Coupling relationships between ECGP and other keys:

$$
\frac{d\sigma}{dt} = f(\zeta_1, \zeta_2, \zeta_3) + \eta_{\text{ECGP}}(t)
$$

where $f(\cdot)$ describes the influence of FELC, RFI, etc. on the branching ratio.

---

## 📝 Summary

This section formally formulates causal percolation as a coupled system of branching ratio $\sigma$ and effective connectivity flow $A_{ij}(t)$, proposing ECGP criterion $C_{\text{ECGP}}$ and dimensionless $\zeta_4$, laying the foundation for the *information propagation layer* of CTM pipeline distance $D_w$.

**Key Achievements:**
- ✅ Established dynamic criterion for causal percolation  
- ✅ Integrated branching ratio, avalanche indicators, and causal coverage  
- ✅ Provided computable critical window indicators  
- ✅ Formed multi-layer coupling system with previous keys  

---

**Next Chapter Preview:** 05-2 ECGP: Effective Causal Gradient Percolation σ→1 (Part 2) will demonstrate experimental validation and clinical application cases.