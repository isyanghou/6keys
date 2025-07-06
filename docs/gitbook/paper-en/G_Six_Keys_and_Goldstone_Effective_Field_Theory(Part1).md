## G1.1 Theoretical Positioning — Six-Key Criticality ⇄ Six-Goldstone Field Theory

> "Six-Key Criticality" gives us a real-time dashboard with **6 knobs + one distance $D_w$**;  
> "Six-Goldstone Field Theory" answers: why exactly 6 keys are needed, and what their "factory calibration" values are.  
> Combined, they can both measure and be falsified, advancing engineering-level indicators to rigorous first-principles theory.

### ✦ One-minute pitch (continued on next page)

![[6K&6S-CFT.svg|450]]

---
<!-- manual page break -->
<div class="pagebreak"></div>

### Framework Comparison

| Aspect | **Six-Key Criticality** | **Six-Goldstone FT** |
| --------- | --------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Objective** | Quantify consciousness critical pipeline with 6 indicators $\zeta_{1\text{–}6}$; directly interfaces with EEG / MEG / fMRI / two-photon data | Find fundamental conservation laws and symmetries that force "exactly 6 indicators" to emerge; formulated as a single action $S$ |
| **Mathematical Core** | Critical pipeline manifold $\Sigma_{\mathrm{CT}}$ + weighted distance $D_w=\sqrt{\sum_i w_i\zeta_i^2}$ | Spontaneous symmetry breaking  $$G=U(1)_{\phi}\times\mathbb R^{+}_{\!\sigma}\times SO(3)_{n}\times U(1)_{\tau}\;$$<br>$$\longrightarrow\;H=\{1\},\;\dim(G/H)=6$$  vacuum manifold $$\mathcal M_{\text{vac}} = G/H \simeq S^{6}$$ |
| **Validation Method** | Observe if $\zeta_i$ simultaneously fall within critical window; closed-loop experiments to individually pull out certain $\zeta_i$ to test if consciousness collapses | Measure critical exponents, Goldstone dissipation spectrum, near-conserved flows $(E, I, \chi)$; design "falsifiable tests" to refute one by one |
| **Implementation Maturity** | Python SDK, Demo, Docker available; ready for clinical/BCI deployment | Currently at proposal 0.x; requires numerical simulation of $\sigma$-model (O(7)/O(6) ≅ S⁶) and in-vivo validation |

---

### Why exactly "6 keys" are necessary?

* Ignoring additional Gauge projections, biological boundary conditions **completely break** the global symmetry group, resulting in a vacuum manifold of $S^{6}$; its dimension is exactly 6 ⇒ **6 Goldstone modes** necessarily remain, corresponding precisely to $\zeta_{1\text{–}6}$.  
* Any other modes have mass $m > m_0$ and lifetime $<10$ ms, already averaged out in coarse-graining; only the six keys survive within the 100 ms "reportable window".

---

### Roadmap for Dual-Layer Collaboration (Overview)

1. **Short-term**: Use the RG fixed points from Six-Goldstone field theory to recalculate six-key weights $w_i$, and cross-validate with public data.  
2. **Mid-term**: Complete numerical simulation of NLσM on O(7)/O(6) ≅ S⁶, confirming only 6 massless spectral lines remain.  
3. **Long-term**: Closed-loop animal experiments—single-parameter pulling of certain $\zeta_i$ out of the pipeline, observing if behavioral breakpoints occur as predicted by theory.

---

> **One-sentence summary**: Six-Key Criticality = operational **frontend**, Six-Goldstone FT = first-principles **backend**; the former measures, the latter explains, both indispensable.

## G1.2 G → H Spontaneous Symmetry Breaking and vacuum $\boldsymbol{S^{6}}$

> **Core proposition**  
> The effective global symmetry group of the brain-astroglia network  
> 
 $$
 G = U(1)_{\phi}\;\times\;\mathbb R^{+}_{\!\sigma}\;\times\;SO(3)_{n}\;\times\;U(1)_{\tau}
 $$
> 
> is **completely broken** to the trivial group $H = \{1\}$ under biological boundary conditions.  
> This leaves $\dim(G/H)=6$ low-energy degrees of freedom, precisely constituting the six keys $\zeta_{1\text{–}6}$; their critical dynamics will be described by Goldstone–6–CFT.

---
### Geometry of the Vacuum Manifold: $\mathbb R^{7}\ \to\ S^{6}$

