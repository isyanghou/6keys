---
title: "02-4_Bayesian Update × Six-Key Criticality: Convergence of Free Energy, Precision, and D_w"
date: 2025-06-22
language: en-US
encoding: UTF-8
---
# 10-2 Bayesian Update and Six-Key Criticality Dynamic Coupling  
> *Making prediction-error minimization tangible in Six-Key space.*

---
## Introduction: Why Incorporate Bayesian Brain into Six Keys?

1. **Theoretical Complementarity**  
   - Bayesian/Free Energy Principle (FEP) provides "*update norms*";  
   - Six-Key-CTM depicts "*system states*" and their critical dynamics.  
2. **Hierarchical Closed Loop**  
   - Perceptual update rate ←→ Critical amplification of σ, β₁  
   - Prior precision regulation ←→ Metabolic and glial support of g_eff, P  
3. **Experimental Integration**  
   - Measuring prediction error signal (PE) is difficult,  
   - But FEP variables can be converted to easily observable indicators through six-key projection.

---
## Mathematical Connection: Mapping Free Energy F to D_w

### Classical Formula

$$F = \operatorname{E}_{q(s)}[\ln q(s) - \ln p(o,s)] = \underbrace{D_{\mathrm{KL}}\!\big(q(s)\,\|\,p(s|o)\big)}_{\text{error}} - \ln p(o)$$

Objective: $\displaystyle \min_{q} F$.

### Six-Key Transformation Steps

1. Map hierarchical connections of hidden state $s$ to CTM neutral channel  
   $$s \xrightarrow{\;f\;} x \in \Sigma_{\mathrm{CT}}$$
2. Take six-key projection $\pi(x)=\Psi$, define "precision gap" for each key  

| Key      | Corresponding Error              | Precision Weight |
| -------- | -------------------------------- | ---------------- |
| Φ        | prediction-error entropy         | `π_Φ`            |
| P        | metabolic budget error           | `π_P`            |
| κ̄       | geometric distortion error       | `π_κ`            |
| σ        | avalanche size error             | `π_σ`            |
| β₁       | cycle persistence error          | `π_β`            |
| `g_eff`  | astro-gain error                 | `π_g`            |

3. Write free energy as weighted squared error

$$F \approx \tfrac12 \sum_{i=1}^{6} \pi_i \, \zeta_i^2 + \text{const.}$$

If we set $\pi_i = w_i / \varepsilon_i^2$, we obtain

$$F \propto D_w^2 \quad\Longrightarrow\quad
\min F \;\; \Leftrightarrow \;\; \min D_w.$$

> Conclusion: **Bayesian free energy minimum ≈ Six-key tubule center**.  
> Conversely, precision imbalance → certain $\pi_i$ abnormal → corresponding $\zeta_i$ amplified → D_w deviates from critical channel.

---
## Precision Regulation Imbalance and Hallucination Models

### A: Prior Excess (π_prior ↑)

- Physiological example: Dopamine enhancement, psychopathology  
- Observational predictions  
  - σ, β₁ increase (local criticality expansion)  
  - Φ decrease (integration degradation)  
  - Behavior: auditory hallucinations, detachment from reality

### B: Excessive Sensory Noise (π_likelihood ↓)

- Physiological example: Hallucinogens (LSD, ketamine)  
- Observational predictions  
  - κ̄ unimodal → geometric distortion  
  - g_eff increases power consumption for compensation  
  - Behavior: visual hallucinations, spatiotemporal distortion

---

### Six-Key Indicator Comparison

| Imbalance Mode | σ   | β₁  | Φ   | P   | κ̄  | g_eff |
| -------------- | --- | --- | --- | --- | --- | ----- |
| Prior Excess   | ↑   | ↑   | ↓   | ↔   | ↔   | ↔     |
| Excessive Noise| ↑   | ↔   | ↑   | ↑   | ↑   | ↑     |

---
## Simulation and Validation Workflow

### Simulation

```python
from sixkeys import CTMSim
sim = CTMSim(dt=1e-3)
sim.set_precision(pi_prior=3.0, pi_like=0.5)  # Prior excess
psi = sim.run(60)  # 60 s
Dw  = sim.compute_Dw(psi)
```

- Test π parameter sweep → Plot F–D_w coherence curves  
- Verify stable slope of $F \propto D_w^2$

### Human Brain Experiments

1. **Pharmacological**  
   - Placebo vs. low-dose LSD  
   - EEG + MEG → Six-key projection  
   - Compare predicted κ̄, P changes from π_like↓  
2. **Behavioral Intervention**  
   - Hidden audiovisual information noise  
   - Measure σ(t), β₁(t) vs. illusion report rate

---
## Integration with Core Chapters

| Core Chapter | Connection Point | New Bridging Added in This Appendix |
|--------------|------------------|--------------------------------------|
| Chapter 3 FELC | Φ–P energy–integration coupling | F = D_w² → energy efficiency curve |
| Chapter 5 ECGP | σ critical branching | Precision imbalance → gray/hallucination zone |
| Chapter 7 ACI  | g_eff metabolic precision | Astro-gain as π_prior gate |

---
## Summary

1. **Mathematical Mapping**: Free energy F, after precision reweighting, can be proportional to the square of six-key distance $D_w$.  
2. **Mechanism Correspondence**: Precision weighting (π_i) determines which key in the six-key system first shows deviation—providing parametric description of hallucinations and illusions.  
3. **Validation Feasibility**: Pharmacology + multimodal brain imaging can directly test F–D_w relationship slope and correspond to behavioral illusion rates.  
4. **Framework Gains**: Six-Key-CTM provides concrete "geometric coordinates" for Bayesian brain, while enabling free energy principle to obtain observable, controllable critical indicators.  

> Through this appendix, Bayesian updating no longer remains at the abstract level of "minimum surprise" slogans; it is anchored in the geometric system of six keys, transformed into concrete, experimentally testable mathematical and physiological variables, thereby enriching our overall understanding of consciousness dynamics.