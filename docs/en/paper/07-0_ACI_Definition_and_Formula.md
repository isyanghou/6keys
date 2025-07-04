---
title: "07-0_ACI-mermaid"
date: 2025-06-22
language: en-US
encoding: UTF-8
---
### Figure 7‑0 🔑 ACI – Neuron–Astrocyte Dual-Loop Coupling (ζ₆)

![ACI.svg](../../assets/diagrams/ACI.svg){180}
###### Figure 07-0.1 ACI – Neuron–Astrocyte Dual-Loop Coupling (ζ₆)
#### Causal Mapping
Coupling efficiency $g_{\text{eff}}(t)$ ranges between 0 (decoupled) and 1 (fully coupled). When $g_{\text{eff}} \ge g_c = 0.65$ and maintained for $\tau_c \approx 150\,\mathrm{ms}$, **$C_{\text{ACI}} = 1$**.
Definition:
$$
\zeta_6 = \frac{g_{\text{eff}} - g_c}{\varepsilon_6}
$$
**Experimental Correspondence**: Zhang (2025) shows that laryngeal stimulation can enhance calcium wave frequency (astro‑wave), leading to $g_{\text{eff}} \uparrow 0.78 \pm 0.05$, corresponding to **$\zeta_6 \approx 0.2$**; subsequently observed prefrontal FELC amplitude increase of 14% (delay ~80 ms), consistent with six-key sequence predictions.
Mapping weight $w_6 = 0.06$ serves as the terminal fine-tuning component of $D_w^2$:
$$
D_{w}^{2} = \sum_{i=1}^{6} w_i\,\zeta_{i}^{2}, \qquad \sum_{i=1}^{6} w_i = 1
$$
##### Key Formula
$$
C_{\text{ACI}} =
\begin{cases}
1, & \text{if } g_{\text{eff}}(t) \ge g_c \text{ for } \tau_c \\
0, & \text{otherwise}
\end{cases}
$$
---