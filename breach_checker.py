import hashlib
import requests
from pybloom_live import BloomFilter

#  Online Check (HIBP API)
def is_password_breached_online(password):
    sha1_hash = hashlib.sha1(password.encode()).hexdigest().upper()
    prefix, suffix = sha1_hash[:5], sha1_hash[5:]

    response = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}")
    if response.status_code != 200:
        return False  # API request failed

    hashes = (line.split(":") for line in response.text.splitlines())
    return any(suffix == h for h, count in hashes)

#  Offline Check (Bloom Filter)
breached_passwords = BloomFilter(capacity=10000, error_rate=0.01)

# Manually add known breached passwords
for password in ["123456", "password", "qwerty", "letmein", "abc123"]:
    breached_passwords.add(password)

def is_password_breached_offline(password):
    """Checks if the password exists in the local breached list."""
    return password in breached_passwords

#  Final Function: Combines Online & Offline Checks
def is_password_breached(password):
    """Check breach using both offline and online methods."""
    return is_password_breached_offline(password) or is_password_breached_online(password)
