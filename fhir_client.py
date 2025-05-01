"""
Retrieves and prints information on 5 patients and their observations from a FHIR server.
You can absolutely grab other FHIR resource types like Conditions, Medications, Allergies, Procedures, etc.
They're all exposed just like Patients and Observations.
"""
import requests
from requests.exceptions import Timeout, ConnectionError, RequestException
from pprint import pprint
import sys

FHIR_BASE_URL = "https://hapi.fhir.org/baseR4"


def fetch_fhir_resources(resource_type, query_params=None):
    """
    Fetch FHIR resources from the server.
    Args:
        resource_type (str): FHIR resource type (e.g., 'Patient', 'Observation')
        query_params (dict): Optional query parameters for the request
    Returns:
        list: List of resource entries or empty list on error
    """
    url = f"{FHIR_BASE_URL}/{resource_type}"
    if query_params:
        url += f"?{'&'.join(f'{k}={v}' for k, v in query_params.items())}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json().get("entry", [])
    except Timeout:
        print(f"❌ Error: Request timed out when fetching {resource_type.lower()}. The server took too long to respond.")
        return [] if resource_type != "Patient" else sys.exit(1)
    except ConnectionError:
        print(f"❌ Error: Connection error when fetching {resource_type.lower()}. Check your network connection.")
        return [] if resource_type != "Patient" else sys.exit(1)
    except RequestException as e:
        print(f"❌ Error fetching {resource_type.lower()}: {e}")
        return [] if resource_type != "Patient" else sys.exit(1)


def main():
    print("Fetching patients...")
    patients = fetch_fhir_resources("Patient", {"_count": "5"})

    for entry in patients:
        patient = entry["resource"]
        patient_id = patient["id"]
        name = patient.get("name", [{}])[0]
        full_name = f"{name.get('given', ['?'])[0]} {name.get('family', '?')}"

        print(f"\n🧑 Patient: {full_name} (ID: {patient_id})")

        observations = fetch_fhir_resources("Observation", {"subject": f"Patient/{patient_id}"})
        print(f"  Found {len(observations)} observations.")

        for obs in observations[:3]:  # Limit to 3 for demo
            obs_resource = obs["resource"]
            code = obs_resource.get('code', {}).get('coding', [{}])[0].get('code', 'Unknown')
            value = obs_resource.get("valueQuantity", {}).get("value", "N/A")
            unit = obs_resource.get("valueQuantity", {}).get("unit", "")
            print(f"    🔬 {code}: {value} {unit}")


if __name__ == "__main__":
    main()
