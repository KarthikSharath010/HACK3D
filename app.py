from flask import Flask, request, jsonify
from flask_cors import CORS  

from password_checker import check_password_strength
from policy_enforcer import enforce_password_policy
from breach_checker import is_password_breached

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/check_password', methods=['POST'])
def check_password():
    data = request.json  # Extract JSON data from request
    password = data.get("password")  # Get the password input

    if not password:  # If no password is provided, return an error
        return jsonify({"error": "Password is required"}), 400

    strength = check_password_strength(password)  # Check strength using zxcvbn
    policy_status, policy_message = enforce_password_policy(password)  # Enforce password policy
    breached = is_password_breached(password)  # Check if the password is leaked

    return jsonify({  
        "strength": strength,
        "policy_compliance": {"valid": policy_status, "message": policy_message},
        "breached": breached
    })

if __name__ == "__main__":
    app.run(debug=True)