---
title: "D_Experimental Details Reference Blueprint"
date: 2025-06-22
language: en-US
encoding: UTF-8
---
# Appendix D　Experimental Details and Gantt Timeline
(For blueprint reference only)

## D.1 Overall Experimental Matrix

### Six-Key Experimental Matrix Overview (Human/Mouse)
## C.4　Model Applicability Table for Each Experimental State

| ID   | Mode                     | FELC | RFI | ECGP | PWC | TEB | ACI |
|------|--------------------------|------|-----|------|-----|-----|-----|
| H01  | Human Anesthesia (Propofol) | ✓    | ✓   | ✓    | ✓   | ✓   | —   |
| H02  | Normal Sleep (N2–N3)        | ✓    | —   | —    | ✓   | ✓   | —   |
| M01  | Mouse Propofol              | ✓    | ✓   | ✓    | ✓   | ✓   | ✓   |
| M02  | Astrocyte Optogenetic Inhibition | ✓    | —   | —    | —   | ✓   | ✓   |


### Notes

- **H01** corresponds to the dual-key synchronization experiment in Chapter 9; **H02** is used to verify PWC collapse in sleep K-complexes.
- **M01‐M02** provide ACI (astrocyte coupling) and FELC/RFI sequence validation.

## D.2 Resource Estimation and Personnel Allocation

### Main Resource and Personnel Requirements

| Category | Item                    | Quantity/Time       | Estimated Cost (USD) |
|----------|-------------------------|---------------------|----------------------|
| **Equipment** | 64-ch HD-EEG rental        | 4 weeks             | $8,000               |
|          | MEG scanning hours         | 60 h                | $12,000              |
|          | PET–MR simultaneous scanning | 25 h                | $18,000              |
| **Animal** | Neuropixels probes         | 15 units            | $6,000               |
|          | Two-photon microscopy rental | 3 weeks             | $9,000               |
| **Personnel** | RA (EEG/MEG)            | 1.0 FTE × 6 months  | $21,000              |
|          | RA (Mouse lab)          | 0.5 FTE × 6 months  | $8,400               |
| **Cloud** | GPU A100 nodes            | 3,000 GPU·h         | $4,500               |
| **Total** | —                        | —                   | **$86,900**          |

## D.3 Gantt Timeline (18 months)

### Phase 1 │ Design and IRB (2025-07 ~ 2025-10)

- **H01 protocol** (2025-07 ~ 2025-08)
- **IRB & Animal review** (2025-08 ~ 2025-10)

### Phase 2 │ Data Collection (2025-11 ~ 2026-03)

- **Human H01** (2025-11 ~ 2026-01)
- **Human H02** (2026-01 ~ 2026-02)
- **Mouse M01** (2025-12 ~ 2026-02)
- **Mouse M02** (2026-02 ~ 2026-03)

### Phase 3 │ Analysis and Cross-validation (2026-02 ~ 2026-06)

- **Six-key computation** (2026-02 ~ 2026-04)
- **CSE & $D_w$ synchronization statistics** (2026-04 ~ 2026-05)
- **Public data comparison** (2026-05 ~ 2026-06)

### Phase 4 │ Writing and Submission (2026-06 ~ 2026-12)

- **Manuscript v1.1** (2026-06 ~ 2026-08)
- **Preprint & Code freeze** (2026-08 ~ 2026-09)
- **Journal submission** (2026-09 ~ 2026-12)

### Diagram Notes

- Each Phase is grouped in bold; gray grid represents months.
- Key delivery milestones: *Preprint & Code freeze* marks GitHub tag `v1.1` and arXiv synchronization.
- If Phase delay exceeds 2 weeks, automatic Slack reminder is triggered.

## D.4 Risks and Mitigation Strategies

1. **IRB Delay**: Submit 3 months early; if approval >90 days, start mouse M01/M02 first.

2. **MEG Schedule Conflict**: Reserve alternative slots in 2026-01; if necessary, switch to HD-EEG + sEEG structure.

3. **GPU Cloud Quota Insufficient**: Sign MOU with university HPC center; set up offline batch queue.

4. **Animal Optogenetics Failure**: Simultaneously prepare chemogenetics (DREADDs) alternative.

---

## Core Elements of Experimental Design

### Cross-species Validation Strategy
- **Human Experiments**: Comparative studies of anesthesia and natural sleep
- **Mouse Experiments**: Precise manipulation through optogenetics and pharmacology
- **Cross-validation**: Cross-species consistency of six-key indicators
- **Clinical Translation**: From basic research to application potential

### Technical Integration Advantages
- **Multimodal Recording**: Simultaneous measurement of EEG/MEG/PET-MR
- **High Spatiotemporal Resolution**: Precise monitoring with Neuropixels and two-photon
- **Computational Resources**: Large-scale data processing with GPU clusters
- **Open Science**: Complete data and code sharing

### Quality Control Mechanisms
- **Standardized Procedures**: Unified data collection and processing protocols
- **Peer Review**: Multi-stage expert review mechanisms
- **Reproducibility Guarantee**: Complete experimental records and code version control
- **Ethical Compliance**: Strict IRB and animal experiment review

### Expected Outcomes and Impact
- **Theoretical Validation**: Empirical support for the six-key system
- **Methodological Innovation**: Practical implementation of Critical Tube Manifold
- **Clinical Applications**: New tools for consciousness state monitoring
- **Open Source Contribution**: Public resources for neuroscience research

---

## Conclusion

This proposal is for reference only; actual implementation requires adjustment of timeline and resource allocation based on specific conditions.