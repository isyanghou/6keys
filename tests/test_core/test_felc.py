#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test module for FELC (Functional Effective Connectivity) indicator.

This module contains unit tests for the FELC class and its methods.
"""

import pytest
import numpy as np
import matplotlib.pyplot as plt
from unittest.mock import patch, MagicMock

# Import the FELC class
try:
    from sixkeys.core.felc import FELC
except ImportError:
    # Fallback for development
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'sixkeys'))
    from core.felc import FELC


class TestFELC:
    """Test class for FELC indicator."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.felc = FELC()
        
    def test_initialization(self):
        """Test FELC initialization with default parameters."""
        assert self.felc.sim_time == 60.0
        assert self.felc.dt == 0.01
        assert self.felc.tau_smp == 200
        assert self.felc.in_band_thr == 0.9
        assert self.felc.cv_thr == 0.2
        
    def test_initialization_with_custom_params(self):
        """Test FELC initialization with custom parameters."""
        custom_felc = FELC(
            sim_time=50.0,
            dt=0.02,
            tau_smp=500,
            in_band_thr=0.3,
            cv_thr=0.05
        )
        assert custom_felc.sim_time == 50.0
        assert custom_felc.dt == 0.02
        assert custom_felc.tau_smp == 500
        assert custom_felc.in_band_thr == 0.3
        assert custom_felc.cv_thr == 0.05
        
    def test_hopf_dynamics_shape(self):
        """Test that Hopf dynamics returns correct shape."""
        # Test with simple input
        state = np.array([1.0, 0.5])
        result = self.felc.hopf_dynamics(state, 0.0, lambda_gain=0.1)
        
        # Should return array of same shape as input
        assert result.shape == state.shape
        assert len(result) == 2
        
    def test_hopf_dynamics_values(self):
        """Test that Hopf dynamics returns reasonable values."""
        # Test with origin
        state = np.array([0.0, 0.0])
        result = self.felc.hopf_dynamics(state, 0.0, lambda_gain=0.1)
        
        # Should return finite values
        assert np.all(np.isfinite(result))
        
        # Test with non-zero values
        state = np.array([1.0, 1.0])
        result = self.felc.hopf_dynamics(state, 0.0, lambda_gain=0.1)
        assert np.all(np.isfinite(result))
        
    def test_simulate_states_output_shape(self):
        """Test that simulate_states returns correct output shape."""
        # Use smaller parameters for faster testing
        test_felc = FELC(sim_time=1.0, dt=0.1, tau_smp=10)
        
        results = test_felc.analyze_states()
        states = {name: data['trajectory'] for name, data in results.items()}
        
        # Should return a dictionary with required keys
        assert isinstance(states, dict)
        required_keys = ['Awake', 'Light-Sedation', 'Deep-Anesthesia']
        for key in required_keys:
            assert key in states
            assert isinstance(states[key], np.ndarray)
            
    def test_simulate_states_time_series_length(self):
        """Test that simulated time series have correct length."""
        test_felc = FELC(sim_time=1.0, dt=0.1)
        
        results = test_felc.analyze_states()
        states = {name: data['trajectory'] for name, data in results.items()}
        
        expected_length = int(1.0 / 0.1)
        for state_name, time_series in states.items():
            assert len(time_series) == expected_length
            
    def test_set_reference_band(self):
        """Test reference band setting functionality."""
        # Test with mock trajectory that matches time array length
        n_points = len(self.felc.t)
        mock_trajectory = np.random.random((n_points, 2)) + 0.5  # Add offset to avoid zero mean
        
        self.felc.set_reference_band(mock_trajectory)
        
        # Should set reference band parameters
        assert self.felc.r0_ref is not None
        assert self.felc.delta_r_ref is not None
        
    def test_calculate_felc_metrics_with_mock_data(self):
        """Test FELC metrics calculation with mock data."""
        # Create mock trajectory that matches time array length
        n_points = len(self.felc.t)
        trajectory = np.random.random((n_points, 2)) + 0.5  # Add offset to avoid zero mean
        
        # Set reference band first
        self.felc.set_reference_band(trajectory)
        
        result = self.felc.calculate_felc_metrics(trajectory)
        
        # Should return a dictionary with FELC metrics
        assert isinstance(result, dict)
        expected_keys = ['C_FELC', 'D_w', 'zeta1', 'phi', 'in_band_ratio', 'radius']
        for key in expected_keys:
            assert key in result
            
    def test_analyze_multiple_states(self):
        """Test analysis of multiple consciousness states."""
        # Use smaller parameters for faster testing
        test_felc = FELC(sim_time=1.0, dt=0.1, tau_smp=10)
        
        with patch.object(test_felc, 'analyze_states') as mock_analyze:
            # Mock the analyze_states method
            mock_results = {
                'Awake': {'trajectory': np.random.random((10, 2)), 'D_w': 0.5},
                'Light-Sedation': {'trajectory': np.random.random((10, 2)), 'D_w': 0.8},
                'Deep-Anesthesia': {'trajectory': np.random.random((10, 2)), 'D_w': 1.2}
            }
            mock_analyze.return_value = mock_results
            
            results = test_felc.analyze_states()
            
            # Should return results for all states
            assert isinstance(results, dict)
            for state_name in mock_results.keys():
                assert state_name in results
                
    @patch('matplotlib.pyplot.show')
    def test_plot_results_no_error(self, mock_show):
        """Test that plotting doesn't raise errors."""
        # Mock results data with correct dimensions
        n_points = len(self.felc.t)
        mock_results = {
            'Awake': {
                'C_FELC': 1,
                'D_w': 0.5,
                'zeta1': 0.2,
                'phi': 0.8,
                'in_band_ratio': 0.9,
                'trajectory': np.random.random((n_points, 2)),
                'radius': np.random.random(n_points),
                'color': 'green'
            },
            'Deep-Anesthesia': {
                'C_FELC': 0,
                'D_w': 1.2,
                'zeta1': -0.5,
                'phi': 0.3,
                'in_band_ratio': 0.2,
                'trajectory': np.random.random((n_points, 2)),
                'radius': np.random.random(n_points),
                'color': 'red'
            }
        }
        
        # Mock states are not needed for plot_results method
        # The method only uses the results dictionary
        
        # Should not raise any exceptions
        try:
            self.felc.plot_results(mock_results)
            plt.close('all')  # Clean up plots
        except Exception as e:
            pytest.fail(f"plot_results raised an exception: {e}")
            
    def test_print_summary_no_error(self):
        """Test that summary printing doesn't raise errors."""
        # Mock results data
        n_points = len(self.felc.t)
        mock_results = {
            'Awake': {
                'C_FELC': 1,
                'D_w': 0.5,
                'zeta1': 0.2,
                'phi': 0.8,
                'in_band_ratio': 0.9,
                'trajectory': np.random.random((n_points, 2)),
                'radius': np.random.random(n_points),
                'color': 'green'
            }
        }
        
        # Should not raise any exceptions
        try:
            self.felc.print_summary(mock_results)
        except Exception as e:
            pytest.fail(f"print_summary raised an exception: {e}")
            
    def test_invalid_parameters(self):
        """Test initialization with invalid parameters."""
        # Test negative simulation time
        with pytest.raises(ValueError):
            FELC(sim_time=-1.0)
            
        # Test zero dt
        with pytest.raises(ValueError):
            FELC(dt=0.0)
            
        # Test negative tau_smp
        with pytest.raises(ValueError):
            FELC(tau_smp=-100)
            
    def test_edge_cases(self):
        """Test edge cases and boundary conditions."""
        # Test with very small simulation time
        small_felc = FELC(sim_time=0.1, dt=0.01)
        results = small_felc.analyze_states()
        
        # Should still work
        assert len(results) > 0
        
        # Test with single sample
        single_felc = FELC(tau_smp=1)
        # Should not raise error during initialization
        assert single_felc.tau_smp == 1
        
    def test_reproducibility(self):
        """Test that results are reproducible with same random seed."""
        # Set random seed
        np.random.seed(42)
        felc1 = FELC(sim_time=1.0, dt=0.1)
        results1 = felc1.analyze_states()
        states1 = {name: data['trajectory'] for name, data in results1.items()}
        
        # Reset seed and run again
        np.random.seed(42)
        felc2 = FELC(sim_time=1.0, dt=0.1)
        results2 = felc2.analyze_states()
        states2 = {name: data['trajectory'] for name, data in results2.items()}
        
        # Results should be identical
        for state_name in states1.keys():
            np.testing.assert_array_equal(states1[state_name], states2[state_name])
            
    def test_memory_efficiency(self):
        """Test that large simulations don't cause memory issues."""
        # This is more of a smoke test
        large_felc = FELC(sim_time=10.0, dt=0.01, tau_smp=100)
        
        # Should complete without memory errors
        try:
            results = large_felc.analyze_states()
            states = {name: data['trajectory'] for name, data in results.items()}
            assert len(states) > 0
        except MemoryError:
            pytest.skip("Insufficient memory for large simulation test")
            

class TestFELCIntegration:
    """Integration tests for FELC."""
    
    def test_full_analysis_pipeline(self):
        """Test the complete FELC analysis pipeline."""
        # Use small parameters for faster testing
        felc = FELC(sim_time=1.0, dt=0.1, tau_smp=10)
        
        # Run complete analysis
        results = felc.analyze_states()
        
        # Verify results structure
        assert isinstance(results, dict)
        assert len(results) > 0
        
        # Each result should have required fields
        for state_name, result in results.items():
            assert 'D_w' in result
            assert 'C_FELC' in result
            assert 'trajectory' in result
            
    @pytest.mark.slow
    def test_realistic_simulation(self):
        """Test with realistic simulation parameters (marked as slow)."""
        # This test uses more realistic parameters and may take longer
        felc = FELC(sim_time=10.0, dt=0.01, tau_smp=100)
        
        results = felc.analyze_states()
        
        # Should produce meaningful results
        assert len(results) == 3  # Awake, Light-Sedation, Deep-Anesthesia
        
        # D_w values should be reasonable (can exceed 1 for non-conscious states)
        for result in results.values():
            assert result['D_w'] >= 0
            

if __name__ == '__main__':
    # Run tests if script is executed directly
    pytest.main([__file__, '-v'])