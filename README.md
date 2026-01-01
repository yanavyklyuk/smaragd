# Backend Smaragd

Backend API for СмарагдМед - a medical risk prediction system.
This service manages patient data and provides ML-based predictions for postoperative outcomes using FastAPI and Scikit-learn.

## Tech Stack

- **Python 3.10+**
- **FastAPI** - High-performance web framework
- **SQLAlchemy** - ORM for database interactions
- **SQLite** - Embedded database (stored in `database/smaragd.db`)
- **Pydantic** - Data validation and settings management
- **Scikit-learn / Joblib** - ML model loading and inference
- **SHAP** - Model explainability (feature contribution)

## Project Structure

```text
smaragd/
├── backend/
│   ├── controllers/      # Business logic handlers
│   ├── models/           # SQLAlchemy models & Pydantic schemas
│   ├── routers/          # API endpoints definition
│   ├── services/         # ML inference & DB services
│   ├── config.py         # Database & App configuration
│   └── main.py           # Application entry point
├── database/             # SQLite database storage
│   └── smaragd.db
├── ml_models/            # Serialized ML models (.pkl)
│   ├── model_hospitalisation.pkl
│   └── model_complication.pkl
├── requirements.txt      # Project dependencies
└── README.md

```

## Getting Started

### 1. Prerequisites

* Python 3.10 or higher installed.

### 2. Installation

Clone the repository and navigate to the project root:

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

```

Install the required dependencies:

```bash
pip install -r requirements.txt

```

### 3. Database Setup

The project uses **SQLite**. The database file is automatically created at `database/smaragd.db` upon the first run if it doesn't exist.

Tables are initialized automatically via SQLAlchemy in `main.py`.

### 4. Running the Application

Make sure you are in the root directory (`smaragd/`) so that python can resolve the `backend` package imports.

Start the server using Uvicorn:

```bash
uvicorn backend.main:app --reload

```

The API will be available at `http://localhost:8000`.

## API Documentation

Interactive API documentation is automatically generated:

* **Swagger UI:** [http://localhost:8000/docs](https://www.google.com/search?q=http://localhost:8000/docs)
* **ReDoc:** [http://localhost:8000/redoc](https://www.google.com/search?q=http://localhost:8000/redoc)

## Features

### Patient Management (`/patients`)

* Full CRUD operations for patient data.
* Search patients by name.
* Data persistence using SQLite.

### ML Analysis (`/ml`)

The system uses pre-trained models located in `ml_models/`.

#### Hospitalization Risk (`/ml/hospitalization/`)

* **Predict:** Estimates risk of prolonged hospitalization.
* **Explain:** Returns SHAP values showing which features influenced the decision.

#### Complications Risk (`/ml/complications/`)

* **Predict:** Estimates risk of pulmonary complications.
* **Explain:** Feature contribution analysis.

## Machine Learning Details

* **Model Loading:** Models are loaded lazily/globally in `backend/services/ml_service.py` using `joblib`.
* **Data Preprocessing:** Input data is mapped from English Pydantic models to Cyrillic feature names expected by the models (via `COLUMN_MAPPING`).
* **Explainability:** Uses `shap.LinearExplainer` to provide transparency for medical decisions.
