---
title: "A_Mathematical Derivations Detailed"
date: 2025-06-22
language: en-US
encoding: UTF-8
---
# Appendix A　Mathematical Derivations Detailed

This appendix supplements the key formula sources and complete derivations that were only briefly outlined in each chapter, with annotations corresponding to equation numbers in the main text. To maintain readability, this appendix is arranged in a three-part format of "Background→Derivation→Notes", with corresponding `Python/Julia/MATLAB` reference implementation paths provided at the end of each section.

## A.1 Center Manifold Expansion of Critical Tubule Manifold (CTM)

### Background

Main text equation (2.3) defines the six-dimensional Jacobian $J_{\text{CTM}}(\Psi)$ satisfying $\lambda_{\parallel}\approx0, \lambda_{\perp}<0$. Here we prove that for a general smooth vector field $\dot{x}=f(x)$ with such spectral splitting, there must exist a *neutrally stable channel* $\Sigma_{\text{CT}}$ near $x$ whose projection $\pi(\Sigma_{\text{CT}})$ is a six-dimensional tubule.

### Derivation

Consider the block system:

$$
\dot{u} = A u + g(u,v), \qquad
\dot{v} = B v + h(u,v)
\tag{A.1}
$$

where $A\in\mathbb{R}^{m\times m}$ has $\max\operatorname{Re}\lambda(A)=0$, and $B\in\mathbb{R}^{n\times n}$ has $\max\operatorname{Re}\lambda(B)<-\kappa<0$.

According to the **Center Manifold Theorem** (Carr 1981, Thm 1.1), there exists a smooth mapping $v=W(u)$ such that $\mathcal{M}_{c}=\{(u,W(u))\}$ is a locally invariant manifold. Taking $\lVert u\rVert \le r_0$ and adding a contractive Lyapunov function $V(v)=v^{\top}Bv$ in the $v$-direction, we can prove:

$$
\Sigma_{\text{CT}}
=\left\{(u,v)\,\middle|\;
v=W(u)+\epsilon,\;
\lVert\epsilon\rVert\le
\frac{\kappa}{\lVert B\rVert}\,r_0
\right\}
\tag{A.2}
$$

is a *neutrally stable channel*. Defining $u$ as the six-key vector $\Psi$ yields main text equation (2.4).

### Notes and Code

- **Code**: `models/ctm_center_manifold.ipynb` demonstrates using `sympy.mpmath` to find third-order approximation of $W(u)$.
- **Extension**: If $A$ contains weak positive real part $\varepsilon$, the channel will exhibit $O(e^{\varepsilon t})$ slow drift, explaining long-term sleep period critical window variations.

## A.2 Bayesian Hierarchical Weight Derivation for $D_w$

### Background

Main text equation (2.6) gives $D_w^2=\sum w_i\zeta_i^2$, claiming that $w_i$ is automatically learned by **hierarchical Gaussian process**.

### Derivation

Let training data $\mathcal{D}=\{\zeta^{(k)},y^{(k)}\}_{k=1}^N$, where $y^{(k)}=1$ represents awake state. Maximize logistic regression likelihood conditioned on awake labels:

$$
p(y\!=\!1|\zeta,w)
=\sigma\!\bigl(-D_w^2\bigr),\quad
\sigma(z)=\tfrac1{1+e^{-z}}
\tag{A.3}
$$

Give Gaussian process prior $w\sim\mathcal{GP}(m,K)$ for $w$. **Variational Evidence Lower Bound (ELBO)** $\mathcal{L}(q)$ using $q(w)=\mathcal{N}(\mu,\Sigma)$ yields closed form:

$$
\mu = \Sigma\,
\sum_{k}2\,\zeta^{(k)}
\bigl(y^{(k)}-\sigma(-\zeta^{(k)\!\top}\!\mu)\bigr)
\tag{A.4}
$$

$$
\Sigma^{-1}
=K^{-1}
+2\sum_{k}
\sigma\!\bigl(-\zeta^{(k)\!\top}\!\mu\bigr)
\bigl(1-\sigma(\cdot)\bigr)
\zeta^{(k)}\zeta^{(k)\!\top}
\tag{A.5}
$$

Taking $\hat{w}=\mu$ gives MAP weights, substituting back into main text equation (2.6).

### Notes

Notebook `stats/learn_w_gp.ipynb` implements the above equations and demonstrates EM 3-step iteration convergence $\lVert w^{(t+1)}-w^{(t)}\rVert<10^{-4}$.

## A.3 Discrete Ricci Curvature and Ricci Flow

### Quick Proof of Ollivier–Ricci Curvature

