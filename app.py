from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process_document():
    data = request.json  # JSON sent from Salesforce or Postman
    print("Received data:", data)

    # Just for demo: pretend we did ML processing here
    result = {
        "document_type": "Contract",
        "signature_detected": True,
        "expiry_issues_found": False,
        "validation_score": 0.92
    }

    return jsonify(result), 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
