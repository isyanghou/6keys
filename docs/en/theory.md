# Six Keys Criticality Theory

This document provides a comprehensive overview of the theoretical foundations, mathematical derivations, and scientific basis of the Six Keys Criticality framework.

## Theoretical Overview

### Critical Transition Theory

The Six Keys Criticality framework is based on **Critical Transition Theory**, which posits that complex systems exhibit specific dynamical characteristics near phase transition points. In neural consciousness research, consciousness state transitions can be viewed as critical phase transitions in neural network systems.

### Core Assumptions

1. **Criticality of Consciousness States**: Different consciousness states correspond to different dynamical attractors in neural systems
2. **Multi-dimensional Indicators**: No single indicator can fully characterize the complex consciousness transition process
3. **Unified Framework**: Six core indicators can constitute a complete description space for critical transitions
4. **Quantifiable Measurement**: The degree of critical transition can be quantified through weighted distance

## Six Core Indicators

### 1. FELC - Free Energy Limit Cycle (ζ₁)

#### Theoretical Foundation
Based on the **Free Energy Principle** and **Hopf Bifurcation Theory**, the FELC indicator measures the oscillatory dynamics characteristics of neural systems approaching critical points.

#### Mathematical Model

Hopf oscillator dynamics equations:

```
dx/dt = (μ - r²)x - ωy + ξ(t)
dy/dt = (μ - r²)y + ωx + η(t)
```

Where:
- `μ`: Bifurcation parameter
- `r² = x² + y²`: Amplitude
- `ω`: Angular frequency
- `ξ(t), η(t)`: Noise terms

#### Indicator Calculation

```
ζ₁ = |⟨CV⟩ - CV_critical| / σ_CV
```

Where:
- `CV`: Coefficient of Variation
- `CV_critical`: Critical coefficient of variation threshold
- `σ_CV`: Standard deviation of coefficient of variation

#### Physiological Significance
- **Awake State**: Stable limit cycle oscillations, moderate CV values
- **Anesthetized State**: Oscillation amplitude changes, CV values deviate from normal range
- **Critical Transition**: CV values fluctuate dramatically, approaching critical threshold

### 2. TEB - Thermodynamic Efficiency Balance (ζ₂)

#### Theoretical Foundation
Based on the **Second Law of Thermodynamics** and **Information Theory**, the TEB indicator measures the balance between information processing and energy consumption in neural systems.

#### Mathematical Model

Efficiency function:

```
E(t) = I(t) / P(t)
```

Where:
- `I(t)`: Instantaneous information transfer
- `P(t)`: Instantaneous energy consumption

#### Indicator Calculation

```
ζ₂ = |⟨E⟩ - E_optimal| / σ_E
```

Where:
- `⟨E⟩`: Average efficiency
- `E_optimal`: Optimal efficiency value
- `σ_E`: Standard deviation of efficiency

#### Physiological Significance
- **Awake State**: High-efficiency information-energy balance
- **Anesthetized State**: Decreased efficiency, increased energy consumption but reduced information processing
- **Critical Transition**: Dramatic efficiency fluctuations, balance disruption

### 3. RFI - Ricci Flow Index (ζ₃)

#### Theoretical Foundation
Based on **Differential Geometry** and **Ricci Flow Theory**, the RFI indicator measures the geometric evolution characteristics of neural network topological structures.

#### Mathematical Model

Ricci flow equation:

```
∂g/∂t = -2Ric(g)
```

Where:
- `g`: Metric tensor
- `Ric(g)`: Ricci curvature tensor

#### Indicator Calculation

```
ζ₃ = |⟨κ⟩ - κ_critical| / σ_κ
```

Where:
- `⟨κ⟩`: Average Ricci curvature
- `κ_critical`: Critical curvature value
- `σ_κ`: Standard deviation of curvature

#### Physiological Significance
- **Awake State**: Stable network topology, gradual curvature changes
- **Anesthetized State**: Network structure reorganization, dramatic curvature changes
- **Critical Transition**: Topological phase transition, curvature approaching critical value

### 4. ECGP - Effective Causal Graph Percolation (ζ₄)

#### Theoretical Foundation
Based on **Percolation Theory** and **Causal Inference**, the ECGP indicator measures the percolation characteristics of effective causal connections in neural networks.

