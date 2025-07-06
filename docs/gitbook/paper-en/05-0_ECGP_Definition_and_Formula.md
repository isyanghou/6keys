---
title: "05-0_ECGP-mermaid"
date: 2025-06-22
language: en-US
encoding: UTF-8
---

### Figure 5‑0 🔑 ECGP – Effective Causal Gradient Percolation (ζ₄)

![[ECGP.svg|200]]
###### Figure 05-0.1 ECGP Effective Causal Gradient Percolation ζ₄
#### Causal Mapping

When effective connectivity density $\sigma_{\mathrm{eff}}(t)$ approaches 1 and percolating clusters emerge, **$C_{\text{ECGP}} = 1$**. Define:
$$
\zeta_4 = \frac{\sigma_{\mathrm{eff}} - \sigma_c}{\varepsilon_4}, \qquad \sigma_c = 0.95
$$

If $\sigma_{\mathrm{eff}} \ge \sigma_c$ persists for $\tau_c \approx 120\,\mathrm{ms}$, then percolation cluster area $A_p \uparrow$, leading to **$\zeta_4 \uparrow$**, which is then mapped through weight $w_4 = 0.18$ into:
$$
D_{w}^{2} = w_{1}\,\zeta_{1}^{2} + w_{3}\,\zeta_{3}^{2} + w_{4}\,\zeta_{4}^{2} + \dots
$$
Animal experiments show that under anesthesia, $\sigma_{\mathrm{eff}}$ drops to $0.88 \pm 0.03$, resulting in $\zeta_4 \approx -0.3$ → **suppression of subsequent PWC phase circulation**, consistent with cross-species data from Varley 2024.
###### For supporting literature related to this chapter, please refer to Appendix C-3