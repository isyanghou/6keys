---
title: "08-0_TEB-mermaid"
date: 2025-06-22
language: en-US
encoding: UTF-8
---
### 08-0 🔑 TEB – Information-Power Efficiency (ζ₂ ≡ η)


![TEB.svg](../../assets/diagrams/TEB.svg){200}
###### Figure 08-0.1 TEB – Information-Power Efficiency (ζ₂ ≡ η)

> *Weight note*: `w₂` is a provisional value; final global normalization will ensure $(\sum_{i=1}^{6} w_i = 1)$.

---
#### Causal Mapping

When information-power efficiency $η_{\text{eff}}(t)$ exceeds the critical threshold $η_c = 0.35$ and maintains this level for $\tau_c \approx 200\,\mathrm{ms}$, **$C_{\text{TEB}} = 1$**. Definition:

$$
\zeta_2 = \frac{η_{\text{eff}} - η_c}{\varepsilon_2}
$$

Efficiency decline (such as during sleep or high-magnesium anesthesia) leads to $η_{\text{eff}} \approx 0.28$, corresponding to **$\zeta_2 \approx -0.2$**, which is incorporated through weighting $w_2$ into:

$$
D_{w}^{2} = \sum_{i=1}^{6} w_i\,\zeta_{i}^{2}
$$

Tschantz 2023 simulations demonstrate that active inference networks switch to "energy-saving mode" when $η_{\text{eff}}$ falls below 0.3, a state consistent with the six-key model's prediction of low consciousness–high $D_w^2$ states.

---

##### Key Formula

$$
C_{\text{TEB}} =
\begin{cases}
1, & \text{if } η_{\text{eff}}(t) \ge η_c \text{ for } \tau_c \\
0, & \text{otherwise}
\end{cases}
$$

---
###### For supporting literature related to this chapter, please refer to Appendix C-3