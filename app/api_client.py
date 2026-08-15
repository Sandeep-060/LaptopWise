import os
import requests


# FastAPI Configuration
API_BASE_URL = os.getenv(
    "LAPTOPWISE_API_URL",
    "http://127.0.0.1:8000",
).rstrip("/")

REQUEST_TIMEOUT = 10


# API Client Exception
class APIClientError(Exception):
    """
    Represents a user-safe error from the LaptopWise API client.
    """
    pass


# Internal Request Helper
def _post(endpoint, payload):
    """
    Send a POST request to the LaptopWise FastAPI backend.
    Returns:
        dict: JSON response from the API.

    Raises:
        APIClientError: If the API cannot be reached,
                        returns an HTTP error, or returns
                        an unexpected response.
    """

    url = f"{API_BASE_URL}{endpoint}"

    try:
        response = requests.post(
            url,
            json=payload,
            timeout=REQUEST_TIMEOUT,
        )

    except requests.exceptions.Timeout:
        raise APIClientError(
            "The LaptopWise API request timed out. "
            "Please try again."
        )

    except requests.exceptions.ConnectionError:
        raise APIClientError(
            "Unable to connect to the LaptopWise API. "
            "Please make sure the FastAPI server is running."
        )

    except requests.exceptions.RequestException:
        raise APIClientError(
            "Unable to communicate with the LaptopWise API. "
            "Please try again."
        )

    # HTTP Errors
    if response.status_code >= 400:

        try:
            error_data = response.json()
        except ValueError:
            error_data = None

        # FastAPI commonly returns:
        # {"detail": "..."}
        if isinstance(error_data, dict):
            detail = error_data.get("detail")

            if isinstance(detail, str):
                raise APIClientError(detail)

        if response.status_code == 400:
            raise APIClientError(
                "The submitted laptop information is invalid."
            )

        if response.status_code == 422:
            raise APIClientError(
                "Some of the submitted information is invalid."
            )

        if response.status_code >= 500:
            raise APIClientError(
                "The LaptopWise API could not process the request "
                "right now."
            )

        raise APIClientError(
            "The LaptopWise API returned an unexpected error."
        )

    # Parse JSON Response
    try:
        data = response.json()
    except ValueError:
        raise APIClientError(
            "The LaptopWise API returned an unexpected response."
        )

    if not isinstance(data, dict):
        raise APIClientError(
            "The LaptopWise API returned an unexpected response."
        )

    return data


# Price Prediction
def predict_price(laptop_data):
    """
    Send laptop specifications to FastAPI /predict.

    Args:
        laptop_data (dict): The 15 LaptopWise features.

    Returns:
        dict: API prediction response.
    """

    response_data = _post(
        "/predict",
        laptop_data,
    )

    if "predicted_price" not in response_data:
        raise APIClientError(
            "The prediction response was missing the "
            "predicted price."
        )

    return response_data


# Deal Comparison
def compare_deal(laptop_data, asking_price):
    """
    Send laptop specifications and asking price
    to FastAPI /compare.

    Args:
        laptop_data (dict): The 15 LaptopWise features.
        asking_price (float): Seller's asking price.

    Returns:
        dict: API deal comparison response.
    """

    payload = {
        **laptop_data,
        "asking_price": asking_price,
    }

    response_data = _post(
        "/compare",
        payload,
    )

    required_fields = (
        "predicted_price",
        "asking_price",
        "difference",
        "status",
    )

    missing_fields = [
        field
        for field in required_fields
        if field not in response_data
    ]

    if missing_fields:
        raise APIClientError(
            "The deal comparison response was incomplete."
        )

    return response_data