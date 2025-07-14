"""
Comprehensive Salary Analysis and Prediction System for Tunisian Government Departments
================================================================================

This module provides a complete framework for analyzing salary data from 2013-2023
and predicting trends for 2025-2030 for Tunisian government departments.

Author: AI Assistant
Date: July 2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.seasonal import seasonal_decompose
import warnings
import json
from pathlib import Path
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.offline as pyo

warnings.filterwarnings('ignore')

# Set plotting style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class SalaryAnalyzer:
    """
    Main class for salary analysis and prediction system.
    
    This class handles data loading, cleaning, analysis, and prediction
    for Tunisian government salary data from 2013-2023 with forecasts to 2030.
    """
    
    def __init__(self, data_directory=".", encoding='utf-8'):
        """
        Initialize the SalaryAnalyzer with data directory path.
        
        Args:
            data_directory (str): Path to directory containing data files
            encoding (str): File encoding to use for reading data
        """
        self.data_dir = Path(data_directory)
        self.encoding = encoding
        
        # Data containers
        self.main_data = None
        self.nomenclature_tables = {}
        self.merged_data = None
        
        # Analysis results
        self.staff_evolution = None
        self.salary_mass_evolution = None
        self.allowance_analysis = None
        self.prediction_results = {}
        
        # File mappings
        self.data_files = {
            'main': 'tab_paie_13_23.cleaned.txt',
            'grade': 'table_grade.cleaned.txt',
            'corps': 'table_corps.cleaned.txt',
            'establishment': 'table_etablissement.cleaned.txt',
            'category': 'table_categorie.cleaned.txt',
            'nature': 'table_nature.cleaned.txt',
            'indemnite': 'table_indemnite.cleaned.txt',
            'organigramme': 'table_organigramme_5_ministeres.cleaned.txt'
        }
        
        print("SalaryAnalyzer initialized successfully!")
        print(f"Data directory: {self.data_dir}")
        
    def load_and_clean_data(self):
        """
        Load all data files and perform initial cleaning.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            print("Loading data files...")
            
            # Load nomenclature tables first (smaller files)
            for table_name, filename in self.data_files.items():
                if table_name == 'main':
                    continue
                    
                file_path = self.data_dir / filename
                if file_path.exists():
                    print(f"Loading {table_name} table...")
                    
                    # Detect separator and load accordingly
                    if table_name in ['grade', 'corps']:
                        self.nomenclature_tables[table_name] = pd.read_csv(
                            file_path, 
                            sep=';', 
                            encoding=self.encoding,
                            header=None
                        )
                    else:
                        self.nomenclature_tables[table_name] = pd.read_csv(
                            file_path, 
                            sep=';', 
                            encoding=self.encoding
                        )
                else:
                    print(f"Warning: {filename} not found")
            
            # Load main payroll data
            main_file = self.data_dir / self.data_files['main']
            if main_file.exists():
                print("Loading main payroll data (this may take a while)...")
                
                # Try to load main data with proper column names
                main_columns = [
                    'Codetab', 'Mois', 'Annee', 'Type', 'Nligne', 'Codind', 
                    'Montind', 'Article', 'Par', 'Codgrd', 'Codcorps', 'Hcorps',
                    'Codefam', 'Codsfam', 'Codnat', 'Dire', 'Sdir', 'Serv',
                    'Deleg', 'Centreg', 'Gouv', 'Id_agent'
                ]
                
                # Load in chunks to handle large file
                chunk_list = []
                chunk_size = 10000
                
                for chunk in pd.read_csv(main_file, sep=';', encoding=self.encoding, 
                                       names=main_columns, chunksize=chunk_size):
                    chunk_list.append(chunk)
                
                self.main_data = pd.concat(chunk_list, ignore_index=True)
                print(f"Main data loaded: {len(self.main_data)} records")
                
            else:
                print(f"Error: Main data file {self.data_files['main']} not found")
                return False
            
            # Clean and prepare data
            self._clean_main_data()
            self._prepare_nomenclature_tables()
            
            print("Data loading completed successfully!")
            return True
            
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
    
    def _clean_main_data(self):
        """Clean and prepare the main payroll data."""
        print("Cleaning main data...")
        
        # Convert data types
        self.main_data['Annee'] = pd.to_numeric(self.main_data['Annee'], errors='coerce')
        self.main_data['Mois'] = pd.to_numeric(self.main_data['Mois'], errors='coerce')
        self.main_data['Montind'] = pd.to_numeric(self.main_data['Montind'], errors='coerce')
        self.main_data['Type'] = pd.to_numeric(self.main_data['Type'], errors='coerce')
        
        # Filter valid years (2013-2023)
        self.main_data = self.main_data[
            (self.main_data['Annee'] >= 2013) & 
            (self.main_data['Annee'] <= 2023)
        ]
        
        # Remove rows with missing critical data
        critical_columns = ['Annee', 'Mois', 'Montind', 'Id_agent', 'Codetab']
        self.main_data = self.main_data.dropna(subset=critical_columns)
        
        # Create date column with proper error handling
        try:
            # Create a temporary DataFrame with year, month, day columns
            date_df = pd.DataFrame({
                'year': self.main_data['Annee'],
                'month': self.main_data['Mois'],
                'day': 1
            })
            self.main_data['Date'] = pd.to_datetime(date_df, errors='coerce')
        except Exception as e:
            print(f"Warning: Could not create datetime column: {e}")
            # Create a simple date string instead
            self.main_data['Date'] = self.main_data['Annee'].astype(str) + '-' + self.main_data['Mois'].astype(str).str.zfill(2) + '-01'
        
        print(f"Main data cleaned: {len(self.main_data)} records remaining")
    
    def _prepare_nomenclature_tables(self):
        """Prepare nomenclature tables with proper column names."""
        print("Preparing nomenclature tables...")
        
        # Grade table
        if 'grade' in self.nomenclature_tables:
            self.nomenclature_tables['grade'].columns = [
                'Codgrd', 'Code2', 'Level', 'Grade_Name_FR', 'Grade_Name_AR', 'Ministry'
            ]
        
        # Corps table
        if 'corps' in self.nomenclature_tables:
            self.nomenclature_tables['corps'].columns = [
                'Codcorps', 'Corps_Name_FR', 'Corps_Name_AR'
            ]
        
        # Establishment table
        if 'establishment' in self.nomenclature_tables:
            self.nomenclature_tables['establishment'].columns = [
                'Codetab', 'Establishment_Name_FR', 'Establishment_Name_AR', 'Type'
            ]
        
        print("Nomenclature tables prepared successfully!")
    
    def merge_data_with_nomenclature(self):
        """Merge main data with nomenclature tables for enriched analysis."""
        print("Merging data with nomenclature tables...")
        
        self.merged_data = self.main_data.copy()
        
        # Merge with grade table
        if 'grade' in self.nomenclature_tables:
            self.merged_data = pd.merge(
                self.merged_data,
                self.nomenclature_tables['grade'][['Codgrd', 'Grade_Name_FR', 'Level', 'Ministry']],
                on='Codgrd',
                how='left'
            )
        
        # Merge with corps table
        if 'corps' in self.nomenclature_tables:
            self.merged_data = pd.merge(
                self.merged_data,
                self.nomenclature_tables['corps'][['Codcorps', 'Corps_Name_FR']],
                on='Codcorps',
                how='left'
            )
        
        # Merge with establishment table
        if 'establishment' in self.nomenclature_tables:
            self.merged_data = pd.merge(
                self.merged_data,
                self.nomenclature_tables['establishment'][['Codetab', 'Establishment_Name_FR']],
                on='Codetab',
                how='left'
            )
        
        print(f"Data merged successfully: {len(self.merged_data)} records")
        return self.merged_data
    
    def calculate_staff_evolution(self):
        """
        Calculate staff evolution over time by department, corps, and grade.
        
        Returns:
            dict: Dictionary containing staff evolution data
        """
        print("Calculating staff evolution...")
        
        if self.merged_data is None:
            self.merge_data_with_nomenclature()
        
        # Calculate unique staff count by year
        staff_by_year = self.merged_data.groupby('Annee')['Id_agent'].nunique().reset_index()
        staff_by_year.columns = ['Year', 'Staff_Count']
        
        # Calculate staff by ministry and year
        staff_by_ministry = self.merged_data.groupby(['Annee', 'Ministry'])['Id_agent'].nunique().reset_index()
        staff_by_ministry.columns = ['Year', 'Ministry', 'Staff_Count']
        
        # Calculate staff by corps and year
        staff_by_corps = self.merged_data.groupby(['Annee', 'Corps_Name_FR'])['Id_agent'].nunique().reset_index()
        staff_by_corps.columns = ['Year', 'Corps', 'Staff_Count']
        
        # Calculate staff by grade and year
        staff_by_grade = self.merged_data.groupby(['Annee', 'Grade_Name_FR'])['Id_agent'].nunique().reset_index()
        staff_by_grade.columns = ['Year', 'Grade', 'Staff_Count']
        
        self.staff_evolution = {
            'total': staff_by_year,
            'by_ministry': staff_by_ministry,
            'by_corps': staff_by_corps,
            'by_grade': staff_by_grade
        }
        
        print("Staff evolution calculation completed!")
        return self.staff_evolution
    
    def calculate_salary_mass(self):
        """
        Calculate salary mass evolution over time.
        
        Returns:
            dict: Dictionary containing salary mass data
        """
        print("Calculating salary mass evolution...")
        
        if self.merged_data is None:
            self.merge_data_with_nomenclature()
        
        # Calculate total salary mass by year
        salary_mass_total = self.merged_data.groupby('Annee')['Montind'].sum().reset_index()
        salary_mass_total.columns = ['Year', 'Total_Salary_Mass']
        
        # Calculate salary mass by ministry
        salary_mass_ministry = self.merged_data.groupby(['Annee', 'Ministry'])['Montind'].sum().reset_index()
        salary_mass_ministry.columns = ['Year', 'Ministry', 'Salary_Mass']
        
        # Calculate salary mass by corps
        salary_mass_corps = self.merged_data.groupby(['Annee', 'Corps_Name_FR'])['Montind'].sum().reset_index()
        salary_mass_corps.columns = ['Year', 'Corps', 'Salary_Mass']
        
        # Calculate average salary per agent
        avg_salary_per_agent = self.merged_data.groupby(['Annee', 'Id_agent'])['Montind'].sum().reset_index()
        avg_salary_yearly = avg_salary_per_agent.groupby('Annee')['Montind'].mean().reset_index()
        avg_salary_yearly.columns = ['Year', 'Average_Salary_Per_Agent']
        
        self.salary_mass_evolution = {
            'total': salary_mass_total,
            'by_ministry': salary_mass_ministry,
            'by_corps': salary_mass_corps,
            'average_per_agent': avg_salary_yearly
        }
        
        print("Salary mass calculation completed!")
        return self.salary_mass_evolution
    
    def analyze_allowances(self):
        """
        Analyze allowance evolution by type, department, corps, and grade.
        
        Returns:
            dict: Dictionary containing allowance analysis
        """
        print("Analyzing allowance evolution...")
        
        if self.merged_data is None:
            self.merge_data_with_nomenclature()
        
        # Allowance amounts by year and type
        allowance_by_type = self.merged_data.groupby(['Annee', 'Type'])['Montind'].agg(['sum', 'mean', 'count']).reset_index()
        allowance_by_type.columns = ['Year', 'Type', 'Total_Amount', 'Average_Amount', 'Count']
        
        # Allowance by ministry, corps, and grade
        allowance_detailed = self.merged_data.groupby([
            'Annee', 'Ministry', 'Corps_Name_FR', 'Grade_Name_FR'
        ])['Montind'].agg(['sum', 'mean', 'count']).reset_index()
        allowance_detailed.columns = ['Year', 'Ministry', 'Corps', 'Grade', 'Total_Amount', 'Average_Amount', 'Count']
        
        # Number of allowances per agent by year
        allowances_per_agent = self.merged_data.groupby(['Annee', 'Id_agent']).size().reset_index(name='Allowance_Count')
        avg_allowances_per_agent = allowances_per_agent.groupby('Annee')['Allowance_Count'].mean().reset_index()
        avg_allowances_per_agent.columns = ['Year', 'Average_Allowances_Per_Agent']
        
        self.allowance_analysis = {
            'by_type': allowance_by_type,
            'detailed': allowance_detailed,
            'per_agent': avg_allowances_per_agent
        }
        
        print("Allowance analysis completed!")
        return self.allowance_analysis
        
    def predict_future_trends(self, target_years=[2025, 2026, 2027, 2028, 2029, 2030]):
        """
        Predict future trends using multiple forecasting methods.
        
        Args:
            target_years (list): Years to predict for
            
        Returns:
            dict: Dictionary containing prediction results
        """
        print(f"Predicting trends for years: {target_years}")
        
        if self.staff_evolution is None:
            self.calculate_staff_evolution()
        
        if self.salary_mass_evolution is None:
            self.calculate_salary_mass()
        
        predictions = {}
        
        # Predict staff evolution
        predictions['staff'] = self._predict_time_series(
            self.staff_evolution['total'], 'Staff_Count', target_years
        )
        
        # Predict salary mass
        predictions['salary_mass'] = self._predict_time_series(
            self.salary_mass_evolution['total'], 'Total_Salary_Mass', target_years
        )
        
        # Predict average salary per agent
        predictions['avg_salary'] = self._predict_time_series(
            self.salary_mass_evolution['average_per_agent'], 'Average_Salary_Per_Agent', target_years
        )
        
        # Predict by ministry
        predictions['by_ministry'] = {}
        for ministry in self.staff_evolution['by_ministry']['Ministry'].unique():
            if pd.notna(ministry):
                ministry_data = self.staff_evolution['by_ministry'][
                    self.staff_evolution['by_ministry']['Ministry'] == ministry
                ]
                predictions['by_ministry'][ministry] = self._predict_time_series(
                    ministry_data, 'Staff_Count', target_years
                )
        
        self.prediction_results = predictions
        print("Future trend predictions completed!")
        return predictions
    
    def _predict_time_series(self, data, value_column, target_years):
        """
        Predict time series using multiple methods and return best result.
        
        Args:
            data (DataFrame): Historical data
            value_column (str): Column name containing values to predict
            target_years (list): Years to predict
            
        Returns:
            dict: Prediction results with confidence intervals
        """
        try:
            # Prepare data
            X = data['Year'].values.reshape(-1, 1)
            y = data[value_column].values
            
            # Method 1: Linear Regression
            lr_model = LinearRegression()
            lr_model.fit(X, y)
            lr_predictions = lr_model.predict(np.array(target_years).reshape(-1, 1))
            lr_score = lr_model.score(X, y)
            
            # Method 2: Random Forest
            rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
            rf_model.fit(X, y)
            rf_predictions = rf_model.predict(np.array(target_years).reshape(-1, 1))
            rf_score = rf_model.score(X, y)
            
            # Method 3: ARIMA (if enough data points)
            arima_predictions = None
            arima_score = 0
            
            if len(data) >= 8:  # Need enough data for ARIMA
                try:
                    # Create time series
                    ts_data = pd.Series(y, index=pd.to_datetime(data['Year'], format='%Y'))
                    
                    # Fit ARIMA model
                    arima_model = ARIMA(ts_data, order=(1, 1, 1))
                    arima_fitted = arima_model.fit()
                    
                    # Forecast
                    n_periods = len(target_years)
                    arima_forecast = arima_fitted.forecast(steps=n_periods)
                    arima_predictions = arima_forecast.values
                    arima_score = 1 - (arima_fitted.aic / 1000)  # Normalized AIC score
                    
                except:
                    arima_predictions = None
                    arima_score = 0
            
            # Choose best method based on score
            methods = {
                'Linear Regression': (lr_predictions, lr_score),
                'Random Forest': (rf_predictions, rf_score),
                'ARIMA': (arima_predictions, arima_score) if arima_predictions is not None else (None, 0)
            }
            
            best_method = max(methods.items(), key=lambda x: x[1][1] if x[1][0] is not None else -1)
            best_predictions = best_method[1][0]
            best_score = best_method[1][1]
            
            # Calculate confidence intervals (simple approach)
            historical_std = np.std(y)
            confidence_lower = best_predictions - 1.96 * historical_std
            confidence_upper = best_predictions + 1.96 * historical_std
            
            return {
                'years': target_years,
                'predictions': best_predictions.tolist() if best_predictions is not None else [],
                'confidence_lower': confidence_lower.tolist() if best_predictions is not None else [],
                'confidence_upper': confidence_upper.tolist() if best_predictions is not None else [],
                'method': best_method[0],
                'score': best_score,
                'all_methods': {name: pred[0].tolist() if pred[0] is not None else [] 
                               for name, pred in methods.items()}
            }
            
        except Exception as e:
            print(f"Error in time series prediction: {e}")
            return {
                'years': target_years,
                'predictions': [],
                'confidence_lower': [],
                'confidence_upper': [],
                'method': 'None',
                'score': 0,
                'all_methods': {}
            }
    
    def generate_allowance_report(self):
        """
        Generate detailed allowance analysis report in the required format.
        
        Returns:
            dict: Structured allowance report
        """
        print("Generating allowance report...")
        
        if self.allowance_analysis is None:
            self.analyze_allowances()
        
        # Predict allowance trends
        allowance_predictions = self._predict_allowance_trends()
        
        # Structure the report as requested
        report = {}
        
        # Group by Ministry -> Corps -> Grade
        detailed_data = self.allowance_analysis['detailed']
        
        for ministry in detailed_data['Ministry'].unique():
            if pd.notna(ministry):
                report[ministry] = {}
                ministry_data = detailed_data[detailed_data['Ministry'] == ministry]
                
                for corps in ministry_data['Corps'].unique():
                    if pd.notna(corps):
                        report[ministry][corps] = {}
                        corps_data = ministry_data[ministry_data['Corps'] == corps]
                        
                        for grade in corps_data['Grade'].unique():
                            if pd.notna(grade):
                                grade_data = corps_data[corps_data['Grade'] == grade]
                                
                                # Historical data
                                historical = {}
                                for _, row in grade_data.iterrows():
                                    year = int(row['Year'])
                                    historical[year] = {
                                        'total_amount': row['Total_Amount'],
                                        'average_amount': row['Average_Amount'],
                                        'count': row['Count']
                                    }
                                
                                # Add predictions if available
                                predicted = self._get_grade_predictions(ministry, corps, grade, allowance_predictions)
                                
                                report[ministry][corps][grade] = {
                                    'historical': historical,
                                    'predictions': predicted
                                }
        
        print("Allowance report generated successfully!")
        return report
    
    def _predict_allowance_trends(self):
        """Predict allowance trends for future years."""
        predictions = {}
        
        if self.allowance_analysis is None:
            return predictions
        
        detailed_data = self.allowance_analysis['detailed']
        target_years = [2025, 2026, 2027, 2028, 2029, 2030]
        
        # Group predictions by ministry, corps, grade
        for (ministry, corps, grade), group in detailed_data.groupby(['Ministry', 'Corps', 'Grade']):
            if len(group) >= 3:  # Need enough data points
                key = f"{ministry}_{corps}_{grade}"
                
                # Predict total amount
                amount_pred = self._predict_time_series(group, 'Total_Amount', target_years)
                
                # Predict count
                count_pred = self._predict_time_series(group, 'Count', target_years)
                
                predictions[key] = {
                    'amount': amount_pred,
                    'count': count_pred
                }
        
        return predictions
    
    def _get_grade_predictions(self, ministry, corps, grade, allowance_predictions):
        """Get predictions for a specific grade."""
        key = f"{ministry}_{corps}_{grade}"
        
        if key in allowance_predictions:
            pred_data = allowance_predictions[key]
            predictions = {}
            
            for i, year in enumerate(pred_data['amount']['years']):
                predictions[year] = {
                    'predicted_amount': pred_data['amount']['predictions'][i] if i < len(pred_data['amount']['predictions']) else 0,
                    'predicted_count': pred_data['count']['predictions'][i] if i < len(pred_data['count']['predictions']) else 0,
                    'amount_confidence_lower': pred_data['amount']['confidence_lower'][i] if i < len(pred_data['amount']['confidence_lower']) else 0,
                    'amount_confidence_upper': pred_data['amount']['confidence_upper'][i] if i < len(pred_data['amount']['confidence_upper']) else 0
                }
            
            return predictions
        
        return {}
    
    def create_visualizations(self):
        """
        Create comprehensive visualizations for the analysis.
        
        Returns:
            dict: Dictionary containing all visualization figures
        """
        print("Creating visualizations...")
        
        figures = {}
        
        # 1. Staff Evolution Over Time
        if self.staff_evolution is not None:
            figures['staff_evolution'] = self._create_staff_evolution_plot()
        
        # 2. Salary Mass Evolution
        if self.salary_mass_evolution is not None:
            figures['salary_mass_evolution'] = self._create_salary_mass_plot()
        
        # 3. Predictions Visualization
        if self.prediction_results:
            figures['predictions'] = self._create_predictions_plot()
        
        # 4. Ministry Comparison
        figures['ministry_comparison'] = self._create_ministry_comparison_plot()
        
        # 5. Allowance Analysis
        if self.allowance_analysis is not None:
            figures['allowance_analysis'] = self._create_allowance_plot()
        
        print("Visualizations created successfully!")
        return figures
    
    def _create_staff_evolution_plot(self):
        """Create staff evolution visualization."""
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Staff Evolution Analysis (2013-2023)', fontsize=16, fontweight='bold')
        
        # Total staff evolution
        total_data = self.staff_evolution['total']
        axes[0, 0].plot(total_data['Year'], total_data['Staff_Count'], marker='o', linewidth=2)
        axes[0, 0].set_title('Total Staff Evolution')
        axes[0, 0].set_xlabel('Year')
        axes[0, 0].set_ylabel('Number of Staff')
        axes[0, 0].grid(True, alpha=0.3)
        
        # Staff by ministry
        ministry_data = self.staff_evolution['by_ministry']
        for ministry in ministry_data['Ministry'].unique():
            if pd.notna(ministry):
                m_data = ministry_data[ministry_data['Ministry'] == ministry]
                axes[0, 1].plot(m_data['Year'], m_data['Staff_Count'], marker='o', label=str(ministry)[:20])
        
        axes[0, 1].set_title('Staff Evolution by Ministry')
        axes[0, 1].set_xlabel('Year')
        axes[0, 1].set_ylabel('Number of Staff')
        axes[0, 1].legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        axes[0, 1].grid(True, alpha=0.3)
        
        # Top 10 corps by staff count
        corps_data = self.staff_evolution['by_corps']
        top_corps = corps_data.groupby('Corps')['Staff_Count'].sum().nlargest(10).index
        
        for corps in top_corps:
            if pd.notna(corps):
                c_data = corps_data[corps_data['Corps'] == corps]
                axes[1, 0].plot(c_data['Year'], c_data['Staff_Count'], marker='o', label=str(corps)[:15])
        
        axes[1, 0].set_title('Top 10 Corps - Staff Evolution')
        axes[1, 0].set_xlabel('Year')
        axes[1, 0].set_ylabel('Number of Staff')
        axes[1, 0].legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        axes[1, 0].grid(True, alpha=0.3)
        
        # Staff distribution by year (box plot)
        yearly_data = []
        years = []
        for year in sorted(total_data['Year'].unique()):
            year_corps_data = corps_data[corps_data['Year'] == year]['Staff_Count']
            yearly_data.append(year_corps_data.values)
            years.append(str(year))
        
        axes[1, 1].boxplot(yearly_data, labels=years)
        axes[1, 1].set_title('Staff Distribution by Corps (Box Plot)')
        axes[1, 1].set_xlabel('Year')
        axes[1, 1].set_ylabel('Staff Count per Corps')
        axes[1, 1].tick_params(axis='x', rotation=45)
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def _create_salary_mass_plot(self):
        """Create salary mass evolution visualization."""
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Salary Mass Evolution Analysis (2013-2023)', fontsize=16, fontweight='bold')
        
        # Total salary mass
        total_data = self.salary_mass_evolution['total']
        axes[0, 0].plot(total_data['Year'], total_data['Total_Salary_Mass'] / 1e6, marker='o', linewidth=2)
        axes[0, 0].set_title('Total Salary Mass Evolution')
        axes[0, 0].set_xlabel('Year')
        axes[0, 0].set_ylabel('Total Salary Mass (Millions)')
        axes[0, 0].grid(True, alpha=0.3)
        
        # Average salary per agent
        avg_data = self.salary_mass_evolution['average_per_agent']
        axes[0, 1].plot(avg_data['Year'], avg_data['Average_Salary_Per_Agent'], marker='o', linewidth=2, color='green')
        axes[0, 1].set_title('Average Salary per Agent')
        axes[0, 1].set_xlabel('Year')
        axes[0, 1].set_ylabel('Average Salary')
        axes[0, 1].grid(True, alpha=0.3)
        
        # Salary mass by ministry
        ministry_data = self.salary_mass_evolution['by_ministry']
        for ministry in ministry_data['Ministry'].unique():
            if pd.notna(ministry):
                m_data = ministry_data[ministry_data['Ministry'] == ministry]
                axes[1, 0].plot(m_data['Year'], m_data['Salary_Mass'] / 1e6, marker='o', label=str(ministry)[:20])
        
        axes[1, 0].set_title('Salary Mass by Ministry')
        axes[1, 0].set_xlabel('Year')
        axes[1, 0].set_ylabel('Salary Mass (Millions)')
        axes[1, 0].legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        axes[1, 0].grid(True, alpha=0.3)
        
        # Growth rate analysis
        total_data_sorted = total_data.sort_values('Year')
        growth_rates = total_data_sorted['Total_Salary_Mass'].pct_change() * 100
        axes[1, 1].bar(total_data_sorted['Year'][1:], growth_rates[1:], alpha=0.7, color='coral')
        axes[1, 1].set_title('Annual Salary Mass Growth Rate')
        axes[1, 1].set_xlabel('Year')
        axes[1, 1].set_ylabel('Growth Rate (%)')
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def _create_predictions_plot(self):
        """Create predictions visualization with confidence intervals."""
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Future Predictions (2025-2030)', fontsize=16, fontweight='bold')
        
        # Staff predictions
        if 'staff' in self.prediction_results:
            pred_data = self.prediction_results['staff']
            historical_staff = self.staff_evolution['total']
            
            # Plot historical data
            axes[0, 0].plot(historical_staff['Year'], historical_staff['Staff_Count'], 
                          marker='o', linewidth=2, label='Historical', color='blue')
            
            # Plot predictions with confidence intervals
            if pred_data['predictions']:
                axes[0, 0].plot(pred_data['years'], pred_data['predictions'], 
                              marker='s', linewidth=2, label='Predicted', color='red', linestyle='--')
                axes[0, 0].fill_between(pred_data['years'], pred_data['confidence_lower'], 
                                      pred_data['confidence_upper'], alpha=0.3, color='red')
            
            axes[0, 0].set_title('Staff Count Predictions')
            axes[0, 0].set_xlabel('Year')
            axes[0, 0].set_ylabel('Number of Staff')
            axes[0, 0].legend()
            axes[0, 0].grid(True, alpha=0.3)
        
        # Salary mass predictions
        if 'salary_mass' in self.prediction_results:
            pred_data = self.prediction_results['salary_mass']
            historical_salary = self.salary_mass_evolution['total']
            
            axes[0, 1].plot(historical_salary['Year'], historical_salary['Total_Salary_Mass'] / 1e6, 
                          marker='o', linewidth=2, label='Historical', color='blue')
            
            if pred_data['predictions']:
                axes[0, 1].plot(pred_data['years'], [p/1e6 for p in pred_data['predictions']], 
                              marker='s', linewidth=2, label='Predicted', color='red', linestyle='--')
                axes[0, 1].fill_between(pred_data['years'], 
                                      [p/1e6 for p in pred_data['confidence_lower']], 
                                      [p/1e6 for p in pred_data['confidence_upper']], 
                                      alpha=0.3, color='red')
            
            axes[0, 1].set_title('Salary Mass Predictions')
            axes[0, 1].set_xlabel('Year')
            axes[0, 1].set_ylabel('Salary Mass (Millions)')
            axes[0, 1].legend()
            axes[0, 1].grid(True, alpha=0.3)
        
        # Average salary predictions
        if 'avg_salary' in self.prediction_results:
            pred_data = self.prediction_results['avg_salary']
            historical_avg = self.salary_mass_evolution['average_per_agent']
            
            axes[1, 0].plot(historical_avg['Year'], historical_avg['Average_Salary_Per_Agent'], 
                          marker='o', linewidth=2, label='Historical', color='blue')
            
            if pred_data['predictions']:
                axes[1, 0].plot(pred_data['years'], pred_data['predictions'], 
                              marker='s', linewidth=2, label='Predicted', color='red', linestyle='--')
                axes[1, 0].fill_between(pred_data['years'], pred_data['confidence_lower'], 
                                      pred_data['confidence_upper'], alpha=0.3, color='red')
            
            axes[1, 0].set_title('Average Salary per Agent Predictions')
            axes[1, 0].set_xlabel('Year')
            axes[1, 0].set_ylabel('Average Salary')
            axes[1, 0].legend()
            axes[1, 0].grid(True, alpha=0.3)
        
        # Prediction accuracy comparison
        methods_accuracy = {}
        for metric in ['staff', 'salary_mass', 'avg_salary']:
            if metric in self.prediction_results and 'score' in self.prediction_results[metric]:
                methods_accuracy[metric] = self.prediction_results[metric]['score']
        
        if methods_accuracy:
            metrics = list(methods_accuracy.keys())
            scores = list(methods_accuracy.values())
            axes[1, 1].bar(metrics, scores, alpha=0.7, color='green')
            axes[1, 1].set_title('Prediction Model Accuracy')
            axes[1, 1].set_xlabel('Metric')
            axes[1, 1].set_ylabel('R² Score')
            axes[1, 1].tick_params(axis='x', rotation=45)
            axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def _create_ministry_comparison_plot(self):
        """Create ministry comparison visualization."""
        if self.staff_evolution is None or self.salary_mass_evolution is None:
            return None
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Ministry Comparison Analysis', fontsize=16, fontweight='bold')
        
        # Ministry staff comparison (latest year)
        latest_year = self.staff_evolution['by_ministry']['Year'].max()
        latest_ministry_staff = self.staff_evolution['by_ministry'](
            self.staff_evolution['by_ministry']['Year'] == latest_year
        )
        
        ministries = latest_ministry_staff['Ministry'].fillna('Unknown')
        staff_counts = latest_ministry_staff['Staff_Count']
        
        axes[0, 0].barh(ministries, staff_counts, alpha=0.7)
        axes[0, 0].set_title(f'Staff Count by Ministry ({latest_year})')
        axes[0, 0].set_xlabel('Number of Staff')
        axes[0, 0].grid(True, alpha=0.3)
        
        # Ministry salary mass comparison
        latest_ministry_salary = self.salary_mass_evolution['by_ministry'](
            self.salary_mass_evolution['by_ministry']['Year'] == latest_year
        )
        
        salary_masses = latest_ministry_salary['Salary_Mass'] / 1e6
        axes[0, 1].barh(ministries, salary_masses, alpha=0.7, color='orange')
        axes[0, 1].set_title(f'Salary Mass by Ministry ({latest_year})')
        axes[0, 1].set_xlabel('Salary Mass (Millions)')
        axes[0, 1].grid(True, alpha=0.3)
        
        # Growth rate by ministry
        ministry_growth = {}
        for ministry in self.staff_evolution['by_ministry']['Ministry'].unique():
            if pd.notna(ministry):
                m_data = self.staff_evolution['by_ministry'](
                    self.staff_evolution['by_ministry']['Ministry'] == ministry
                ).sort_values('Year')
                
                if len(m_data) > 1:
                    first_year = m_data.iloc[0]['Staff_Count']
                    last_year = m_data.iloc[-1]['Staff_Count']
                    growth_rate = ((last_year - first_year) / first_year) * 100
                    ministry_growth[ministry] = growth_rate
        
        if ministry_growth:
            ministries_growth = list(ministry_growth.keys())
            growth_rates = list(ministry_growth.values())
            colors = ['green' if rate >= 0 else 'red' for rate in growth_rates]
            
            axes[1, 0].barh(ministries_growth, growth_rates, alpha=0.7, color=colors)
            axes[1, 0].set_title('Staff Growth Rate by Ministry (2013-2023)')
            axes[1, 0].set_xlabel('Growth Rate (%)')
            axes[1, 0].axvline(x=0, color='black', linestyle='-', alpha=0.3)
            axes[1, 0].grid(True, alpha=0.3)
        
        # Average salary per ministry
        ministry_avg_salary = {}
        for ministry in latest_ministry_staff['Ministry'].unique():
            if pd.notna(ministry):
                m_staff = latest_ministry_staff[latest_ministry_staff['Ministry'] == ministry]['Staff_Count'].iloc[0]
                m_salary = latest_ministry_salary[latest_ministry_salary['Ministry'] == ministry]['Salary_Mass'].iloc[0]
                if m_staff > 0:
                    ministry_avg_salary[ministry] = m_salary / m_staff
        
        if ministry_avg_salary:
            ministries_avg = list(ministry_avg_salary.keys())
            avg_salaries = list(ministry_avg_salary.values())
            
            axes[1, 1].barh(ministries_avg, avg_salaries, alpha=0.7, color='purple')
            axes[1, 1].set_title(f'Average Salary per Agent by Ministry ({latest_year})')
            axes[1, 1].set_xlabel('Average Salary')
            axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def _create_allowance_plot(self):
        """Create allowance analysis visualization."""
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Allowance Analysis', fontsize=16, fontweight='bold')
        
        # Allowance by type over time
        type_data = self.allowance_analysis['by_type']
        for allowance_type in type_data['Type'].unique():
            if pd.notna(allowance_type):
                t_data = type_data[type_data['Type'] == allowance_type]
                axes[0, 0].plot(t_data['Year'], t_data['Total_Amount'] / 1e6, 
                              marker='o', label=f'Type {allowance_type}')
        
        axes[0, 0].set_title('Total Allowance Amount by Type')
        axes[0, 0].set_xlabel('Year')
        axes[0, 0].set_ylabel('Amount (Millions)')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # Average allowances per agent
        avg_allowances = self.allowance_analysis['per_agent']
        axes[0, 1].plot(avg_allowances['Year'], avg_allowances['Average_Allowances_Per_Agent'], 
                       marker='o', linewidth=2, color='green')
        axes[0, 1].set_title('Average Allowances per Agent')
        axes[0, 1].set_xlabel('Year')
        axes[0, 1].set_ylabel('Number of Allowances')
        axes[0, 1].grid(True, alpha=0.3)
        
        # Distribution of allowance amounts (latest year)
        latest_year = type_data['Year'].max()
        latest_amounts = type_data[type_data['Year'] == latest_year]['Average_Amount']
        
        axes[1, 0].hist(latest_amounts, bins=20, alpha=0.7, color='skyblue', edgecolor='black')
        axes[1, 0].set_title(f'Distribution of Average Allowance Amounts ({latest_year})')
        axes[1, 0].set_xlabel('Average Amount')
        axes[1, 0].set_ylabel('Frequency')
        axes[1, 0].grid(True, alpha=0.3)
        
        # Allowance count by type
        latest_counts = type_data[type_data['Year'] == latest_year]
        axes[1, 1].pie(latest_counts['Count'], labels=[f'Type {t}' for t in latest_counts['Type']], 
                      autopct='%1.1f%%', startangle=90)
        axes[1, 1].set_title(f'Allowance Count Distribution by Type ({latest_year})')
        
        plt.tight_layout()
        return fig
    
    def generate_final_report(self, output_file='salary_analysis_report.json'):
        """
        Generate comprehensive final report with all analysis results.
        
        Args:
            output_file (str): Output file name for the report
            
        Returns:
            dict: Complete analysis report
        """
        print("Generating final comprehensive report...")
        
        # Ensure all analyses are completed
        if self.staff_evolution is None:
            self.calculate_staff_evolution()
        
        if self.salary_mass_evolution is None:
            self.calculate_salary_mass()
        
        if self.allowance_analysis is None:
            self.analyze_allowances()
        
        if not self.prediction_results:
            self.predict_future_trends()
        
        allowance_report = self.generate_allowance_report()
        
        # Compile final report
        final_report = {
            'metadata': {
                'generated_date': datetime.now().isoformat(),
                'data_period': '2013-2023',
                'prediction_period': '2025-2030',
                'total_records': len(self.main_data) if self.main_data is not None else 0
            },
            'executive_summary': self._generate_executive_summary(),
            'staff_evolution': {
                'historical': self.staff_evolution,
                'predictions': self.prediction_results.get('staff', {})
            },
            'salary_mass_analysis': {
                'historical': self.salary_mass_evolution,
                'predictions': self.prediction_results.get('salary_mass', {}),
                'average_salary_predictions': self.prediction_results.get('avg_salary', {})
            },
            'allowance_analysis': {
                'detailed_report': allowance_report,
                'summary': self.allowance_analysis
            },
            'ministry_predictions': self.prediction_results.get('by_ministry', {}),
            'key_findings': self._generate_key_findings(),
            'recommendations': self._generate_recommendations()
        }
        
        # Save report to file
        output_path = self.data_dir / output_file
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(final_report, f, indent=2, ensure_ascii=False, default=str)
            print(f"Report saved to: {output_path}")
        except Exception as e:
            print(f"Error saving report: {e}")
        
        print("Final report generation completed!")
        return final_report
    
    def _generate_executive_summary(self):
        """Generate executive summary of the analysis."""
        summary = {
            'total_staff_2023': 0,
            'predicted_staff_2030': 0,
            'total_salary_mass_2023': 0,
            'predicted_salary_mass_2030': 0,
            'average_annual_growth_rate': 0,
            'top_growing_ministry': 'N/A'
        }
        
        try:
            # Latest staff count
            if self.staff_evolution and 'total' in self.staff_evolution:
                latest_staff = self.staff_evolution['total'][
                    self.staff_evolution['total']['Year'] == self.staff_evolution['total']['Year'].max()
                ]
                if not latest_staff.empty:
                    summary['total_staff_2023'] = int(latest_staff.iloc[0]['Staff_Count'])
            
            # Predicted staff 2030
            if 'staff' in self.prediction_results and self.prediction_results['staff']['predictions']:
                predictions = self.prediction_results['staff']
                if 2030 in predictions['years']:
                    idx = predictions['years'].index(2030)
                    summary['predicted_staff_2030'] = int(predictions['predictions'][idx])
            
            # Latest salary mass
            if self.salary_mass_evolution and 'total' in self.salary_mass_evolution:
                latest_salary = self.salary_mass_evolution['total'][
                    self.salary_mass_evolution['total']['Year'] == self.salary_mass_evolution['total']['Year'].max()
                ]
                if not latest_salary.empty:
                    summary['total_salary_mass_2023'] = float(latest_salary.iloc[0]['Total_Salary_Mass'])
            
            # Predicted salary mass 2030
            if 'salary_mass' in self.prediction_results and self.prediction_results['salary_mass']['predictions']:
                predictions = self.prediction_results['salary_mass']
                if 2030 in predictions['years']:
                    idx = predictions['years'].index(2030)
                    summary['predicted_salary_mass_2030'] = float(predictions['predictions'][idx])
            
            # Calculate growth rate
            if summary['total_salary_mass_2023'] > 0 and summary['predicted_salary_mass_2030'] > 0:
                years_diff = 7  # 2030 - 2023
                growth_rate = ((summary['predicted_salary_mass_2030'] / summary['total_salary_mass_2023']) ** (1/years_diff) - 1) * 100
                summary['average_annual_growth_rate'] = round(growth_rate, 2)
        
        except Exception as e:
            print(f"Error generating executive summary: {e}")
        
        return summary
    
    def _generate_key_findings(self):
        """Generate key findings from the analysis."""
        findings = []
        
        try:
            # Staff evolution findings
            if self.staff_evolution:
                total_data = self.staff_evolution['total']
                if len(total_data) > 1:
                    first_year = total_data.iloc[0]
                    last_year = total_data.iloc[-1]
                    total_growth = ((last_year['Staff_Count'] - first_year['Staff_Count']) / first_year['Staff_Count']) * 100
                    
                    findings.append(f"Total staff increased by {total_growth:.1f}% from {first_year['Year']} to {last_year['Year']}")
            
            # Salary mass findings
            if self.salary_mass_evolution:
                total_salary = self.salary_mass_evolution['total']
                if len(total_salary) > 1:
                    first_year = total_salary.iloc[0]
                    last_year = total_salary.iloc[-1]
                    salary_growth = ((last_year['Total_Salary_Mass'] - first_year['Total_Salary_Mass']) / first_year['Total_Salary_Mass']) * 100
                    
                    findings.append(f"Total salary mass increased by {salary_growth:.1f}% over the analysis period")
            
            # Top ministry by staff
            if 'by_ministry' in self.staff_evolution:
                ministry_data = self.staff_evolution['by_ministry']
                latest_year = ministry_data['Year'].max()
                top_ministry = ministry_data[ministry_data['Year'] == latest_year].nlargest(1, 'Staff_Count')
                
                if not top_ministry.empty:
                    findings.append(f"Largest ministry by staff count: {top_ministry.iloc[0]['Ministry']} with {top_ministry.iloc[0]['Staff_Count']} employees")
            
            # Prediction confidence
            if self.prediction_results:
                avg_confidence = 0
                count = 0
                for metric, data in self.prediction_results.items():
                    if isinstance(data, dict) and 'score' in data:
                        avg_confidence += data['score']
                        count += 1
                
                if count > 0:
                    avg_confidence /= count
                    findings.append(f"Average prediction model confidence: {avg_confidence:.2f} (R² score)")
            
        except Exception as e:
            print(f"Error generating key findings: {e}")
            findings.append("Error occurred while generating findings")
        
        return findings
    
    def _generate_recommendations(self):
        """Generate recommendations based on the analysis."""
        recommendations = [
            "Budget Planning: Based on salary mass predictions, prepare for increased budget allocation in the coming years",
            "Workforce Management: Monitor staff growth trends to ensure optimal resource allocation",
            "Ministry-specific Strategies: Focus on high-growth ministries for capacity building and infrastructure development",
            "Regular Monitoring: Implement quarterly reviews to track actual vs predicted trends",
            "Data Quality: Maintain consistent data collection practices to improve prediction accuracy",
            "Risk Assessment: Consider economic factors that might impact salary trends beyond historical patterns"
        ]
        
        return recommendations
    
    def save_visualizations(self, output_dir='visualizations'):
        """
        Save all visualizations to files.
        
        Args:
            output_dir (str): Directory to save visualizations
        """
        output_path = self.data_dir / output_dir
        output_path.mkdir(exist_ok=True)
        
        print(f"Saving visualizations to: {output_path}")
        
        figures = self.create_visualizations()
        
        for fig_name, fig in figures.items():
            if fig is not None:
                file_path = output_path / f"{fig_name}.png"
                fig.savefig(file_path, dpi=300, bbox_inches='tight')
                plt.close(fig)
                print(f"Saved: {file_path}")
        
        print("All visualizations saved successfully!")

