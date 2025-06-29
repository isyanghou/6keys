#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Basic Usage Example for Six Keys Criticality Framework

六鑰臨界基本使用示例

This example demonstrates how to use the Six Keys Criticality framework
for analyzing neural consciousness states.
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
import os

# Add parent directory to path for importing sixkeys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import sixkeys as sk


def main():
    """
    Main demonstration function.
    """
    print("🔑 Six Keys Criticality Framework - Basic Usage Example")
    print("=" * 60)
    
    # Set random seed for reproducibility
    np.random.seed(42)
    
    # Setup plotting style
    sk.utils.setup_plot_style()
    
    print("\n1. Creating Six Keys Analyzer...")
    # Create analyzer with default parameters
    analyzer = sk.SixKeysAnalyzer(
        theta_c=1.0,  # Critical threshold
        random_state=42
    )
    
    print(f"   Enabled indicators: {analyzer.enable_indicators}")
    print(f"   Critical threshold: {analyzer.theta_c}")
    
    print("\n2. Analyzing simulated consciousness states...")
    # Analyze default consciousness states
    results = analyzer.analyze_simulated_states()
    
    print(f"   Analyzed {len(results)} states: {list(results.keys())}")
    
    print("\n3. Creating visualizations...")
    
    # Create radar chart
    print("   - Radar chart")
    radar_fig = analyzer.plot_radar_chart(results)
    
    # Create phase diagram
    print("   - Phase diagram")
    phase_fig = analyzer.plot_phase_diagram(results)
    
    # Create comprehensive summary
    print("   - Comprehensive summary")
    summary_fig = sk.utils.plot_criticality_summary(results, theta_c=analyzer.theta_c)
    
    print("\n4. Analysis Summary:")
    analyzer.print_summary(results)
    
    print("\n5. Individual Indicator Analysis:")
    
    # Demonstrate individual FELC analysis
    print("\n   🔑 FELC (ζ₁) Analysis:")
    felc = sk.FELC(random_state=42)
    felc_results = felc.analyze_states()
    felc.print_summary(felc_results)
    
    # Demonstrate individual TEB analysis
    print("\n   🔑 TEB (ζ₂) Analysis:")
    teb = sk.TEB()
    np.random.seed(2025)  # TEB uses different seed in original
    teb_results = teb.analyze_states()
    teb.print_summary(teb_results)
    
    print("\n6. Custom State Analysis:")
    
    # Define custom states
    custom_states = {
        "Healthy-Awake": {"lambda_gain": 1.5, "eta_target": 1.05, "color": "darkgreen"},
        "Mild-Sedation": {"lambda_gain": 0.8, "eta_target": 0.95, "color": "gold"},
        "Pathological": {"lambda_gain": -0.5, "eta_target": 0.60, "color": "darkred"},
    }
    
    print("   Analyzing custom states with different parameters...")
    
    # Note: This would require extending the analyzer to handle custom parameters
    # For now, we'll demonstrate the concept
    print("   Custom states defined:")
    for state, params in custom_states.items():
        print(f"     - {state}: λ={params['lambda_gain']}, η_target={params['eta_target']}")
    
    print("\n7. Saving Results:")
    
    # Save figures
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    radar_fig.savefig(f"{output_dir}/radar_chart.png", dpi=300, bbox_inches='tight')
    phase_fig.savefig(f"{output_dir}/phase_diagram.png", dpi=300, bbox_inches='tight')
    summary_fig.savefig(f"{output_dir}/summary.png", dpi=300, bbox_inches='tight')
    
    print(f"   Figures saved to '{output_dir}/' directory")
    
    # Save results to file (would require implementing save_results function)
    # sk.utils.save_results(results, f"{output_dir}/analysis_results.json")
    
    print("\n✅ Analysis complete! Check the generated plots.")
    
    # Show plots
    plt.show()
    
    return analyzer, results, radar_fig, phase_fig, summary_fig


