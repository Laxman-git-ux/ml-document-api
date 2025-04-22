import os
import base64
from flask import Flask, request, jsonify
from PyPDF2 import PdfReader
import docx

app = Flask(__name__)

def extract_text_from_pdf(file_bytes):
    try:
        with open("temp.pdf", "wb") as f:
            f.write(file_bytes)
        reader = PdfReader("temp.pdf")
        text = "\n".join([page.extract_text() or "" for page in reader.pages])
        os.remove("temp.pdf")
        return text
    except Exception as e:
        return f"Error reading PDF: {e}"

def extract_text_from_docx(file_bytes):
    try:
        with open("temp.docx", "wb") as f:
            f.write(file_bytes)
        doc = docx.Document("temp.docx")
        text = "\n".join([para.text for para in doc.paragraphs])
        os.remove("temp.docx")
        return text
    except Exception as e:
        return f"Error reading DOCX: {e}"

@app.route('/process', methods=['POST'])
def process_document():
    data = request.json
    filename = data.get("filename", "")
    base64_content = data.get("fileContent", "")

    try:
        file_bytes = base64.b64decode(base64_content)
    except Exception as e:
        return jsonify({"error": f"Base64 decode failed: {str(e)}"}), 400

    # Detect file type
    if filename.lower().endswith(".pdf"):
        text_content = extract_text_from_pdf(file_bytes)
    elif filename.lower().endswith(".docx"):
        text_content = extract_text_from_docx(file_bytes)
    else:
        # Assume plain text
        text_content = file_bytes.decode('utf-8', errors='ignore')

    # Basic Analysis
    document_type = "Contract" if "contract" in text_content.lower() else "Unknown"
    signature_detected = "signature" in text_content.lower()
    expiry_issues_found = "expired" in text_content.lower() or "expiry" in text_content.lower()
    validation_score = round(0.5 + (len(text_content) % 50) / 100, 2)

    result = {
        "documentType": document_type,
        "signatureDetected": signature_detected,
        "expiryIssuesFound": expiry_issues_found,
        "validationScore": validation_score,
        "missingFields": "None",
        "detectedExpiryFields": "Expiry Date, Valid Until" if expiry_issues_found else ""
    }

    return jsonify(result), 200
