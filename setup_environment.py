"""
Setup and Installation Script for Tunisian Government Salary Analysis System
============================================================================

This script helps set up the environment and install required packages
for the salary analysis system.

Usage:
    python setup_environment.py
"""

import subprocess
import sys
import os
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required.")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    
    print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
    return True

def install_packages():
    """Install required packages using pip."""
    print("🔄 Installing required packages...")
    
    packages = [
        "pandas>=1.5.0",
        "numpy>=1.21.0", 
        "scikit-learn>=1.1.0",
        "statsmodels>=0.13.0",
        "matplotlib>=3.5.0",
        "seaborn>=0.11.0",
        "plotly>=5.10.0"
    ]
    
    try:
        for package in packages:
            print(f"   Installing {package}...")
            result = subprocess.run([sys.executable, '-m', 'pip', 'install', package], 
                                  capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"   ❌ Failed to install {package}")
                print(f"   Error: {result.stderr}")
                return False
            else:
                print(f"   ✅ {package} installed successfully")
        
        print("✅ All packages installed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error during installation: {e}")
        return False

def check_data_files():
    """Check if required data files are present."""
    print("🔍 Checking for required data files...")
    
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
    present_files = []
    
    for file in required_files:
        if Path(file).exists():
            present_files.append(file)
            print(f"   ✅ {file}")
        else:
            missing_files.append(file)
            print(f"   ❌ {file}")
    
    if missing_files:
        print(f"\n⚠️  Missing {len(missing_files)} required data files:")
        for file in missing_files:
            print(f"     - {file}")
        print("\nPlease ensure all data files are in the current directory.")
        return False
    
    print(f"\n✅ All {len(present_files)} data files found!")
    return True

def test_imports():
    """Test if all required packages can be imported."""
    print("🧪 Testing package imports...")
    
    import_tests = [
        ("pandas", "import pandas as pd"),
        ("numpy", "import numpy as np"),
        ("matplotlib", "import matplotlib.pyplot as plt"),
        ("seaborn", "import seaborn as sns"),
        ("sklearn", "from sklearn.linear_model import LinearRegression"),
        ("statsmodels", "from statsmodels.tsa.arima.model import ARIMA"),
        ("plotly", "import plotly.graph_objects as go")
    ]
    
    all_successful = True
    
    for package_name, import_statement in import_tests:
        try:
            exec(import_statement)
            print(f"   ✅ {package_name}")
        except ImportError as e:
            print(f"   ❌ {package_name}: {e}")
            all_successful = False
        except Exception as e:
            print(f"   ⚠️  {package_name}: {e}")
    
    if all_successful:
        print("✅ All packages imported successfully!")
    else:
        print("❌ Some packages failed to import. Please check the installation.")
    
    return all_successful

def test_analyzer():
    """Test the SalaryAnalyzer class."""
    print("🧪 Testing SalaryAnalyzer...")
    
    try:
        from salary_analyzer import SalaryAnalyzer
        
        # Try to initialize
        analyzer = SalaryAnalyzer(data_directory=".", encoding='utf-8')
        print("   ✅ SalaryAnalyzer initialized successfully")
        
        # Test data loading (only if files are present)
        if check_data_files():
            print("   🔄 Testing data loading...")
            if analyzer.load_and_clean_data():
                print("   ✅ Data loading test successful")
                return True
            else:
                print("   ❌ Data loading test failed")
                return False
        else:
            print("   ⚠️  Cannot test data loading - missing data files")
            return True
            
    except ImportError as e:
        print(f"   ❌ Cannot import SalaryAnalyzer: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Error testing SalaryAnalyzer: {e}")
        return False

def create_output_directories():
    """Create necessary output directories."""
    print("📁 Creating output directories...")
    
    directories = ['visualizations', 'reports', 'outputs']
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"   ✅ {directory}/")
    
    print("✅ Output directories created!")

def display_usage_instructions():
    """Display usage instructions."""
    print("\n" + "="*60)
    print("USAGE INSTRUCTIONS")
    print("="*60)
    
    print("\n🚀 QUICK START:")
    print("   1. Run the demonstration script:")
    print("      python demo_analysis.py")
    print()
    print("   2. Or run the complete analysis:")
    print("      python salary_analyzer.py")
    print()
    print("   3. For allowance reports only:")
    print("      python allowance_report_generator.py")
    
    print("\n📋 AVAILABLE SCRIPTS:")
    print("   • salary_analyzer.py - Main analysis class")
    print("   • demo_analysis.py - Interactive demonstration")
    print("   • allowance_report_generator.py - Detailed allowance reports")
    print("   • setup_environment.py - This setup script")
    
    print("\n📊 OUTPUT FILES:")
    print("   • salary_analysis_report.json - Complete analysis report")
    print("   • allowance_amounts_report.json - Allowance amounts by dept/corps/grade")
    print("   • allowance_counts_report.json - Allowance counts by dept/corps/grade")
    print("   • visualizations/ - All charts and graphs")
    
    print("\n🔧 CUSTOMIZATION:")
    print("   • Modify prediction years in salary_analyzer.py")
    print("   • Adjust visualization settings in create_visualizations()")
    print("   • Change output formats in generate_final_report()")

def main():
    """Main setup function."""
    print("🇹🇳 TUNISIAN GOVERNMENT SALARY ANALYSIS SYSTEM SETUP")
    print("=" * 60)
    print("This script will set up your environment for salary analysis.")
    print("=" * 60)
    
    # Step 1: Check Python version
    if not check_python_version():
        return
    
    # Step 2: Install packages
    print("\n" + "-" * 60)
    install_choice = input("Do you want to install required packages? (y/n): ").lower().strip()
    
    if install_choice in ['y', 'yes']:
        if not install_packages():
            print("❌ Package installation failed. Please install manually:")
            print("   pip install -r requirements.txt")
            return
    else:
        print("⚠️  Skipping package installation. Make sure packages are installed manually.")
    
    # Step 3: Test imports
    print("\n" + "-" * 60)
    if not test_imports():
        print("❌ Import tests failed. Please check package installation.")
        return
    
    # Step 4: Check data files
    print("\n" + "-" * 60)
    data_files_present = check_data_files()
    
    # Step 5: Create output directories
    print("\n" + "-" * 60)
    create_output_directories()
    
    # Step 6: Test analyzer (if data files present)
    if data_files_present:
        print("\n" + "-" * 60)
        if test_analyzer():
            print("✅ Analyzer test successful!")
        else:
            print("❌ Analyzer test failed.")
    
    # Step 7: Display results
    print("\n" + "=" * 60)
    print("SETUP COMPLETE!")
    print("=" * 60)
    
    if data_files_present:
        print("✅ Environment ready for analysis!")
        print("✅ All data files present")
        print("✅ All packages installed and tested")
        
        # Ask if user wants to run demo
        demo_choice = input("\nWould you like to run the demonstration now? (y/n): ").lower().strip()
        if demo_choice in ['y', 'yes']:
            print("\n🚀 Starting demonstration...")
            try:
                import demo_analysis
                demo_analysis.main()
            except Exception as e:
                print(f"❌ Error running demonstration: {e}")
                print("You can run it manually with: python demo_analysis.py")
    else:
        print("⚠️  Environment partially ready")
        print("❌ Missing data files - please add them to proceed")
        print("✅ All packages installed and tested")
    
    # Display usage instructions
    display_usage_instructions()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Setup interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\n❌ Unexpected error during setup: {e}")
        import traceback
        traceback.print_exc()
