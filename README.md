# NetDetectAI-DOS

**AI-Powered DoS Attack Detection System**

NetDetectAI-DoS is an end-to-end cybersecurity detection system designed to identify Denial of Service (DoS) attacks from network traffic data using machine learning. It includes a comparison of five ML algorithms and a deployed Django-based web application for interactive predictions.

How It Works

### Data Collection
- Network traffic is captured using **Wireshark** in `.csv` format.

---

### ⚙️ Feature Engineering
- Extracted key flow features such as:
  - 'Flow Duration', 'Flow_Byts/s', 'Tot_Fwd_Pkts', 'Tot_Bwd_Pkts', 
    'Fwd_Pkt_Len_Max', 'Bwd_Pkt_Len_Max', 'Fwd_IAT_Mean', 'Bwd_IAT_Mean',
    'SYN_Flag_Cnt', 'RST_Flag_Cnt', 'ACK_Flag_Cnt', 'Flow_Pkts/s'
- Processed and cleaned using **Pandas** and **NumPy**.

---

### Model Training
- Trained and evaluated multiple machine learning classifiers:
  - ✅ **Random Forest** (best performance)
  - Decision Tree  
  - K-Nearest Neighbors (KNN)  
  - Neural Network  
  - Long Short-Term Memory (LSTM)
- Utilized **Scikit-learn** for modeling and evaluation.

---

## 💻 Web Application Features

Built using **Django** + **Chart.js** + **Bootstrap**:

- Upload a `.csv` file containing network traffic
- Visualize DoS vs Normal traffic 
- Prediction using Random Forest (best model)
- Download prediction results as CSV
- User Authentication: Sign up, Login, Password Reset
-  User history 
    

---

### Deployment
- Deployed using **Render (Free Tier)** with full online functionality.
"""

🔗  
 **Best Algorithm Chosen**: Random Forest  
 **Notebook**: Notebook.ipynb`

---

## Machine Learning Models Used

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

## 📂 Dataset Used
  
- Training Purpose:training_data.csv(updated_dataset.csv in notebook)

   Testing Purpose:test_data.csv
---

## 🧪 Jupyter Notebook (Exploration & Modeling)

File: `Notebook.ipynb`

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
#Web app Screenshots
![Screenshot 2025-06-05 220433](https://github.com/user-attachments/assets/0e3475af-6c58-4ac2-96ed-d3534e7e4358)
![Screenshot 2025-06-05 225733](https://github.com/user-attachments/assets/8e8316c4-d284-4b11-9ebf-48d0837f2d55)
![Screenshot 2025-06-05 220704](https://github.com/user-attachments/assets/07718563-eaad-423f-90c4-44f0b32009cd)
![Screenshot 2025-06-05 221011](https://github.com/user-attachments/assets/f3a089aa-7dbc-4c71-8c1b-0def271d30b5)
![Screenshot 2025-06-05 220554](https://github.com/user-attachments/assets/62578792-3c83-493c-8448-da587b56968f)
![Uploading Screenshot 2025-06-06 000820.png…]()



##  How to Run Locally

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
