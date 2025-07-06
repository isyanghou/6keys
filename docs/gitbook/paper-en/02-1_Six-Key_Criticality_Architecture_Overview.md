---
title: "02-1_Six-Key_Criticality_Architecture_Overview"
date: 2025-06-22
language: en-US
encoding: UTF-8
---
## 02-1 Six-Key Overall Coupling Diagram (Overview)

> **Reading Guide**  
> - Six keys (Key #1–#6) are color-coded, with all ζ indicators weighted and fed into the same **CTM tube distance Dw²**.  
> - Solid lines → indicate **numerical input** (ζᵢ → Dw²); dashed lines → indicate **sequential stages/conditional triggering**.  
> - Dual-layer structure: **outer sequence** (efficiency → energy → geometry …) + **inner convergence** (all keys → Dw²).


![[六鑰結構圖.svg]]

###### Figure 02-1.1 Six-Key Overall Coupling Diagram 1

![[六鑰流動.svg]]

###### Figure 02-1.2 Six-Key Overall Coupling Diagram 2
---
### Global Weighting Formula

$$

D_{w}^{2} \;=\; \sum_{i=1}^{6} w_i\,\zeta_i^{2}, \qquad
\begin{aligned}
&0 < w_i < 1, \,\; \; \sum_{i=1}^{6} w_i = 1\\[4pt]
&\text{Critical transition when } \Delta D_w \;{\Large\gtrsim}\; θ_1 = 0.15
\end{aligned}

$$

> **Notes**:  
> 1. Current default weights \(w_1=0.42, w_2=0.04, w_3=0.22, w_4=0.18, w_5=0.12, w_6=0.06\).  
> 2. Threshold \(θ_1\) can be recalibrated according to datasets; recommended to use grid-search for optimal ROC-AUC in cross-validation procedures.