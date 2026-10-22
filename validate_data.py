
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Project directory
BASE_DIR = Path(__file__).parent
INPUT_FILE = BASE_DIR / "customer_data_formatted.csv"
OUTPUT_FILE = BASE_DIR / "validation_report.csv"
DASHBOARD_FILE = BASE_DIR / "validation_dashboard.png"

# Load customer dataset
df = pd.read_csv(INPUT_FILE)

issues = []
issue_masks = {}

def add_issue(check_name, records, description):
    """Record validation issues and affected rows."""
    records = records.fillna(False).astype(bool)
    issue_count = int(records.sum())

    issues.append({
        "Validation_Check": check_name,
        "Issue_Count": issue_count,
        "Description": description
    })

    issue_masks[check_name] = records

# 1. Check missing values
for column in df.columns:
    missing = df[column].isna()
    if missing.any():
        add_issue(
            f"Missing values: {column}",
            missing,
            f"{column} contains missing values."
        )

# 2. Check duplicate customer IDs
if "ID" in df.columns:
    duplicate_ids = df["ID"].duplicated(keep=False)
    if duplicate_ids.any():
        add_issue(
            "Duplicate customer IDs",
            duplicate_ids,
            "Customer IDs appear more than once."
        )

# 3. Check negative values in count/purchase fields
count_columns = [
    "Kidhome", "Teenhome", "Recency",
    "MntWines", "MntFruits", "MntMeatProducts",
    "MntFishProducts", "MntSweetProducts", "MntGoldProds",
    "NumDealsPurchases", "NumWebPurchases",
    "NumCatalogPurchases", "NumStorePurchases",
    "NumWebVisitsMonth"
]

for column in count_columns:
    if column in df.columns:
        invalid = df[column].notna() & (df[column] < 0)
        if invalid.any():
            add_issue(
                f"Negative values: {column}",
                invalid,
                f"{column} should not contain negative values."
            )

# 4. Check education categories
if "Education" in df.columns:
    valid_education = {
        "Basic", "2n Cycle", "Graduation", "Master", "PhD"
    }
    invalid = (
        df["Education"].notna()
        & ~df["Education"].isin(valid_education)
    )
    if invalid.any():
        add_issue(
            "Invalid education category",
            invalid,
            "Education contains an unexpected category."
        )

# 5. Check marital status categories
if "Marital_Status" in df.columns:
    valid_status = {
        "Single", "Together", "Married",
        "Divorced", "Widow", "Alone", "Absurd", "YOLO"
    }
    invalid = (
        df["Marital_Status"].notna()
        & ~df["Marital_Status"].isin(valid_status)
    )
    if invalid.any():
        add_issue(
            "Invalid marital status",
            invalid,
            "Marital_Status contains an unexpected category."
        )

# 6. Check registration dates
if "Dt_Customer" in df.columns:
    dates = pd.to_datetime(
        df["Dt_Customer"], errors="coerce", dayfirst=True
    )
    invalid_dates = df["Dt_Customer"].notna() & dates.isna()
    if invalid_dates.any():
        add_issue(
            "Invalid registration dates",
            invalid_dates,
            "Dt_Customer contains unparseable dates."
        )

# 7. Check non-positive income
if "Income" in df.columns:
    invalid_income = df["Income"].notna() & (df["Income"] <= 0)
    if invalid_income.any():
        add_issue(
            "Non-positive income",
            invalid_income,
            "Income is zero or negative and should be reviewed."
        )

# Build validation report
report_columns = [
    "Validation_Check", "Issue_Count", "Description"
]
report = pd.DataFrame(issues, columns=report_columns)

if report.empty:
    report = pd.DataFrame([{
        "Validation_Check": "All checks passed",
        "Issue_Count": 0,
        "Description": "No issues were detected by the configured checks."
    }])

report.to_csv(OUTPUT_FILE, index=False)

# Calculate dashboard summary
total_records = len(df)
total_columns = len(df.columns)
total_issues = sum(
    int(mask.sum()) for mask in issue_masks.values()
)
affected_rows = (
    pd.concat(issue_masks.values(), axis=1).any(axis=1).sum()
    if issue_masks else 0
)
clean_records = total_records - affected_rows
quality_score = (
    clean_records / total_records * 100 if total_records else 100
)

