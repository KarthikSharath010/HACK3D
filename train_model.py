from flask import Flask, request, jsonify
from flask_cors import CORS  
import joblib
import numpy as np
import string

# Import existing functions
from password_checker import check_password_strength
from policy_enforcer import enforce_password_policy
from breach_checker import is_password_breached

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# 🔹 Load the ML model & scaler
model = joblib.load("password_model.pkl")
scaler = joblib.load("scaler.pkl")  # Load the scaler

print("✅ ML Model & Scaler Loaded!")

# 🔹 Updated Feature Extraction Function (now includes 6 features)
def extract_features(password):
    """Convert password into numerical features (6 features)"""
    length = len(password)
    num_digits = sum(c.isdigit() for c in password)
    num_uppercase = sum(c.isupper() for c in password)
    num_lowercase = sum(c.islower() for c in password)
    num_special = sum(c in string.punctuation for c in password)
    
    # Entropy calculation
    char_set_size = len(set(password))
    entropy = np.log2(char_set_size) * length if length > 0 else 0

    return np.array([length, num_digits, num_uppercase, num_lowercase, num_special, entropy])

# 🔹 API Route to Check Password Security
@app.route('/check_password', methods=['POST'])
def check_password():
    data = request.json  
    password = data.get("password")  

    if not password:  
        return jsonify({"error": "Password is required"}), 400

    # ✅ Strength Analysis (zxcvbn-based)
    strength = check_password_strength(password)  

    # ✅ Custom Policy Enforcement
    policy_status, policy_message = enforce_password_policy(password)  

    # ✅ Breach Check
    breached = is_password_breached(password)  

    # ✅ ML Model Prediction (now using 6 features & scaled input)
    features = extract_features(password).reshape(1, -1)
    print("Extracted feature shape:", features.shape)
    features_scaled = scaler.transform(features)  # Scale the extracted features
    ml_strength = model.predict(features_scaled)[0]

    return jsonify({  
        "zxcvbn_strength": strength,
        "ml_strength": int(ml_strength),  # ML model prediction
        "policy_compliance": {"valid": policy_status, "message": policy_message},
        "breached": breached
    })

if __name__ == "__main__":
    app.run(debug=True)
