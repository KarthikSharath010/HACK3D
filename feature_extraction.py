from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import os
import re
import json
import csv
from pdfminer.high_level import extract_text
import ollama

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Ensure the uploads folder exists
UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route("/")
def index():
    """Serve the frontend HTML file."""
    return send_from_directory("templates", "index.html")

@app.route("/upload", methods=["POST"])
def upload():
    """Handle file upload and processing."""
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    if file.filename.endswith(".pdf"):
        # Save the uploaded file
        pdf_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(pdf_path)

        # Process the PDF
        print("🔍 Extracting text from PDF...")
        text = extract_text_from_pdf(pdf_path)

        print("🛡️ Extracting password policies with regex...")
        extracted_policies = extract_policies(text)

        print("🤖 Summarizing policies using Llama (Ollama)...")
        summarized_policies = summarize_policies(extracted_policies)

        print("📌 Mapping extracted policies to structured format...")
        structured_policies = map_policies_to_structure(summarized_policies)

        print("💾 Saving extracted policies as JSON...")
        save_policies_as_json(structured_policies, "extracted_policies2")

        print("💾 Saving extracted policies as CSV...")
        save_policies_as_csv(structured_policies, "extracted_policies2")

        print("✅ Extraction, summarization, and file export complete!")

        # Return the structured policies as JSON
        return jsonify(structured_policies)
    else:
        return jsonify({"error": "File must be a PDF"}), 400

# ... (rest of your code)

if __name__ == "__main__":
    app.run(debug=True)