| Step | Geometry/Equation                                                           | Physical Interpretation                                                                                       |
| ---- | --------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| 1    | **Embedding** $\Phi(x)\in\mathbb R^{7}$                                     | Introduce a 7-dimensional real vector field, with one radial + six angular components                         |
| 2    | **Potential well locking** $V(\Phi)=\lambda\left(\Phi^{2}-v^{2}\right)^{2}$ | Give the radial mode $\rho=\lvert\Phi\rvert$ a mass $m_{\rho}^{2}=4\lambda v^{2}$, making it a heavy particle |
| 3    | **Unit vector constraint** $\;U(x)=\Phi(x)/v\in S^{6}\cong SO(7)/SO(6)$     | Freeze the radial component at $\rho=v$, leaving 6 angular Goldstones—target space is the vacuum manifold     |


> **Note** If step 2 is omitted, the radial component would also have zero eigenvalue, incorrectly counting **7** Goldstones; potential well locking ensures only 6 massless angular modes remain, and makes RG flow easier to converge.

---
![[對稱群破缺.svg]]
###### Figure 1.2 Spontaneous Symmetry Breaking and 6 Goldstone Modes

---
### Generators $T_i$ and Six-Key Mapping

| $T_i$ | Group Component | Biological Meaning | Indicator $\zeta_i$ |
|---------|--------|----------|----------------|
| $T_1$ | $U(1)_{\phi}$ | Metabolic phase | $\zeta_1$ |
| $T_2$ | $\mathbb R^{+}_{\!\sigma}$ | Information scale (dilaton-like) | $\zeta_2$ |
| $T_{3,4,5}$ | $SO(3)_{n}$ | Spatial orientation x / y / z | $\zeta_{3,4,5}$ |
| $T_6$ | $U(1)_{\tau}$ | Topological winding phase | $\zeta_6$ |

> The six generators can be represented on the antisymmetric basis $T_{i7}-T_{7i}$ of $SO(7)$; they do not commute with each other, but exhibit approximately isotropic rigidity in the low-energy effective gauge.

---

### Why do biological boundary conditions force $H=\{1\}$?

* **Metabolic locking**: Energy supply chain selects a specific $\phi$ phase ⇒ $U(1)_{\phi}$ explicitly broken  
* **Sensory orientation**: External input breaks three-axis isotropy ⇒ $SO(3)_{n}$ orientation selection  
* **Information dilution**: Slow-varying astroglia coupling fixes $\mathbb R^{+}_{\!\sigma}$ scale  
* **Network topology**: Connection graph constraints remove $U(1)_{\tau}$ freedom  

Thus, the vacuum has only a single point, $\;H=\{e\}\;\Rightarrow\;\dim(G/H)=6$.

---

### From Goldstone $\psi_i$ to macroscopic six keys $\zeta_i$

$$
\Psi_i(t)=\frac{1}{|\Omega|}\int_{\Omega}\psi_i(x,t)\,d^{3}x
$$

The spatial average of zero modes becomes the measurable indicators $\zeta_i$. If any $\psi_i$ gets "massive" → trajectory leaves the critical pipeline $\Sigma_{c}$, immediately verifiable at the behavioral level.

---

### Experimental Implications Overview

* Two pseudo-Goldstones ($\zeta_{1,2}$), though carrying soft masses, remain approximately critical within the 100 ms reporting window—this is precisely why the "anesthesia ladder" can sensitively hook onto energy/scale flows.  
* Any detection of a "seventh soft mode" or proof that deleting any $\zeta_i$ does not collapse consciousness ⇒ This field theory is refuted.

---

## G1.3 Action $L$ and Three (Near) Conserved Flows

> **Purpose**: To write down a **minimal** field theory framework that can both generate the "six keys" and account for non-equilibrium properties and topological coupling.  
> Complete treatment requires Schwinger–Keldysh (SK) formalism; below is a single-index notation, with physical interpretations and directions for future expansion.

---

### 1. Four-part Lagrangian

$$
S=\!\int\! d^{4}x\,L,\qquad  
L = L_{0}+V+L_{\text{diss}}+L_{\text{top}} .
$$

