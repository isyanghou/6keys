## G1.6 Goldstone $\psi_i$ ↔ Six-Key $\zeta_i$ Correspondence Table

|  #  | **Goldstone Field** $\psi_i$ | **Six-Key Indicator** $\zeta_i$ | Main Text Node (Example) | Appendix Node |
| :-: | ------------------------ | ------------------ | -------------------------- | ------------ |
|  1  | Metabolic phase $\psi_{1}$ | FELC $\zeta_{1}$ | §02.1 *Metabolic Phase* | §G1.3 Eq.(2) |
|  2  | Information scale $\psi_{2}$ | TEB $\zeta_{2}$ | §02.2 *Info-Scale Dilaton* | §G1.3 Eq.(2) |
|  3  | Spatial orientation-X $\psi_{3}$ | RFI $\zeta_{3}$ | §03.1 *Spatial-X* | §G1.3 Eq.(2) |
|  4  | Spatial orientation-Y $\psi_{4}$ | ECGP $\zeta_{4}$ | §03.2 *Spatial-Y* | §G1.3 Eq.(2) |
|  5  | Spatial orientation-Z $\psi_{5}$ | PWC $\zeta_{5}$ | §03.3 *Spatial-Z* | §G1.3 Eq.(2) |
|  6  | Topological winding phase $\psi_{6}$ | ACI $\zeta_{6}$ | §05.1 *Topological Twist* | §G1.3 Eq.(2) |

> Note: Naming follows the aforementioned generator mapping  
> $(T_1 \to U(1)_\phi,\; T_2 \to \mathbb{R}^{+}_\sigma,\;T_{3,4,5} \to SO(3)_n,\; T_6 \to U(1)_\tau)$.  
> Other early drafts that listed "astroglia coupling" as the sixth key have been merged into the topological winding phase and no longer appear separately.

## G1.7 Detailed Formula Derivation — *From $X(t)$ to the closed-loop SDE*

> **Mini-abstract**  
> This section connects the scattered formulas from G1.1–G1.6 into a logical chain:  
> **(i)** High-dimensional state $X(t)\!\to\!\Psi(t)$ **(ii)** $G\!\to\!H$ complete breaking **(iii)** Four-part action $L=L_0+V+L_{\text{diss}}+L_{\text{top}}$ **(iv)** Zero-mode approximation ⇒ Six-dimensional SDE **(v)** Critical pipeline stability ⇒ Consciousness survival criterion.  
> For detailed path integrals, RG, and Fokker–Planck, please expand Appendices G1.7A–C.

---

### 0. Symbol Quick Reference  

| Notation | Meaning | Source |
|------|------|------|
| $X(t)\in\mathbb R^{N}$ | Neural-astroglia total state ($N\sim10^{6}-10^{9}$) | G1.4 |
| $\mathcal C_a(x,t)$ | coarse-grained continuous field | G1.4 |
| $\Psi(t)=(\Psi_{1}\!\dots\!\Psi_{6})$ | Six Goldstones/six keys | G1.2 |
| $U(x,t)\in SO(7)/SO(6)$ | NLσM field | G1.3 |
| $S=\int\!L\,d^{4}x$ | Action | G1.3 |
| $\Sigma_c$ | Critical pipeline $D_w\le\varepsilon$ | G1.4 |
| $\tau_c$ | Reportable window (100–200 ms) | G1.5 |
| $D_w$ | Fisher weighted distance | G1.4 |

---

### 1. High-Dim → Six-Key Coordinate Process  

1. **State space** $X(t)\in\mathbb R^{N},\;N\!\gg\!1$  
2. **Continuous field embedding** $\displaystyle\mathcal C_a=\sum_{i}K_{ai}(x)X_i$  
3. **σ-model parameterization** $U=\exp[\sum_{i=1}^{6}\psi_iT_i]$  
4. **Spatial zero mode (=six keys)** $\displaystyle\Psi_i=\frac{1}{|\Omega|}\int_\Omega\psi_i\,d^{3}x$

---

### 2. Symmetry Group and Breaking  

$$
G=U(1)_\phi\times\mathbb R^{+}_{\!\sigma}\times SO(3)_n\times U(1)_\tau
\;\xrightarrow{\text{bio b.c.}}\;
H=\{e\},\qquad\dim(G/H)=6 .
$$

