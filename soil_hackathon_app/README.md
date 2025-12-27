# 🌍 Global Development Predictor

Machine Learning application to predict **HDI** and **Happiness Index** using Streamlit.

---

## 📌 Overview

| Model                    | Type           | Output          |
| ------------------------ | -------------- | --------------- |
| HDI Prediction           | Regression     | HDI Score (0-1) |
| Happiness Classification | Classification | Level (1-8)     |

---

## 📁 Project Structure

\`\`\`
ml_streamlit_app/
├── app/
│ ├── main.py # Main application
│ ├── config.py # Configuration
│ └── components/
│ ├── visualizations.py # Charts
│ └── input_forms.py # Input forms
├── saved_models/
│ ├── classification/ # Happiness model files
│ └── regression/ # HDI model files
├── data/
│ └── sample_dataset.csv # Dataset
├── requirements.txt
└── README.md
\`\`\`

---

## 🚀 Installation

\`\`\`bash

# Clone repo

git clone https://github.com/yourusername/ml_streamlit_app.git
cd ml_streamlit_app

# Create virtual environment

python -m venv venv
source venv/bin/activate # Windows: venv\Scripts\activate

# Install dependencies

pip install -r requirements.txt

# Run app

streamlit run app/main.py
\`\`\`

Open: http://localhost:8501

---

## 📦 Requirements

\`\`\`
streamlit>=1.28.0
pandas>=2.0.0
numpy>=1.24.0
scikit-learn>=1.3.0
joblib>=1.3.0
plotly>=5.17.0
statsmodels>=0.14.0
\`\`\`

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
