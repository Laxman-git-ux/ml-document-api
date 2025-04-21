from flask import Flask, request, jsonify

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
    app.run(debug=True)
