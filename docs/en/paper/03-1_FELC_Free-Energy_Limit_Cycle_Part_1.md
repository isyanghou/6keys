---
title: "03-1_FELC Free-Energy Limit Cycle (Part 1)"
date: 2025-06-22
language: en-US
encoding: UTF-8
---
# 03-1 FELC: Free-Energy Limit Cycle (Part 1)

## 🎯 Purpose — Theoretical Motivation and Literature

### Core Motivation

1. **From "Minimization" to "Limit Cycle"**
   - The Free Energy Principle (FEP) proposed by Friston et al. only claims that systems should minimize variational free energy $F$
   - However, living brains do not perpetually remain at static minima, but maintain *low-amplitude, periodic fluctuations*
   - Corresponding to perceptual update windows of ~80–150 ms and $\gamma$–$\beta$ interactive oscillations

2. **Neurophysiological Evidence**
   - During *wakefulness*, free energy-related amplitudes exhibit periodic lower bounds
   - *Deep anesthesia* shows monotonic decay and locks at zero
   - Dual-cortical avalanche experiments also show damped oscillations near criticality, consistent with "limit cycle" concepts

3. **Gain and Consciousness States**
   - Brainstem cholinergic and NE systems modulate neural gain $\lambda$
   - Gain reduction $\Rightarrow$ limit cycle converges to fixed point, behaviorally corresponding to loss of consciousness

4. **Research Gap**
   - Existing free energy literature mostly focuses on averages or trends
   - Lacks quantitative indicators of *temporal morphology* and *critical amplitude*
   - Therefore, we propose "Free-Energy Limit Cycle (FELC)" as the **dynamic criterion** for the first key $\Phi$ among the six keys
   - Standardizing it as $\zeta_1=\frac{\Phi-\Phi^\ast}{\varepsilon_1}$ and further incorporating it into CTM's weighted distance $D_w$

---
### 🔑 Core Hypothesis

> **Only when free energy trajectories fall within a stable limit cycle with radius $r_0$ and amplitude $\Delta r$ constraints ($C_{\text{FELC}}=1$), can the system potentially enter the CTM tube $\pi(\Sigma_{\mathrm{CT}})$ and maintain $D_w \leq \theta_c$.**

---
## 📐 Mathematical Formulation and Core Equations

### Limit Cycle Dynamics

Consider a two-dimensional phase space free energy dynamical system:

$$\begin{cases}
\dot{F} = \lambda F - \alpha F^3 + \beta G \\
\dot{G} = -\omega F + \gamma G - \delta G^3
\end{cases}$$

Where:
- $F$: Variational free energy
- $G$: Auxiliary dynamical variable (corresponding to prediction error gradient)
- $\lambda$: Linear gain parameter
- $\alpha, \delta$: Nonlinear damping coefficients
- $\beta, \gamma$: Coupling strength
- $\omega$: Characteristic frequency

### FELC Criterion Function

Define limit cycle stability criterion:

$$
C_{\text{FELC}} = \begin{cases}
1 & \text{if } r_0 - \Delta r \leq |\mathbf{x}(t)| \leq r_0 + \Delta r \text{ for all } t \in [T-\tau, T] \\
0 & \text{otherwise}
\end{cases}
$$
Where:
- $\mathbf{x}(t) = (F(t), G(t))^T$: System state vector  
- $r_0$: Standard limit cycle radius  
- $\Delta r$: Allowable amplitude deviation  
- $\tau$: Observation time window  

### Standardized Coordinates

Standardize FELC state as the first dimension in the six-key framework:

$$
\zeta_1 = \frac{\Phi - \Phi^\ast}{\varepsilon_1}
$$

Where:
- $\Phi = \langle |\mathbf{x}(t)| \rangle_\tau$: Average trajectory radius within time window  
- $\Phi^\ast = r_0$: Ideal limit cycle radius  
- $\varepsilon_1$: Standardization scale parameter  
### Critical Passage Criterion

$$
C_{\text{FELC}} = \begin{cases}
1 & \text{if } r_0 - \Delta r \leq |\mathbf{x}(t)| \leq r_0 + \Delta r \text{ for all } t \in [T-\tau, T] \\
0 & \text{otherwise}
\end{cases}
$$
---
## 🔬 Implementation Details and Computational Workflow

### Parameter Setting Guidelines:

| Parameter    | Suggested Range | Physical Meaning                        |
|--------------|----------------|-----------------------------------------|
| $r_0$        | 0.5–2.0        | Standard trajectory radius for healthy consciousness |
| $\Delta r$   | 0.1–0.5        | Allowable physiological variation range |
| $\tau$       | 50–200 ms      | Corresponding to neural oscillation periods |
| $\lambda$    | 0.1–1.0        | Neural gain, related to arousal level   |
| $\omega$     | 10–100 Hz      | Characteristic frequency, corresponding to $\gamma$ band |
### Algorithm Steps: (continued on next page)

```python
def compute_FELC_criterion(F_trajectory, G_trajectory, r0, delta_r, tau):
    """
    Compute Free-Energy Limit Cycle criterion
    
    Parameters:
    -----------
    F_trajectory : array
        Free energy time series
    G_trajectory : array  
        Auxiliary variable time series
    r0 : float
        Standard limit cycle radius
    delta_r : float
        Allowable amplitude deviation
    tau : int
        Observation time window length
    
    Returns:
    --------
    C_FELC : int
        Limit cycle criterion (0 or 1)
    zeta1 : float
        Standardized coordinate
    """
    # Calculate trajectory radius
    radius = np.sqrt(F_trajectory**2 + G_trajectory**2)
    
    # Check recent tau time points
    recent_radius = radius[-tau:]
    
    # Determine if within limit cycle range
    in_range = np.all((recent_radius >= r0 - delta_r) & 
                     (recent_radius <= r0 + delta_r))
    
    C_FELC = 1 if in_range else 0
    
    # Calculate standardized coordinate
    phi = np.mean(recent_radius)
    zeta1 = (phi - r0) / delta_r  # Use delta_r as standardization scale
    
    return C_FELC, zeta1
```