# Example usage and main execution
def main():
    """
    Main function to demonstrate the SalaryAnalyzer usage.
    """
    print("=== Tunisian Government Salary Analysis System ===")
    print("=" * 50)
    
    # Initialize analyzer
    analyzer = SalaryAnalyzer(data_directory=".", encoding='utf-8')
    
    # Load and process data
    if analyzer.load_and_clean_data():
        print("\nStep 1: Data loading completed successfully!")
        
        # Merge data with nomenclature
        analyzer.merge_data_with_nomenclature()
        print("Step 2: Data merged with nomenclature tables!")
        
        # Calculate staff evolution
        analyzer.calculate_staff_evolution()
        print("Step 3: Staff evolution analysis completed!")
        
        # Calculate salary mass
        analyzer.calculate_salary_mass()
        print("Step 4: Salary mass analysis completed!")
        
        # Analyze allowances
        analyzer.analyze_allowances()
        print("Step 5: Allowance analysis completed!")
        
        # Predict future trends
        analyzer.predict_future_trends()
        print("Step 6: Future trends prediction completed!")
        
        # Generate visualizations
        analyzer.save_visualizations()
        print("Step 7: Visualizations created and saved!")
        
        # Generate final report
        final_report = analyzer.generate_final_report()
        print("Step 8: Final report generated!")
        
        print("\n" + "=" * 50)
        print("ANALYSIS COMPLETED SUCCESSFULLY!")
        print("=" * 50)
        
        # Print summary
        summary = final_report['executive_summary']
        print(f"\nEXECUTIVE SUMMARY:")
        print(f"- Total Staff 2023: {summary['total_staff_2023']:,}")
        print(f"- Predicted Staff 2030: {summary['predicted_staff_2030']:,}")
        print(f"- Salary Mass 2023: {summary['total_salary_mass_2023']:,.0f}")
        print(f"- Predicted Salary Mass 2030: {summary['predicted_salary_mass_2030']:,.0f}")
        print(f"- Average Annual Growth Rate: {summary['average_annual_growth_rate']}%")
        
    else:
        print("Error: Failed to load data. Please check your data files.")

if __name__ == "__main__":
    main()
