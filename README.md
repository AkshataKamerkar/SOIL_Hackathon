# 🌍 TwinMetricsAI

**TwinMetricsAI** is an end-to-end **Machine Learning web application** that predicts a country’s  
**Human Development Index (HDI)** and **Happiness Index** using socio-economic indicators.  
The application is built with **Streamlit** and powered by **robust ensemble ML models**, designed for stability, generalization, and real-world deployment.

---

## 📌 Overview

| Model               | Task Type      | Output                |
| ------------------- | -------------- | --------------------- |
| **HDI Prediction**  | Regression     | HDI Score (0–1)       |
| **Happiness Index** | Classification | Happiness Level (1–8) |

---

## Training Notebooks

All the Data PreProcessing and Model Training Notebooks are present in the `notebooks/` directory

- SOIL_HACKATHON_CLASSIFICATION.ipynb
- SOIL_HACKATHON_DATA_PROCESSING.ipynb
- SOIL_HACKATHON_REGRESSION.ipynb

# Run the Notebooks

```
1. Run SOIL_HACKATHON_CLASSIFICATION.ipynb -> Get the DataSet
2. Use that DataSet to Run SOIL_HACKATHON_REGRESSION.ipynb -> Get the Regression Model
3. Use that DataSet to Run SOIL_HACKATHON_DATA_PROCESSING.ipynb -> Get the Classification Model
```

## 📊 Model Performance Summary

### 🔹 HDI Regression (Ensemble Model)

| Metric   | Training | Holdout       | Cross-Validation |
| -------- | -------- | ------------- | ---------------- |
| R² Score | 0.931    | 0.87 ± 0.03   | 0.86 ± 0.02      |
| RMSE     | 0.038    | 0.042 ± 0.008 | 0.043 ± 0.007    |
| MAE      | 0.029    | 0.033 ± 0.006 | 0.034 ± 0.005    |
| MAPE (%) | 4.2%     | 4.8% ± 1.1%   | 5.0% ± 0.9%      |

**Stability & Reliability**

- Coefficient of Variation (CV): **3.1%** → Excellent
- Train–Test Gap: **5.4%** → Low Overfitting
- Prediction Stability: **97.2%** → Very Stable

---

### 🔹 Happiness Classification (Model Comparison)

| **Model**                 | **Test Accuracy** | **F1 Score** | **Overfit Gap** |
| ------------------------- | ----------------- | ------------ | --------------- |
| **Extra Trees (Tuned)**   | **94.87%**        | **91.90%**   | 7.69%           |
| **Voting Ensemble**       | 92.31%            | 91.59%       | 7.69%           |
| **SVM (Tuned)**           | 89.74%            | 89.86%       | **6.33%**       |
| **Stacking Ensemble**     | 89.74%            | 89.24%       | 7.64%           |
| **XGBoost (Tuned)**       | 84.62%            | 84.49%       | 15.38%          |
| **Random Forest (Tuned)** | 79.49%            | 80.16%       | 18.55%          |

**Key Observations**

- **Best Overall Classifier:** Extra Trees (highest accuracy & F1 with controlled overfitting)
- **Most Stable Model:** SVM (lowest overfit gap)
- **Ensemble methods** consistently outperform individual learners

---

## 🚀 Live Deployment

**Deployed Application:**  
👉 https://soilhackathon-team-datageeks.streamlit.app/

> The application is **LIVE**, interactive, and ready for real-time predictions.

**GitHub Repo Link:**
👉 https://github.com/AkshataKamerkar/SOIL_Hackathon

---

## 📁 Project Structure

```text
├── app/
│   ├── assets/
│   │   └── styles.css            # Custom UI styling
│   ├── main.py                   # Streamlit app entry point
│   ├── config.py                 # Configuration
│   ├── components/
│   │   ├── visualizations.py     # Charts & plots
│   │   ├── result_cards.py       # Prediction summaries
│   │   └── input_forms.py        # User inputs
│   └── models/
│       ├── feature_engineering.py
│       ├── model_loader.py
│       └── predictor.py
├── saved_models/
│   ├── classification/           # Happiness models
│   └── regression/               # HDI models
├── data/
│   ├── Original_dataset.csv
│   └── Cleaned_dataset.xlsx
├── requirements.txt
└── README.md
```

## 🚀 Installation

# Clone repo

```
git clone https://github.com/AkshataKamerkar/SOIL_Hackathon.git
```

```
cd soil_hackathon_app
```

# Create virtual environment

```python -m venv venv
source venv/bin/activate # Windows: venv\Scripts\activate
```

# Install dependencies

```
pip install -r requirements.txt
```

# Run app

```
streamlit run app/main.py
```

Open: http://localhost:8501

---

## Running Application Directly from the Folder

# Install dependencies

```
pip install -r requirements.txt
```

# Run app

```
streamlit run app/main.py
```

Open: http://localhost:8501

---

## 📦 Requirements

```
streamlit>=1.28.0
pandas>=2.0.0
numpy>=1.24.0
scikit-learn>=1.3.0
joblib>=1.3.0
plotly>=5.17.0
statsmodels>=0.14.0
```

---

## 🤖 Model Files

**Classification:** saved_models/classification/

- model.joblib
- scaler.joblib
- label_encoder.joblib
- feature_names.json

**Regression:** saved_models/regression/

- hdi_model_v51.joblib

---

## 🛠 Troubleshooting

| Issue            | Solution                                     |
| ---------------- | -------------------------------------------- |
| Module not found | pip install -r requirements.txt              |
| Port in use      | streamlit run app/main.py --server.port 8502 |

---

## 👥 Team

**Team DATAGEEKS**
