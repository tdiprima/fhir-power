## 🧠 What You Learned:

### ✅ **FHIR Basics**
- FHIR (Fast Healthcare Interoperability Resources) is like LEGO for healthcare data: patients, meds, vitals — all in neat, structured pieces.
- You can pull FHIR data using simple REST calls — no login needed for public servers.
- [HAPI FHIR public test server](https://hapi.fhir.org/)

#### ✅ What you can do (w/o auth) using HAPI test server:

```python
# Examples of other public resource types you can query
f"{FHIR_BASE_URL}/Condition?subject=Patient/{patient_id}"
f"{FHIR_BASE_URL}/MedicationRequest?subject=Patient/{patient_id}"
f"{FHIR_BASE_URL}/AllergyIntolerance?subject=Patient/{patient_id}"
```

Just like `Observation`, these return bundles of resources — you just `get("entry", [])` and parse.


### ✅ **SMART on FHIR**
- **SMART** = **Substitutable Medical Applications, Reusable Technologies**
- SMART is the secure "front door" to real EHR systems (like Epic, Cerner).
- It uses OAuth2 to authenticate apps and grant controlled access to patient data.
- The [SMART App Launcher](https://launch.smarthealthit.org) simulates the full login + token flow — and yes, it can launch local apps!

#### ✅ **Built a Local SMART App**
- Flask app that:
  - Authenticates with SMART
  - Gets a patient token
  - Pulls patient details, conditions, meds, and observations

#### ✅ **Visualized Vitals**
- Used **Plotly.js** to graph clinical observation data
- Filtered observations to only chart useful types (no more spaghetti lines)

### 🧰 Tools You Used:
- `Flask` for the local web server
- `requests` for hitting FHIR APIs
- `Plotly.js` for front-end charting
- SMART Sandbox (`launch.smarthealthit.org`) for simulation

You're not just poking FHIR anymore — you're talking to it, charting it, and getting real signal from synthetic patient data.

<br>
