from pathlib import Path
import joblib
from numbers import Real
import math
import pandas as pd

# Production Input Contract
SELECTED_FEATURES = (
    "Brand",
    "Series",
    "Thickness",
    "Weight",
    "Operating System",
    "Display Size",
    "Display Touchscreen",
    "Processor",
    "Graphic Processor",
    "RAM_Capacity_GB",
    "RAM Type",
    "SSD Capacity",
    "HDD Capacity",
    "Battery Capacity",
    "Fingerprint scanner",
)

NUMERICAL_FEATURES = (
    "Thickness",
    "Weight",
    "Display Size",
    "RAM_Capacity_GB",
    "SSD Capacity",
    "HDD Capacity",
    "Battery Capacity",
)

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

# Model Artifact
PROJECT_ROOT = Path(__file__).resolve().parent.parent

MODEL_PATH = (
    PROJECT_ROOT
    / "models"
    / "final_laptopwise_pipeline.joblib"
)

# Model Loading
_MODEL = None

def load_model():
    """
    Load and return the finalized LaptopWise ML pipeline.

    The model is loaded from disk only once and then
    reused from memory for subsequent predictions.
    """
    global _MODEL

    if _MODEL is None:
        if not MODEL_PATH.exists():
            raise FileNotFoundError(f"Model artifact not found: {MODEL_PATH}")

        _MODEL = joblib.load(MODEL_PATH)

    return _MODEL

# Input Validation
def validate_input(data):
    """
    Validate a LaptopWise prediction input.
    Returns:
        dict: Validated input data.
    Raises:
        TypeError: If input is not a dictionary or has invalid types.
        ValueError: If required fields are missing, extra fields exist,
                    or values are invalid.
    """

    # 1. Check overall input type
    if not isinstance(data, dict):
        raise TypeError("Input must be provided as a dictionary.")

    # 2. Check for missing features
    missing_features = [
        feature
        for feature in SELECTED_FEATURES
        if feature not in data
    ]

    if missing_features:
        raise ValueError(f"Missing required features: {missing_features}")

    # 3. Check for unexpected features
    extra_features = [
        feature
        for feature in data
        if feature not in SELECTED_FEATURES
    ]

    if extra_features:
        raise ValueError(f"Unexpected features provided: {extra_features}")

    # 4. Validate each feature value
    for feature in NUMERICAL_FEATURES:
        value = data[feature]
        if isinstance(value, bool) or not isinstance(value, Real):
            raise ValueError(f"Invalid numeric value for '{feature}': {value}")

        if not math.isfinite(value):
            raise ValueError(f"Numeric value for '{feature}' must be finite.")

    for feature in CATEGORICAL_FEATURES:
        value = data[feature]
        if not isinstance(value, str):
            raise ValueError(
                f"Invalid categorical value for '{feature}': "
                "value must be a string."
            )

        if not value.strip():
            raise ValueError(f"Categorical feature '{feature}' cannot be empty.")

    return data

# Input Construction
def prepare_input(data):
    """
    Validate and construct a one-row DataFrame for prediction.

    Returns:
        pandas.DataFrame: One-row DataFrame containing the
        validated 15 LaptopWise input features.
    """

    validated_data = validate_input(data)

    return pd.DataFrame([validated_data],columns=SELECTED_FEATURES)


# Price Prediction
def predict_price(data):
    """
    Predict the price of a laptop from its 15 input features.

    Returns:
        float: Predicted laptop price in rupees.
    """

    input_data = prepare_input(data)
    model = load_model()
    prediction = model.predict(input_data)
    return float(prediction[0])

# Deal Comparison
def compare_deal(data, asking_price):
    """
    Compare the model's predicted laptop price with
    the user's asking price.

    Returns:
        dict: Deal comparison result.
    """

    if isinstance(asking_price, bool) or not isinstance(asking_price, Real):
        raise ValueError("Asking price must be a numeric value.")

    if not math.isfinite(asking_price):
        raise ValueError("Asking price must be a finite number.")

    if asking_price <= 0:
        raise ValueError("Asking price must be greater than zero.")

    predicted_price = predict_price(data)
    difference = predicted_price - asking_price

    if difference > 0:
        status = "below_estimated_price"
    elif difference < 0:
        status = "above_estimated_price"
    else:
        status = "around_estimated_price"

    return {
        "predicted_price": round(predicted_price, 2),
        "asking_price": round(float(asking_price), 2),
        "difference": round(difference, 2),
        "status": status,
    }

