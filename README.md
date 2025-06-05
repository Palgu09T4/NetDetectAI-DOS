# NetDetectAI-DOS
# NetDetectAI-DoS 🚀
**AI-Powered DoS Attack Detection System (Web App + ML Model)**

NetDetectAI-DoS is an end-to-end cybersecurity detection system designed to identify Denial of Service (DoS) attacks from network traffic data using machine learning. It includes a comparison of five ML algorithms and a deployed Django-based web application for interactive predictions.

🔗  
🧠 **Best Algorithm Chosen**: Random Forest  
📓 **Notebook**: `Mini Project G15.ipynb`

---

## 🧠 Machine Learning Models Used

Five machine learning algorithms were trained and evaluated:

- ✅ **Random Forest Classifier** (Best Performance)
- Decision Tree Classifier
- K-Nearest Neighbors (KNN)
- Neural Network
- Long short Term memory(LSTM)

The comparison was based on:
- Accuracy (Train/Test)
- Classification report (Precision, Recall, F1)
- Confusion Matrix
- ROC AUC Curves
- Feature Importance

### 📊 Result Summary

| Model                    | Accuracy (Test) | ROC AUC Score                   |
| ------------------------ | --------------- | ------------------------------- |
| **Random Forest**        | ✅ Highest      | ✅ Highest                    |
| Decision Tree Classifier | High            | Good                            |
| K-Nearest Neighbors      | Moderate        | Fair                            |
| Neural Network (MLP)     | Moderate–High   | Fair–Good (if tuned)            |
| Long Short Term Memory   | Variable        | Good (only if time-series data) |


---

## 💻 Web Application Features

Built using **Django** + **Chart.js** + **Bootstrap**:

- 📁 Upload a `.csv` file containing network traffic
- 📊 Visualize DoS vs Normal traffic 
- 🧪 Prediction using Random Forest (best model)
- 📥 Download prediction results as CSV
- 🔐 User Authentication: Sign up, Login, Password Reset
- 📜 User history

---

## 📂 Dataset Used
  
- Training Purpose:training_data.csv
- **Key Features Used**:
  - 'Flow Duration', 'Flow_Byts/s', 'Tot_Fwd_Pkts', 'Tot_Bwd_Pkts', 
    'Fwd_Pkt_Len_Max', 'Bwd_Pkt_Len_Max', 'Fwd_IAT_Mean', 'Bwd_IAT_Mean',
    'SYN_Flag_Cnt', 'RST_Flag_Cnt', 'ACK_Flag_Cnt', 'Flow_Pkts/s'

   Testing Purpose:test_data.csv
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
| Layer           | Tech Used                                          |
| --------------- | -------------------------------------------------- |
| Frontend        | HTML, CSS, Bootstrap, Chart.js                     |
| Backend         | Django, Django REST Framework                      |
| ML Frameworks   | Scikit-learn, Pandas, NumPy, Matplotlib            |
| Data Collection | **Wireshark** (for capturing real network traffic) |
| Notebook Env    | Jupyter Notebook                                   |
| Deployment      | Render (Free Tier)                                 |

---

## 🚀 How to Run Locally

```bash
# Clone the repo
git clone https://github.com/Palgu09T4/NetDetectAI-DOS.git


# Create virtual environment
python -m venv env
source env/bin/activate  # or env\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Run locally
python manage.py runserver
