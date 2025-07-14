"""
Quick System Demonstration
==========================
"""

from salary_analyzer import SalaryAnalyzer

def main():
    print("🇹🇳 QUICK SYSTEM DEMONSTRATION")
    print("=" * 50)
    
    # Initialize analyzer
    print("🔄 Initializing analyzer...")
    analyzer = SalaryAnalyzer()
    
    # Load data
    print("🔄 Loading data...")
    if not analyzer.load_and_clean_data():
        print("❌ Failed to load data")
        return
    
    print(f"✅ Data loaded: {len(analyzer.main_data):,} records")
    
    # Merge with nomenclature
    print("🔄 Merging with nomenclature...")
    analyzer.merge_data_with_nomenclature()
    
    # Calculate staff evolution
    print("🔄 Calculating staff evolution...")
    staff_data = analyzer.calculate_staff_evolution()
    
    print("\n📊 STAFF EVOLUTION RESULTS:")
    print("Total staff by year:")
    for _, row in staff_data['total'].iterrows():
        year = int(row['Year'])
        count = int(row['Staff_Count'])
        print(f"  {year}: {count:,} employees")
    
    # Calculate salary mass
    print("\n🔄 Calculating salary mass...")
    salary_data = analyzer.calculate_salary_mass()
    
    print("\n💰 SALARY MASS RESULTS:")
    print("Total salary mass by year:")
    for _, row in salary_data['total'].head().iterrows():
        year = int(row['Year'])
        amount = row['Total_Salary_Mass'] / 1e6
        print(f"  {year}: {amount:,.1f} million TND")
    
    # Quick prediction test
    print("\n🔄 Testing predictions...")
    predictions = analyzer.predict_future_trends([2025, 2026, 2027])
    
    if 'staff' in predictions and predictions['staff']['predictions']:
        print("\n🔮 STAFF PREDICTIONS:")
        pred_data = predictions['staff']
        for i, year in enumerate(pred_data['years']):
            if i < len(pred_data['predictions']):
                pred = int(pred_data['predictions'][i])
                print(f"  {year}: {pred:,} employees (predicted)")
    
    print("\n✅ DEMONSTRATION COMPLETED SUCCESSFULLY!")
    print("The system is working correctly and ready for full analysis.")

if __name__ == "__main__":
    main()
