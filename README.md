# Tunisian Government Salary Analysis and Prediction System

## 📋 Overview

This comprehensive system analyzes Tunisian government payroll data from 2013-2023 and provides predictions for 2025-2030. It includes staff evolution analysis, salary mass calculations, allowance tracking, and future trend predictions for all government departments.

## 🎯 Project Objectives

### Primary Goals
1. **Staff Evolution Analysis**: Track employee numbers across ministries, corps, and grades
2. **Salary Mass Prediction**: Forecast total salary expenditure for budget planning
3. **Allowance Analysis**: Detailed tracking of allowance amounts and distribution
4. **Future Predictions**: Machine learning-based forecasts for 2025-2030

### Key Features
- ✅ Historical trend analysis (2013-2023)
- ✅ Multiple prediction models (Linear Regression, Random Forest, ARIMA)
- ✅ Interactive visualizations and charts
- ✅ Detailed allowance reports by department/corps/grade
- ✅ Comprehensive JSON and text reports
- ✅ Confidence intervals for predictions

## 📊 Data Schema

### Main Dataset: `tab_paie_13_23.cleaned.txt`
- **Period**: 2013-2023 payroll data
- **Coverage**: 7 Tunisian government ministries
- **Focus**: Administrative family jobs only

### Data Fields
| Field | Description |
|-------|-------------|
| Codetab | Establishment code |
| Mois | Payroll month |
| Annee | Payroll year |
| Type | Payroll type (1: salary, 2: bonus, 3: overtime, 4: other) |
| Nligne | Line number |
| Codind | Allowance code |
| Montind | Allowance amount |
| Article | Article |
| Par | Paragraph |
| Codgrd | Grade code |
| Codcorps | Corps code |
| Hcorps | Hierarchy in corps |
| Codfam | Family code |
| Codsfam | Subfamily code |
| Codnat | Agent nature |
| Dire | Direction |
| Sdir | Sub-direction |
| Serv | Service |
| Deleg | Credit delegation |
| Centreg | Regional/central structure |
| Gouv | Governorate assignment |
| Id_agent | Agent identification |

### Nomenclature Tables
- `table_grade.cleaned.txt` - Grade classifications
- `table_corps.cleaned.txt` - Corps information
- `table_etablissement.cleaned.txt` - Establishment details
- `table_categorie.cleaned.txt` - Category classifications
- `table_nature.cleaned.txt` - Nature classifications
- `table_indemnite.cleaned.txt` - Allowance types
- `table_organigramme_5_ministeres.cleaned.txt` - Organizational structure

## 🚀 Quick Start

### 1. Environment Setup
```powershell
# Install Python packages
python setup_environment.py

# Or manually install requirements
pip install -r requirements.txt
```

### 2. Run Analysis
```powershell
# Interactive demonstration
python demo_analysis.py

# Complete analysis pipeline
python salary_analyzer.py

# Generate specific allowance reports
python allowance_report_generator.py
```

### 3. Required Files
Ensure all data files are in the project directory:
- ✅ `tab_paie_13_23.cleaned.txt` (main dataset)
- ✅ `table_*.cleaned.txt` (nomenclature tables)

## 🛠️ System Components

### Core Class: `SalaryAnalyzer`
```python
from salary_analyzer import SalaryAnalyzer

# Initialize
analyzer = SalaryAnalyzer(data_directory=".", encoding='utf-8')

# Load and process data
analyzer.load_and_clean_data()
analyzer.merge_data_with_nomenclature()

# Perform analysis
analyzer.calculate_staff_evolution()
analyzer.calculate_salary_mass()
analyzer.analyze_allowances()

# Generate predictions
analyzer.predict_future_trends([2025, 2026, 2027, 2028, 2029, 2030])

# Create visualizations and reports
analyzer.save_visualizations()
analyzer.generate_final_report()
```

### Key Methods

#### Data Processing
- `load_and_clean_data()` - Load and clean all data files
- `merge_data_with_nomenclature()` - Enrich data with classifications

#### Analysis Functions
- `calculate_staff_evolution()` - Track employee numbers over time
- `calculate_salary_mass()` - Calculate total salary expenditure
- `analyze_allowances()` - Detailed allowance analysis

#### Prediction Models
- `predict_future_trends()` - Multi-model forecasting
- `_predict_time_series()` - Individual time series prediction

#### Visualization & Reporting
- `create_visualizations()` - Generate all charts and graphs
- `generate_final_report()` - Comprehensive JSON report
- `generate_allowance_report()` - Detailed allowance structure

## 📈 Analysis Outputs

### 1. Staff Evolution Report
**Historical Trends (2013-2023)**
- Total staff count by year
- Staff distribution by ministry
- Top corps by employee count
- Growth rate analysis

**Predictions (2025-2030)**
- Forecasted staff numbers
- Confidence intervals
- Ministry-specific projections

### 2. Salary Mass Analysis
**Key Metrics**
- Total salary mass evolution
- Average salary per agent
- Ministry-wise salary distribution
- Annual growth rates

**Future Projections**
- Predicted total salary mass (2025-2030)
- Budget planning recommendations
- Risk assessment

### 3. Allowance Reports

#### Format A: Allowance Amounts by Department/Corps/Grade
```
+ Department
  + Corps
    + Grade
                2013  2014  ...  2023  2025  2026  2027  2028  2029  2030
      Allowance1  Amount predictions
      Allowance2  Amount predictions
      ...
```

