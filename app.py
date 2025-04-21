from flask import Flask, request, jsonify
from PIL import Image
from io import BytesIO
import pytesseract
import base64
import spacy

app = Flask(__name__)

# Load spaCy NLP model
nlp = spacy.load("en_core_web_sm")

@app.route('/process', methods=['POST'])
def process_document():
    data = request.get_json()
    filename = data.get("filename", "unknown")
    file_content = data.get("fileContent", "")

    # Decode base64 to image
    try:
        image_data = base64.b64decode(file_content)
        image = Image.open(BytesIO(image_data))
        text = pytesseract.image_to_string(image)
    except Exception as e:
        return jsonify({"error": f"Failed to decode/process file: {str(e)}"}), 400

    # NLP processing
    doc = nlp(text)
    people = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
    dates = [ent.text for ent in doc.ents if ent.label_ == "DATE"]

    result = {
        "documentType": "Detected: Offer Letter" if "offer" in text.lower() else "General Document",
        "validationScore": round(len(people) / 5, 2),  # Dummy logic
        "missingFields": "Name, Passport No" if len(people) < 2 else "",
        "signatureDetected": "signature" in text.lower(),
        "expiryIssuesFound": any("2020" in d or "expired" in d.lower() for d in dates),
        "detectedExpiryFields": ", ".join(dates)
    }

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