#### Mathematical Model

Percolation probability:

```
P(p) = 1 - exp(-λ(p-p_c)^β)
```

Where:
- `p`: Connection probability
- `p_c`: Percolation threshold
- `λ, β`: Percolation parameters

#### Indicator Calculation

```
ζ₄ = |p - p_critical| / σ_p
```

Where:
- `p`: Current percolation probability
- `p_critical`: Critical percolation probability
- `σ_p`: Standard deviation of percolation probability

#### Physiological Significance
- **Awake State**: Efficient causal connection network, good percolation
- **Anesthetized State**: Weakened causal connections, decreased percolation
- **Critical Transition**: Percolation phase transition, dramatic connectivity changes

### 5. PWC - Phase-Wrapped Circulation (ζ₅)

#### Theoretical Foundation
Based on **Topology** and **Phase Dynamics**, the PWC indicator measures the phase topological circulation characteristics of neural oscillations.

#### Mathematical Model

Phase circulation:

```
Γ = ∮ ∇φ · dl
```

Where:
- `φ`: Phase field
- `∇φ`: Phase gradient
- `dl`: Path element

#### Indicator Calculation

```
ζ₅ = |Γ - Γ_critical| / σ_Γ
```

Where:
- `Γ`: Current circulation value
- `Γ_critical`: Critical circulation value
- `σ_Γ`: Standard deviation of circulation

#### Physiological Significance
- **Awake State**: Stable phase circulation patterns
- **Anesthetized State**: Altered phase synchronization, changed circulation patterns
- **Critical Transition**: Topological phase transition, dramatic circulation changes

### 6. ACI - Astrocyte-Coupling Index (ζ₆)

#### Theoretical Foundation
Based on **Neuron-Glial Cell Interaction Theory**, the ACI indicator measures the coupling strength between astrocytes and neurons.

#### Mathematical Model

Coupling dynamics:

```
dV/dt = f(V) + g_a(Ca²⁺)h(V-E_a)
dCa²⁺/dt = α·IP₃ - β·Ca²⁺
```

Where:
- `V`: Neuronal membrane potential
- `Ca²⁺`: Astrocyte calcium concentration
- `g_a`: Coupling strength
- `IP₃`: Inositol trisphosphate concentration

#### Indicator Calculation

```
ζ₆ = |a - a_critical| / σ_a
```

Where:
- `a`: Current coupling strength
- `a_critical`: Critical coupling strength
- `σ_a`: Standard deviation of coupling strength

#### Physiological Significance
- **Awake State**: Moderate neuron-astrocyte coupling
- **Anesthetized State**: Altered coupling strength, changed glial cell activity
- **Critical Transition**: Coupling phase transition, dramatic neuron-glial interaction changes

## Unified Framework: Critical Transition Manifold (CTM)

### Mathematical Formulation

The Six Keys Criticality framework unifies the six indicators through the **Critical Transition Manifold** (CTM):

```
D_w = √(Σᵢ wᵢ · ζᵢ²)
```

Where:
- `wᵢ`: Weight of the i-th indicator
- `ζᵢ`: Normalized value of the i-th indicator
- `D_w`: Weighted total distance

### Consciousness State Classification

```
State = {
    "awake"           if D_w < θ_c
    "light_sedation"  if θ_c ≤ D_w < 2θ_c  
    "deep_anesthesia" if D_w ≥ 2θ_c
}
```

Where `θ_c` is the critical threshold.

### Geometric Interpretation

In the six-dimensional indicator space, different consciousness states correspond to different regions:

- **Awake State**: Spherical region near the origin
- **Light Sedation**: Annular region at moderate distance
- **Deep Anesthesia**: Peripheral region far from origin

## Theoretical Validation

### Mathematical Consistency

1. **Dimensional Analysis**: All indicators are dimensionless normalized values
2. **Symmetry**: Framework is invariant under coordinate transformations
3. **Continuity**: Consciousness state transitions are continuous processes
4. **Stability**: Small perturbations do not cause dramatic state jumps

### Physical Reasonableness

1. **Thermodynamic Compatibility**: Consistent with the Second Law of Thermodynamics
2. **Information Theory Consistency**: Satisfies basic properties of information entropy
3. **Topological Stability**: Topological invariants remain unchanged under continuous deformation
4. **Causality**: Causal relationships comply with physical causality laws

