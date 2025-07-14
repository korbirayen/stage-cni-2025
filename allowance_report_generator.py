"""
Allowance Evolution Report Generator
===================================

This script generates detailed allowance reports in the specific format requested:
- Allowance amounts by Department/Corps/Grade
- Number of allowances by Department/Corps/Grade
- Predictions for 2025-2030

Output format:
+ Department
  + Corps
    + Grade
                2013  2014  ...  2023  2025  2026  2027  2028  2029  2030
      Allowance1  Amount predictions
      Allowance2  Amount predictions
      ...
"""

import sys
from pathlib import Path
import pandas as pd
import json

# Import our salary analyzer
sys.path.append(str(Path(__file__).parent))
from salary_analyzer import SalaryAnalyzer

class AllowanceReportGenerator:
    """Generate detailed allowance reports in the requested format."""
    
    def __init__(self, analyzer):
        """
        Initialize with a SalaryAnalyzer instance.
        
        Args:
            analyzer: Initialized SalaryAnalyzer instance
        """
        self.analyzer = analyzer
        
    def generate_allowance_amount_report(self):
        """
        Generate allowance amount evolution report by Department/Corps/Grade.
        
        Returns:
            dict: Structured report with allowance amounts
        """
        print("Generating allowance amount evolution report...")
        
        # Ensure data is loaded and analyzed
        if self.analyzer.merged_data is None:
            self.analyzer.merge_data_with_nomenclature()
        
        if self.analyzer.allowance_analysis is None:
            self.analyzer.analyze_allowances()
        
        # Get unique allowance types/codes
        allowance_types = self.analyzer.merged_data['Codind'].unique()
        allowance_types = [code for code in allowance_types if pd.notna(code)]
        
        # Structure: Department -> Corps -> Grade -> Allowance -> Year -> Amount
        report = {}
        
        # Process data by ministry/department
        for ministry in self.analyzer.merged_data['Ministry'].unique():
            if pd.notna(ministry):
                ministry_data = self.analyzer.merged_data[
                    self.analyzer.merged_data['Ministry'] == ministry
                ]
                
                report[ministry] = {}
                
                # Process by corps
                for corps in ministry_data['Corps_Name_FR'].unique():
                    if pd.notna(corps):
                        corps_data = ministry_data[
                            ministry_data['Corps_Name_FR'] == corps
                        ]
                        
                        report[ministry][corps] = {}
                        
                        # Process by grade
                        for grade in corps_data['Grade_Name_FR'].unique():
                            if pd.notna(grade):
                                grade_data = corps_data[
                                    corps_data['Grade_Name_FR'] == grade
                                ]
                                
                                report[ministry][corps][grade] = {}
                                
                                # Process each allowance type
                                for allowance_code in allowance_types:
                                    allowance_data = grade_data[
                                        grade_data['Codind'] == allowance_code
                                    ]
                                    
                                    if len(allowance_data) > 0:
                                        # Calculate historical amounts by year
                                        yearly_amounts = allowance_data.groupby('Annee')['Montind'].sum()
                                        
                                        # Create year series (2013-2030)
                                        years = list(range(2013, 2031))
                                        amounts = {}
                                        
                                        # Fill historical data (2013-2023)
                                        for year in range(2013, 2024):
                                            amounts[year] = yearly_amounts.get(year, 0)
                                        
                                        # Predict future amounts (2025-2030)
                                        if len(yearly_amounts) >= 3:  # Need enough data for prediction
                                            predictions = self._predict_allowance_amounts(yearly_amounts)
                                            for year in range(2025, 2031):
                                                amounts[year] = predictions.get(year, 0)
                                        else:
                                            # Use last known amount as prediction if insufficient data
                                            last_amount = yearly_amounts.iloc[-1] if len(yearly_amounts) > 0 else 0
                                            for year in range(2025, 2031):
                                                amounts[year] = last_amount
                                        
                                        # Skip 2024 (transition year)
                                        amounts[2024] = 0
                                        
                                        report[ministry][corps][grade][f"Allowance_{allowance_code}"] = amounts
        
        return report
    
    def generate_allowance_count_report(self):
        """
        Generate number of allowances evolution report by Department/Corps/Grade.
        
        Returns:
            dict: Structured report with allowance counts
        """
        print("Generating allowance count evolution report...")
        
        # Structure: Department -> Corps -> Grade -> Year -> Count
        report = {}
        
        # Process data by ministry/department
        for ministry in self.analyzer.merged_data['Ministry'].unique():
            if pd.notna(ministry):
                ministry_data = self.analyzer.merged_data[
                    self.analyzer.merged_data['Ministry'] == ministry
                ]
                
                report[ministry] = {}
                
                # Process by corps
                for corps in ministry_data['Corps_Name_FR'].unique():
                    if pd.notna(corps):
                        corps_data = ministry_data[
                            ministry_data['Corps_Name_FR'] == corps
                        ]
                        
                        report[ministry][corps] = {}
                        
                        # Process by grade
                        for grade in corps_data['Grade_Name_FR'].unique():
                            if pd.notna(grade):
                                grade_data = corps_data[
                                    corps_data['Grade_Name_FR'] == grade
                                ]
                                
                                # Count allowances by year
                                yearly_counts = grade_data.groupby('Annee').size()
                                
                                # Create year series (2013-2030)
                                counts = {}
                                
                                # Fill historical data (2013-2023)
                                for year in range(2013, 2024):
                                    counts[year] = yearly_counts.get(year, 0)
                                
                                # Predict future counts (2025-2030)
                                if len(yearly_counts) >= 3:
                                    predictions = self._predict_allowance_counts(yearly_counts)
                                    for year in range(2025, 2031):
                                        counts[year] = predictions.get(year, 0)
                                else:
                                    # Use last known count as prediction
                                    last_count = yearly_counts.iloc[-1] if len(yearly_counts) > 0 else 0
                                    for year in range(2025, 2031):
                                        counts[year] = last_count
                                
                                # Skip 2024
                                counts[2024] = 0
                                
                                report[ministry][corps][grade] = counts
        
        return report
    
    def _predict_allowance_amounts(self, yearly_amounts):
        """
        Predict future allowance amounts using simple trend analysis.
        
        Args:
            yearly_amounts: Series of yearly amounts
            
        Returns:
            dict: Predicted amounts for 2025-2030
        """
        try:
            # Calculate trend
            years = list(yearly_amounts.index)
            amounts = list(yearly_amounts.values)
            
            if len(years) < 2:
                return {year: amounts[0] if amounts else 0 for year in range(2025, 2031)}
            
            # Simple linear trend
            year_diff = years[-1] - years[0]
            amount_diff = amounts[-1] - amounts[0]
            annual_trend = amount_diff / year_diff if year_diff > 0 else 0
            
            # Project future values
            base_amount = amounts[-1]
            predictions = {}
            
            for year in range(2025, 2031):
                years_ahead = year - years[-1]
                predicted_amount = max(0, base_amount + (annual_trend * years_ahead))
                predictions[year] = predicted_amount
            
            return predictions
            
        except Exception:
            # Fallback: use last known amount
            last_amount = amounts[-1] if amounts else 0
            return {year: last_amount for year in range(2025, 2031)}
    
    def _predict_allowance_counts(self, yearly_counts):
        """
        Predict future allowance counts.
        
        Args:
            yearly_counts: Series of yearly counts
            
        Returns:
            dict: Predicted counts for 2025-2030
        """
        try:
            # Calculate average or trend
            counts = list(yearly_counts.values)
            
            if len(counts) == 0:
                return {year: 0 for year in range(2025, 2031)}
            
            # Use average of last 3 years or all available years
            recent_counts = counts[-3:] if len(counts) >= 3 else counts
            avg_count = sum(recent_counts) / len(recent_counts)
            
            # Round to integer
            predicted_count = max(0, int(round(avg_count)))
            
            return {year: predicted_count for year in range(2025, 2031)}
            
        except Exception:
            return {year: 0 for year in range(2025, 2031)}
    
    def format_amount_report_for_display(self, report):
        """
        Format the allowance amount report for console display.
        
        Args:
            report: The allowance amount report
            
        Returns:
            str: Formatted report string
        """
        output = []
        output.append("ALLOWANCE AMOUNT EVOLUTION REPORT")
        output.append("=" * 50)
        output.append("Format: Department > Corps > Grade > Allowance")
        output.append("Years: 2013-2023 (Historical) | 2025-2030 (Predicted)")
        output.append("=" * 50)
        
        for dept_name, dept_data in report.items():
            output.append(f"\n+ {dept_name}")
            
            for corps_name, corps_data in dept_data.items():
                output.append(f"  + {corps_name}")
                
                for grade_name, grade_data in corps_data.items():
                    output.append(f"    + {grade_name}")
                    
                    # Header with years
                    years = "                    " + "  ".join([str(y) for y in range(2013, 2031) if y != 2024])
                    output.append(f"      {years}")
                    
                    # Each allowance
                    for allowance_name, amounts in grade_data.items():
                        amounts_str = "  ".join([f"{amounts.get(y, 0):8.0f}" for y in range(2013, 2031) if y != 2024])
                        output.append(f"      {allowance_name:<15} {amounts_str}")
                    
                    output.append("")  # Empty line between grades
        
        return "\n".join(output)
    
    def format_count_report_for_display(self, report):
        """
        Format the allowance count report for console display.
        
        Args:
            report: The allowance count report
            
        Returns:
            str: Formatted report string
        """
        output = []
        output.append("NUMBER OF ALLOWANCES EVOLUTION REPORT")
        output.append("=" * 50)
        output.append("Format: Department > Corps > Grade")
        output.append("Years: 2013-2023 (Historical) | 2025-2030 (Predicted)")
        output.append("=" * 50)
        
        for dept_name, dept_data in report.items():
            output.append(f"\n+ {dept_name}")
            
            for corps_name, corps_data in dept_data.items():
                output.append(f"  + {corps_name}")
                
                # Header with years
                years = "                " + "  ".join([str(y) for y in range(2013, 2031) if y != 2024])
                output.append(f"    {years}")
                
                # Each grade
                for grade_name, counts in corps_data.items():
                    counts_str = "  ".join([f"{counts.get(y, 0):6.0f}" for y in range(2013, 2031) if y != 2024])
                    grade_display = grade_name[:12] + "..." if len(grade_name) > 15 else grade_name
                    output.append(f"    {grade_display:<15} {counts_str}")
                
                output.append("")  # Empty line between corps
        
        return "\n".join(output)
    
    def save_reports_to_files(self, amount_report, count_report):
        """
        Save both reports to JSON and text files.
        
        Args:
            amount_report: Allowance amount report
            count_report: Allowance count report
        """
        # Convert numpy types to native Python types for JSON serialization
        def convert_numpy_types(obj):
            if isinstance(obj, dict):
                return {key: convert_numpy_types(value) for key, value in obj.items()}
            elif isinstance(obj, list):
                return [convert_numpy_types(item) for item in obj]
            elif hasattr(obj, 'item'):  # numpy types
                return obj.item()
            else:
                return obj
        
        # Convert reports
        amount_report_clean = convert_numpy_types(amount_report)
        count_report_clean = convert_numpy_types(count_report)
        
        # Save JSON files
        with open('allowance_amounts_report.json', 'w', encoding='utf-8') as f:
            json.dump(amount_report_clean, f, indent=2, ensure_ascii=False, default=str)
        
        with open('allowance_counts_report.json', 'w', encoding='utf-8') as f:
            json.dump(count_report_clean, f, indent=2, ensure_ascii=False, default=str)
        
        # Save formatted text files
        with open('allowance_amounts_report.txt', 'w', encoding='utf-8') as f:
            f.write(self.format_amount_report_for_display(amount_report))
        
        with open('allowance_counts_report.txt', 'w', encoding='utf-8') as f:
            f.write(self.format_count_report_for_display(count_report))
        
        print("Reports saved to:")
        print("  - allowance_amounts_report.json")
        print("  - allowance_amounts_report.txt")
        print("  - allowance_counts_report.json")
        print("  - allowance_counts_report.txt")