def demonstrate_individual_indicators():
    """演示各個指標的單獨使用。"""
    print("\n" + "="*60)
    print("個別指標演示")
    print("="*60)
    
    # FELC 指標演示
    print("\n1. FELC (自由能景觀臨界) 指標:")
    print("-" * 40)
    
    felc = FELC()
    felc_result = felc.analyze(
        target_energy=0.0,
        noise_level=0.05,
        sim_time=30.0
    )
    
    print(f"   ζ₁ (FELC坐標): {felc_result.zeta_1:.4f}")
    print(f"   C_FELC (二值準則): {felc_result.C_FELC}")
    print(f"   目標能量: {felc_result.target_energy}")
    print(f"   實際平均能量: {felc_result.mean_energy:.4f}")
    
    # TEB 指標演示
    print("\n2. TEB (熱力學效率邊界) 指標:")
    print("-" * 40)
    
    teb = TEB()
    teb_result = teb.analyze(
        target_efficiency=0.75,
        noise_level=0.03,
        sim_time=30.0
    )
    
    print(f"   ζ₂ (TEB坐標): {teb_result.zeta_2:.4f}")
    print(f"   C_TEB (二值準則): {teb_result.C_TEB}")
    print(f"   目標效率: {teb_result.target_efficiency}")
    print(f"   實際平均效率: {teb_result.mean_efficiency:.4f}")
    
    # RFI 指標演示
    print("\n3. RFI (Ricci曲率流指標) 指標:")
    print("-" * 40)
    
    from sixkeys.core import RFI
    rfi = RFI()
    rfi_result = rfi.analyze(
        kappa_target=0.0,
        sim_time=30.0
    )
    
    print(f"   ζ₃ (RFI坐標): {rfi_result.zeta_3:.4f}")
    print(f"   C_RFI (二值準則): {rfi_result.C_RFI}")
    print(f"   目標曲率: {rfi_result.kappa_target}")
    print(f"   實際平均曲率: {rfi_result.mean_curvature:.4f}")
    
    # ECGP 指標演示
    print("\n4. ECGP (有效因果圖滲透) 指標:")
    print("-" * 40)
    
    from sixkeys.core import ECGP
    ecgp = ECGP()
    ecgp_result = ecgp.analyze(
        p_target=0.6,
        sim_time=30.0
    )
    
    print(f"   ζ₄ (ECGP坐標): {ecgp_result.zeta_4:.4f}")
    print(f"   C_ECGP (二值準則): {ecgp_result.C_ECGP}")
    print(f"   目標滲透強度: {ecgp_result.p_target}")
    print(f"   實際平均滲透強度: {ecgp_result.mean_percolation:.4f}")
    
    # PWC 指標演示
    print("\n5. PWC (相位包裹環流) 指標:")
    print("-" * 40)
    
    from sixkeys.core import PWC
    pwc = PWC()
    pwc_result = pwc.analyze(
        gamma_target=0.0,
        sim_time=30.0
    )
    
    print(f"   ζ₅ (PWC坐標): {pwc_result.zeta_5:.4f}")
    print(f"   C_PWC (二值準則): {pwc_result.C_PWC}")
    print(f"   目標環流強度: {pwc_result.gamma_target}")
    print(f"   實際平均環流強度: {pwc_result.mean_circulation:.4f}")
    
    # ACI 指標演示
    print("\n6. ACI (星形膠質細胞耦合) 指標:")
    print("-" * 40)
    
    from sixkeys.core import ACI
    aci = ACI()
    aci_result = aci.analyze(
        a_target=0.5,
        sim_time=30.0
    )
    
    print(f"   ζ₆ (ACI坐標): {aci_result.zeta_6:.4f}")
    print(f"   C_ACI (二值準則): {aci_result.C_ACI}")
    print(f"   目標耦合強度: {aci_result.a_target}")
    print(f"   實際平均耦合強度: {aci_result.mean_coupling:.4f}")
    
    # 可視化選項
    print("\n可視化選項:")
    print("   felc.plot_analysis(felc_result)  # 繪製FELC分析圖")
    print("   teb.plot_analysis(teb_result)    # 繪製TEB分析圖")
    print("   rfi.plot_analysis(rfi_result)    # 繪製RFI分析圖")
    print("   ecgp.plot_analysis(ecgp_result)  # 繪製ECGP分析圖")
    print("   pwc.plot_analysis(pwc_result)    # 繪製PWC分析圖")
    print("   aci.plot_analysis(aci_result)    # 繪製ACI分析圖")


