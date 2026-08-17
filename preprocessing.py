from pathlib import Path

import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


# ============================================================
# CONFIGURATION
# ============================================================

INPUT_FILE = Path(
    "data/processed/cleaned_data.csv"
)

OUTPUT_FILE = Path(
    "data/processed/preprocessed_data.csv"
)


# ============================================================
# LOAD DATA
# ============================================================

def load_data(file_path: Path) -> pd.DataFrame:
    """Load the cleaned dataset."""

    if not file_path.exists():
        raise FileNotFoundError(
            f"Cleaned dataset not found: {file_path}"
        )

    return pd.read_csv(file_path)


# ============================================================
# IDENTIFY COLUMN TYPES
# ============================================================

def identify_columns(df: pd.DataFrame):

    numerical_columns = df.select_dtypes(
        include=["number"]
    ).columns.tolist()

    categorical_columns = df.select_dtypes(
        include=["object", "string", "category"]
    ).columns.tolist()

    return numerical_columns, categorical_columns


# ============================================================
# BUILD PREPROCESSING PIPELINE
# ============================================================

def build_preprocessor(
    numerical_columns,
    categorical_columns
):

    # Numerical preprocessing
    numerical_pipeline = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(
                    strategy="median"
                )
            ),
            (
                "scaler",
                StandardScaler()
            )
        ]
    )

    # Categorical preprocessing
    categorical_pipeline = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(
                    strategy="most_frequent"
                )
            ),
            (
                "encoder",
                OneHotEncoder(
                    handle_unknown="ignore",
                    sparse_output=False
                )
            )
        ]
    )

    # Combine both pipelines
    preprocessor = ColumnTransformer(
        transformers=[
            (
                "numerical",
                numerical_pipeline,
                numerical_columns
            ),
            (
                "categorical",
                categorical_pipeline,
                categorical_columns
            )
        ],
        remainder="drop"
    )

    return preprocessor


# ============================================================
# PREPROCESS DATA
# ============================================================

def preprocess_data(
    df: pd.DataFrame,
    preprocessor
) -> pd.DataFrame:

    processed_array = preprocessor.fit_transform(df)

    # Get generated feature names
    feature_names = (
        preprocessor
        .get_feature_names_out()
    )

    processed_df = pd.DataFrame(
        processed_array,
        columns=feature_names,
        index=df.index
    )

    return processed_df


# ============================================================
# SAVE DATA
# ============================================================

def save_data(
    df: pd.DataFrame,
    output_file: Path
):

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        output_file,
        index=False
    )


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)
    print("ANDROID GAMES — PREPROCESSING PIPELINE")
    print("=" * 70)

    # --------------------------------------------------------
    # Load
    # --------------------------------------------------------

    print("\n[1] Loading cleaned dataset...")

    df = load_data(INPUT_FILE)

    print(
        f"Rows    : {df.shape[0]:,}"
    )

    print(
        f"Columns : {df.shape[1]:,}"
    )

    # --------------------------------------------------------
    # Identify column types
    # --------------------------------------------------------

    print("\n[2] Identifying column types...")

    numerical_columns, categorical_columns = (
        identify_columns(df)
    )

    print(
        f"Numerical columns   : "
        f"{len(numerical_columns)}"
    )

    print(
        f"Categorical columns : "
        f"{len(categorical_columns)}"
    )

    # --------------------------------------------------------
    # Build pipeline
    # --------------------------------------------------------

    print("\n[3] Building preprocessing pipeline...")

    preprocessor = build_preprocessor(
        numerical_columns,
        categorical_columns
    )

    # --------------------------------------------------------
    # Transform data
    # --------------------------------------------------------

    print("\n[4] Applying preprocessing...")

    processed_df = preprocess_data(
        df,
        preprocessor
    )

    # --------------------------------------------------------
    # Display result
    # --------------------------------------------------------

    print("\n[5] PREPROCESSING RESULT")

    print(
        f"Original shape    : "
        f"{df.shape}"
    )

    print(
        f"Processed shape   : "
        f"{processed_df.shape}"
    )

    print("\nFirst 5 rows:")

    print(
        processed_df.head()
    )

    # --------------------------------------------------------
    # Save
    # --------------------------------------------------------

    print("\n[6] Saving preprocessed dataset...")

    save_data(
        processed_df,
        OUTPUT_FILE
    )

    print(
        f"Saved to: {OUTPUT_FILE}"
    )

    print("\n" + "=" * 70)
    print("PREPROCESSING COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    main()