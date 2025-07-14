"""
Quick Data Analysis Test
========================

This script tests the data loading and provides basic information
about the dataset structure.
"""

import pandas as pd
import numpy as np
from pathlib import Path

def analyze_data_structure():
    """Analyze the main data file structure."""
    print("🔍 ANALYZING DATA STRUCTURE")
    print("=" * 50)
    
    try:
        # Define column names based on schema
        main_columns = [
            'Codetab', 'Mois', 'Annee', 'Type', 'Nligne', 'Codind', 
            'Montind', 'Article', 'Par', 'Codgrd', 'Codcorps', 'Hcorps',
            'Codefam', 'Codsfam', 'Codnat', 'Dire', 'Sdir', 'Serv',
            'Deleg', 'Centreg', 'Gouv', 'Id_agent'
        ]
        
        # Read first 1000 rows to analyze structure
        print("📊 Reading sample data...")
        sample_data = pd.read_csv(
            'tab_paie_13_23.cleaned.txt', 
            sep=';', 
            encoding='utf-8',
            nrows=1000,
            header=None
        )
        
        print(f"✅ Sample loaded: {len(sample_data)} rows, {len(sample_data.columns)} columns")
        print(f"Expected columns: {len(main_columns)}")
        
        # Display first few rows
        print("\n📋 FIRST 5 ROWS:")
        print(sample_data.head())
        
        # Display column info
        print(f"\n📊 COLUMN INFORMATION:")
        print(f"Number of columns: {len(sample_data.columns)}")
        print(f"Data types:")
        for i, col in enumerate(sample_data.columns):
            if i < len(main_columns):
                print(f"  Column {i} ({main_columns[i]}): {sample_data[col].dtype}")
            else:
                print(f"  Column {i} (Extra): {sample_data[col].dtype}")
        
        # Check year and month columns specifically
        if len(sample_data.columns) >= 3:
            print(f"\n📅 DATE ANALYSIS:")
            annee_col = sample_data.iloc[:, 2]  # Annee should be column 2
            mois_col = sample_data.iloc[:, 1]   # Mois should be column 1
            
            print(f"Year range: {annee_col.min()} - {annee_col.max()}")
            print(f"Month range: {mois_col.min()} - {mois_col.max()}")
            print(f"Year unique values: {sorted(annee_col.unique())}")
            print(f"Month unique values: {sorted(mois_col.unique())}")
        
        # Check for missing values
        print(f"\n❓ MISSING VALUES:")
        for i, col in enumerate(sample_data.columns[:10]):  # First 10 columns
            missing = sample_data[col].isna().sum()
            if i < len(main_columns):
                print(f"  {main_columns[i]}: {missing} missing ({missing/len(sample_data)*100:.1f}%)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error analyzing data: {e}")
        return False

def test_fixed_loader():
    """Test the fixed data loader."""
    print("\n🧪 TESTING FIXED DATA LOADER")
    print("=" * 50)
    
    try:
        # Test loading with proper error handling
        main_columns = [
            'Codetab', 'Mois', 'Annee', 'Type', 'Nligne', 'Codind', 
            'Montind', 'Article', 'Par', 'Codgrd', 'Codcorps', 'Hcorps',
            'Codefam', 'Codsfam', 'Codnat', 'Dire', 'Sdir', 'Serv',
            'Deleg', 'Centreg', 'Gouv', 'Id_agent'
        ]
        
        # Load sample data
        print("📊 Loading sample with proper column names...")
        sample_data = pd.read_csv(
            'tab_paie_13_23.cleaned.txt', 
            sep=';', 
            encoding='utf-8',
            names=main_columns,
            nrows=1000
        )
        
        print(f"✅ Data loaded successfully!")
        print(f"Shape: {sample_data.shape}")
        
        # Clean data types
        print("🔄 Converting data types...")
        sample_data['Annee'] = pd.to_numeric(sample_data['Annee'], errors='coerce')
        sample_data['Mois'] = pd.to_numeric(sample_data['Mois'], errors='coerce')
        sample_data['Montind'] = pd.to_numeric(sample_data['Montind'], errors='coerce')
        
        # Filter valid years
        valid_data = sample_data[
            (sample_data['Annee'] >= 2013) & 
            (sample_data['Annee'] <= 2023) &
            (sample_data['Mois'] >= 1) & 
            (sample_data['Mois'] <= 12)
        ]
        
        print(f"✅ Valid data: {len(valid_data)} rows")
        print(f"Year range: {valid_data['Annee'].min()} - {valid_data['Annee'].max()}")
        print(f"Month range: {valid_data['Mois'].min()} - {valid_data['Mois'].max()}")
        
        # Test date creation with fixed method
        print("🔄 Testing date creation...")
        try:
            # Method 1: Simple date string
            valid_data['Date_str'] = valid_data['Annee'].astype(str) + '-' + valid_data['Mois'].astype(str).str.zfill(2)
            print(f"✅ Date string created: {valid_data['Date_str'].head().tolist()}")
            
            # Method 2: Proper datetime with day=1
            valid_data_copy = valid_data.copy()
            valid_data_copy['day'] = 1
            valid_data_copy['Date'] = pd.to_datetime(valid_data_copy[['Annee', 'Mois', 'day']], errors='coerce')
            print(f"✅ DateTime created: {valid_data_copy['Date'].head().tolist()}")
            
        except Exception as e:
            print(f"⚠️ Date creation warning: {e}")
        
        # Basic statistics
        print(f"\n📊 BASIC STATISTICS:")
        print(f"Unique agents: {valid_data['Id_agent'].nunique()}")
        print(f"Unique establishments: {valid_data['Codetab'].nunique()}")
        print(f"Total amount: {valid_data['Montind'].sum():,.0f}")
        print(f"Average amount: {valid_data['Montind'].mean():.2f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in fixed loader test: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function."""
    print("🇹🇳 DATA STRUCTURE ANALYSIS TEST")
    print("=" * 60)
    
    # Test 1: Analyze data structure
    if analyze_data_structure():
        print("✅ Data structure analysis completed!")
    else:
        print("❌ Data structure analysis failed!")
        return
    
    # Test 2: Test fixed loader
    if test_fixed_loader():
        print("✅ Fixed loader test completed!")
    else:
        print("❌ Fixed loader test failed!")
        return
    
    print("\n" + "=" * 60)
    print("🎉 ALL TESTS COMPLETED!")
    print("The data structure is now understood and the loader should work.")
    print("=" * 60)

if __name__ == "__main__":
    main()
