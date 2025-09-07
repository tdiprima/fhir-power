"""
docker pull hapiproject/hapi:latest

docker run -d \
    --name myhapi \
    -p 8080:8080 \
    hapiproject/hapi:latest
"""
import requests

# BASE = "http://localhost:8080/baseR4"   # or "/fhir"
BASE = "http://localhost:8080/fhir"
params = {"_count": 5}

r = requests.get(f"{BASE}/Patient", params=params)
r.raise_for_status()
bundle = r.json()
print(bundle)