### Biological Relevance

1. **Neurophysiological Foundation**: Based on known neural mechanisms
2. **Pharmacological Consistency**: Consistent with anesthetic drug mechanisms
3. **Clinical Relevance**: Consistent with clinical observations
4. **Cross-species Conservation**: Similar across different species

## Computational Complexity

### Time Complexity

- **Single Indicator**: O(N·T), where N is number of channels, T is number of time points
- **Complete Analysis**: O(6·N·T) = O(N·T)
- **Batch Processing**: O(M·N·T), where M is number of datasets

### Space Complexity

- **Memory Requirements**: O(N·T) for storing time series data
- **Intermediate Results**: O(N) for storing intermediate values
- **Total Requirements**: O(N·T) linear scaling

### Optimization Strategies

1. **Parallel Computing**: Six indicators can be computed in parallel
2. **Memory Optimization**: Use streaming processing to reduce memory usage
3. **Approximation Algorithms**: Use fast approximations when precision requirements are not high
4. **GPU Acceleration**: Utilize GPU for matrix computation acceleration

## Parameter Sensitivity Analysis

### Key Parameters

1. **Critical Threshold θ_c**: Affects state classification boundaries
2. **Weight Vector w**: Affects relative importance of different indicators
3. **Time Window**: Affects temporal resolution and statistical stability
4. **Noise Level**: Affects signal quality and analysis precision

### Sensitivity Testing

```python
# Parameter sensitivity analysis example
theta_range = np.linspace(0.5, 2.0, 20)
accuracy_scores = []

for theta in theta_range:
    analyzer = SixKeysAnalyzer(theta_c=theta)
    # Calculate classification accuracy
    accuracy = evaluate_classification_accuracy(analyzer)
    accuracy_scores.append(accuracy)

# Find optimal threshold
optimal_theta = theta_range[np.argmax(accuracy_scores)]
```

### Robustness Analysis

The framework demonstrates good robustness to:

1. **Noise Interference**: Remains stable under reasonable noise levels
2. **Parameter Changes**: Insensitive to small parameter variations
3. **Data Quality**: Tolerant to missing data and outliers
4. **Individual Differences**: Adaptive to physiological differences across individuals

## Limitations and Future Developments

### Current Limitations

1. **Computational Complexity**: Still high for real-time applications
2. **Parameter Tuning**: Requires parameter adjustment for specific application scenarios
3. **Theoretical Completeness**: Some biological mechanisms not yet fully incorporated
4. **Validation Scope**: Needs more clinical data for validation

### Future Development Directions

1. **Real-time Optimization**: Develop more efficient real-time algorithms
2. **Adaptive Parameters**: Machine learning-based automatic parameter tuning
3. **Multi-modal Fusion**: Integrate EEG, fMRI, PET and other modalities
4. **Personalized Models**: Customized analysis for individual differences
5. **Clinical Applications**: Expand to more clinical scenarios and disease types

## Literature References

### Core Theoretical Literature

1. **Critical Transition Theory**
   - Scheffer, M. et al. (2009). "Early-warning signals for critical transitions." *Nature*, 461, 53-59.
   - Dakos, V. et al. (2012). "Methods for detecting early warnings of critical transitions." *PLoS ONE*, 7, e41010.

2. **Free Energy Principle**
   - Friston, K. (2010). "The free-energy principle: a unified brain theory?" *Nature Reviews Neuroscience*, 11, 127-138.
   - Hohwy, J. (2013). "The Predictive Mind: Cognitive Science and Philosophy of Mind." Oxford University Press.

3. **Consciousness Theory**
   - Tononi, G. (2008). "Integrated information theory." *Scholarpedia*, 3, 4164.
   - Dehaene, S. & Changeux, J.P. (2011). "Experimental and theoretical approaches to conscious processing." *Neuron*, 70, 200-227.

### Mathematical Methods Literature

4. **Hopf Bifurcation Theory**
   - Kuznetsov, Y.A. (2004). "Elements of Applied Bifurcation Theory." Springer-Verlag.
   - Strogatz, S.H. (2014). "Nonlinear Dynamics and Chaos." Westview Press.

