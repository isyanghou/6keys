---
title: "08-1_TEB Information-Energy Efficiency η(Part 1)"
date: 2025-06-22
language: en-US
encoding: UTF-8
---
# 08-1 TEB Information-Energy Efficiency $\eta$(Part 1) ⚡📊

> **The Sixth Key: Information-Energy Efficiency (TEB)** - Critical Balance of the Efficiency Layer
> 
> **Core Concept**: When efficiency $\eta(t)=\frac{\dot{I}(t)}{P(t)}$ maintains within the critical window, the brain can sustain FELC limit cycles and RFI flat geometry without overheating or energy waste

---

## Purpose — Theoretical Motivation and Literature 🎯

### 1. Feynman Limit and Brain Energy Paradox 🧠⚡

Based on Landauer's principle, the human brain could theoretically process $\sim 10^{20}$ bits/second per watt, yet measured peak values are only $10^{13}$ bits/second. Critical theory suggests that brain mechanisms must compromise between "reportable consciousness" and "metabolic safety," precisely falling within a sub-optimal efficiency window.

### 2. Experimental Evidence 📈

PET studies reveal:
- **Awake cortical power consumption**: $P(t) \approx 12$ W
- **Information flux**: $\dot{I}(t) \approx 1.5 \times 10^{13}$ bits/s
- **Deep anesthesia state**: Power consumption decreases by only 20%, but $\dot{I}$ drops 10×
- **Efficiency change**: $\eta = \dot{I}/P$ decreases to 0.15 times baseline

### 3. Research Gap 🔍

Previous free energy or energy consumption studies rarely monitor "information output/power input" as a single time variable, nor integrate it with other critical indicators ($\Phi, \kappa, \beta_1$, etc.).

This chapter proposes **TEB (Thermo-Energetic Balance)** with $\eta(t)$ as the core efficiency measure, dimensionlessly normalized as ζ₂, completing the second component of the six keys.

---

## Core Hypothesis 💡

**When efficiency $\eta(t) = \frac{\dot{I}(t)}{P(t)}$ maintains within the critical window $[\eta_{\min}, \eta_{\max}]$ (approximately 0.8–1.2 × awake baseline), the brain can sustain FELC limit cycles and RFI flat geometry without overheating or energy waste; if $\eta$ falls outside this window, energy and information flow decouple → $D_w$ rapidly increases and triggers CTM channel escape.**

---

## Formulation — Core Equations 📐

### 8.1 Information Flow Rate $\dot{I}(t)$ Estimation

$$\dot{I}(t) = \frac{1}{\Delta t} \operatorname{MI}(X_t, X_{t+\Delta t}), \quad \Delta t = 10 \text{ ms} \tag{8.1}$$

Where:
- $\operatorname{MI}$ is mutual information
- $X_t$ is the neural state in the first $k=12$ principal components

### 8.2 Instantaneous Power $P(t)$ 💪

**fMRI/PET method**:
$$P(t) = \rho C_{\text{BF}}(t) \Delta\text{CMRO}_2$$

**Neuropixels method**:
$$P(t) = \frac{1}{N} \sum_i V_{\text{Na}} q_i(t)$$

Where $q_i$ is the spike count, with units uniformly converted to watts.

### 8.3 Efficiency $\eta$ and TEB Criterion ⚖️

**Efficiency definition**:
$$\eta(t) = \frac{\dot{I}(t)}{P(t)}, \quad \eta^* = \langle\eta\rangle_{\text{awake}}$$

**TEB criterion**:
$$C_{\text{TEB}} = \begin{cases}
1, & \eta_{\min} \leq \eta(t) \leq \eta_{\max} \text{ for } \tau_C = 100 \text{ ms} \\
0, & \text{otherwise}
\end{cases} \tag{8.2}$$

**Recommended parameters**:
- $\eta_{\min} = 0.8\eta^*$
- $\eta_{\max} = 1.2\eta^*$

