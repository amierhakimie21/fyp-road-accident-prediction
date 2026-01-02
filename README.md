# 🚗 Road Accident Severity Prediction System

This project is developed as part of a **Final Year Project (FYP)**.  
The system predicts **road accident severity** using machine learning techniques
based on historical road accident data and driving conditions.

The main objective of this project is to provide a **decision-support tool**
that helps users understand potential accident severity and promotes safer
driving behaviour.

---

## 🎯 Project Objectives
- To analyse historical road accident data
- To predict accident severity (Slight, Serious, Fatal) using machine learning
- To develop a user-friendly web application for accident severity assessment
- To support road safety awareness through data-driven insights

---

## 🔍 System Features
- Accident severity prediction based on driving and environmental conditions
- Clear and user-friendly web interface
- Probability-based confidence display
- Visual explanation of prediction results
- Safety recommendations for drivers
- Suitable for academic and demonstration purposes

---

## 🧠 Machine Learning Approach

### Model Type
- **Algorithm**: Random Forest Classifier
- **Learning Type**: Supervised Learning
- **Problem Type**: Multiclass Classification

### Target Variable
- Accident Severity:
  - Slight
  - Serious
  - Fatal

### Input Features
- Year
- Month
- Day of week
- Time of day (hour)
- Weather conditions
- Light conditions
- Road type
- Speed limit
- Urban or rural area
- Road surface conditions

### Model Evaluation
- Hold-out validation accuracy
- 5-Fold cross-validation
- Classification report (Precision, Recall, F1-score)

The model was trained using **real-world accident data** and evaluated
using honest and realistic performance metrics without data leakage.

---

## 🛠️ Technologies Used
- Python
- Streamlit
- Pandas
- scikit-learn
- Altair
- Joblib

---

## ▶️ How to Run the Application (Local)

1. Clone the repository:
```bash
git clone https://github.com/your-username/fyp-road-accident.git