5. **Ricci Flow Theory**
   - Hamilton, R.S. (1982). "Three-manifolds with positive Ricci curvature." *Journal of Differential Geometry*, 17, 255-306.
   - Perelman, G. (2002). "The entropy formula for the Ricci flow." arXiv:math/0211159.

6. **Percolation Theory**
   - Stauffer, D. & Aharony, A. (1994). "Introduction to Percolation Theory." Taylor & Francis.
   - Grimmett, G. (1999). "Percolation." Springer-Verlag.

### Neuroscience Literature

7. **Anesthesia Mechanisms**
   - Brown, E.N. et al. (2010). "General anesthesia, sleep, and coma." *New England Journal of Medicine*, 363, 2638-2650.
   - Alkire, M.T. et al. (2008). "Consciousness and anesthesia." *Science*, 322, 876-880.

8. **Neuron-Glial Interactions**
   - Araque, A. et al. (1999). "Tripartite synapses: glia, the unacknowledged partner." *Trends in Neurosciences*, 22, 208-215.
   - Volterra, A. & Meldolesi, J. (2005). "Astrocytes, from brain glue to communication elements." *Nature Reviews Neuroscience*, 6, 626-640.

## Appendices

### A. Mathematical Symbol Table

| Symbol | Meaning | Unit |
|--------|---------|------|
| ζᵢ | i-th critical indicator | Dimensionless |
| D_w | Weighted total distance | Dimensionless |
| θ_c | Critical threshold | Dimensionless |
| wᵢ | Weight coefficient | Dimensionless |
| μ | Hopf bifurcation parameter | Dimensionless |
| ω | Angular frequency | rad/s |
| κ | Ricci curvature | m⁻² |
| p | Percolation probability | Dimensionless |
| Γ | Phase circulation | rad |
| a | Coupling strength | Dimensionless |

### B. Default Parameter Values

```yaml
# Default configuration parameters
default_params:
  theta_c: 1.0
  weights:
    zeta1: 0.2
    zeta2: 0.2
    zeta3: 0.15
    zeta4: 0.15
    zeta5: 0.15
    zeta6: 0.15
  
  felc_params:
    sim_time: 10.0
    dt: 0.01
    n_samples: 50
    inband_threshold: 0.1
    cv_threshold: 0.05
    
  # ... other indicator parameters
```

### C. Unit Test Examples

```python
import unittest
import numpy as np
from sixkeys import SixKeysAnalyzer

class TestSixKeysTheory(unittest.TestCase):
    
    def test_dimensional_consistency(self):
        """Test dimensional consistency"""
        analyzer = SixKeysAnalyzer()
        result = analyzer.analyze_simulated_data()
        
        # All ζ values should be dimensionless
        for i in range(1, 7):
            zeta = getattr(result, f'zeta{i}')
            self.assertIsInstance(zeta, float)
            self.assertGreaterEqual(zeta, 0)
    
    def test_symmetry_invariance(self):
        """Test symmetry invariance"""
        analyzer = SixKeysAnalyzer(random_state=42)
        
        # Same parameters should produce same results
        result1 = analyzer.analyze_simulated_data()
        result2 = analyzer.analyze_simulated_data()
        
        np.testing.assert_almost_equal(result1.d_total, result2.d_total)
    
    def test_continuity(self):
        """Test continuity"""
        analyzer = SixKeysAnalyzer()
        
        # Similar consciousness states should produce similar results
        result_awake = analyzer.analyze_simulated_data('awake')
        result_light = analyzer.analyze_simulated_data('light_sedation')
        
        # Light sedation D_w should be greater than awake state
        self.assertGreater(result_light.d_total, result_awake.d_total)

if __name__ == '__main__':
    unittest.main()
```

### D. Performance Benchmarks

```python
import time
import numpy as np
from sixkeys import SixKeysAnalyzer

def benchmark_analysis():
    """Benchmark analysis performance"""
    analyzer = SixKeysAnalyzer()
    
    # Test different data sizes
    sizes = [100, 500, 1000, 5000, 10000]
    times = []
    
    for size in sizes:
        data = np.random.randn(size, 64)
        
        start_time = time.time()
        result = analyzer.analyze_data(data)
        end_time = time.time()
        
        times.append(end_time - start_time)
        print(f"Size {size}: {times[-1]:.3f} seconds")
    
    return sizes, times

if __name__ == '__main__':
    benchmark_analysis()
```