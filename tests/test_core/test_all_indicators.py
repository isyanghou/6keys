"""Tests for all six indicators in the SixKeys framework."""

import pytest
import numpy as np
from sixkeys.core import FELC, TEB, RFI, ECGP, PWC, ACI
from sixkeys.analysis import SixKeysAnalyzer


class TestAllIndicators:
    """Test suite for all six indicators."""
    
    def test_all_indicators_initialization(self):
        """Test that all indicators can be initialized."""
        felc = FELC()
        teb = TEB()
        rfi = RFI()
        ecgp = ECGP()
        pwc = PWC()
        aci = ACI()
        
        assert felc is not None
        assert teb is not None
        assert rfi is not None
        assert ecgp is not None
        assert pwc is not None
        assert aci is not None
    
    def test_felc_analysis(self):
        """Test FELC indicator analysis."""
        felc = FELC()
        result = felc.analyze(target_energy=0.0, noise_level=0.05, sim_time=10.0)
        
        assert hasattr(result, 'zeta_1')
        assert isinstance(result.zeta_1, (int, float))
        assert hasattr(result, 'C_FELC')
        assert result.C_FELC in [0, 1]
    
    def test_teb_analysis(self):
        """Test TEB indicator analysis."""
        teb = TEB()
        result = teb.analyze(target_efficiency=0.75, noise_level=0.03, sim_time=10.0)
        
        assert hasattr(result, 'zeta_2')
        assert isinstance(result.zeta_2, (int, float))
        assert hasattr(result, 'C_TEB')
        assert result.C_TEB in [0, 1]
    
    def test_rfi_analysis(self):
        """Test RFI indicator analysis."""
        rfi = RFI()
        result = rfi.analyze(kappa_target=0.0, sim_time=10.0)
        
        assert hasattr(result, 'zeta_3')
        assert isinstance(result.zeta_3, (int, float))
        assert hasattr(result, 'C_RFI')
        assert result.C_RFI in [0, 1]
    
    def test_ecgp_analysis(self):
        """Test ECGP indicator analysis."""
        ecgp = ECGP()
        result = ecgp.analyze(p_target=0.6, sim_time=10.0)
        
        assert hasattr(result, 'zeta_4')
        assert isinstance(result.zeta_4, (int, float))
        assert hasattr(result, 'C_ECGP')
        assert result.C_ECGP in [0, 1]
    
    def test_pwc_analysis(self):
        """Test PWC indicator analysis."""
        pwc = PWC()
        result = pwc.analyze(gamma_target=0.0, sim_time=10.0)
        
        assert hasattr(result, 'zeta_5')
        assert isinstance(result.zeta_5, (int, float))
        assert hasattr(result, 'C_PWC')
        assert result.C_PWC in [0, 1]
    
    def test_aci_analysis(self):
        """Test ACI indicator analysis."""
        aci = ACI()
        result = aci.analyze(a_target=0.5, sim_time=10.0)
        
        assert hasattr(result, 'zeta_6')
        assert isinstance(result.zeta_6, (int, float))
        assert hasattr(result, 'C_ACI')
        assert result.C_ACI in [0, 1]
    
    def test_sixkeys_analyzer_all_indicators(self):
        """Test SixKeysAnalyzer with all six indicators."""
        analyzer = SixKeysAnalyzer()
        
        # Test that all indicators are enabled by default
        expected_indicators = {'FELC', 'TEB', 'RFI', 'ECGP', 'PWC', 'ACI'}
        assert analyzer.enable_indicators == expected_indicators
        
        # Test analysis with all indicators
        result = analyzer.analyze_simulated_data(
            consciousness_state='awake',
            duration=10.0
        )
        
        assert len(result.zeta_values) == 6
        assert 'FELC' in result.zeta_values
        assert 'TEB' in result.zeta_values
        assert 'RFI' in result.zeta_values
        assert 'ECGP' in result.zeta_values
        assert 'PWC' in result.zeta_values
        assert 'ACI' in result.zeta_values
        
        # Test that all zeta values are numeric
        for indicator, zeta_value in result.zeta_values.items():
            assert isinstance(zeta_value, (int, float))
        
        # Test total distance calculation
        assert isinstance(result.d_total, (int, float))
        assert result.d_total >= 0
    
    def test_different_consciousness_states(self):
        """Test analysis with different consciousness states."""
        analyzer = SixKeysAnalyzer()
        
        states = ['awake', 'light_sedation', 'deep_anesthesia']
        results = {}
        
        for state in states:
            result = analyzer.analyze_simulated_data(
                consciousness_state=state,
                duration=5.0
            )
            results[state] = result
            
            # Verify all indicators are present
            assert len(result.zeta_values) == 6
            assert result.consciousness_state in ['Conscious', 'Non-conscious']
        
        # Verify different states produce different results
        awake_zetas = list(results['awake'].zeta_values.values())
        anesthesia_zetas = list(results['deep_anesthesia'].zeta_values.values())
        
        # At least some values should be different
        assert not np.allclose(awake_zetas, anesthesia_zetas, rtol=0.1)
    
    def test_indicator_weights(self):
        """Test that indicator weights are properly applied."""
        # Test with equal weights
        analyzer1 = SixKeysAnalyzer(weights={
            'zeta1': 1.0, 'zeta2': 1.0, 'zeta3': 1.0,
            'zeta4': 1.0, 'zeta5': 1.0, 'zeta6': 1.0
        })
        
        # Test with different weights
        analyzer2 = SixKeysAnalyzer(weights={
            'zeta1': 2.0, 'zeta2': 1.0, 'zeta3': 0.5,
            'zeta4': 1.5, 'zeta5': 0.8, 'zeta6': 1.2
        })
        
        result1 = analyzer1.analyze_simulated_data(duration=5.0)
        result2 = analyzer2.analyze_simulated_data(duration=5.0)
        
        # Same zeta values but different total distances due to weights
        assert result1.zeta_values == result2.zeta_values
        assert result1.d_total != result2.d_total
    
    def test_selective_indicators(self):
        """Test analyzer with only selected indicators."""
        # Test with only FELC and TEB
        analyzer = SixKeysAnalyzer(enable_indicators={'FELC', 'TEB'})
        
        result = analyzer.analyze_simulated_data(duration=5.0)
        
        assert len(result.zeta_values) == 2
        assert 'FELC' in result.zeta_values
        assert 'TEB' in result.zeta_values
        assert 'RFI' not in result.zeta_values
        assert 'ECGP' not in result.zeta_values
        assert 'PWC' not in result.zeta_values
        assert 'ACI' not in result.zeta_values
    
    def test_reproducibility(self):
        """Test that results are reproducible."""
        analyzer = SixKeysAnalyzer()
        
        result1 = analyzer.analyze_simulated_data(
            consciousness_state='awake',
            duration=5.0
        )
        
        result2 = analyzer.analyze_simulated_data(
            consciousness_state='awake',
            duration=5.0
        )
        
        # Results should be identical due to seeding
        for indicator in result1.zeta_values:
            assert np.isclose(result1.zeta_values[indicator], 
                            result2.zeta_values[indicator])
        
        assert np.isclose(result1.d_total, result2.d_total)
    
    def test_error_handling(self):
        """Test error handling for invalid inputs."""
        analyzer = SixKeysAnalyzer()
        
        # Test invalid consciousness state
        with pytest.raises(ValueError):
            analyzer.analyze_simulated_data(consciousness_state='invalid_state')
        
        # Test invalid duration
        with pytest.raises((ValueError, TypeError)):
            analyzer.analyze_simulated_data(duration=-1.0)
        
        # Test invalid dt
        with pytest.raises((ValueError, TypeError)):
            analyzer.analyze_simulated_data(dt=0.0)
    
    def test_metadata_completeness(self):
        """Test that analysis metadata is complete."""
        analyzer = SixKeysAnalyzer()
        result = analyzer.analyze_simulated_data(duration=5.0)
        
        metadata = result.metadata
        
        assert 'analysis_type' in metadata
        assert 'target_state' in metadata
        assert 'duration' in metadata
        assert 'dt' in metadata
        assert 'enabled_indicators' in metadata
        assert 'weights' in metadata
        
        assert metadata['analysis_type'] == 'simulated'
        assert len(metadata['enabled_indicators']) == 6
        assert len(metadata['weights']) == 6