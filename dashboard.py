"""
Flask application that integrates with a FHIR server through OAuth2 to fetch and display
patient data such as conditions, medications, and observations, including vital signs.
"""

import requests
from flask import Flask, redirect, render_template_string, request

app = Flask(__name__)

# SMART Sandbox config (you can change client_id and redirect later)
AUTH_BASE = "https://launch.smarthealthit.org/v/r4/sim/eyJhIjoiMSJ9"  # no /fhir here
FHIR_BASE = f"{AUTH_BASE}/fhir"
CLIENT_ID = "my-smart-app"  # Use this for public sandbox apps
REDIRECT_URI = "http://localhost:8000/callback"

# Templates (minimal)
home_page = """<h1>Welcome to SMART App</h1><a href='/launch'>Launch App</a>"""
error_page = """<h1>Something went wrong</h1><p>{{ msg }}</p>"""


@app.route("/")
def home():
    return home_page


@app.route("/launch")
def launch():
    # Redirect to SMART auth page
    launch_url = (
        f"{AUTH_BASE}/auth/authorize?"
        f"response_type=code"
        f"&client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&scope=launch patient/*.read openid profile"
        f"&aud={FHIR_BASE}"
        f"&state=xyz"
    )
    return redirect(launch_url)


@app.route("/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return render_template_string(error_page, msg="Missing auth code")

    # Exchange code for access token
    token_url = f"{AUTH_BASE}/auth/token"
    token_response = requests.post(
        token_url,
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI,
            "client_id": CLIENT_ID,
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    token_data = token_response.json()
    access_token = token_data.get("access_token")
    patient_id = token_data.get("patient")

    if not access_token or not patient_id:
        return render_template_string(error_page, msg="Token exchange failed")

    headers = {"Authorization": f"Bearer {access_token}"}

    # Get patient
    patient = requests.get(f"{FHIR_BASE}/Patient/{patient_id}", headers=headers).json()
    name = patient.get("name", [{}])[0]
    full_name = f"{name.get('given', ['?'])[0]} {name.get('family', '?')}"

    # Get conditions
    conditions = (
        requests.get(f"{FHIR_BASE}/Condition?patient={patient_id}", headers=headers)
        .json()
        .get("entry", [])
    )
    cond_list = [
        c["resource"]["code"]["text"] for c in conditions if "code" in c["resource"]
    ]
    cond_list.sort()

    # Get medications
    meds = (
        requests.get(
            f"{FHIR_BASE}/MedicationRequest?patient={patient_id}", headers=headers
        )
        .json()
        .get("entry", [])
    )
    med_list = [
        m["resource"]["medicationCodeableConcept"]["text"]
        for m in meds
        if "medicationCodeableConcept" in m["resource"]
    ]
    med_list.sort()

    # Get observations
    obs = (
        requests.get(f"{FHIR_BASE}/Observation?patient={patient_id}", headers=headers)
        .json()
        .get("entry", [])
    )
    obs_list = []

    for o in obs:
        res = o["resource"]
        code = res.get("code", {}).get("text", "Unknown")

        val = res.get("valueQuantity", {}).get("value")
        unit = res.get("valueQuantity", {}).get("unit", "")

        if val is not None:
            obs_list.append({"label": code, "value": f"{val} {unit}"})

    # Sort obs_list by label (alphabetically)
    obs_list.sort(key=lambda x: x["label"].lower())

    return render_template_string(
        """
    <html>
    <head>
    </head>
    <body>
        <h1>👋 Hello, {{ name }}</h1>
        <p> Patient ID: {{ patient_id }}</p>
        <h2>🩺 Conditions</h2>
        <ul>{% for item in conditions %}<li>{{ item }}</li>{% endfor %}</ul>

        <h2>💊 Medications</h2>
        <ul>{% for item in medications %}<li>{{ item }}</li>{% endfor %}</ul>

        <h2>🔬 Observations</h2>
        <ul>{% for item in observations %}<li>{{ item["label"] }}: {{ item["value"] }}</li>{% endfor %}</ul>
    </body>
    </html>
    """,
        name=full_name,
        conditions=cond_list,
        medications=med_list,
        observations=obs_list,
        patient_id=patient_id,
    )


if __name__ == "__main__":
    app.run(port=8000, debug=True)
