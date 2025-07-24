# FHIR Power ⚡

A collection of Python scripts for working with FHIR (Fast Healthcare Interoperability Resources) servers, designed to demonstrate various healthcare data integration patterns.

## Scripts Overview 🔧

### dashboard.py
**Flask web application with SMART on FHIR integration**

Creates a web dashboard that uses OAuth2 authentication to connect to SMART-enabled FHIR servers and display patient data including conditions, medications, and observations.

**Features:**

- 🔐 OAuth2/SMART authentication flow
- 👤 Patient data retrieval and display
- 🩺 Conditions, medications, and vital signs visualization
- 🌐 Web-based interface

**Run:** `python dashboard.py`  
**Access:** http://localhost:8000

### fhir\_client.py
**Basic FHIR client for patient and observation data**

Retrieves patient information and their associated observations from a public FHIR server, with robust error handling and timeout management.

**Features:**

- 📊 Fetches patient data and observations
- ⚡ Configurable query parameters
- 🛡️ Error handling for network issues
- 📋 Formatted output with emojis

**Run:** `python fhir_client.py`

### health\_summ\_clin_trial.py
**AI-powered health summary and clinical trial matching**

Uses OpenAI's API to generate health summaries from FHIR patient data and suggest relevant clinical trials based on patient conditions.

**Features:**

- 🤖 OpenAI integration for health summaries
- 🔬 Clinical trial recommendations
- 📄 Discharge summary processing
- 💡 General health advice generation

**Requirements:**

- OpenAI API key: `export OPENAI_API_KEY=your_key_here`

**Run:** `python health_summ_clin_trial.py`

### local\_fhir_test.py
**Simple local FHIR server testing script**

Minimal script for testing connectivity to a local FHIR server installation.

**Features:**

- 🏠 Local FHIR server testing
- ⚙️ Basic patient data retrieval
- 🔧 Configurable server endpoints

**Run:** `python local_fhir_test.py`

## Supporting Files 📁

### visualize_fhir.html
Interactive D3.js visualization showing FHIR data structure relationships between Patient, Encounter, Observation, Condition, MedicationRequest, and Procedure resources.

**Open:** Open in web browser directly

### patient_ids.json
Sample patient IDs and basic information for testing purposes.

### docs/
Documentation folder containing:

- `Smart-and-FHIR.md` - SMART on FHIR implementation guide
- `common_errors.md` - Common FHIR integration errors and solutions
- `hapi_server_error_fix.md` - HAPI FHIR server troubleshooting

## Quick Start 🚀

1. **Install dependencies:**

   ```bash
   pip install requests flask openai
   ```

2. **For basic FHIR exploration:**

   ```bash
   python fhir_client.py
   ```

3. **For web dashboard:**

   ```bash
   python dashboard.py
   # Visit http://localhost:8000
   ```

4. **For AI-powered analysis (requires OpenAI API key):**

   ```bash
   export OPENAI_API_KEY=your_key_here
   python health_summ_clin_trial.py
   ```

## FHIR Servers Used 🏥

- **Public Test Server:** `https://hapi.fhir.org/baseR4`
- **SMART Sandbox:** `https://launch.smarthealthit.org/v/r4/sim/`
- **Local Development:** `http://localhost:8080/fhir`

## License 📜

See [LICENSE](LICENSE) file for details.

<br>
