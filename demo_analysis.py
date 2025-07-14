"""
Demonstration script for the Tunisian Government Salary Analysis System
======================================================================

This script demonstrates how to use the SalaryAnalyzer class for comprehensive
salary analysis and prediction for Tunisian government departments.

Usage:
    python demo_analysis.py

Requirements:
    - All data files must be present in the same directory
    - Install required packages: pip install -r requirements.txt
"""

import sys
import os
from pathlib import Path

# Add current directory to path to import salary_analyzer
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

try:
    from salary_analyzer import SalaryAnalyzer
except ImportError as e:
    print(f"Error importing SalaryAnalyzer: {e}")
    print("Please ensure all required packages are installed:")
    print("pip install -r requirements.txt")
    sys.exit(1)

def check_data_files():
    """Check if all required data files are present."""
    required_files = [
        'tab_paie_13_23.cleaned.txt',
        'table_grade.cleaned.txt',
        'table_corps.cleaned.txt',
        'table_etablissement.cleaned.txt',
        'table_categorie.cleaned.txt',
        'table_nature.cleaned.txt',
        'table_indemnite.cleaned.txt',
        'table_organigramme_5_ministeres.cleaned.txt'
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required data files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    print("✅ All required data files found!")
    return True

def run_basic_analysis():
    """Run basic analysis demonstration."""
    print("\n" + "="*60)
    print("         BASIC ANALYSIS DEMONSTRATION")
    print("="*60)
    
    try:
        # Initialize analyzer
        print("🔄 Initializing SalaryAnalyzer...")
        analyzer = SalaryAnalyzer(data_directory=".", encoding='utf-8')
        
        # Load data
        print("🔄 Loading and cleaning data...")
        if not analyzer.load_and_clean_data():
            print("❌ Failed to load data!")
            return False
        
        # Merge with nomenclature
        print("🔄 Merging with nomenclature tables...")
        analyzer.merge_data_with_nomenclature()
        
        # Basic statistics
        print("\n📊 BASIC STATISTICS:")
        print(f"   - Total records: {len(analyzer.main_data):,}")
        print(f"   - Date range: {analyzer.main_data['Annee'].min()} - {analyzer.main_data['Annee'].max()}")
        print(f"   - Unique agents: {analyzer.main_data['Id_agent'].nunique():,}")
        print(f"   - Unique establishments: {analyzer.main_data['Codetab'].nunique():,}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in basic analysis: {e}")
        return False

def run_staff_analysis():
    """Run staff evolution analysis."""
    print("\n" + "="*60)
    print("         STAFF EVOLUTION ANALYSIS")
    print("="*60)
    
    try:
        analyzer = SalaryAnalyzer(data_directory=".", encoding='utf-8')
        
        if not analyzer.load_and_clean_data():
            return False
        
        analyzer.merge_data_with_nomenclature()
        
        print("🔄 Calculating staff evolution...")
        staff_evolution = analyzer.calculate_staff_evolution()
        
        # Display results
        print("\n📈 STAFF EVOLUTION RESULTS:")
        
        # Total staff by year
        total_staff = staff_evolution['total']
        print("   Year-by-year staff count:")
        for _, row in total_staff.iterrows():
            print(f"      {int(row['Year'])}: {int(row['Staff_Count']):,} employees")
        
        # Growth analysis
        if len(total_staff) > 1:
            first_year = total_staff.iloc[0]
            last_year = total_staff.iloc[-1]
            total_growth = ((last_year['Staff_Count'] - first_year['Staff_Count']) / first_year['Staff_Count']) * 100
            print(f"\n   📊 Overall growth: {total_growth:.1f}% from {int(first_year['Year'])} to {int(last_year['Year'])}")
        
        # Top ministries by staff
        latest_year = staff_evolution['by_ministry']['Year'].max()
        top_ministries = staff_evolution['by_ministry'][
            staff_evolution['by_ministry']['Year'] == latest_year
        ].nlargest(5, 'Staff_Count')
        
        print(f"\n   🏢 Top 5 ministries by staff count ({int(latest_year)}):")
        for _, row in top_ministries.iterrows():
            ministry_name = str(row['Ministry'])[:40] if row['Ministry'] else 'Unknown'
            print(f"      {ministry_name}: {int(row['Staff_Count']):,} employees")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in staff analysis: {e}")
        return False

def run_salary_analysis():
    """Run salary mass analysis."""
    print("\n" + "="*60)
    print("         SALARY MASS ANALYSIS")
    print("="*60)
    
    try:
        analyzer = SalaryAnalyzer(data_directory=".", encoding='utf-8')
        
        if not analyzer.load_and_clean_data():
            return False
        
        analyzer.merge_data_with_nomenclature()
        
        print("🔄 Calculating salary mass evolution...")
        salary_evolution = analyzer.calculate_salary_mass()
        
        # Display results
        print("\n💰 SALARY MASS RESULTS:")
        
        # Total salary mass by year
        total_salary = salary_evolution['total']
        print("   Year-by-year total salary mass:")
        for _, row in total_salary.iterrows():
            amount_millions = row['Total_Salary_Mass'] / 1e6
            print(f"      {int(row['Year'])}: {amount_millions:,.1f} million TND")
        
        # Average salary per agent
        avg_salary = salary_evolution['average_per_agent']
        print("\n   Average salary per agent:")
        for _, row in avg_salary.iterrows():
            print(f"      {int(row['Year'])}: {row['Average_Salary_Per_Agent']:,.0f} TND")
        
        # Growth analysis
        if len(total_salary) > 1:
            first_year = total_salary.iloc[0]
            last_year = total_salary.iloc[-1]
            salary_growth = ((last_year['Total_Salary_Mass'] - first_year['Total_Salary_Mass']) / first_year['Total_Salary_Mass']) * 100
            print(f"\n   📊 Salary mass growth: {salary_growth:.1f}% from {int(first_year['Year'])} to {int(last_year['Year'])}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in salary analysis: {e}")
        return False

def run_prediction_analysis():
    """Run future predictions analysis."""
    print("\n" + "="*60)
    print("         FUTURE PREDICTIONS (2025-2030)")
    print("="*60)
    
    try:
        analyzer = SalaryAnalyzer(data_directory=".", encoding='utf-8')
        
        if not analyzer.load_and_clean_data():
            return False
        
        analyzer.merge_data_with_nomenclature()
        analyzer.calculate_staff_evolution()
        analyzer.calculate_salary_mass()
        
        print("🔄 Generating predictions for 2025-2030...")
        predictions = analyzer.predict_future_trends([2025, 2026, 2027, 2028, 2029, 2030])
        
        # Display staff predictions
        if 'staff' in predictions and predictions['staff']['predictions']:
            print("\n👥 STAFF COUNT PREDICTIONS:")
            staff_pred = predictions['staff']
            print(f"   Method used: {staff_pred['method']}")
            print(f"   Model accuracy (R²): {staff_pred['score']:.3f}")
            
            for i, year in enumerate(staff_pred['years']):
                if i < len(staff_pred['predictions']):
                    pred = int(staff_pred['predictions'][i])
                    lower = int(staff_pred['confidence_lower'][i])
                    upper = int(staff_pred['confidence_upper'][i])
                    print(f"      {year}: {pred:,} employees (range: {lower:,} - {upper:,})")
        
        # Display salary mass predictions
        if 'salary_mass' in predictions and predictions['salary_mass']['predictions']:
            print("\n💰 SALARY MASS PREDICTIONS:")
            salary_pred = predictions['salary_mass']
            print(f"   Method used: {salary_pred['method']}")
            print(f"   Model accuracy (R²): {salary_pred['score']:.3f}")
            
            for i, year in enumerate(salary_pred['years']):
                if i < len(salary_pred['predictions']):
                    pred = salary_pred['predictions'][i] / 1e6
                    lower = salary_pred['confidence_lower'][i] / 1e6
                    upper = salary_pred['confidence_upper'][i] / 1e6
                    print(f"      {year}: {pred:,.1f} million TND (range: {lower:,.1f} - {upper:,.1f})")
        
        # Display average salary predictions
        if 'avg_salary' in predictions and predictions['avg_salary']['predictions']:
            print("\n📊 AVERAGE SALARY PER AGENT PREDICTIONS:")
            avg_pred = predictions['avg_salary']
            print(f"   Method used: {avg_pred['method']}")
            print(f"   Model accuracy (R²): {avg_pred['score']:.3f}")
            
            for i, year in enumerate(avg_pred['years']):
                if i < len(avg_pred['predictions']):
                    pred = avg_pred['predictions'][i]
                    lower = avg_pred['confidence_lower'][i]
                    upper = avg_pred['confidence_upper'][i]
                    print(f"      {year}: {pred:,.0f} TND (range: {lower:,.0f} - {upper:,.0f})")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in prediction analysis: {e}")
        return False

def run_full_analysis():
    """Run the complete analysis pipeline."""
    print("\n" + "="*60)
    print("         COMPLETE ANALYSIS PIPELINE")
    print("="*60)
    
    try:
        analyzer = SalaryAnalyzer(data_directory=".", encoding='utf-8')
        
        # Step 1: Load data
        print("🔄 Step 1: Loading and cleaning data...")
        if not analyzer.load_and_clean_data():
            return False
        
        # Step 2: Merge with nomenclature
        print("🔄 Step 2: Merging with nomenclature tables...")
        analyzer.merge_data_with_nomenclature()
        
        # Step 3: Calculate staff evolution
        print("🔄 Step 3: Calculating staff evolution...")
        analyzer.calculate_staff_evolution()
        
        # Step 4: Calculate salary mass
        print("🔄 Step 4: Calculating salary mass evolution...")
        analyzer.calculate_salary_mass()
        
        # Step 5: Analyze allowances
        print("🔄 Step 5: Analyzing allowances...")
        analyzer.analyze_allowances()
        
        # Step 6: Generate predictions
        print("🔄 Step 6: Generating future predictions...")
        analyzer.predict_future_trends()
        
        # Step 7: Create visualizations
        print("🔄 Step 7: Creating and saving visualizations...")
        analyzer.save_visualizations()
        
        # Step 8: Generate final report
        print("🔄 Step 8: Generating comprehensive report...")
        final_report = analyzer.generate_final_report()
        
        # Display summary
        print("\n✅ ANALYSIS COMPLETED SUCCESSFULLY!")
        print("\n📋 EXECUTIVE SUMMARY:")
        summary = final_report['executive_summary']
        print(f"   • Total Staff (2023): {summary['total_staff_2023']:,}")
        print(f"   • Predicted Staff (2030): {summary['predicted_staff_2030']:,}")
        print(f"   • Salary Mass (2023): {summary['total_salary_mass_2023']:,.0f} TND")
        print(f"   • Predicted Salary Mass (2030): {summary['predicted_salary_mass_2030']:,.0f} TND")
        print(f"   • Average Annual Growth Rate: {summary['average_annual_growth_rate']}%")
        
        print("\n📊 KEY FINDINGS:")
        for finding in final_report['key_findings'][:3]:  # Show first 3 findings
            print(f"   • {finding}")
        
        print("\n💡 RECOMMENDATIONS:")
        for recommendation in final_report['recommendations'][:3]:  # Show first 3 recommendations
            print(f"   • {recommendation}")
        
        print("\n📁 OUTPUT FILES GENERATED:")
        print("   • salary_analysis_report.json - Complete analysis report")
        print("   • visualizations/ - Directory with all charts and graphs")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in full analysis: {e}")
        return False

def main():
    """Main demonstration function."""
    print("🇹🇳 TUNISIAN GOVERNMENT SALARY ANALYSIS SYSTEM")
    print("=" * 60)
    print("This demonstration script shows the capabilities of the")
    print("SalaryAnalyzer for analyzing payroll data (2013-2023)")
    print("and predicting trends for 2025-2030.")
    print("=" * 60)
    
    # Check data files
    if not check_data_files():
        print("\n❌ Cannot proceed without required data files.")
        print("Please ensure all .cleaned.txt files are in the current directory.")
        return
    
    # Interactive menu
    while True:
        print("\n🔍 SELECT ANALYSIS TYPE:")
        print("   1. Basic Analysis (Data overview)")
        print("   2. Staff Evolution Analysis")
        print("   3. Salary Mass Analysis")
        print("   4. Future Predictions (2025-2030)")
        print("   5. Complete Analysis Pipeline")
        print("   6. Exit")
        
        try:
            choice = input("\nEnter your choice (1-6): ").strip()
            
            if choice == '1':
                run_basic_analysis()
            elif choice == '2':
                run_staff_analysis()
            elif choice == '3':
                run_salary_analysis()
            elif choice == '4':
                run_prediction_analysis()
            elif choice == '5':
                run_full_analysis()
            elif choice == '6':
                print("\n👋 Thank you for using the Salary Analysis System!")
                break
            else:
                print("❌ Invalid choice. Please enter a number between 1-6.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Analysis interrupted by user. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ An error occurred: {e}")
            print("Please try again or check your data files.")

if __name__ == "__main__":
    main()
