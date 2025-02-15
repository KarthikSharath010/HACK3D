import re

# Define custom password policy rules
PASSWORD_POLICY = {
    "min_length": 8,
    "max_length": 32,
    "require_uppercase": True,
    "require_lowercase": True,
    "require_numbers": True,
    "require_special": True,
    "allowed_special_chars": "!@#$%^&*()-_=+",
}

def enforce_password_policy(password):
    """Check if a password meets the defined policy requirements."""
    
    if len(password) < PASSWORD_POLICY["min_length"]:
        return False, "Password is too short. Must be at least {} characters.".format(PASSWORD_POLICY["min_length"])
    
    if len(password) > PASSWORD_POLICY["max_length"]:
        return False, "Password is too long. Maximum allowed length is {} characters.".format(PASSWORD_POLICY["max_length"])

    if PASSWORD_POLICY["require_uppercase"] and not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter."

    if PASSWORD_POLICY["require_lowercase"] and not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter."

    if PASSWORD_POLICY["require_numbers"] and not re.search(r"\d", password):
        return False, "Password must contain at least one number."

    if PASSWORD_POLICY["require_special"] and not re.search(r"[{}]".format(re.escape(PASSWORD_POLICY["allowed_special_chars"])), password):
        return False, "Password must contain at least one special character from: {}".format(PASSWORD_POLICY["allowed_special_chars"])

    return True, "Password meets all policy requirements."
