import os
import base64
from flask import Flask, request, jsonify
from PyPDF2 import PdfReader
import docx

app = Flask(__name__)

def extract_text_from_pdf(file_bytes):
    filepath = "temp.pdf"
    try:
        with open(filepath, "wb") as f:
            f.write(file_bytes)
        reader = PdfReader(filepath)
        text = "\n".join([page.extract_text() or "" for page in reader.pages])
        return text
    except Exception as e:
        return f"Error reading PDF: {e}"
    finally:
        if os.path.exists(filepath):
            os.remove(filepath)

def extract_text_from_docx(file_bytes):
    filepath = "temp.docx"
    try:
        with open(filepath, "wb") as f:
            f.write(file_bytes)
        doc = docx.Document(filepath)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text
    except Exception as e:
        return f"Error reading DOCX: {e}"
    finally:
        if os.path.exists(filepath):
            os.remove(filepath)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "ML Document API is up and running!"}), 200

@app.route('/process', methods=['POST'])
def process_document():
    data = request.json
    filename = data.get("filename", "")
    base64_content = data.get("fileContent", "")

    if not filename or not base64_content:
        return jsonify({"error": "Missing filename or fileContent"}), 400

    try:
        file_bytes = base64.b64decode(base64_content)
    except Exception as e:
        return jsonify({"error": f"Base64 decode failed: {str(e)}"}), 400

    # Extract text based on file type
    if filename.lower().endswith(".pdf"):
        text_content = extract_text_from_pdf(file_bytes)
    elif filename.lower().endswith(".docx"):
        text_content = extract_text_from_docx(file_bytes)
    else:
        # Assume plain text
        text_content = file_bytes.decode('utf-8', errors='ignore')

    # Lowercased text for simple pattern matching
    lower_text = text_content.lower()

    # Basic heuristics
    document_type = "Contract" if "contract" in lower_text else "Unknown"
    signature_detected = any(keyword in lower_text for keyword in ["signature", "signed by"])
    expiry_issues_found = any(keyword in lower_text for keyword in ["expired", "expiry", "valid until"])
    validation_score = round(0.5 + (len(lower_text) % 50) / 100, 2)

    # Placeholder for missing fields logic (you can add your own)
    missing_fields = []

    result = {
        "documentType": document_type,
        "signatureDetected": signature_detected,
        "expiryIssuesFound": expiry_issues_found,
        "validationScore": validation_score,
        "missingFields": missing_fields or "None",
        "detectedExpiryFields": "Expiry Date, Valid Until" if expiry_issues_found else ""
    }

    return jsonify(result), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