| Block | Formula | Physical Role |
| ------------- | ---------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------- |
| **Kinetic term (NLσM)** | $L_{0}= \dfrac{\kappa}{2}\,\text{Tr}\!\bigl[(U^{-1}\partial_{\mu}U)(U^{-1}\partial^{\mu}U)\bigr],$ $\;U\in SO(7)/SO(6)\cong S^{6}$ | Reversible motion of six Goldstones |
| **Potential term (radial locking)** | $V=\lambda\bigl(\Psi^{2}-v^{2}\bigr)^{2}$ | Gives mass to radial mode, constrains vacuum to $S^{6}$ |
| **Dissipation + Noise** | $L_{\text{diss}} = -\gamma\,U_{a}\,\bigl(\partial_{t}-D\nabla^{2}\bigr)U_{r}\!+\;iT_{\!\text{eff}}\gamma\,U_{a}^{2}$ | Describes irreversibility using SK double-copy $(U_{r},U_{a})$, satisfies FDT |
| **Topological coupling** | $L_{\text{top}} = \theta\,\varepsilon^{\mu\nu\rho}\,a_{\mu}\partial_{\nu}a_{\rho},\quad a_{\mu}=f(\Psi)$<br>(taking cortical 2+1D slice) | Represents winding charge/spiral waves as 2+1D Chern–Simons |

> • For 3+1D description, Wess–Zumino–Witten or BF-type coupling can be used instead.  
> • The dissipation block already includes noise; omitting noise would break FDT, and conserved flows would not close.

---

### 2. Three "Near-Conserved" Flows

$$
\partial_{\mu}J^{\mu}_{A}= -\Gamma_{A}\,J_{A}+\xi_{A},
\qquad A = E,\;I,\;\chi .
$$

| Flow Name $A$ | Near-Conservation | Physical Interpretation | Related Keys $\zeta_i$ |
|---------|-----------|-----------|----------------------|
| $E$ | $\partial_{\mu}T^{\mu0}= -\Gamma_{E}\,T^{\mu0}+\xi_{E}$ | Energy/metabolic flow | $\zeta_{1},\;\zeta_{2}$ |
| $I$ | $\partial_{\mu}J^{\mu\nu}= -\Gamma_{I}\,J^{\mu\nu}+\xi_{I}$ | Information tensor flow | $\zeta_{3},\;\zeta_{4},\;\zeta_{5}$ |
| $\chi$ | $\partial_{\mu}K^{\mu}= -\Gamma_{\chi}\,K^{\mu}+\xi_{\chi}$ | Topological charge·circulation | $\zeta_{6}$ |

$\Gamma_{A}$ is the decay rate, determined by $\gamma, D$;  
$\xi_{A}$ is Gaussian white noise, satisfying $\langle\xi_{A}(t)\,\xi_{A}(t')\rangle = 2\,\Gamma_{A} T_{\!\text{eff}}\delta(t-t')$.

---

### 3. Important Symbol Reference (Table G-1)

| Symbol / Parameter | Physical Meaning | Related Keys | Notes |
| -------------------- | ------------- | -------------------- | -------------------------- |
| $\kappa$ | NLσM rigidity | $\zeta_{1}$ oscillation frequency | RG fixed point $\kappa^{\ast}$ |
| $\lambda$ | Radial locking strength | Radial stability | $\lambda>0$ ensures rebound |
| $v$ | Vacuum radius | Pipeline center | Determines $D_{w}$ origin |
| $\gamma$ | Dissipation coefficient | Related to noise in all $\zeta_i$ | Can be modulated by astroglia Ca²⁺ |
| $D$ | Diffusion constant | —— | Controls $\Gamma_{A}$ |
| $T_{\!\text{eff}}$ | Effective temperature | —— | Non-equilibrium noise amplitude |
| $\theta$ | CS coupling constant | $\zeta_{6}$ | Determines spiral wave chirality |
| $a_{\mu}$ | Synthetic $U(1)$ field | —— | $a_{\mu}=f(\Psi)$ ensures variational closure |

---

### Usage Guide

1. **Theory→Experiment**:  
   * Given $L$, one can derive the six-dimensional Langevin equation, calculate soft mode spectral lines, correlation length, and $\Gamma_{A}$.  
2. **Experiment→Refutation**:  
   * If a seventh massless spectral line is observed or if consciousness is preserved despite a certain $\zeta_i$ being heavily massed ⇒ This $L$ is refuted.  

> For an overview, return to the pitch diagram in G1.1; for numerical implementation, proceed directly to the Python demo in G1.8.


## G1.4 From Field Theory to Six-Key ODE — "High-Dim ➜ Low-Dim" Convergence Process  

