import os, json
from flask import Flask, render_template, request, send_from_directory
from fpdf import FPDF
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
app = Flask(__name__)

# Load permit rules
with open("permits.json") as f:
    RULES = json.load(f)

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process():
    user_input = request.form["description"]

    prompt = f"""
    You are PermitPilot, an assistant for homeowners in Santa Monica, California.
    The user describes a project. Output a JSON object with these fields:
    {{
      "project_type": "residential_remodel" or "window_replacement",
      "valuation": number,
      "structural": true or false
    }}
    User: {user_input}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1
    )

    try:
        parsed = json.loads(response.choices[0].message.content)
    except Exception:
        parsed = {"project_type": "residential_remodel", "valuation": 0, "structural": False}

    project_type = parsed.get("project_type", "residential_remodel")
    permit = RULES.get(project_type, RULES["residential_remodel"])

    # Generate PDF summary
    pdf_path = os.path.join("static", "summary.pdf")
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="PermitPilot Summary", ln=True)
    pdf.cell(200, 10, txt=f"Jurisdiction: {permit['jurisdiction']}", ln=True)
    pdf.cell(200, 10, txt=f"Project Type: {project_type}", ln=True)
    pdf.cell(200, 10, txt=f"Estimated Valuation: ${parsed.get('valuation', 0)}", ln=True)
    pdf.cell(200, 10, txt=f"Estimated Fee: ${permit['base_fee']}", ln=True)
    pdf.multi_cell(0, 10, txt=f"Description: {permit['description']}")
    pdf.output(pdf_path)

    return render_template("result.html",
                           permit=permit,
                           parsed=parsed,
                           pdf_file="summary.pdf")

@app.route("/download/<path:filename>")
def download(filename):
    return send_from_directory("static", filename, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