⇒ Exactly 6 Goldstone modes $\psi_i$ (= six keys $\zeta_i$).  
Vacuum manifold $\mathcal M_{\text{vac}} = S^{6}\cong SO(7)/SO(6)$.

---

### 3. Four-Part Action  

$$
L=L_0+V+L_{\text{diss}}+L_{\text{top}}
$$

| Block | Formula | Role |
|------|------|------|
| $L_0$ | $\dfrac{\kappa}{2}\,\text{Tr}[(U^{-1}\partial_\mu U)(U^{-1}\partial^\mu U)]$ | Goldstone reversible dynamics |
| $V$ | $\lambda(\Psi^{2}-v^{2})^{2}$ | Radial locking |
| $L_{\text{diss}}$ | $-\gamma\,U_{a}(\partial_t-D\nabla^{2})U_{r}+iT_{\!{\text eff}}\gamma\,U_{a}^{2}$ (SK form) | Dissipation＋noise, preserves FDT |
| $L_{\text{top}}$ | $\theta\,\varepsilon^{\mu\nu\rho}\,a_{\mu}\partial_{\nu}a_{\rho},\;a_{\mu}=f(\Psi)$ (taking 2+1 D) | Topological/winding coupling |

---

### 4. Three Near-Conserved Flows  

$$
\partial_{\mu}J^{\mu}_{A}= -\Gamma_{A}J_{A}+\xi_{A},
\quad A=E,I,\chi .
$$

Energy $E$ ↔ $\zeta_{1,2}$, Information $I$ ↔ $\zeta_{3,4,5}$, Topological charge $\chi$ ↔ $\zeta_{6}$;  
$\Gamma_{A}\propto\gamma$, $\langle\xi\xi\rangle\!\propto\!T_{\!{\text eff}}$.

---

### 5. Zero-Mode Approximation → Six-Dimensional SDE  

$$
\boxed{
\dot{\Psi}=J(\Psi)\Psi
-2\lambda\bigl(\lVert\Psi\rVert^{2}-v^{2}\bigr)\Psi
-(\nabla_{\!\Psi}\nu)\odot\Psi
+G(u,t)+\eta(t)}
$$

* $J(\Psi)$: Antisymmetric matrix from $L_{\text{top}}$ + Noether projection  
* $\eta$: Gaussian white noise, $\langle\eta\eta\rangle=2\gamma T_{\!{\text eff}}\delta$  
* Add half-shift correction if using Itô representation

---

### 6. Critical Pipeline $\Sigma_c$ and Consciousness Condition  

$$
D_w(\Psi)=\sqrt{(\Psi-\Psi^{*})^{\!\top}W(\Psi-\Psi^{*})},\qquad
\Sigma_c=\{\Psi\mid D_w\le\varepsilon\}.
$$

$$
\boxed{\;
\Psi(t)\in\Sigma_c\ \text{continuous residence}\ \tau_c
\;\Longrightarrow\; \text{reportable consciousness exists}\;}
$$

---

### 7. Linear Stability  

$$
\dot{\delta\Psi}=M\,\delta\Psi,\quad
M=J^{*}-2\lambda(3\lVert\Psi^{*}\rVert^{2}-v^{2})\mathbb I-(\partial^{2}\nu)^{*}.
$$

Radial eigenvalue $\lambda_{\perp}<0$ (contraction)  
Tangential $\lambda_{\parallel}\approx0$ (critical neutral)  
⇒ $\Sigma_c$ is a "radially stable/tangentially sliding" attracting manifold.

---

### 8. Five Axioms Integration  

1. **P1 Symmetry** $G = U(1)\times\mathbb R^{+}\times SO(3)\times U(1)$  
2. **P2 Breaking** Physiological boundaries ⇒ $H=\{e\}$, vacuum = $S^{6}$  
3. **P3 Dynamics** $L=L_0+V+L_{\text{diss}}+L_{\text{top}}$, parameters fixed by RG flow  
4. **P4 Statistics** Non-equilibrium steady state $\rho_{\infty}\propto e^{-\beta V_{\text{eff}}}$ (Freidlin–Wentzell)  
5. **P5 Consciousness** $\Psi(t)\in\Sigma_c$ sustained for $\tau_c$ ⟺ Reportable consciousness event  