> **Folding Goal**: To compress the $10^{9}$-scale neural-astroglia state space $X(t)$ sequentially through  
> ① Continuous field coarse-graining → ② Goldstone NLσM → ③ Spatial zero-mode projection,  
> ultimately into a **six-dimensional stochastic differential equation** for direct experimental and numerical control.
 $$
   \dot{\boldsymbol\Psi}=F(\boldsymbol\Psi)+\eta(t)
$$  
### ✦ Process Overview

![[G1.4.svg]]

---
### ① Continuous Field Coarse-Graining  $(X_i \mapsto \mathcal C_a)$

* High-dimensional vector: $X_i(t)\in\mathbb R^{N},\;N\sim10^{6{~}\text{–}~}10^{9}$  
* Coarse-graining kernel: $\displaystyle \mathcal C_a(x,t)=\sum_{i}K_{ai}(x)\,X_i(t)$  
  * Kernel function $K_{ai}(x)$ satisfies $\int\!K_{ai}=1$, support length ≈ 50 µm  
* Spatial resolution: 10 µm – 1 mm; temporal resolution: 0.1 ms  

---
### ② Continuous Field → Goldstone NLσM  $(\mathcal C_a \mapsto \psi_i)$

* Embed $\mathcal C_a(x,t)$ into target space $SO(7)/SO(6)\cong S^{6}$:  
  $$
    U(x)=\exp\!\Bigl[\sum_{i=1}^{6}\psi_i(x,t)\,T_i\Bigr],
  \qquad T_i = E_{i7}-E_{7i}.
  $$
* Spontaneous symmetry breaking: $SO(7)\!\rightarrow SO(6)$, leaving 6 angular Goldstones, mass $m_{\psi}=0$ (or sub-mHz pseudo-GB).  

---
### ③ Spatial Zero-Mode Averaging  $(\psi_i \mapsto \Psi_i)$

$$
  \Psi_i(t)=\frac{1}{|\Omega|}\int_{\Omega}\psi_i(x,t)\,d^{3}x,
\qquad
  |\Omega|\approx100\text{–}1000\;\mu\text{m}^{3},\;
  \Delta t\approx100\text{ ms}.
$$

Obtaining the six-dimensional vector $\boldsymbol\Psi(t)=(\Psi_1,\dots,\Psi_6)$.  
All $k\neq0$ modes have been integrated out, leaving only the **six-key zero modes**.

---
### ③′ Non-dimensionalization  $(\Psi_i \mapsto \zeta_i)$

To unify dimensions and stabilize numerics, define  
$$
  \zeta_i(t)=\frac{\Psi_i(t)-\mu_i}{\sigma_i},
\qquad
  \boldsymbol\zeta=(\zeta_1,\dots,\zeta_6),
$$
where $\mu_i,\sigma_i$ are long-window averages and standard deviations (or other benchmarks).

---
### ④ Six-Dimensional Stochastic Dynamics Equation

$$
  \boxed{\;
    \dot{\boldsymbol\zeta}=J(\boldsymbol\zeta)\,\boldsymbol\zeta
    -2\lambda\bigl(\lVert\boldsymbol\zeta\rVert^{2}-v^{2}\bigr)\boldsymbol\zeta
    -(\nabla_{\!\zeta}\nu)\odot\boldsymbol\zeta
    +\eta(t)\;}
$$

* $J(\boldsymbol\zeta)$: Antisymmetric matrix from topological coupling/Noether projection  
* $\nu(\boldsymbol\zeta)=\nu_0+\nu_g\,g_{\text{eff}}(\boldsymbol\zeta)$: Astroglia dissipation  
* $\odot$: Hadamard multiplication (component by component)  
* Noise: $\displaystyle \eta(t)\sim\mathcal N\!\bigl(0,\;2\nu_0 k_{\!B}T_{\text{eff}}\bigr)$; specify if using Stratonovich  

---
### Critical Pipeline Definition

$$
  D_{W}(\boldsymbol\Psi)=
  (\boldsymbol\Psi-\boldsymbol\Psi^{\!*})^{\!\top}
  W\,
  (\boldsymbol\Psi-\boldsymbol\Psi^{\!*})\le\varepsilon.
$$

Residence within $\Sigma_{c}=\{D_{W}\le\varepsilon\}$ for longer than $\tau_{c}\approx100\text{–}200$ ms  
⇔ Operational definition of "consciousness online".

---

> **Notes**  
> * If a seventh soft mode is detected in the $0.5\text{–}20$ Hz band ⇒ $\dim(G/H)\neq6$ → Theory needs revision.  
* See G1.7 for RG flow and SDE parameter mapping; see G1.5 for falsifiable experiment design.

