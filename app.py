import spacy
from flask import Flask, request, jsonify

app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")

@app.route('/process', methods=['POST'])
def process_document():
    data = request.json
    print("Received data:", data)

    content = data.get("fileContent", "")  # Assume base64, decode for real use

    # For now, pretend content is plain text
    decoded_text = "This is a contract between ABC Corp and XYZ Ltd. It expires on 2025-12-31."

    doc = nlp(decoded_text)

    # Basic logic to detect if it's a contract
    is_contract = any("contract" in token.text.lower() for token in doc)

    # Extract named entities
    entities = [{"text": ent.text, "label": ent.label_} for ent in doc.ents]

    response = {
        "documentType": "Contract" if is_contract else "Other",
        "signatureDetected": "sign" in decoded_text.lower(),
        "expiryIssuesFound": not any(ent.label_ == "DATE" for ent in doc.ents),
        "validationScore": round(0.75 + 0.1 * is_contract, 2),
        "detectedExpiryFields": ", ".join(ent.text for ent in doc.ents if ent.label_ == "DATE"),
        "missingFields": None if is_contract else "Contract terms"
    }

    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
