import os
import json
from flask import Flask, render_template, request, send_from_directory
from fpdf import FPDF
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load permit rules
with open("permits.json", "r") as f:
    RULES = json.load(f)


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/process", methods=["POST"])
def process():
    user_input = request.form["description"]

    prompt = f"""
    You are PermitPilot, an assistant for homeowners in Santa Monica, California.
    The user describes a project. Output a valid JSON object with the following keys:
    {{
        "project_type": "residential_remodel" or "window_replacement",
        "valuation": number (estimated cost in USD),
        "structural": true or false
    }}
    User description: {user_input}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
        )
        # Extract and parse JSON safely
        message_content = response.choices[0].message.content.strip()
        parsed = json.loads(message_content)
    except Exception as e:
        print("Error parsing model output:", e)
        parsed = {
            "project_type": "residential_remodel",
            "valuation": 0,
            "structural": False,
        }

    project_type = parsed.get("project_type", "residential_remodel")
    permit = RULES.get(project_type, RULES["residential_remodel"])

    # --- Generate PDF summary ---
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="PermitPilot Summary", ln=True)
    pdf.cell(200, 10, txt=f"Jurisdiction: {permit['jurisdiction']}", ln=True)
    pdf.cell(200, 10, txt=f"Project Type: {project_type}", ln=True)
    pdf.cell(200, 10, txt=f"Estimated Valuation: ${parsed.get('valuation', 0)}", ln=True)
    pdf.cell(200, 10, txt=f"Estimated Fee: ${permit['base_fee']}", ln=True)
    pdf.multi_cell(0, 10, txt=f"Description: {permit['description']}")
    pdf_path = os.path.join("static", "summary.pdf")
    pdf.output(pdf_path)

    return render_template(
        "result.html",
        permit=permit,
        parsed=parsed,
        pdf_file="summary.pdf",
    )


@app.route("/download/<path:filename>")
def download(filename):
    return send_from_directory("static", filename, as_attachment=True)


if __name__ == "__main__":
    # For Replit hosting
    app.run(host="0.0.0.0", port=8080, debug=True)
