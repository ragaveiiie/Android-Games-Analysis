# Android Games Analysis & Data Preprocessing

## Project Overview

**Android Games Analysis** is a Python-based data preprocessing, data quality analysis, visualization, and dashboard project for analyzing an Android games dataset.

The project takes raw Android games data, cleans and standardizes it, performs data-quality checks, generates visualizations, and provides an interactive dashboard for exploring the dataset.

##  Objectives

* Load and preprocess Android games data
* Standardize column names and text values
* Handle missing-value representations
* Convert suitable columns to numeric data types
* Remove duplicate records
* Analyze data quality
* Detect potential numerical outliers
* Analyze correlations between numerical variables
* Generate multiple statistical visualizations
* Provide an interactive dashboard for data exploration
* Produce cleaned data for further analysis and reporting

##  Technologies Used

* **Python**
* **Pandas** — data manipulation and analysis
* **NumPy** — numerical operations
* **Matplotlib** — data visualization
* **Seaborn** — statistical visualization
* **Plotly** — interactive charts
* **Scikit-learn** — machine-learning/data-analysis support
* **Streamlit** — interactive dashboard
* **OpenPyXL** — spreadsheet support

## Project Structure

```text
BudgetWise_Preprocessing/
│
├── data/
│   ├── raw/
│   │   └── android_games_eda_ready.csv
│   │
│   └── processed/
│       └── cleaned_data.csv
│
├── outputs/
│   └── figures/
│       ├── 01_missing_values.png
│       ├── 02_duplicates.png
│       ├── 03_numerical_distributions.png
│       ├── 04_outlier_analysis.png
│       ├── 05_correlation_heatmap.png
│       └── 06_categorical_distribution.png
│
├── main.py
├── dashboard_app.py
├── data_cleaning.py
├── data_quality.py
├── visualization.py
├── preprocessing.py
├── analysis.py
├── check_data.py
├── requirements.txt
├── .gitignore
└── README.md
```

##  Data Processing Pipeline

```text
Raw Android Games Dataset
          ↓
     Load Dataset
          ↓
 Standardize Column Names
          ↓
 Normalize Missing Values
          ↓
 Standardize Text Columns
          ↓
 Convert Numeric Columns
          ↓
 Remove Duplicate Records
          ↓
   Cleaned Dataset
          ↓
 ┌────────┴────────┐
 ↓                 ↓
Data Quality    Visualization
Analysis        & Dashboard
 ↓                 ↓
Reports          Charts
```

##  Data Cleaning

The `data_cleaning.py` module performs:

1. Dataset loading
2. Column-name standardization
3. Missing-value normalization
4. Text standardization
5. Numeric-column conversion
6. Duplicate removal
7. Missing-value reporting
8. Saving the cleaned dataset

The cleaned dataset is saved as:

```text
data/processed/cleaned_data.csv
```

##  Data Quality Analysis

The `data_quality.py` module analyzes:

* Dataset dimensions
* Missing values
* Duplicate records
* Unique values
* Constant columns
* Negative numerical values
* Potential outliers using the IQR method

The project does not automatically remove potential outliers during quality analysis. They are reported for further evaluation.

##  Visualizations

The visualization module generates multiple charts, including:

### 1. Missing Values

Shows the number of missing values in each column.

### 2. Duplicate Records

Compares unique and duplicate records.

### 3. Numerical Distributions

Displays distributions of useful numerical variables.

### 4. Outlier Analysis

Uses box plots to identify potential outliers.

### 5. Correlation Heatmap

Shows relationships between numerical variables.

### 6. Categorical Distribution

Displays the most frequent values in suitable categorical columns.

Generated figures are stored in:

```text
outputs/figures/
```

##  Interactive Dashboard

The project also includes:

```text
dashboard_app.py
```

The Streamlit dashboard provides interactive exploration of the Android games dataset.

Depending on the available columns, users can:

* Filter data
* Select variables
* Compare numerical values
* Explore categorical distributions
* View different chart types
* Analyze relationships between variables
* Examine dataset statistics

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/ragaveiiie/Android-Games-Analysis.git
```

### 2. Open the project

```bash
cd Android-Games-Analysis
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment on Windows

```powershell
.venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

##  Run the Data Pipeline

Run:

```bash
python main.py
```

This runs the project's preprocessing, quality-analysis, and visualization workflow.

##  Run the Dashboard

Start Streamlit with:

```bash
streamlit run dashboard_app.py
```

The dashboard will normally open in your browser at:

```text
http://localhost:8501
```

##  Dataset

The project uses an Android games dataset stored in:

```text
data/raw/android_games_eda_ready.csv
```

The processed dataset is generated at:

```text
data/processed/cleaned_data.csv
```

##  Key Features

| Feature                     | Status |
| --------------------------- | ------ |
| Raw data loading            | ✅      |
| Column standardization      | ✅      |
| Missing-value handling      | ✅      |
| Numeric conversion          | ✅      |
| Duplicate detection/removal | ✅      |
| Data-quality analysis       | ✅      |
| Outlier analysis            | ✅      |
| Correlation analysis        | ✅      |
| Multiple visualizations     | ✅      |
| Interactive dashboard       | ✅      |
| Cleaned CSV generation      | ✅      |

##  Project Use

This project can be used as an academic/internship project for demonstrating:

* Python programming
* Data preprocessing
* Exploratory data analysis
* Data-quality assessment
* Statistical visualization
* Interactive dashboard development
* Data-driven reporting

##  Author

**Yashaswi AJ**

GitHub: `https://github.com/ragaveiiie`

##  License

This project is intended for educational, academic, and internship purposes.
