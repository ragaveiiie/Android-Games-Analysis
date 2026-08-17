from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# ============================================================
# CONFIGURATION
# ============================================================

DATA_DIR = Path("data/processed")
OUTPUT_DIR = Path("outputs/figures")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

sns.set_theme(style="whitegrid")


# ============================================================
# LOAD DATA
# ============================================================

def load_data():
    csv_files = list(DATA_DIR.glob("*.csv"))

    if not csv_files:
        raise FileNotFoundError(
            "No CSV file found inside data/processed/"
        )

    file_path = csv_files[0]

    print(f"Loading dataset: {file_path}")

    return pd.read_csv(file_path)


# ============================================================
# SAVE CHART
# ============================================================

def save_chart(filename):
    output_path = OUTPUT_DIR / filename

    plt.tight_layout()

    plt.savefig(
        output_path,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print(f"Saved: {output_path}")


# ============================================================
# 1. MISSING VALUES
# ============================================================

def missing_values_chart(df):

    missing = (
        df.isnull()
        .sum()
        .sort_values(ascending=False)
    )

    missing = missing[missing > 0]

    if missing.empty:
        print("1. No missing values found.")
        return

    plt.figure(figsize=(10, 6))

    sns.barplot(
        x=missing.values,
        y=missing.index
    )

    plt.title("Missing Values by Column")
    plt.xlabel("Number of Missing Values")
    plt.ylabel("Column")

    save_chart("01_missing_values.png")


# ============================================================
# 2. DUPLICATE RECORDS
# ============================================================

def duplicate_chart(df):

    duplicate_count = df.duplicated().sum()
    unique_count = len(df) - duplicate_count

    values = [
        unique_count,
        duplicate_count
    ]

    labels = [
        "Unique Records",
        "Duplicate Records"
    ]

    plt.figure(figsize=(8, 5))

    sns.barplot(
        x=labels,
        y=values
    )

    plt.title("Unique vs Duplicate Records")
    plt.xlabel("Record Type")
    plt.ylabel("Number of Records")

    save_chart("02_duplicates.png")


# ============================================================
# 3. NUMERICAL DISTRIBUTION
# ============================================================

def numerical_distribution(df):

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()

    # Ignore ID-like columns
    useful_columns = [
        column
        for column in numeric_columns
        if df[column].nunique() > 5
    ]

    if not useful_columns:
        print("3. No suitable numerical columns found.")
        return

    # Select up to 4 useful numerical columns
    selected = useful_columns[:4]

    fig, axes = plt.subplots(
        2,
        2,
        figsize=(12, 8)
    )

    axes = axes.flatten()

    for i, column in enumerate(selected):

        sns.histplot(
            data=df,
            x=column,
            kde=True,
            ax=axes[i]
        )

        axes[i].set_title(
            f"Distribution of {column}"
        )

        axes[i].set_xlabel(column)
        axes[i].set_ylabel("Frequency")

    # Hide unused plots
    for i in range(len(selected), 4):
        axes[i].set_visible(False)

    plt.suptitle(
        "Numerical Variable Distributions"
    )

    save_chart("03_numerical_distributions.png")


# ============================================================
# 4. OUTLIER ANALYSIS
# ============================================================

def outlier_chart(df):

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()

    useful_columns = [
        column
        for column in numeric_columns
        if df[column].nunique() > 5
    ]

    if not useful_columns:
        print("4. No suitable numerical columns found.")
        return

    selected = useful_columns[:6]

    plt.figure(
        figsize=(12, 7)
    )

    sns.boxplot(
        data=df[selected]
    )

    plt.title(
        "Outlier Analysis Using Box Plots"
    )

    plt.xlabel("Numerical Variables")
    plt.ylabel("Value")

    plt.xticks(
        rotation=45,
        ha="right"
    )

    save_chart("04_outlier_analysis.png")


# ============================================================
# 5. CORRELATION HEATMAP
# ============================================================

def correlation_heatmap(df):

    numeric_df = df.select_dtypes(
        include="number"
    )

    if numeric_df.shape[1] < 2:
        print(
            "5. Not enough numerical columns "
            "for correlation analysis."
        )
        return

    correlation = numeric_df.corr()

    plt.figure(
        figsize=(12, 8)
    )

    sns.heatmap(
        correlation,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        center=0
    )

    plt.title(
        "Correlation Between Numerical Variables"
    )

    save_chart("05_correlation_heatmap.png")


# ============================================================
# 6. CATEGORICAL DISTRIBUTION
# ============================================================

def categorical_distribution(df):

    categorical_columns = df.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()

    if not categorical_columns:
        print(
            "6. No categorical columns found."
        )
        return

    # Select first useful categorical column
    selected_column = None

    for column in categorical_columns:

        unique_count = df[column].nunique()

        if 2 <= unique_count <= 20:
            selected_column = column
            break

    if selected_column is None:
        print(
            "6. No suitable categorical column found."
        )
        return

    counts = (
        df[selected_column]
        .value_counts()
        .head(10)
    )

    plt.figure(
        figsize=(10, 6)
    )

    sns.barplot(
        x=counts.values,
        y=counts.index
    )

    plt.title(
        f"Top Categories - {selected_column}"
    )

    plt.xlabel("Number of Records")
    plt.ylabel(selected_column)

    save_chart(
        "06_categorical_distribution.png"
    )


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 60)
    print("BUDGETWISE — VISUALIZATION")
    print("=" * 60)

    df = load_data()

    print(
        f"Rows    : {len(df):,}"
    )

    print(
        f"Columns : {len(df.columns):,}"
    )

    print("\nCreating 6 visualizations...\n")

    # 1
    missing_values_chart(df)

    # 2
    duplicate_chart(df)

    # 3
    numerical_distribution(df)

    # 4
    outlier_chart(df)

    # 5
    correlation_heatmap(df)

    # 6
    categorical_distribution(df)

    print("\n" + "=" * 60)
    print("ALL VISUALIZATIONS COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()