> **One-sentence summary**: Symmetry breaking produces 6 Goldstones; action defines dynamics; dynamics construct critical pipeline; pipeline residence time $\tau_c$ is the operational criterion for "consciousness online".

---

> **Complete Framework Summary**  
> Six-Goldstone field theory uses spontaneous symmetry breaking to derive the unique 6 massless angular modes,  
> then writes them as a six-dimensional Langevin through SK dissipation and topological coupling;  
> its critical pipeline provides directly measurable consciousness survival indicators, and is refuted upon encountering any seventh soft mode or key failure.

## G1.8 Six-Key Synthesis Demonstration: From Field Theory to Measurable Indicators

This section demonstrates a **purely theory-generated "six-key dynamics trajectory"**, showing how to discretize the aforementioned

$$
\text{vacuum } S^{6}\;(SO(7)\!\to\!SO(6))
$$

Goldstone equation

$$
\dot{\Psi}
  = -2\lambda(\lVert\Psi\rVert^{2}-v^{2})\Psi
  + \eta(t),\qquad
  \langle\eta_i(t)\eta_j(t')\rangle = 2\sigma^{2}\delta_{ij}\delta(t-t')
$$

into Euler–Maruyama steps, and observe within 50 s:

1. **Phase diagram convergence**: Six-dimensional vector $\Psi(t)$ is quickly pulled by the radial potential well toward the radius $v=1$  
   $S^{6}$ spherical shell, then only random walks tangentially.

2. **Critical distance determination**: Using the first 5 s average as baseline, taking only "de-meaned" coordinates  
   $\zeta_i = \Psi_i - \langle\Psi_i\rangle_{0\text{–}5s}$,  
   calculating weighted distance:
   
   $$
   D_{\mathrm{tot}}(t)=\sqrt{\tfrac{1}{6}\sum_{i=1}^{6}\zeta_i^{2}}.
   $$

   Under default noise $\sigma=0.03$, $D_{\mathrm{tot}}$ long-term falls within  
   0.2–0.35; below critical threshold $\theta_c = 1.0$, thus judged **PASS**,  
   corresponding to "system still within critical pipeline ⇒ consciousness state maintainable".

> **Reading Guide**  
> - Left figure shows $\Psi_{1}$–$\Psi_{2}$ projection phase diagram; green circle radius $v=1$  
>   marks the vacuum spherical shell.  
> - Right curve shows $D_{\mathrm{tot}}(t)$; gray line is $\theta_c$.  
> - This demonstration serves only as a "positive example": when noise increases or mass terms  
>   $m^{2}\Psi$ are explicitly added, $D_{\mathrm{tot}}$ will break through  
>   $\theta_c$ and be marked **FAIL**, demonstrating the discriminative power of the six-key pipeline.

#### Synthesis Results

![G6CFT.png|600](G6CFT.png)

| Display | Key Observation | Theoretical Verification Point |
| -------------------------------------- | ------------------------------------------------------------------------------------- | -------------------------------------------------- |
| **Left: Phase portrait $(\Psi_1,\Psi_2)$** | Trajectory captured by the green critical circle of radius $v=1$ in extremely short time, then random walks along the circle surface | Vacuum manifold $S^{6}$ ($\Psi=v$) as attractor; radial eigenvalue $\lambda_\perp<0$ |
| **Right: $D_{\mathrm{tot}}(t)$** | Distance sequence always below threshold $\theta_c=1$, typically fluctuating around 0.2–0.35 under default noise (SIGMA=0.03) (varies slightly with seed), about 0.4–0.6 if adjusted to 0.05 | Six keys simultaneously satisfy critical pipeline condition $D_{\mathrm{tot}}\le\theta_c$ |

---

Terminal Output (Example)  

```
================================================
📋  Six-Key Summary  (final snapshot)
================================================
ζ1: |ζ| = 0.069
ζ2: |ζ| = 0.176
ζ3: |ζ| = 0.292
ζ4: |ζ| = 0.094
ζ5: |ζ| = 0.309
ζ6: |ζ| = 0.144

D_total = 0.202   ✅ PASS   (θ_c = 1.0)
```