def demonstrate_real_data_analysis():
    """
    Demonstrate how to analyze real neural data (placeholder).
    """
    print("\n" + "=" * 60)
    print("🧠 Real Neural Data Analysis (Conceptual)")
    print("=" * 60)
    
    print("\nFor real neural data analysis, you would:")
    print("\n1. Load your neural time series data:")
    print("   data = sk.load_data('path/to/neural_data.mat')")
    print("   # Expected shape: (n_timepoints, n_channels)")
    
    print("\n2. Preprocess the data:")
    print("   data_clean = sk.utils.preprocess_neural_data(data)")
    print("   data_filtered = sk.utils.filter_data(data_clean, low_freq=1, high_freq=40)")
    
    print("\n3. Analyze criticality:")
    print("   analyzer = sk.SixKeysAnalyzer()")
    print("   results = analyzer.analyze_data(data_filtered)")
    
    print("\n4. Visualize and interpret results:")
    print("   sk.utils.plot_criticality_summary(results)")
    print("   analyzer.print_summary(results)")
    
    print("Note: Real data analysis requires additional indicators (ζ₃-ζ₆)")
    print("      - RFI (ζ₃): Ricci曲率流指標")
    print("      - ECGP (ζ₄): 有效因果圖滲透")
    print("      - PWC (ζ₅): 相位包裹環流")
    print("      - ACI (ζ₆): 星形膠質細胞耦合指標")


def demonstrate_batch_analysis():
    """
    Demonstrate batch analysis of multiple datasets (placeholder).
    """
    print("\n" + "=" * 60)
    print("📊 Batch Analysis (Conceptual)")
    print("=" * 60)
    
    print("\nFor batch analysis of multiple subjects/sessions:")
    print("\n1. Setup batch analyzer:")
    print("   batch_analyzer = sk.BatchAnalyzer()")
    
    print("\n2. Add datasets:")
    print("   batch_analyzer.add_dataset('subject_01', data1)")
    print("   batch_analyzer.add_dataset('subject_02', data2)")
    print("   # ... add more datasets")
    
    print("\n3. Run batch analysis:")
    print("   batch_results = batch_analyzer.analyze_all()")
    
    print("\n4. Generate group statistics:")
    print("   group_stats = batch_analyzer.compute_group_statistics()")
    print("   batch_analyzer.plot_group_comparison()")
    
    print("\nNote: Batch analysis functionality will be added in future versions.")


if __name__ == "__main__":
    # Run main demonstration
    analyzer, results, radar_fig, phase_fig, summary_fig = main()
    
    # Show additional conceptual examples
    demonstrate_individual_indicators()
    demonstrate_real_data_analysis()
    demonstrate_batch_analysis()
    
    print("\n" + "=" * 60)
    print("🎯 Next Steps:")
    print("=" * 60)
    print("1. Explore individual indicator modules (FELC, TEB, etc.)")
    print("2. Try different parameter settings")
    print("3. Implement additional indicators (ζ₃-ζ₆)")
    print("4. Apply to your own neural datasets")
    print("5. Contribute to the project development")
    
    print("\n📚 For more information:")
    print("   - Documentation: https://sixkeys.readthedocs.io/")
    print("   - GitHub: https://github.com/yourusername/sixkeys")
    print("   - Examples: ./examples/ directory")
    print("   - Notebooks: ./notebooks/ directory")
    
    print("\n🙏 Thank you for using Six Keys Criticality Framework!")