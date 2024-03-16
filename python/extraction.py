import requests
import pandas as pd
from io import StringIO

def fetch_data(package_id, idx=None):

    base_url = "https://ckan0.cf.opendata.inter.prod-toronto.ca"
    package_url = f"{base_url}/api/3/action/package_show"
    params = {"id": package_id}
    
    package_response = requests.get(package_url, params=params)
    package_response.raise_for_status()  # Ensure we got a successful response
    package = package_response.json()
    
    resources = package["result"]["resources"]
    
    if idx is not None:
        # Fetch a specific resource by index
        if 0 <= idx < len(resources) and resources[idx]["datastore_active"]:
            data_url = f"{base_url}/datastore/dump/{resources[idx]['id']}"
            data_response = requests.get(data_url)
            data_response.raise_for_status()
            data = pd.read_csv(StringIO(data_response.text))
            return data
        
    return None  



