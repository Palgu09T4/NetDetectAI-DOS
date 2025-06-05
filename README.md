# NetDetectAI-DOS
# NetDetectAI-DoS 🚀
**AI-Powered DoS Attack Detection System (Web App + ML Model)**

NetDetectAI-DoS is an end-to-end cybersecurity detection system designed to identify Denial of Service (DoS) attacks from network traffic data using machine learning. It includes a comparison of five ML algorithms and a deployed Django-based web application for interactive predictions.

🔗 **Live App**: [https://netdetectai-dos-1.onrender.com](https://netdetectai-dos-1.onrender.com)  
🧠 **Best Algorithm Chosen**: Random Forest  
📓 **Notebook**: `Mini Project G15.ipynb`

---

## 🧠 Machine Learning Models Used

Five machine learning algorithms were trained and evaluated:

- ✅ **Random Forest Classifier** (Best Performance)
- Decision Tree Classifier
- Logistic Regression
- Support Vector Machine (SVM)
- K-Nearest Neighbors (KNN)

The comparison was based on:
- Accuracy (Train/Test)
- Classification report (Precision, Recall, F1)
- Confusion Matrix
- ROC AUC Curves
- Feature Importance

### 📊 Result Summary

| Model              | Accuracy (Test) | ROC AUC Score |
|-------------------|------------------|----------------|
| **Random Forest**  | ✅ Highest       | ✅ Highest      |
| Decision Tree     | Medium          | Good           |
| Logistic Regression | Moderate      | Fair           |
| SVM               | Moderate         | Fair           |
| KNN               | Lower            | Lower          |

---

## 💻 Web Application Features

Built using **Django** + **Chart.js** + **Bootstrap**:

- 📁 Upload a `.csv` file containing network traffic
- 📊 Visualize DoS vs Normal traffic (Pie chart, Bar graph, Time series)
- 🧪 Prediction using Random Forest (best model)
- 📥 Download prediction results as CSV
- 🔐 User Authentication: Sign up, Login, Password Reset
- 📜 Upload history per user

---

## 📂 Dataset Used

- **Source**: Network flow logs (with DoS/Normal labels)
- **Key Features Used**:
  - Flow Duration
  - Flow Bytes/s
  - Fwd/Bwd Packet Count
  - SYN/ACK/RST Flag Count
  - Inter-Arrival Times
  - Flow Packets/s

---

## 🧪 Jupyter Notebook (Exploration & Modeling)

File: `Mini Project G15.ipynb`

Includes:
- EDA (Exploratory Data Analysis)
- Feature Engineering & Scaling
- Model Training & GridSearchCV
- Evaluation (Confusion Matrix, ROC Curves)
- Prediction on unseen test data
- Final CSV export 

---

## 🛠 Tech Stack

| Layer          | Tech Used                               |
|----------------|------------------------------------------|
| Frontend       | HTML, CSS, Bootstrap, Chart.js           |
| Backend        | Django, Django REST Framework            |
| ML Frameworks  | Scikit-learn, Pandas, NumPy, Matplotlib  |
| Deployment     | Render (Free Tier)                       |
| Notebook Env   | Jupyter Notebook                         |

---

## 🚀 How to Run Locally

```bash
# Clone the repo
git clone https://github.com/Palgu09T4/NetDetectAI-DOS.git
cd netdetectai-dos

# Create virtual environment
python -m venv env
source env/bin/activate  # or env\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Run locally
python manage.py runserver
