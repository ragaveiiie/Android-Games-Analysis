from pathlib import Path
import pandas as pd


# ============================================================
# CONFIGURATION
# ============================================================

DATA_FILE = Path("data/raw/android_games_eda_ready.csv")


# ============================================================
# LOAD DATASET
# ============================================================

def load_data(file_path: Path) -> pd.DataFrame:
    """Load the raw Android games dataset."""

    if not file_path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {file_path}"
        )

    df = pd.read_csv(file_path)

    return df


# ============================================================
# DATASET INSPECTION
# ============================================================

def inspect_data(df: pd.DataFrame) -> None:
    """Display important information about the dataset."""

    print("\n" + "=" * 70)
    print("ANDROID GAMES DATASET - INITIAL INSPECTION")
    print("=" * 70)

    # Dataset dimensions
    print("\n[1] DATASET SIZE")
    print(f"Rows    : {df.shape[0]:,}")
    print(f"Columns : {df.shape[1]:,}")

    # Column names
    print("\n[2] COLUMNS")

    for index, column in enumerate(df.columns, start=1):
        print(f"{index:2}. {column}")

    # Data types
    print("\n[3] DATA TYPES")
    print(df.dtypes)

    # First records
    print("\n[4] FIRST 5 ROWS")
    print(df.head())

    # Missing values
    print("\n[5] MISSING VALUES")

    missing = df.isnull().sum()

    missing = missing[
        missing > 0
    ].sort_values(
        ascending=False
    )

    if missing.empty:
        print("No missing values found.")

    else:
        print(missing)

    # Duplicate rows
    print("\n[6] DUPLICATE ROWS")

    duplicate_count = df.duplicated().sum()

    print(f"Duplicate rows: {duplicate_count:,}")

    # Numerical columns
    print("\n[7] NUMERICAL COLUMNS")

    numerical_columns = df.select_dtypes(
        include="number"
    ).columns

    for column in numerical_columns:
        print(f"  - {column}")

    # Categorical columns
    print("\n[8] CATEGORICAL COLUMNS")

    categorical_columns = df.select_dtypes(
        include=["object", "category"]
    ).columns

    for column in categorical_columns:
        print(f"  - {column}")

    # Statistical summary
    print("\n[9] STATISTICAL SUMMARY")

    print(
        df.describe(
            include="all"
        ).transpose()
    )


# ============================================================
# MAIN
# ============================================================

def main():

    print("Loading Android Games dataset...")

    df = load_data(DATA_FILE)

    inspect_data(df)


if __name__ == "__main__":
    main()