# Prepare chart data
chart_data = report[report["Issue_Count"] > 0].copy()
chart_data = chart_data.sort_values("Issue_Count", ascending=True)

# Create dashboard image
fig = plt.figure(figsize=(14, 9))
fig.suptitle(
    "BUSINESS DATA VALIDATION DASHBOARD",
    fontsize=19,
    fontweight="bold",
    y=0.97
)

fig.text(
    0.5, 0.925,
    "Customer Dataset Quality Summary",
    ha="center",
    fontsize=11
)

# Summary cards
cards = [
    ("RECORDS CHECKED", f"{total_records:,}"),
    ("COLUMNS ANALYZED", f"{total_columns:,}"),
    ("ISSUES DETECTED", f"{total_issues:,}"),
    ("CLEAN RECORDS", f"{clean_records:,}")
]

card_positions = [0.06, 0.29, 0.52, 0.75]

for x, (label, value) in zip(card_positions, cards):
    ax = fig.add_axes([x, 0.76, 0.19, 0.105])
    ax.set_facecolor("#EDF4FA")
    ax.text(
        0.5, 0.68, value,
        ha="center", va="center",
        fontsize=21, fontweight="bold",
        color="#17365D"
    )
    ax.text(
        0.5, 0.22, label,
        ha="center", va="center",
        fontsize=9, color="#334155"
    )
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

# Quality score
score_ax = fig.add_axes([0.08, 0.48, 0.32, 0.19])
score_ax.pie(
    [quality_score, 100 - quality_score],
    startangle=90,
    counterclock=False,
    wedgeprops={"width": 0.28}
)
score_ax.text(
    0, 0, f"{quality_score:.1f}%",
    ha="center", va="center",
    fontsize=20, fontweight="bold"
)
score_ax.set_title(
    "Records Without Detected Issues",
    fontsize=11, pad=12
)

# Validation issues chart
bar_ax = fig.add_axes([0.48, 0.43, 0.46, 0.27])

if not chart_data.empty:
    bar_ax.barh(
        chart_data["Validation_Check"],
        chart_data["Issue_Count"]
    )
    bar_ax.set_xlabel("Number of detected issues")
    bar_ax.set_title("Detected Validation Issues", fontsize=12)
    bar_ax.grid(axis="x", alpha=0.25)
    bar_ax.set_axisbelow(True)
else:
    bar_ax.text(
        0.5, 0.5, "No validation issues detected",
        ha="center", va="center"
    )
    bar_ax.set_axis_off()

# Detailed issue summary
summary_ax = fig.add_axes([0.07, 0.06, 0.87, 0.28])
summary_ax.axis("off")

table_data = [
    [row.Validation_Check, str(row.Issue_Count), row.Description]
    for row in report.itertuples(index=False)
]

table = summary_ax.table(
    cellText=table_data,
    colLabels=["Validation Check", "Issue Count", "Description"],
    cellLoc="left",
    colLoc="left",
    loc="center",
    colWidths=[0.32, 0.13, 0.55]
)
table.auto_set_font_size(False)
table.set_fontsize(8)
table.scale(1, 1.5)

for (row, col), cell in table.get_celld().items():
    if row == 0:
        cell.set_text_props(weight="bold", color="white")
        cell.set_facecolor("#17365D")
    else:
        cell.set_facecolor("#F1F5F9" if row % 2 == 0 else "white")

fig.savefig(
    DASHBOARD_FILE,
    dpi=180,
    bbox_inches="tight"
)
plt.close(fig)

# Display results
print("DATA VALIDATION COMPLETED")
print(f"Total records checked: {total_records}")
print(f"Total columns checked: {total_columns}")
print(f"Total detected issues: {total_issues}")
print(f"Records with no detected issues: {clean_records}")
print(f"Quality score: {quality_score:.2f}%")
print(f"CSV report saved to: {OUTPUT_FILE.name}")
print(f"Dashboard image saved to: {DASHBOARD_FILE.name}")
print("\nVALIDATION REPORT")
print(report.to_string(index=False))
