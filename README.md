# 🔐 AI-Powered Password Security System

A smart password security tool that monitors and flags weak, reused, or compromised passwords using AI and custom policies.

## 🚀 Features
- ✅ AI-based password strength analysis  
- 🔍 Breach detection & risk-based policy enforcement  
- 🔄 Local offline breach checking  
- 📊 Enterprise directory integration for policy enforcement  

## 📦 Installation

Clone the repository:
```
git clone https://github.com/yourusername/password-security-ai.git
cd password-security-ai
```

Install dependencies:
```
pip install -r requirements.txt
```

## 🛠 Usage

Start the Flask server:
```
python app.py
```

Send a password for analysis via API:
```
curl -X POST http://127.0.0.1:5000/check_password -d "password=yourpassword"
```

## 🖥 Tech Stack
- **Backend:** Python, Flask, Scikit-Learn  
- **AI Model:** Logistic Regression for password strength prediction  
- **Security Tools:** Local breach checking, risk assessment  

## ⚠️ Common Issues & Fixes
### ❌ CORS Error: "Blocked by CORS policy"
If you're making API requests from a frontend or another domain, you might see a CORS error.

Fix: Install Flask-CORS and enable it in your app:

Install Flask-CORS:

```
pip install flask-cors
```

Add this to app.py:

```
from flask_cors import CORS
CORS(app)
```
Restart the Flask server after making these changes.

### ❌ Flask API Not Responding
- Ensure that the Flask server is running (`python app.py`).
- If using a different port, update the API URL accordingly.