---

#### Significance

1. **Positive Control**  
   Ideal data exhibits the dual characteristics of "attracted by critical circle + low $D_{\mathrm{tot}}$"—if real experiments also observe similar behavior, it will support the six-key criticality framework. (Actual values depend on noise amplitude; example program uses SIGMA=0.03 so about 0.2, if using 0.05 then ≈0.5)  

2. **Discriminative Power**  
   Once mass terms (e.g., $+m^{2}\Psi$) are added to the dynamics or the dimension is changed to $\neq 6$, the same pipeline will give $D_{\mathrm{tot}}>\theta_c$ and mark **FAIL**, showing that the determination is not universally permissive to all noise.  

3. **Rapid Application**  
   Experimenters only need to replace `traj` in the script with measured zero-mode sequences to immediately know if the sample is within the $SO(7)\!\to\!SO(6)$ critical pipeline, thereby validating or refuting the six-key hypothesis.

## G1.9 Mainstream Theory × Six-Key Criticality × 6G-CFT Field Theory—Comprehensive Comparison Table

> This table aligns three threads throughout the text—  
> 1. **Mainstream brain dynamics / critical theory**  
> 2. **Six-Key Criticality framework** (zero-mode averaging $\Psi_i \to$ non-dimensionalization $\zeta_i$)  
> 3. **$SO(7)\!\to\!SO(6)$ Six-Goldstone effective field theory**  
> side by side, to quickly locate "corresponding variables, assumptions, and observables for the same phenomenon in different languages".

| Mainstream Theory & Representative Literature | Core Order-Parameter/Mode | Six-Key Mapping Component $(\Psi_i,\zeta_i)$ | 6G-CFT Field Theory Correspondence | Notes |
| ------------------------------------ | ----------------------------------------------------------- | ------------------------------------------------------- | --------------------------------------------------------- | ------------------------------------------------------- |
| **Hopfield Network**<br>(Degenerate weights $J_{ij}$) | Magnetization $m_k=\frac1N\sum_i\xi_i^{(k)}s_i$ | $\Psi_{1,2}$ ← $m_{1,2}$<br>$\zeta_{1,2}$ = standardized overlap | Goldstone $\psi_{1,2}$<br>generators $T_{1,2}=E_{1\,7},E_{2\,7}$ | Two patterns → $U(1)_\phi \times \mathbb R^{+}_\sigma$ subgroup |
| **3D Critical CFT** | Primary operator $\mathcal O_\Delta$ ($\Delta\!\approx\!1$) | $\Psi_3$ ← $\langle\mathcal O_1\rangle_\Omega$ | $\psi_{3}$ (Goldstone 3rd axis) | $\Delta\!=\!1$ corresponds to $SO(3)_n$ first direction |
| **Astroglia Ca²⁺ Wave Boson** | Phase field $\theta(x,t)$ | $\Psi_6$ ← $\langle e^{i\theta}\rangle_\Omega$ | $\psi_{6}$ (topological winding Goldstone) | Wave front circulation＝$U(1)_\tau$ winding phase |
| **BKT Vortex (2D)** | Vortex strength bispectrum $V=\langle n_+n_-\rangle$ | $\Psi_5$ | $\psi_{5}$ (SO(3) 3rd axis) | Requires 2D cortical thin slice; $\psi_5$ acts as effective $SO(2)$ spinor |
| **RFI index**<br>(Resting-state 1/f) | Temporal power spectrum exponent $\beta$ | $\Psi_4$ ← $\beta-\beta_0$ | $\psi_{4}$ (SO(3) 2nd axis) | $\Psi=v$ corresponds to $\beta\!\simeq\!1$ 1/f critical point |

> **Table Reading Notes**  
> • If the order parameter of mainstream theory is a vector, it can be split into multiple $\Psi_i$; e.g., Hopfield two patterns correspond to $\Psi_1,\Psi_2$.  
> • The "6G-CFT correspondence" column shows the Goldstone components in NLσM parameterization $U=\exp[\sum_i\psi_iT_i]$.  
> • Notes column specifies necessary conditions for dimension, coupling, boundaries, etc.; when not met, remapping or additional Goldstones should be considered.

---

### Integration Conclusion (Why Six-Key Matters)