#### Format B: Number of Allowances by Department/Corps/Grade
```
+ Department
  + Corps
                2013  2014  ...  2023  2025  2026  2027  2028  2029  2030
    Grade1      Number of allowances (predicted)
    Grade2      Number of allowances (predicted)
    ...
```

## 📊 Visualization Dashboard

### Generated Charts
1. **Staff Evolution Plots**
   - Total staff over time
   - Ministry comparison
   - Top corps analysis
   - Distribution box plots

2. **Salary Mass Visualizations**
   - Total salary mass trends
   - Average salary evolution
   - Ministry breakdown
   - Growth rate analysis

3. **Prediction Charts**
   - Future staff projections with confidence intervals
   - Salary mass forecasts
   - Model accuracy comparison

4. **Ministry Comparison**
   - Staff count rankings
   - Salary mass distribution
   - Growth rate comparison
   - Average salary by ministry

5. **Allowance Analysis**
   - Allowance type distribution
   - Average allowances per agent
   - Amount distribution
   - Count by type

## 🔮 Prediction Models

### Available Models
1. **Linear Regression** - Simple trend analysis
2. **Random Forest** - Non-linear pattern detection
3. **ARIMA** - Time series forecasting (when sufficient data)

### Model Selection
- Automatic best model selection based on R² score
- Fallback mechanisms for insufficient data
- Confidence interval calculation

### Prediction Confidence
- Historical standard deviation-based intervals
- Model accuracy metrics (R² scores)
- Multiple model comparison

## 📁 Output Files

### JSON Reports
- `salary_analysis_report.json` - Complete analysis results
- `allowance_amounts_report.json` - Detailed allowance amounts
- `allowance_counts_report.json` - Allowance count analysis

### Text Reports
- `allowance_amounts_report.txt` - Formatted allowance amounts
- `allowance_counts_report.txt` - Formatted allowance counts

### Visualizations
- `visualizations/staff_evolution.png`
- `visualizations/salary_mass_evolution.png`
- `visualizations/predictions.png`
- `visualizations/ministry_comparison.png`
- `visualizations/allowance_analysis.png`

## 🔧 Configuration & Customization

### Prediction Years
Modify target years in `salary_analyzer.py`:
```python
target_years = [2025, 2026, 2027, 2028, 2029, 2030]
```

### Visualization Settings
Customize plots in the `create_visualizations()` method:
```python
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")
figsize=(15, 12)
```

### Data Encoding
For different file encodings:
```python
analyzer = SalaryAnalyzer(data_directory=".", encoding='latin-1')
```

## 📋 Requirements

### Python Version
- Python 3.8 or higher

### Required Packages
```
pandas>=1.5.0
numpy>=1.21.0
scikit-learn>=1.1.0
statsmodels>=0.13.0
matplotlib>=3.5.0
seaborn>=0.11.0
plotly>=5.10.0
```

### Data Files
All `.cleaned.txt` files must be present in the project directory.

## 🚨 Troubleshooting

### Common Issues

#### 1. Large File Loading
If `tab_paie_13_23.cleaned.txt` is too large:
- The system loads data in chunks automatically
- Increase available RAM if needed
- Consider data sampling for testing

#### 2. Missing Packages
```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

#### 3. Encoding Issues
Try different encodings:
```python
analyzer = SalaryAnalyzer(encoding='latin-1')  # or 'cp1252'
```

#### 4. Memory Issues
For large datasets:
- Close other applications
- Use data sampling for testing
- Process data in smaller chunks

### Error Messages

#### "Files above 50MB cannot be synchronized"
This is a VS Code limitation. The system will still process the file correctly.

#### "Import could not be resolved"
Install the missing package:
```powershell
pip install package_name
```

## 🎯 Use Cases

### Budget Planning
- Forecast salary mass for next 5 years
- Identify high-growth departments
- Plan resource allocation

### Workforce Management
- Track staff evolution trends
- Identify recruitment needs
- Optimize department sizes

### Policy Analysis
- Analyze allowance distribution
- Compare ministry performance
- Assess salary equity

### Risk Assessment
- Identify potential budget overruns
- Monitor unusual growth patterns
- Plan contingency measures

## 🔄 Future Enhancements

### Planned Features
- [ ] Real-time data integration
- [ ] Interactive web dashboard
- [ ] Advanced ML models (LSTM, Prophet)
- [ ] Automated report generation
- [ ] Email notifications for predictions
- [ ] Database integration

### Enhancement Ideas
- [ ] Seasonal adjustment models
- [ ] Economic factor integration
- [ ] Cross-ministry comparison metrics
- [ ] Performance indicators
- [ ] Budget optimization algorithms

## 👥 Contributing

### Code Structure
- `salary_analyzer.py` - Main analysis class
- `demo_analysis.py` - User interface and demonstrations
- `allowance_report_generator.py` - Specialized reporting
- `setup_environment.py` - Environment setup
- `clean_the_data.py` - Data preprocessing utilities

### Development Guidelines
1. Follow existing code style
2. Add docstrings to all functions
3. Include error handling
4. Test with sample data
5. Update documentation

## 📞 Support

### Documentation
- Code comments and docstrings
- This README file
- Demo script examples

### Debugging
1. Run `setup_environment.py` to check configuration
2. Use `demo_analysis.py` for step-by-step testing
3. Check data file integrity
4. Verify package versions

## 📄 License

This project is developed for the Tunisian government salary analysis system. All rights reserved.

---

**System Version**: 1.0  
**Last Updated**: July 2025  
**Compatibility**: Python 3.8+, Windows/Linux/macOS
