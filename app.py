from flask import Flask, request, jsonify
import base64

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process_document():
    data = request.json
    print("Received data:", data)

    filename = data.get("filename")
    base64_content = data.get("fileContent")

    # Decode the content for basic text analysis
    try:
        file_bytes = base64.b64decode(base64_content)
        text_content = file_bytes.decode('utf-8', errors='ignore')
    except Exception as e:
        return jsonify({"error": f"Failed to decode file: {str(e)}"}), 400

    # 🔍 Basic content analysis (replace with real ML later)
    document_type = "Contract" if "contract" in text_content.lower() else "Unknown"
    signature_detected = "signature" in text_content.lower()
    expiry_issues_found = "expired" in text_content.lower() or "expiry" in text_content.lower()

    # Simulate some validation score
    validation_score = round(0.5 + (len(text_content) % 50) / 100, 2)

    # Build the smart response
    result = {
        "documentType": document_type,
        "signatureDetected": signature_detected,
        "expiryIssuesFound": expiry_issues_found,
        "validationScore": validation_score,
        "missingFields": "None",
        "detectedExpiryFields": "Expiry Date, Valid Until" if expiry_issues_found else ""
    }

    return jsonify(result), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
