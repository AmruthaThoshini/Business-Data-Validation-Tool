# Business Data Validation Tool

A Python-based data quality validation tool that analyzes customer datasets, detects common data issues, generates a CSV validation report, and creates a visual dashboard in PNG format.

## Project Overview

Data quality is important for reliable business reporting and analysis. This project automates basic data validation checks on a customer dataset and summarizes the detected issues in a structured report and visual dashboard.

The project uses a customer dataset containing 2,240 records and 29 columns.

## Features

- Detects missing values across dataset columns.
- Identifies duplicate customer IDs.
- Checks for negative values in selected purchase and count fields.
- Validates education and marital status categories.
- Detects unparseable customer registration dates.
- Flags zero or negative income values.
- Generates a CSV validation report.
- Creates a PNG dashboard with summary metrics, a data quality score, charts, and an issue summary.

## Technologies Used

- Python
- Pandas
- Matplotlib
- CSV and Excel datasets

## Project Structure

```text
Business-Data-Validation-Tool/
├── customer_data_formatted.csv
├── customer_data_validation.xlsx
├── validate_data.py
├── validation_report.csv
├── validation_dashboard.png
└── README.md
```

## Validation Results

The initial validation run produced the following results:

| Metric | Result |
|---|---:|
| Records checked | 2,240 |
| Columns analyzed | 29 |
| Missing income values | 24 |
| Records without detected issues | 2,216 |
| Data quality score | 98.9% |

The validation script detected 24 missing values in the `Income` column. No issues were reported by the other configured checks in that run.

The data quality score represents the percentage of records without issues detected by the configured validation rules. It does not guarantee that all data is correct.

## Generated Outputs

### 1. Validation Report

`validation_report.csv` contains the validation check name, number of detected issues, and a description of each issue.

### 2. Validation Dashboard

`validation_dashboard.png` provides a visual summary of the dataset, including record counts, column counts, detected issues, the data quality score, and a chart of validation findings.

## Installation and Setup

### Prerequisites

Install Python 3 and ensure that Python is available from your terminal.

### 1. Clone the repository



```bash
git clone  https://github.com/AmruthaThoshiniBusiness-Data-Validation-Tool.git
cd Business-Data-Validation-Tool
```

### 2. Install dependencies

```bash
python -m pip install pandas matplotlib
```

### 3. Run the validation tool

Ensure that `customer_data_formatted.csv` is in the project folder, then run:

```bash
python validate_data.py
```

The script generates or updates `validation_report.csv` and `validation_dashboard.png` in the project directory.

## Future Improvements

- Add a web-based interactive dashboard.
- Allow users to upload different datasets.
- Export detailed records containing validation issues.
- Add configurable validation rules.
- Include additional data quality checks and automated tests.

## Disclaimer

This project is intended for educational and portfolio purposes. Validation results depend on the rules implemented in the script and the quality of the input dataset.
