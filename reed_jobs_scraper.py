import requests
import pandas as pd
from requests.auth import HTTPBasicAuth

host = 'https://www.reed.co.uk/api/1.0/search'
key = '#PLACEHOLDER'


def fetch_reed_jobs(keywords_a, location_a, max_results_a=100):
    headers = {"Authorization": f"Basic {key}"}
    params = {
        'keywords': keywords_a,
        'locationName': location_a,
        'resultsToTake': max_results_a
    }

    response = requests.get(host, headers=headers, params=params, auth=HTTPBasicAuth(key, ''))
    if response.status_code == 200:
        return response.json()['results']
    else:
        print(f"Failed to fetch data: {response.status_code}")
        return []


keywords = "developer"
location = "London"
max_results = 100

jobs_data = fetch_reed_jobs(keywords, location, max_results)

if not jobs_data:
    print("No data fetched from the Reed API.")
else:
    df_reed = pd.DataFrame(jobs_data)

    print(df_reed.columns)

    df_reed = df_reed.rename(columns={
        'jobTitle': 'title',
        'jobDescription': 'description',
        'employerName': 'display_name_from_company',
        'locationName': 'area_0',
        'date': 'created',
        'minimumSalary': 'salary_min',
        'maximumSalary': 'salary_max'
    })

    df_reed['salary_is_predicted'] = 0

    # Adding 'contract_time' and 'contract_type' columns if they do not exist
    if 'contract_time' not in df_reed.columns:
        df_reed['contract_time'] = None
    if 'contract_type' not in df_reed.columns:
        df_reed['contract_type'] = None

    df_reed['display_name'] = df_reed['area_0']

    if 'tag' in df_reed.columns:
        df_reed['label'] = df_reed['tag']
    else:
        df_reed['label'] = None

    # Normalize contract_type if it exists and is not empty
    if 'contract_type' in df_reed.columns and not df_reed['contract_type'].isnull().all():
        df_reed['contract_type'] = df_reed['contract_type'].str.lower().replace(['remote', 'home office'], 'remote',
                                                                                regex=True)

    # Remove rows with 'Unknown', 'Not specified', or None in contract_time or contract_type
    df_reed = df_reed[~df_reed['contract_time'].isin([None, 'Unknown', 'Not specified'])]
    df_reed = df_reed[~df_reed['contract_type'].isin([None, 'Unknown', 'Not specified'])]
    df_reed = df_reed.dropna(subset=['title', 'description', 'display_name_from_company'])

    expected_columns = ['salary_is_predicted', 'salary_max', 'created', 'salary_min', 'contract_time', 'description',
                        'title', 'contract_type', 'area_0', 'display_name', 'display_name_from_company', 'label']
    for col in expected_columns:
        if col not in df_reed.columns:
            df_reed[col] = None

    df_reed = df_reed[expected_columns]

    df_reed.to_csv('reed_jobs.csv', index=False)
    print("Reed job data fetched and saved to reed_jobs.csv.")
