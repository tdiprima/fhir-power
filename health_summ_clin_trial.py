"""
Retrieves patient data from FHIR server and generates a health summary and clinical trial recommendations.
"""
import requests
import os
import json
from openai import OpenAI

# FHIR server URL (using a public test server with fake data)
FHIR_SERVER = "http://hapi.fhir.org/baseR4"


# Function to query FHIR server for patient data
def query_fhir_patient(patient_id):
    try:
        url = f"{FHIR_SERVER}/Patient/{patient_id}"
        print(f"Querying patient data: {url}")
        response = requests.get(url, headers={"Accept": "application/fhir+json"})
        if response.status_code == 200:
            data = response.json()
            print(f"Successfully retrieved patient data for {patient_id}")
            return data
        else:
            return {"error": f"Failed to fetch patient data: {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}


# Function to query FHIR server for discharge summaries (Observation resources)
def query_fhir_discharge_summary(patient_id):
    try:
        url = f"{FHIR_SERVER}/Observation?patient={patient_id}&category=discharge-summary"
        print(f"Querying discharge summaries: {url}")
        response = requests.get(url, headers={"Accept": "application/fhir+json"})
        if response.status_code == 200:
            data = response.json()
            print(f"Found {data.get('total', 0)} discharge summaries")
            return data
        else:
            return {"error": f"Failed to fetch discharge summary: {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}


# Function to search for clinical trials based on patient condition
def search_clinical_trials(condition):
    # Mock implementation (replace with real clinical trial API like ClinicalTrials.gov)
    mock_trials = {
        "diabetes": [
            {"id": "NCT123456", "title": "Type 2 Diabetes Drug Trial", "eligibility": "Age 18-65, diagnosed with Type 2 Diabetes"},
            {"id": "NCT789012", "title": "Insulin Pump Study", "eligibility": "Age 30-70, Type 1 or 2 Diabetes"}
        ],
        "hypertension": [
            {"id": "NCT345678", "title": "Hypertension Medication Study", "eligibility": "Age 40-80, diagnosed with Hypertension"}
        ]
    }
    return mock_trials.get(condition.lower(), [])


# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Function to generate health summary and clinical trial recommendations
def generate_health_summary(patient_data, conditions):
    # Prepare patient info
    patient_name = "Unknown"
    if "name" in patient_data and patient_data["name"]:
        name_parts = []
        if "given" in patient_data["name"][0]:
            name_parts.extend(patient_data["name"][0]["given"])
        if "family" in patient_data["name"][0]:
            name_parts.append(patient_data["name"][0]["family"])
        patient_name = " ".join(name_parts)
    
    patient_id = patient_data.get("id", "Unknown")
    
    # Format patient data for better readability
    formatted_patient_data = json.dumps(patient_data, indent=2)
    
    # Create prompt based on available conditions
    if conditions:
        prompt = f"""
        You are a healthcare assistant that helps process patient data and match patients to clinical trials.
        
        Patient Information:
        - ID: {patient_id}
        - Name: {patient_name}
        - Conditions: {', '.join(conditions)}
        
        Please provide:
        1. A brief discharge summary based on the conditions
        2. Recommendations for clinical trials that might be relevant for this patient
        3. Any general health advice based on the conditions
        
        Format your response in clear sections with headings.
        """
    else:
        prompt = f"""
        You are a healthcare assistant that helps process patient data and match patients to clinical trials.
        
        Patient Information:
        - ID: {patient_id}
        - Name: {patient_name}
        - No specific conditions found in records
        
        Please provide:
        1. A general health summary based on limited information
        2. Suggestions for common clinical trials that might be relevant for general health screening
        3. General health advice and preventive care recommendations
        
        Format your response in clear sections with headings.
        """
    
    # Call OpenAI API directly
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            temperature=0.2,
            messages=[
                {"role": "system", "content": "You are a helpful healthcare assistant with expertise in medical data and clinical trials."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating health summary: {str(e)}"


# Main function to process FHIR data and generate output
async def main():
    # Example patient ID (use a valid ID from the test server)
    patient_id = "597065"  # Replace with a real ID from hapi.fhir.org
    
    # Step 1: Fetch patient data
    patient_data = query_fhir_patient(patient_id)
    if "error" in patient_data:
        print(f"Error fetching patient data: {patient_data['error']}")
        return
    
    # Step 2: Fetch discharge summary
    discharge_data = query_fhir_discharge_summary(patient_id)
    if "error" in discharge_data:
        print(f"Error fetching discharge summary: {discharge_data['error']}")
        return
    
    # Step 3: Extract conditions from discharge summary (mock parsing)
    conditions = []
    if "entry" in discharge_data and discharge_data["entry"]:
        for entry in discharge_data["entry"]:
            resource = entry.get("resource", {})
            if resource.get("code", {}).get("text"):
                conditions.append(resource["code"]["text"].lower())
    else:
        print(f"No discharge summaries found for patient {patient_id}")
        # If no discharge data, check if we can extract any conditions from patient data
        if "condition" in patient_data:
            for condition in patient_data["condition"]:
                if condition.get("code", {}).get("text"):
                    conditions.append(condition["code"]["text"].lower())
    
    # Step 4: Use OpenAI to process and match clinical trials
    print("\nGenerating health summary and clinical trial recommendations...\n")
    summary = generate_health_summary(patient_data, conditions)
    print("\nHealth Summary and Recommendations:")
    print(summary)

# Run the script
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