### 🔎 Scale and Symbol Quick Reference

| Symbol | Definition/Range |
| ------------- | ---------------------------------------------------- |
| $\Omega$ | Spatial region, $\Omega\approx100\text{–}1000\;\mu\text{m}^{3}$ |
| $\psi_i(x,t)$ | Goldstone field (local, $i=1\!\dots\!6$) |
| $\Psi_i(t)$ | Volume average of $\psi_i$ over $\Omega$ (zero mode) |
| $\zeta_i(t)$ | Non-dimensionalized components of $\Psi_i$ after standardization |
| $N$ | Total number of neurons + astroglia, $10^{6}\!-\!10^{9}$ |
| Time window | $\Delta t\approx100\;\text{ms}$ |
| $m_{\psi}$ | Goldstone mass = 0 (pseudo-GB < 1 Hz) |
| $\lambda,v$ | Landau–Ginzburg coefficients |
| $J,\;\nu$ | Topological coupling matrix, viscosity function |

> Notes  
• Quartic potential derivative gives coefficient $-2\lambda$; specify if using other normalizations.  
• Hadamard multiplication $\odot$ ensures consistency across dimensions.  
• Slow-varying condition written as $|\nabla\psi|\ll1$ to match three-dimensional fields.

---
### 1. Spatial Zero Mode: $(\psi_i(x,t) \longrightarrow \Psi_i(t)$)

$$
\Psi_i(t)=\frac{1}{|\Omega|}\int_{\Omega}\psi_i(x,t)\,d^{3}x,
\qquad i=1,\dots,6.
$$

$\Omega$ is a 100–1000 µm scale cortical sub-region; $(\partial_x\psi_i$) can be neglected in the "slow-varying" window.

---
### 2. Euler–Lagrange → First-Order Stochastic Dynamical System

Variation of $(S=\int\!L\,d^{4}x$) followed by averaging over $(\Omega$) (high-mass modes $\Xi_{\alpha}$ already integrated out) yields

$$
\kappa\,\ddot{\Psi}
+\partial_{\Psi}V
+\nu(\Psi)\,\dot{\Psi}
=J_{\text{topo}}(\Psi)+\Gamma(u,t).\tag{2.1}
$$

Introducing $\dot{\Psi}\equiv\mathbf v$ converts to first-order form:

$$
\dot{\Psi}=J(\Psi)\Psi
-2\lambda\!\bigl(\lVert\Psi\rVert^{2}-v^{2}\bigr)\Psi
-(\nabla_{\Psi}\nu)\odot\Psi
+G(u,t)+\eta(t).\tag{2.2}
$$

* $J(\Psi)$: Antisymmetric matrix from topological coupling/Noether projection  
* $\eta(t)$: Gaussian white noise, $\langle\eta(t)\eta(t')\rangle=2\nu_0k_{B}T_{\text{eff}}\delta(t\!-\!t')$  
* Equation uses Stratonovich convention; add half-shift correction if using Itô  

---
### 3. Convergence to Critical Pipeline \(\Sigma_c\)

* **Weighted Distance**  
  $$
    D_{W}(\Psi)=\sqrt{(\Psi-\Psi^{*})^{\!\top}W(\Psi-\Psi^{*})}.
  $$
* **Pipeline**  
  $(\displaystyle\Sigma_c=\{\Psi\mid D_{W}\le\varepsilon\}$)  
  is an attracting manifold with radial contraction ($\lambda_{\perp}<0$) and tangential criticality ($\lambda_{\parallel}\approx0$).  
* **Consciousness Survival Criterion**  
  $(\Psi(t)\in\Sigma_c$) sustained for $(\tau_c\simeq100$) ms ⇔ Reportable consciousness is "online".

---
### 4. Final Six-Dimensional ODE (Experimental Version)

$$
\boxed{
\dot{\boldsymbol\Psi}=F(\boldsymbol\Psi)+\eta(t)},\qquad
F=J\Psi-2\lambda\bigl(\lVert\Psi\rVert^{2}-v^{2}\bigr)\Psi
-(\nabla_{\!\Psi}\nu)\odot\Psi .
\tag{4.1}
$$

