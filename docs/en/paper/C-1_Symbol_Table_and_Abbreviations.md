---
title: "C_Symbol Table and Abbreviations"
date: 2025-06-22
language: en-US
encoding: UTF-8
---
# Appendix C　Symbol Table and Abbreviations

## C.1.1　Main Symbol Overview (1)

| Symbol                      | Meaning/Definition                                         | Unit         |
| --------------------------- | ---------------------------------------------------------- | ------------ |
| $\Phi$                      | Integrated Information                                     | bit          |
| $P$                         | Power consumption per second                               | W            |
| $\bar{\kappa}$              | Ollivier–Ricci graph average curvature                    | dimensionless|
| $\sigma$                    | Effective branching ratio                                  | dimensionless|
| $\beta_{1}$                 | First Betti number, point cloud circulation count         | dimensionless|
| $g_{\text{eff}}$            | Neuron–astrocyte effective coupling rate                  | dimensionless|
| $\eta$                      | Information–energy efficiency $\dot{I}/P$                  | bit·W$^{-1}$ |
| $D_{w}$                     | Six-key weighted distance $\sqrt{\sum w_i\zeta_i^{2}}$    | dimensionless|
| $\zeta_i$                   | $i$-th key standard component $\frac{\Psi_i-\Psi_i^\ast}{\varepsilon_i}$ | dimensionless|
| $w_i$                       | Six-key weights (hierarchical Bayesian learned)           | —            |
| $\theta_c$                  | Tubule distance critical threshold ($\approx 0.5$)        | dimensionless|
| $\Sigma_{\mathrm{CT}}$      | Critical Tubule Manifold (neutrally stable channel)       | —            |
| $\pi(\Sigma_{\mathrm{CT}})$ | Six-key projected tubule                                   | —            |
| $J_{\mathrm{CTM}}$          | CTM effective Jacobian matrix                              | —            |
| $\lambda_{\parallel}$       | Tubule tangential eigenvalue                               | s$^{-1}$     |
| $\lambda_{\perp}$           | Normal contractive eigenvalue                              | s$^{-1}$     |
| $r$                         | FELC limit cycle radius                                    | (same as $F$)|
| $\omega_{0}$                | FELC fundamental frequency ($\gamma$ rhythm)               | s$^{-1}$     |
| $\kappa_{ij}$               | Edge $(i,j)$ Ricci curvature                              | —            |
| $W_1$                       | First-order Wasserstein distance                          | —            |

---
<!-- Manual page break -->
<div class="pagebreak"></div>

## C.1.2　Main Symbol Overview (2)

| Symbol                      | Meaning/Definition                                         | Unit         |
| --------------------------- | ---------------------------------------------------------- | ------------ |
| $A_{ij}$                    | Time-varying effective connectivity (Hawkes EM)           | —            |
| $f_{\text{GCC}}$            | Maximum global causal cluster size ratio                  | —            |
| $\dot{I}$                   | Instantaneous information flow rate (mutual information rate) | bit·s$^{-1}$ |
| $P(t)$                      | Instantaneous metabolic power                              | W            |
| $G(t)$                      | Average firing rate                                        | Hz           |
| $A(t)$                      | Astrocyte $\mathrm{Ca^{2+}}$ activity                     | $\Delta F/F$ |
| $C_{\text{X}}$              | X-th key binary critical criterion (X ∈ FELC…ACI)         | $\{0,1\}$    |
| $r$                         | FELC limit cycle radius                                    | (same as $F$)|
| $\omega_{0}$                | FELC fundamental frequency ($\gamma$ rhythm)               | s$^{-1}$     |
| $\kappa_{ij}$               | Edge $(i,j)$ Ricci curvature                              | —            |
| $W_1$                       | First-order Wasserstein distance                          | —            |
| $A_{ij}$                    | Time-varying effective connectivity (Hawkes EM)           | —            |
| $f_{\text{GCC}}$            | Maximum global causal cluster size ratio                  | —            |
| $\dot{I}$                   | Instantaneous information flow rate (mutual information rate) | bit·s$^{-1}$ |
| $P(t)$                      | Instantaneous metabolic power                              | W            |
| $G(t)$                      | Average firing rate                                        | Hz           |
| $A(t)$                      | Astrocyte $\mathrm{Ca^{2+}}$ activity                     | $\Delta F/F$ |
| $C_{\text{X}}$              | X-th key binary critical criterion (X ∈ FELC…ACI)         | $\{0,1\}$    |

---

<!-- Manual page break -->
<div class="pagebreak"></div>

## C.2　Common Abbreviations

### Core Theoretical Framework

| Abbr | Full Name/Description |
|------|----------------------|
| CTM | **C**ritical **T**ube **M**anifold |
| FELC | **F**ree-**E**nergy **L**imit **C**ycle |
| RFI | **R**icci-**F**low **I**ndex |
| ECGP | **E**ffective-**C**ausal **G**radient **P**ercolation |
| PWC | **P**hase-**W**inding **C**irculation |
| ACI | **A**stro–**C**ortical coupling **I**ndex |
| TEB | **T**hermo-**E**nergetic **B**alance |
| CSE | **C**ritical **S**ynchrony **E**vent |

---

### Neuroimaging Techniques

| Abbr | Full Name/Description |
|------|----------------------|
| EEG | Electroencephalography |
| MEG | Magnetoencephalography |
| PET | Positron Emission Tomography |
| fMRI | Functional Magnetic Resonance Imaging |
| fMRS | Functional Magnetic Resonance Spectroscopy |
| dMRI | Diffusion MRI |
| NIRS | Near-Infrared Spectroscopy |
| BIDS | Brain Imaging Data Structure |

---

<!-- Manual page break -->
<div class="pagebreak"></div>

### Neuromodulation and Metabolic Techniques

| Abbr | Full Name/Description |
|------|----------------------|
| tACS | Transcranial Alternating Current Stimulation |
| DBS | Deep Brain Stimulation |
| tFUS | Transcranial Focused Ultrasound |
| ANLS | Astrocyte–Neuron Lactate Shuttle |
| CMRglc | Cerebral Metabolic Rate of Glucose |

---

### Computational and Statistical Methods

| Abbr | Full Name/Description |
|------|----------------------|
| GP | Gaussian Process |
| ELBO | Evidence Lower Bound |
| ROC-AUC | Receiver Operating Characteristic — Area Under Curve |
| CI/CD | Continuous Integration / Continuous Deployment |

---

## Symbol Usage Guidelines

### Mathematical Notation Conventions
- **Vectors**: Use bold or arrow notation, such as $\vec{\Psi}$ or $\mathbf{\Psi}$
- **Matrices**: Use uppercase letters, such as $J_{\mathrm{CTM}}$
- **Scalars**: Use italics, such as $D_w$
- **Sets**: Use script or uppercase, such as $\Sigma_{\mathrm{CT}}$

### Subscripts and Superscripts
- **Time dependence**: $(t)$ indicates time function
- **Critical values**: $^\ast$ indicates critical point or equilibrium state
- **Effective values**: $_{\text{eff}}$ indicates effective parameters
- **Average values**: $\bar{\cdot}$ indicates temporal or spatial average

### Unit System
- **Time**: seconds (s)
- **Frequency**: hertz (Hz)
- **Power**: watts (W)
- **Information**: bits (bit)
- **Dimensionless**: standardized ratios or indices

---

**Note**: For reference to figures/equation numbers, see annotations such as "Eq. (2.6)" in each chapter; if symbols conflict with field conventions, this table's definitions take precedence. If any omissions exist, please open an Issue on GitHub for updates.