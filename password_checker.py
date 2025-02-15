from zxcvbn import zxcvbn
import pickle
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

def check_password_strength(password):
    result = zxcvbn(password)
    return {
        "score": result["score"],  # Strength score (0-4)
        "feedback": result["feedback"]  # Suggestions to improve
    }

# Sample Training Data (Weak and Strong Passwords)
leaked_passwords = ["123456", "password", "qwerty", "abc123", "letmein"]
strong_passwords = ["Gf@9#2Ks!", "Myp@$$w0rd123", "zYxWvUtSrQ9!"]

X_train = leaked_passwords + strong_passwords
y_train = [0] * len(leaked_passwords) + [1] * len(strong_passwords)  # 0 = Weak, 1 = Strong

# Convert passwords into character-based n-grams
vectorizer = CountVectorizer(analyzer='char', ngram_range=(1, 3))
X_train_features = vectorizer.fit_transform(X_train)

# Train the Logistic Regression Model
model = LogisticRegression()
model.fit(X_train_features, y_train)

# Save the model and vectorizer
with open("password_model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)
