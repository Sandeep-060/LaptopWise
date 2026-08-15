from pathlib import Path
import pandas as pd


# Dataset Reference
PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "laptop_selected.csv"
)


# Categorical Features
CATEGORICAL_FEATURES = (
    "Brand",
    "Series",
    "Operating System",
    "Display Touchscreen",
    "Processor",
    "Graphic Processor",
    "RAM Type",
    "Fingerprint scanner",
)

# Load Reference Data
def load_category_options():
    """
    Load unique categorical values from the finalized
    LaptopWise selected dataset.

    Returns:
        dict: Mapping of feature name to sorted category values.
    """

    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Reference dataset not found: {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)

    missing_columns = [
        column
        for column in CATEGORICAL_FEATURES
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(f"Missing categorical columns: {missing_columns}")

    options = {}

    for feature in CATEGORICAL_FEATURES:
        values = (
            df[feature]
            .dropna()
            .astype(str)
            .str.strip()
        )

        values = sorted(
            value
            for value in values.unique()
            if value and value != "No6"
        )

        options[feature] = values

    return options