def main():
    """Main function to generate allowance reports."""
    print("🇹🇳 TUNISIAN GOVERNMENT ALLOWANCE EVOLUTION REPORT GENERATOR")
    print("=" * 65)
    
    try:
        # Initialize analyzer
        print("🔄 Initializing SalaryAnalyzer...")
        analyzer = SalaryAnalyzer(data_directory=".", encoding='utf-8')
        
        # Load data
        print("🔄 Loading and processing data...")
        if not analyzer.load_and_clean_data():
            print("❌ Failed to load data!")
            return
        
        # Merge with nomenclature
        analyzer.merge_data_with_nomenclature()
        
        # Analyze allowances
        analyzer.analyze_allowances()
        
        # Create report generator
        print("🔄 Generating detailed allowance reports...")
        report_generator = AllowanceReportGenerator(analyzer)
        
        # Generate reports
        print("📊 Generating allowance amount evolution report...")
        amount_report = report_generator.generate_allowance_amount_report()
        
        print("📊 Generating allowance count evolution report...")
        count_report = report_generator.generate_allowance_count_report()
        
        # Save reports
        print("💾 Saving reports to files...")
        report_generator.save_reports_to_files(amount_report, count_report)
        
        # Display sample of reports
        print("\n" + "="*65)
        print("SAMPLE OUTPUT - ALLOWANCE AMOUNTS (First Department/Corps/Grade)")
        print("="*65)
        
        # Show first few entries
        sample_lines = report_generator.format_amount_report_for_display(amount_report).split('\n')
        for line in sample_lines[:30]:  # Show first 30 lines
            print(line)
        
        print("\n... (Full reports saved to files)")
        
        print("\n" + "="*65)
        print("SAMPLE OUTPUT - ALLOWANCE COUNTS (First Department/Corps)")
        print("="*65)
        
        sample_lines = report_generator.format_count_report_for_display(count_report).split('\n')
        for line in sample_lines[:25]:  # Show first 25 lines
            print(line)
        
        print("\n... (Full reports saved to files)")
        
        print("\n✅ ALLOWANCE REPORTS GENERATED SUCCESSFULLY!")
        print("\nThe reports include:")
        print("  • Historical data (2013-2023)")
        print("  • Future predictions (2025-2030)")
        print("  • Structured by Department → Corps → Grade")
        print("  • Both allowance amounts and counts")
        
    except Exception as e:
        print(f"❌ Error generating reports: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
