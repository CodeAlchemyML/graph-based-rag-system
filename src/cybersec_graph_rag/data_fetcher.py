import os
from dotenv import load_dotenv
import requests

load_dotenv()
nvd_api_key = os.getenv("NVD_API_KEY")

def fetch_nvd_data():
    url = "https://services.nvd.nist.gov/rest/json/cves/1.0"
    headers = {
        'apiKey': nvd_api_key
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    
    else:
        print(f"Error {response.status_code}: {response.text}")
        raise Exception("Failed to fetch data NVD Data: {response.status_code} - {response.text}")

def parse_nvd_data(data):
    entities = []
    relations = []

    for item in data['result']['CVE_Items']:
        cve_id = item['cve']['CVE_data_meta']['ID']
        description = item['cve']['description']['description_data'][0]['value']
        
        entities.append({
            'name': cve_id,
            'type': 'Vulnerability',
            'description': description
        })

        for node in item.get('configurations', {}).get('nodes', []):
            if 'cpe_match' in node:
                for match in node['cpe_match']:
                    if match['vulnerable']:
                        software = match['cpe23Uri']
                        relations.append({
                            'source': cve_id,
                            'target': software,
                            'type': 'Affects'
                        })

    return entities, relations