* **State Vector** $\boldsymbol\Psi\equiv(\zeta_1,\dots,\zeta_6)$: The "six keys".  
* **Parameter Set** $(\kappa,\lambda,v,\nu_0,\nu_g,\theta)$ fixed by RG flow; their values can be directly queried from the G1.8 demo.  
* **External Control** $G(u,t)$: Experimental knobs such as anesthetic dose, VR bandwidth, astroglia Ca²⁺ blockade, etc.  
* **Falsifiability**: If deliberately pulling a certain $\zeta_i$ out of $\Sigma_c$ while the subject maintains reportable consciousness, then equation (4.1) fails ⇒ Theory needs revision.

---

> **Reading Guide**  
> • For complete second-order derivation and Fokker–Planck convergence, please expand Appendix G1.4A.  
> • For numerical implementation only, directly use (4.1) with parameters from Table G-1.

## G1.5 Falsifiable Experiments Overview — "Single-Flow·Dual-Key" Control Schemes

> **Design Goal**: Pull only **one near-conserved flow** $(E$), $(I$), $(\chi$) at a time, causing its corresponding **two keys** $(\zeta_i$) to leave the critical pipeline $(\Sigma_c$).  
> If reportable/behavioral consciousness can still be maintained within 2 s ⇒ Six-Goldstone theory is refuted; otherwise, it is merely "not yet falsified".

| Experiment Name | Control Parameter/Method \(u(t)\) | Coupled Flow | Affected Keys | **Theoretical Prediction** (< 100 ms) | **Falsification Condition** |
| ----------------------------------------------------- | ------------------------------------------------ | ------------ | ------------------------------- | -------------------------------------------------------------------------- | ----------------------------------------------------------- |
| **Anesthesia Coupling Ladder**<br>(Anesthesia-Step) | Fast-acting propofol TCI:<br>\(u_E: 0 \rightarrow 2.0\) µg·ml⁻¹ | $(E$) (Energy) | $\zeta_{1},\zeta_{2}$ | Radial coordinates leave pipeline first; when \(D_w>\varepsilon\), subject should lose reportable consciousness in < \($tau_c\!\approx\!100$) ms | $(\zeta_{1,2}$) departure amplitude > 30% while still correctly completing auditory or visual reporting tasks |
| **VR Bandwidth Stretch**<br>(Bandwidth-Stretch) | Dynamically change visual bit rate:<br>\(u_I: 2 \rightarrow 50\) Mbit·s⁻¹ | $(I$) (Information) | $\zeta_{3},\zeta_{4},\zeta_{5}$ | Exceeding critical bandwidth for continuous 200 ms, $(\zeta_{3,4,5}$) exit \($Sigma_c$) → triggering "scene collapse" or spatial localization failure | $(\zeta_{3,4,5}$) departure > 25% yet still precisely tracking moving targets or semantic scenes |
| **Astroglia Calcium Wave Inhibition**<br>(Astro-Ca²⁺ Clamp) | Local DREADD-hM4Di + CNO 1 µM | $(\chi$) (Topology) | $\zeta_{6}$ | Topological flow frozen ⇒ CS coupling $(\theta\!\to\!0$); $(\zeta_{6}$) drifts from pipeline and EEG transitions to slow-wave state → consciousness lost | EEG shows < 1 Hz large slow waves or $(\zeta_{6}$) departure > 20%, but subject maintains continuous reporting or motor feedback |
| **Spatial Orientation-Z Torque**<br>(Micro-Torque Z-axis)<br>*(Awaiting future technology)* | Precision magnetic field gradient or optogenetics:<br>Selectively activate Z-axis orientation neuron groups | $(I\) (Information) | $\zeta_{5}$ | Spatial orientation Z-axis artificially biased ⇒ $\zeta_{5}$ leaves critical range; theory predicts spatial cognition or balance abnormalities | $(\zeta_{5}$) departure > 25% while subject maintains normal spatial orientation and balance control |

**Common Standards**

1. Real-time reconstruction of six-key vector $(\boldsymbol\Psi(t)$), > 75 Hz sampling.  
2. Use weighted distance $(D_w$) to determine if pipeline $(\Sigma_c$) is exited.  
3. Behaviorally use double-blind "orientation/tracking" tasks, error rate > 50% defines consciousness collapse.  
4. Any single key leaving pipeline without consciousness collapse → Immediate falsification of Six-Goldstone theory; continuous passing only proves "not yet falsified".

> **Note**: $(\tau_c\approx100$) ms source is the longest incoming-decision-reporting pathway; the 2 s safety window exceeds theory by three orders of magnitude, ensuring rigorous testing.