### 8.4 Dimensionless Normalization and Coupling to $D_w$ 🔗

$$\zeta_2(t) = \frac{\eta(t) - \eta^*}{\varepsilon_2}$$

$$D_w^2 = w_2 \zeta_2^2 + \sum_{i \neq 2} w_i \zeta_i^2 \tag{8.3}$$

Where:
- $\varepsilon_2$ is the standard deviation of $\eta$ during awake periods
- If $C_{\text{TEB}} = 0$, $|\zeta_2| \gg 1$
- Often precedes FELC collapse by 10–15 ms (energy-information decoupling precursor)
- Triggers channel escape warning

---

## Implementation Details and Computational Workflow 💻

### Python Algorithm Framework (continued on next page)

```python
# TEB efficiency calculation core
from sixkeys import TEB
import numpy as np

# Initialize TEB module
teb = TEB(
    eta_min_ratio=0.8,    # Minimum efficiency ratio
    eta_max_ratio=1.2,    # Maximum efficiency ratio
    tau_c=0.1,           # Critical duration (s)
    dt=0.01              # Time resolution (s)
)

# Compute information flow rate
info_rate = teb.compute_info_rate(neural_data, k_components=12)

# Compute instantaneous power
power = teb.compute_power(spike_data, method='neuropixels')
# Or use fMRI data
# power = teb.compute_power(fmri_data, method='cmro2')

# Compute efficiency and criterion
efficiency = info_rate / power
C_TEB = teb.is_critical(efficiency)

# Dimensionless normalization
zeta_2 = teb.normalize(efficiency)

# Update CTM channel distance
D_w = teb.update_Dw(zeta_2, other_zetas, weights)
```

### Parameter Setting Guidelines ⚙️

| Parameter               | Recommended Value | Description                     |
|-------------------------|-------------------|---------------------------------|
| $k_{\text{components}}$ | 12                | Principal component dimensions  |
| $\eta_{\min}^{\text{ratio}}$ | 0.8         | Minimum efficiency ratio        |
| $\eta_{\max}^{\text{ratio}}$ | 1.2         | Maximum efficiency ratio        |
| $\tau_c$               | 100 ms            | Critical duration               |
| $dt$                   | 10 ms             | Time resolution                 |
| $w_2$                  | 0.167             | $\zeta_2$ weight (six keys equal) |

---

## Coupling with CTM Channel 🔗

TEB, as the sixth key, couples with CTM channel distance $D_w$ through dimensionless ζ₂:

$$D_w(t) = \sqrt{\sum_{i=1}^{6} w_i \zeta_i^2(t)}$$

Where ζ₂ represents stability of the efficiency layer:
- **$C_{\text{TEB}} = 1$**: Efficiency within critical window, ζ₂ remains stable
- **$C_{\text{TEB}} = 0$**: Efficiency imbalance, ζ₂ surges, driving $D_w$ escape

### Six-Key Escape Sequence 📊

According to theoretical predictions, TEB imbalance is often the **earliest warning signal**:

**TEB → FELC → RFI → ECGP → PWC → ACI**

Energy-information decoupling precursors appear 10-15 ms before FELC collapse.

---

## Section Summary 📝

This section formally formulates information-power efficiency as a single time series $\eta(t)$, proposes TEB criterion $C_{\text{TEB}}$ and dimensionless ζ₂, completing the final gap in $D_w$ (**efficiency layer**).

### Key Achievements 🎯

- Established computational method for information flow rate $\dot{I}(t)$
- Defined multimodal estimation of instantaneous power $P(t)$
- Proposed critical criterion $C_{\text{TEB}}$ for efficiency $\eta(t)$
- Implemented dimensionless coupling with CTM channel distance $D_w$
- Established TEB's role as an early warning mechanism in the six-key system

**The second half of this chapter will demonstrate PET + MEG synchronized data reanalysis, validating the coupling between efficiency windows and critical channels.**

---