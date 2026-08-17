from pathlib import Path

# ============================================================
# DATA CLEANING
# ============================================================

from data_cleaning import (
    load_data,
    standardize_column_names,
    normalize_missing_values,
    standardize_text_columns,
    convert_numeric_columns,
    remove_duplicates,
    create_missing_value_report,
    save_data
)

# ============================================================
# DATA QUALITY
# ============================================================

from data_quality import (
    missing_value_report,
    duplicate_report,
    unique_value_report,
    find_constant_columns,
    negative_value_report,
    outlier_report
)

# ============================================================
# VISUALIZATION
# ============================================================

from visualization import (
    missing_values_chart,
    duplicate_chart,
    numerical_distribution,
    outlier_chart,
    correlation_heatmap,
    categorical_distribution
)


# ============================================================
# FILE PATHS
# ============================================================

RAW_FILE = Path(
    "data/raw/android_games_eda_ready.csv"
)

CLEANED_FILE = Path(
    "data/processed/cleaned_data.csv"
)


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)
    print("ANDROID GAMES DATA PREPROCESSING PIPELINE")
    print("=" * 70)


    # ========================================================
    # 1. LOAD RAW DATA
    # ========================================================

    print("\n[1] LOADING RAW DATA")

    df = load_data(RAW_FILE)

    print(f"Rows    : {len(df):,}")
    print(f"Columns : {len(df.columns):,}")


    # ========================================================
    # 2. ORIGINAL DATA QUALITY
    # ========================================================

    print("\n[2] ORIGINAL DATA QUALITY ANALYSIS")


    # Missing values

    print("\n--- Missing Values ---")

    missing = missing_value_report(df)

    if missing.empty:
        print("No missing values found.")
    else:
        print(missing.to_string())


    # Duplicates

    print("\n--- Duplicate Records ---")

    duplicates = duplicate_report(df)

    print(
        f"Duplicate rows      : "
        f"{duplicates['duplicate_count']:,}"
    )

    print(
        f"Duplicate percentage: "
        f"{duplicates['duplicate_percentage']:.2f}%"
    )


    # ========================================================
    # 3. STANDARDIZE COLUMN NAMES
    # ========================================================

    print(
        "\n[3] STANDARDIZING COLUMN NAMES"
    )

    df = standardize_column_names(df)

    print("Column names standardized.")

    print("\nColumns:")

    for column in df.columns:
        print(f"  - {column}")


    # ========================================================
    # 4. NORMALIZE MISSING VALUES
    # ========================================================

    print(
        "\n[4] NORMALIZING MISSING VALUES"
    )

    df = normalize_missing_values(df)

    print(
        "Missing-value representations normalized."
    )


    # ========================================================
    # 5. STANDARDIZE TEXT
    # ========================================================

    print(
        "\n[5] STANDARDIZING TEXT COLUMNS"
    )

    df = standardize_text_columns(df)

    print(
        "Text columns standardized."
    )


    # ========================================================
    # 6. CONVERT NUMERIC COLUMNS
    # ========================================================

    print(
        "\n[6] CONVERTING NUMERIC COLUMNS"
    )

    df = convert_numeric_columns(df)

    print(
        "Numeric conversion completed."
    )


    # ========================================================
    # 7. REMOVE DUPLICATES
    # ========================================================

    print(
        "\n[7] REMOVING DUPLICATES"
    )

    rows_before = len(df)

    df, duplicates_removed = remove_duplicates(df)

    rows_after = len(df)

    print(
        f"Rows before       : {rows_before:,}"
    )

    print(
        f"Duplicates removed: {duplicates_removed:,}"
    )

    print(
        f"Rows after        : {rows_after:,}"
    )


    # ========================================================
    # 8. CLEANED DATA QUALITY
    # ========================================================

    print(
        "\n[8] CLEANED DATA QUALITY ANALYSIS"
    )


    # Missing values after cleaning

    print("\n--- Missing Values After Cleaning ---")

    missing_after = create_missing_value_report(df)

    if missing_after.empty:

        print(
            "No missing values found."
        )

    else:

        print(
            missing_after.to_string()
        )


    # ========================================================
    # 9. UNIQUE VALUES
    # ========================================================

    print(
        "\n[9] UNIQUE VALUE ANALYSIS"
    )

    unique = unique_value_report(df)

    print(
        unique.to_string()
    )


    # ========================================================
    # 10. CONSTANT COLUMNS
    # ========================================================

    print(
        "\n[10] CONSTANT COLUMN ANALYSIS"
    )

    constant_columns = find_constant_columns(df)

    if constant_columns:

        print(
            "Constant columns:"
        )

        for column in constant_columns:

            print(
                f"  - {column}"
            )

    else:

        print(
            "No constant columns found."
        )


    # ========================================================
    # 11. NEGATIVE VALUES
    # ========================================================

    print(
        "\n[11] NEGATIVE VALUE ANALYSIS"
    )

    negative = negative_value_report(df)

    if negative.empty:

        print(
            "No negative numerical values found."
        )

    else:

        print(
            negative.to_string()
        )


    # ========================================================
    # 12. OUTLIERS
    # ========================================================

    print(
        "\n[12] OUTLIER ANALYSIS"
    )

    outliers = outlier_report(df)

    if outliers.empty:

        print(
            "No numerical columns available."
        )

    else:

        print(
            outliers.to_string(
                index=False
            )
        )


    # ========================================================
    # 13. SAVE CLEANED DATA
    # ========================================================

    print(
        "\n[13] SAVING CLEANED DATA"
    )

    save_data(
        df,
        CLEANED_FILE
    )

    print(
        f"Cleaned data saved to:"
        f"\n{CLEANED_FILE}"
    )


    # ========================================================
    # 14. VISUALIZATION
    # ========================================================

    print(
        "\n[14] CREATING VISUALIZATIONS"
    )

    print(
        "\nCreating missing-value chart..."
    )

    missing_values_chart(df)


    print(
        "Creating duplicate chart..."
    )

    duplicate_chart(df)


    print(
        "Creating numerical distribution charts..."
    )

    numerical_distribution(df)


    print(
        "Creating outlier chart..."
    )

    outlier_chart(df)


    print(
        "Creating correlation heatmap..."
    )

    correlation_heatmap(df)


    print(
        "Creating categorical distribution..."
    )

    categorical_distribution(df)


    # ========================================================
    # COMPLETED
    # ========================================================

    print("\n" + "=" * 70)

    print(
        "ANDROID GAMES PIPELINE COMPLETED SUCCESSFULLY"
    )

    print("=" * 70)

    print(
        f"\nRaw dataset:"
        f"\n{RAW_FILE}"
    )

    print(
        f"\nCleaned dataset:"
        f"\n{CLEANED_FILE}"
    )

    print(
        "\nData preprocessing : COMPLETED"
    )

    print(
        "Data quality       : COMPLETED"
    )

    print(
        "Visualization      : COMPLETED"
    )

    print("=" * 70)


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()