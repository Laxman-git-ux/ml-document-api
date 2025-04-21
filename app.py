from flask import Flask, request, jsonify
import base64

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process_document():
    data = request.json
    print("Received data:", data)

    filename = data.get('filename')
    file_content_base64 = data.get('fileContent')

    # Decode base64 to bytes (optional: save, analyze, OCR, etc.)
    file_bytes = base64.b64decode(file_content_base64)

    # Demo response structure to match Apex expectations
    result = {
        "documentType": "Contract",
        "validationScore": 0.92,
        "missingFields": "Signature Date",
        "signatureDetected": True,
        "expiryIssuesFound": False,
        "detectedExpiryFields": "2025-12-31"
    }

    return jsonify(result), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