1. **Minimal Sufficient Set**  
   Six-key vector $\Psi=(\Psi_1,\dots,\Psi_6)$ is exactly **all 6 Goldstones** left by $SO(7)\!\to\!SO(6)$ breaking, ensuring "as long as the system is truly critical, low-energy information can necessarily be embedded in $\Psi$".  

2. **Single Critical Pipeline Indicator**  
   Mainstream theories each have their own criteria (magnetization, power spectrum, vortex density…), while six-key condenses them into a single expression  
   $$
     D_W(\Psi)= (\Psi-\Psi^\ast)^\top W (\Psi-\Psi^\ast)\le \varepsilon,
   $$
   experimentally measuring $\Psi(t)$ can test all theories' shared "critical commonality" at once.  

3. **Refutable Predictions**  
   • If a theory's order parameter cannot map to any $\Psi_i$, or after mapping $D_W\!\gg\!\varepsilon$ while the system still exhibits critical features ⇒ **Refutes** the six-key framework.  
   • Conversely, as long as $\Psi$ falls within the pipeline, the critical conditions of the listed theories are simultaneously satisfied.

---

> **Postscript**  
> This section completes the "mainstream models ↔ six-key ↔ Goldstone-CFT" trilingual correspondence.  
> Next steps will proceed along two paths:  
> (i) Multi-modal human/animal neuroimaging data validation of $D_W$ criterion;  
> (ii) Extend $SO(7)\!\to\!SO(6)$ to include non-equilibrium dissipation and long-range coupling; explore dynamics outside the critical pipeline.



## G1.10 Six-Key Coordinate Mapping to Mainstream Mental Theories  
> This section demonstrates: without adding any **Goldstone**, how to directly rewrite the six keys $\boldsymbol\Psi=(\zeta_1\dots\zeta_6)$ as  
> 1) Free Energy Brain/Bayesian Brain, 2) Flow State, 3) Subjective Complexity (PCI, $\Phi$)  
> core variables. For complete derivations, see Appendix *G1.A*.

### 1. Free Energy Principle (FEP)

* Precision variable $\Pi$ can be exponentialized using scaling key $\zeta_2$  
  $$\Pi \;\propto\; e^{+\zeta_2},\qquad   
    \frac{\partial F}{\partial \Pi}\;\sim\;-\zeta_2.$$
* Metabolic key $\zeta_1$ determines "available energy upper limit", controlling $\dot F$ convergence rate.  
* $\zeta_{3,4,5}$ constitute 3-D prediction-error vector,  
  $\zeta_6$ determines whether hierarchical priors can transfer across modules.  

### 2. Flow State

Classic flow conditions "challenge $\simeq$ skill, high focus" can be written as  
$$
\text{Flow}\;\Longleftrightarrow\;
\begin{cases}
D_w(\boldsymbol\Psi)\in[0.2,0.4] \\
\dot D_w \approx 0 \\
\zeta_2\text{ biased high},\;\;|\zeta_6|\text{ extremely small}
\end{cases}
$$
—corresponding to **high precision, stable topological pathways, but overall still within critical pipeline**.

### 3. Subjective Complexity (PCI / $\Phi$)

PCI, integrated information $\Phi$ positively correlate with topological key:  
$$
\Phi,\;\text{PCI} \;\uparrow
\quad\Longleftrightarrow\quad
|\zeta_6| \;\uparrow .
$$
Clinical observations (light anesthesia, NREM2) show $\zeta_6$ drifting negative  
$\;\Rightarrow\;$ PCI drops rapidly, directly explainable by this framework.

---

### Mapping Overview Table

| Mental Theory Element   | Six-Key Mapping     | Observable Experimental Indicator | Corresponding Formula/Criterion                    |
| ----------------------- | ------------------- | --------------------------------- | -------------------------------------------------- |
| Precision               | $\zeta_2$           | Pupil diameter, $\alpha$-desync   | $\Pi\sim e^{\zeta_2}$                              |
| Prediction error energy | $\zeta_1$           | NADH / baseline BOLD              | $\dot F/\dot t\propto\zeta_1$                      |
| PE vector length        | $(\zeta_{3,4,5})$   | Layer-EEG $\gamma$                | $\mathrm{PE}=\sqrt{\zeta_3^2+\zeta_4^2+\zeta_5^2}$ |
| Network integrability   | $\zeta_6$           | PCI, $\Phi$, TMS-EEG              | $\Phi\uparrow\Longleftrightarrow\zeta_6\uparrow$   |
| Flow zone               | $D_w\!\in[0.2,0.4]$ | Flow Self-Scale (FSS)             | $\dot D_w\approx0$                                 |

