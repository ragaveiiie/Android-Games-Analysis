from pathlib import Path

import pandas as pd
import numpy as np


# ============================================================
# CONFIGURATION
# ============================================================

DATA_FILE = Path("data/raw/android_games_eda_ready.csv")


# ============================================================
# LOAD DATA
# ============================================================

def load_data(file_path: Path) -> pd.DataFrame:
    """Load the raw dataset."""

    if not file_path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {file_path}"
        )

    return pd.read_csv(file_path)


# ============================================================
# MISSING VALUE ANALYSIS
# ============================================================

def missing_value_report(df: pd.DataFrame) -> pd.DataFrame:
    """Return missing-value statistics."""

    missing_count = df.isna().sum()

    missing_percentage = (
        missing_count / len(df) * 100
    )

    report = pd.DataFrame({
        "missing_count": missing_count,
        "missing_percentage": missing_percentage
    })

    report = report[
        report["missing_count"] > 0
    ].sort_values(
        "missing_percentage",
        ascending=False
    )

    return report


# ============================================================
# DUPLICATE ANALYSIS
# ============================================================

def duplicate_report(df: pd.DataFrame) -> dict:
    """Calculate duplicate statistics."""

    duplicate_count = df.duplicated().sum()

    duplicate_percentage = (
        duplicate_count / len(df) * 100
    )

    return {
        "duplicate_count": duplicate_count,
        "duplicate_percentage": duplicate_percentage
    }


# ============================================================
# UNIQUE VALUE ANALYSIS
# ============================================================

def unique_value_report(df: pd.DataFrame) -> pd.DataFrame:
    """Return number of unique values per column."""

    report = pd.DataFrame({
        "unique_values": df.nunique(dropna=False),
        "data_type": df.dtypes.astype(str)
    })

    return report.sort_values(
        "unique_values"
    )


# ============================================================
# CONSTANT COLUMN DETECTION
# ============================================================

def find_constant_columns(df: pd.DataFrame) -> list:
    """Find columns containing only one unique value."""

    constant_columns = [
        column
        for column in df.columns
        if df[column].nunique(dropna=False) <= 1
    ]

    return constant_columns


# ============================================================
# NEGATIVE VALUE ANALYSIS
# ============================================================

def negative_value_report(df: pd.DataFrame) -> pd.DataFrame:
    """
    Find negative values in numerical columns.

    Negative values are not automatically errors.
    They must be evaluated according to the meaning
    of each column.
    """

    numerical_df = df.select_dtypes(
        include=np.number
    )

    negative_counts = (
        numerical_df < 0
    ).sum()

    report = pd.DataFrame({
        "negative_count": negative_counts
    })

    report = report[
        report["negative_count"] > 0
    ].sort_values(
        "negative_count",
        ascending=False
    )

    return report


# ============================================================
# OUTLIER ANALYSIS — IQR METHOD
# ============================================================

def outlier_report(df: pd.DataFrame) -> pd.DataFrame:
    """
    Detect potential outliers using the IQR method.

    This does NOT remove outliers.
    It only identifies potential outliers.
    """

    numerical_columns = df.select_dtypes(
        include=np.number
    ).columns

    results = []

    for column in numerical_columns:

        series = df[column].dropna()

        if series.empty:
            continue

        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)

        iqr = q3 - q1

        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        outliers = series[
            (series < lower_bound) |
            (series > upper_bound)
        ]

        results.append({
            "column": column,
            "q1": q1,
            "q3": q3,
            "iqr": iqr,
            "lower_bound": lower_bound,
            "upper_bound": upper_bound,
            "outlier_count": len(outliers),
            "outlier_percentage": (
                len(outliers) / len(series) * 100
            )
        })

    return pd.DataFrame(results).sort_values(
        "outlier_count",
        ascending=False
    )


# ============================================================
# MAIN QUALITY REPORT
# ============================================================

def main():

    print("=" * 70)
    print("ANDROID GAMES — DATA QUALITY ANALYSIS")
    print("=" * 70)

    df = load_data(DATA_FILE)

    # --------------------------------------------------------
    # Dataset dimensions
    # --------------------------------------------------------

    print("\n[1] DATASET SIZE")

    print(f"Rows    : {len(df):,}")
    print(f"Columns : {len(df.columns):,}")

    # --------------------------------------------------------
    # Missing values
    # --------------------------------------------------------

    print("\n[2] MISSING VALUE REPORT")

    missing = missing_value_report(df)

    if missing.empty:
        print("No missing values found.")

    else:
        print(missing.to_string())

    # --------------------------------------------------------
    # Duplicates
    # --------------------------------------------------------

    print("\n[3] DUPLICATE REPORT")

    duplicates = duplicate_report(df)

    print(
        f"Duplicate rows      : "
        f"{duplicates['duplicate_count']:,}"
    )

    print(
        f"Duplicate percentage: "
        f"{duplicates['duplicate_percentage']:.2f}%"
    )

    # --------------------------------------------------------
    # Unique values
    # --------------------------------------------------------

    print("\n[4] UNIQUE VALUE REPORT")

    unique = unique_value_report(df)

    print(unique.to_string())

    # --------------------------------------------------------
    # Constant columns
    # --------------------------------------------------------

    print("\n[5] CONSTANT COLUMNS")

    constant_columns = find_constant_columns(df)

    if constant_columns:
        for column in constant_columns:
            print(f"  - {column}")
    else:
        print("No constant columns found.")

    # --------------------------------------------------------
    # Negative values
    # --------------------------------------------------------

    print("\n[6] NEGATIVE VALUE REPORT")

    negative = negative_value_report(df)

    if negative.empty:
        print("No negative numerical values found.")
    else:
        print(negative.to_string())

    # --------------------------------------------------------
    # Outliers
    # --------------------------------------------------------

    print("\n[7] POTENTIAL OUTLIERS — IQR METHOD")

    outliers = outlier_report(df)

    if outliers.empty:
        print("No numerical columns available.")
    else:
        print(
            outliers.to_string(
                index=False
            )
        )

    print("\n" + "=" * 70)
    print("DATA QUALITY ANALYSIS COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    main()