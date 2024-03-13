import requests
import pandas as pd
from io import StringIO

def fetch_data(base_url, package_id, idx=None):
    # Construct URL to retrieve package metadata
    package_url = f"{base_url}/api/3/action/package_show"
    params = {"id": package_id}
    
    # Fetch package metadata
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
    else:
        # Loop through resources in the package
        for resource in resources:
            # Check if the resource is active in the datastore
            if resource["datastore_active"]:
                # Construct URL to fetch resource data
                data_url = f"{base_url}/datastore/dump/{resource['id']}"
                data_response = requests.get(data_url)
                data_response.raise_for_status()
                data = pd.read_csv(StringIO(data_response.text))
                return data  # Return the DataFrame

    # If no active datastore resources were found or returned, you might want to return None or raise an exception
    return None  # Or raise an exception if no data was found

# Example usage for Toronto Open Data
if __name__ == "__main__":
    base_url_toronto = "https://ckan0.cf.opendata.inter.prod-toronto.ca"
    package_id_toronto = "daily-shelter-overnight-service-occupancy-capacity"
    x = fetch_data(base_url_toronto, package_id_toronto)
    if x is not None:
        print(x.head())
    else:
        print("No data returned")


