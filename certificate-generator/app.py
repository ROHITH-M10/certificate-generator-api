from flask import Flask, request, jsonify
import fitz  # PyMuPDF
import os

app = Flask(__name__)

TEMPLATE_PATH = "certificate_template.pdf"
OUTPUT_DIR = "generated_certificates"
NAME_POSITION = (200, 300)
ROLL_POSITION = (200, 350)

os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.route("/generate", methods=["POST"])
def generate_certificate():
    data = request.json
    name = data.get("name")
    roll = data.get("roll")

    if not name or not roll:
        return jsonify({"error": "Missing name or roll"}), 400

    output_path = os.path.join(OUTPUT_DIR, f"{roll}_{name}.pdf")

    # Avoid regenerating same file
    if os.path.exists(output_path):
        return jsonify({"status": "already exists"})

    doc = fitz.open(TEMPLATE_PATH)
    page = doc[0]
    page.insert_text(NAME_POSITION, name, fontsize=20, fill=(0, 0, 0))
    page.insert_text(ROLL_POSITION, roll, fontsize=20, fill=(0, 0, 0))
    doc.save(output_path)
    doc.close()

    return jsonify({"status": "generated", "file": f"{roll}_{name}.pdf"})