For simple graph $G(V,E)$, endpoint distribution $m_i(j)=w_{ij}/d_i$:

$$
\kappa_{ij}=1-\frac{W_1(m_i,m_j)}{d_{ij}}
=1-\frac{\sum_k |m_i(k)-m_j(k)|}{2}
\tag{A.6}
$$

Using triangle inequality, we can prove $\kappa_{ij}>0\Rightarrow$ random walk mixing convergence acceleration. Detailed proof in `graph_ricci.pdf`.

### Discrete Ricci Flow Semi-implicit Scheme

$$
w_{ij}^{(t+\Delta)}
=
\frac{w_{ij}^{(t)}}{1+\eta\kappa_{ij}^{(t)}\Delta},
\quad
\eta=\gamma\frac{\langle w\rangle}{\langle\kappa\rangle}
\tag{A.7}
$$

This scheme guarantees $w_{ij}>0$ when $\eta\Delta<1$ and completes one update in $O(|E|)$.

## A.4 Directed Percolation and Reproduction Number

Mapping the reproduction process (main text 5.2) to $1\!+\!1$ dimensional DP, critical exponents $\tau=3/2, \alpha=1/2$. Using generating function $G(s)=\frac{1-(1-\sigma)s}{1-\sigma s}$, we can obtain avalanche size distribution $P(L)$ via Laplace inversion (detailed steps in `dp_avalanche.ipynb`):

$$
P(L)
\simeq
\frac{1}{\sqrt{2\pi L^{3}}}
\exp\!\bigl(-L(1-\sigma)^2/2\bigr)
\tag{A.8}
$$

## A.5 Vietoris–Rips Complex and Betti Flow

Proof that for phase point cloud $\mathcal{P}\subset\mathbb{T}^d$ satisfying δ-dense condition with any two points having angular distance $<\!\pi/2$, choosing $\epsilon=\pi/2$ VR complex has $\beta_1$ equal to the number of circulation loops. Proof uses Nerve theorem and Gromov–Hausdorff compactness, detailed in `tda_beta1_proof.tex`.

## A.6 Stability of Neuron–Astrocyte Coupling Dynamics

### Linear Stability Analysis

Linearizing (7.2) around $(G^\ast,A^\ast)$:

$$
J=
\begin{pmatrix}
-\alpha g_{\text{eff}}^\ast & -\alpha G^\ast \\
\beta & -\gamma
\end{pmatrix}
\tag{A.9}
$$

Determinant $\det J = \alpha\gamma g_{\text{eff}}^\ast - \alpha\beta G^\ast$. Taking $g_{\text{eff}}^\ast=\beta/(\alpha+\gamma)$ proves $\det J>0, \operatorname{tr}J<0$ → linear asymptotic stability.

If astrocyte inhibition causes $\beta\!\downarrow$, then $\det J\!\downarrow$ can turn negative → Hopf instability, corresponding to FELC limit cycle contraction.

Detailed numerical bifurcation in `aci_stability.ipynb`.

## Conclusion
The above derivations complete the steps omitted in the main text.

---
## Core Mathematical Concepts Summary

### Center Manifold Theory
- **Neutrally Stable Channel**: Geometric structure of $\Sigma_{\text{CT}}$
- **Spectral Splitting**: $\lambda_{\parallel}\approx0, \lambda_{\perp}<0$
- **Local Invariance**: Smooth mapping $v=W(u)$
- **Contractive Property**: Lyapunov function ensures stability

### Bayesian Learning Framework
- **Variational Inference**: ELBO maximization for weight solving
- **Gaussian Process Prior**: $w\sim\mathcal{GP}(m,K)$
- **MAP Estimation**: Optimal solution $\hat{w}=\mu$
- **EM Iteration**: 3-step convergent numerical algorithm

### Geometric and Topological Tools
- **Ollivier-Ricci Curvature**: Curvature definition on discrete graphs
- **Ricci Flow**: Semi-implicit scheme numerical implementation
- **Vietoris-Rips Complex**: Topological data analysis tool
- **Betti Numbers**: Quantification of circulation topology

### Dynamical Systems Analysis
- **Linear Stability**: Eigenvalue analysis of Jacobian matrix
- **Hopf Bifurcation**: Limit cycle generation mechanism
- **Percolation Theory**: Statistical physics of critical phenomena
- **Renewal Process**: Mathematical description of avalanche dynamics

### Computational Implementation Features
- **Numerical Stability**: Semi-implicit scheme ensures positivity
- **Computational Complexity**: Efficient $O(|E|)$ algorithm
- **Convergence Properties**: Fast convergence with $10^{-4}$ precision
- **Open Source Implementation**: Complete Notebook demonstrations