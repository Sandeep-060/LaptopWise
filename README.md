# LaptopWise

### Know the price. Make the right choice.

LaptopWise is an end-to-end machine learning application that estimates the market price of a laptop from its specifications and helps users evaluate whether a seller's asking price looks reasonable.

## Live Demo

- **Streamlit App:** https://laptopwise.streamlit.app/
- **FastAPI:** https://laptopwise.onrender.com/docs
- **GitHub:** https://github.com/Sandeep-060/LaptopWise

## Features

### Estimate Price

Enter the laptop specifications and LaptopWise returns an estimated market price.

### Check a Deal

Enter the laptop specifications together with the seller's asking price. LaptopWise compares the asking price with the estimated value and reports the difference and deal status.

## How It Works

```text
User
  ↓
Streamlit Frontend
  ↓
API Client
  ↓
FastAPI Backend
  ↓
Production ML Pipeline
  ↓
Prediction / Deal Comparison
  ↓
FastAPI Response
  ↓
Streamlit Result
```

The Streamlit frontend communicates with the FastAPI backend through HTTP requests. The backend uses the saved machine learning pipeline for prediction.

## Machine Learning

**Problem:** Laptop price prediction

**Target:** `Price (Rs)`

**Input features:** 15 selected laptop features covering:

- Brand
- Series
- Thickness
- Weight
- Operating System
- Display Size
- Display Touchscreen
- Processor
- Graphic Processor
- RAM Capacity
- RAM Type
- SSD Capacity
- HDD Capacity
- Battery Capacity
- Fingerprint Scanner

### Final Model

**Ridge Regression**

The final production artifact is a saved pipeline containing the required preprocessing steps and the trained model.

## Tech Stack

- Python
- Pandas
- NumPy
- Scikit-learn
- Matplotlib
- Seaborn
- Jupyter Notebook
- FastAPI
- Uvicorn
- Streamlit
- Requests
- Joblib

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | API health check |
| POST | `/predict` | Estimate laptop price |
| POST | `/compare` | Compare asking price with estimated value |

Interactive API documentation is available through FastAPI's generated documentation when the API is running.

## Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/Sandeep-060/LaptopWise.git
cd LaptopWise
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start FastAPI

```bash
uvicorn api.main:app --reload
```

The API will run at:

```text
http://127.0.0.1:8000
```

### 5. Start Streamlit

Open another terminal with the virtual environment activated:

```bash
streamlit run streamlit_app.py
```

For local use, Streamlit connects to the local FastAPI server by default. For deployment, the API URL is configured separately through Streamlit Secrets.

## Deployment

LaptopWise is deployed as two services:

- **Streamlit:** frontend application
- **Render:** FastAPI backend

The Streamlit application communicates with the deployed FastAPI service through its configured API URL.

## Limitations

- The prediction is an estimate and should not be treated as an exact market price.
- Model performance depends on the quality and coverage of the training data.
- Unseen laptop configurations may have higher prediction uncertainty.

## Future Improvements

- Expand the dataset with more recent laptop listings.
- Improve feature engineering and model performance.
- Add richer deal-analysis insights.
- Add automated application and API tests.

## Author

**Sandeep**

Built as an end-to-end machine learning project covering data preparation, model development, deployment, API development, and frontend integration.
