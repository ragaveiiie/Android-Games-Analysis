from pathlib import Path

import pandas as pd
import numpy as np


# ============================================================
# CONFIGURATION
# ============================================================

RAW_FILE = Path(
    "data/raw/android_games_eda_ready.csv"
)

PROCESSED_DIR = Path(
    "data/processed"
)

OUTPUT_FILE = PROCESSED_DIR / "cleaned_data.csv"


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
# STANDARDIZE COLUMN NAMES
# ============================================================

def standardize_column_names(
    df: pd.DataFrame
) -> pd.DataFrame:
    """Convert column names to a consistent format."""

    df = df.copy()

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(r"[^\w]+", "_", regex=True)
        .str.strip("_")
    )

    return df


# ============================================================
# REMOVE EXACT DUPLICATES
# ============================================================

def remove_duplicates(
    df: pd.DataFrame
) -> tuple[pd.DataFrame, int]:
    """Remove exact duplicate rows."""

    before = len(df)

    df = df.drop_duplicates().copy()

    removed = before - len(df)

    return df, removed


# ============================================================
# NORMALIZE MISSING VALUE REPRESENTATIONS
# ============================================================

def normalize_missing_values(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Convert common textual representations of missing
    values into actual NaN values.
    """

    df = df.copy()

    missing_tokens = [
        "",
        " ",
        "na",
        "n/a",
        "null",
        "none",
        "unknown",
        "missing",
        "-"
    ]

    for column in df.select_dtypes(
        include=["object", "string"]
    ).columns:

        df[column] = (
            df[column]
            .astype("string")
            .str.strip()
        )

        df[column] = df[column].replace(
            missing_tokens,
            np.nan
        )

    return df


# ============================================================
# NUMERIC CONVERSION
# ============================================================

def convert_numeric_columns(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Attempt safe conversion of object columns that
    contain numerical values.
    """

    df = df.copy()

    for column in df.columns:

        if df[column].dtype == "object":

            converted = pd.to_numeric(
                df[column],
                errors="coerce"
            )

            # Convert only when most non-null values
            # can successfully be interpreted as numbers.
            original_non_null = df[column].notna().sum()

            converted_non_null = converted.notna().sum()

            if (
                original_non_null > 0
                and converted_non_null / original_non_null >= 0.90
            ):
                df[column] = converted

    return df


# ============================================================
# STRING STANDARDIZATION
# ============================================================

def standardize_text_columns(
    df: pd.DataFrame
) -> pd.DataFrame:
    """Clean whitespace in text columns."""

    df = df.copy()

    text_columns = df.select_dtypes(
        include=["object", "string"]
    ).columns

    for column in text_columns:

        df[column] = (
            df[column]
            .astype("string")
            .str.strip()
        )

    return df


# ============================================================
# MISSING VALUE REPORT
# ============================================================

def create_missing_value_report(
    df: pd.DataFrame
) -> pd.DataFrame:

    missing_count = df.isna().sum()

    missing_percentage = (
        missing_count / len(df) * 100
    )

    report = pd.DataFrame({
        "missing_count": missing_count,
        "missing_percentage": missing_percentage
    })

    return report[
        report["missing_count"] > 0
    ].sort_values(
        "missing_percentage",
        ascending=False
    )


# ============================================================
# SAVE DATA
# ============================================================

def save_data(
    df: pd.DataFrame,
    output_file: Path
) -> None:

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        output_file,
        index=False
    )


# ============================================================
# MAIN CLEANING PIPELINE
# ============================================================

def main():

    print("=" * 70)
    print("ANDROID GAMES — DATA CLEANING PIPELINE")
    print("=" * 70)

    # --------------------------------------------------------
    # Load
    # --------------------------------------------------------

    print("\n[1] Loading raw dataset...")

    df = load_data(RAW_FILE)

    print(
        f"Original rows    : {len(df):,}"
    )

    print(
        f"Original columns : {len(df.columns):,}"
    )

    # --------------------------------------------------------
    # Standardize column names
    # --------------------------------------------------------

    print("\n[2] Standardizing column names...")

    df = standardize_column_names(df)

    # --------------------------------------------------------
    # Normalize missing-value representations
    # --------------------------------------------------------

    print(
        "\n[3] Normalizing missing-value representations..."
    )

    df = normalize_missing_values(df)

    # --------------------------------------------------------
    # Standardize text
    # --------------------------------------------------------

    print("\n[4] Standardizing text columns...")

    df = standardize_text_columns(df)

    # --------------------------------------------------------
    # Convert numeric columns
    # --------------------------------------------------------

    print("\n[5] Converting numeric columns...")

    df = convert_numeric_columns(df)

    # --------------------------------------------------------
    # Remove exact duplicates
    # --------------------------------------------------------

    print("\n[6] Removing exact duplicate rows...")

    df, duplicates_removed = remove_duplicates(df)

    print(
        f"Duplicates removed: {duplicates_removed:,}"
    )

    # --------------------------------------------------------
    # Missing-value report AFTER normalization
    # --------------------------------------------------------

    print("\n[7] Missing-value report")

    missing_report = create_missing_value_report(df)

    if missing_report.empty:
        print("No missing values found.")

    else:
        print(
            missing_report.to_string()
        )

    # --------------------------------------------------------
    # Save
    # --------------------------------------------------------

    print("\n[8] Saving cleaned dataset...")

    save_data(
        df,
        OUTPUT_FILE
    )

    print(
        f"Saved to: {OUTPUT_FILE}"
    )

    print("\n" + "=" * 70)
    print("CLEANING PIPELINE COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    main()