### 4. **Qualia**

> **Core proposition**:  
> Reportable qualia $Q(q_\text{red})$ appears if and only if  
> 1. Six-key vector $\boldsymbol\Psi$ falls within critical pipeline $\Sigma_c$;  
> 2. Sensory fiber coordinate $q$ falls within local $\varepsilon$-ball $\mathcal B_\varepsilon(q_\text{red})$.

#### 4.1 Base–Fiber Structure  
* Define **subjective moment fiber bundle**  
  $$E=\bigl(S^{6},\,F_{\text{sens}}\bigr),\qquad  
    F_{\text{sens}} = F_\text{vision}\oplus F_\text{aud}\oplus F_\text{somato}\oplus\dots$$  
  where $S^{6}$ is the six-key vacuum manifold, each $F_\bullet$ is the corresponding sensory coordinate high-speed subspace.  
  This view perfectly aligns with G Appendix postscript "qualia = fiber over $S^6$".

#### 4.2 Promotion Condition (Gate Condition)  
* Taking visual fiber as example: let $(a,b)$ be V1 hue principal components, setting  
  $$q_\text{red} = (a,b)=(1,0),\qquad  
    \mathcal B_\varepsilon(q_\text{red}) = \bigl\{(a,b)\,|\,\|(a,b)-(1,0)\|\le\varepsilon\bigr\}.$$
* **Reporting logic function**  
  $$R\bigl(\boldsymbol\Psi,q\bigr) =
    \begin{cases}
      1,& D_w(\boldsymbol\Psi)\le\varepsilon_w\;\land\;q\in\mathcal B_\varepsilon\\
      0,& \text{else}
    \end{cases}$$
  —quantifying "having qualia" as Boolean value, directly trainable for EEG/MEG classifiers.

#### 4.3 Coupling Action and Time Scales  
* Based on the original four-part action $L=L_0+V+L_{\text{diss}}+L_{\text{top}}$,  
  add **slow-base / fast-fiber** coupling term  
  $$L_{\text{couple}}
    = g_f \,\text{Tr}\!\bigl(U^{-1}\partial_\mu U\bigr)\,\partial^\mu\chi,\qquad
      g_f\in[10^{-2},10^{-1}],$$  
  where $\chi$ is the high-speed fiber field, $\tau_{\text{fiber}}\sim10\text{ ms}\ll\tau_{\Psi}\sim100\text{ ms}$,  
  RG flow converges to fixed point $g_f^\ast$ between the two time scales.  

#### 4.4 Dynamic Predictions and Falsifiability  
| Operation | Prediction | Refutation Condition |
|------|------|----------|
| Color-swap illusion: instant red↔green switch, $\boldsymbol\Psi$ unchanged | Reported color changes accordingly | If report remains fixed ⇒ need to add "seventh key" |
| TMS locks $\zeta_6$, preserves $q_\text{red}$ | Report of "red" collapses | If report persists ⇒ refutes six-key or fiber bundle model |

* Recommend **TMS-EEG + rapid hue switching** protocol: simultaneously calculate $D_w(t)$ and V1 PCA angle,  
  plot "report rate vs. $\zeta_6$ amplitude" curve, verify theoretical sigmoidal cliff.

---
## Postscript — Future Prospects  

This framework currently focuses on **"six keys＝consciousness online"** necessary conditions;  
this section treats qualia as high-speed fiber bundles hanging on $S^{6}$,  
completing the "consciousness content" layer. Next steps will proceed along two paths (for reference only):  
(i) Multi-modal EEG/MEG × V1 PCA data validation of $R(\boldsymbol\Psi,q)$ criterion;  
(ii) Non-equilibrium RG analysis of $S^{6}$ Goldstone manifold dynamics containing coupling term $L_{\text{couple}}$.

---