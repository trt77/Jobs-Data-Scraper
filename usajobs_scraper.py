import requests
import pandas as pd
import json

host = 'https://data.usajobs.gov/api/search'
key = '#PLACEHOLDER' 

def fetch_usajobs_jobs(keyword, location=None, max_results=100):
    headers = {
        "Authorization-Key": key,
        "Content-Type": "application/json",
        "User-Agent": "YourAppName"  # Replace with your application name
    }
    params = {
        "Keyword": keyword,
        "ResultsPerPage": max_results,
        "Page": 1
    }
    if location:
        params["LocationName"] = location

    response = requests.get(host, headers=headers, params=params)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(json.dumps(data, indent=2))  # Pretty print the JSON response for inspection
        return data['SearchResult']['SearchResultItems']
    else:
        print(f"Failed to fetch data: {response.status_code}")
        return []

keyword = "software"
location = None
max_results = 100

jobs_data = fetch_usajobs_jobs(keyword, location, max_results)

if not jobs_data:
    print("No data fetched from the USAJOBS API.")
else:
    jobs_list = []
    for job in jobs_data:
        job_info = job['MatchedObjectDescriptor']
        job_entry = {
            'title': job_info.get('PositionTitle', 'Unknown'),
            'description': job_info.get('UserArea', {}).get('Details', {}).get('MajorDuties', 'Unknown'),
            'display_name_from_company': job_info.get('OrganizationName', 'Unknown'),
            'area_0': job_info.get('PositionLocationDisplay', 'Unknown'),
            'created': job_info.get('PublicationStartDate', 'Unknown'),
            'salary_min': job_info.get('PositionRemuneration', [{}])[0].get('MinimumRange', 0),
            'salary_max': job_info.get('PositionRemuneration', [{}])[0].get('MaximumRange', 0),
            'contract_time': job_info.get('PositionSchedule', [{}])[0].get('Name', 'Unknown'),
            'contract_type': 'Unknown',
            'display_name': job_info.get('PositionLocationDisplay', 'Unknown'),
            'label': job_info.get('UserArea', {}).get('Details', {}).get('PositionClassification', 'Unknown')
        }
        jobs_list.append(job_entry)

    df_usajobs = pd.DataFrame(jobs_list)

    # Normalize contract_type
    df_usajobs['contract_type'] = df_usajobs['contract_type'].str.lower().replace(['remote', 'home office'], 'remote', regex=True)

    # Remove rows with 'Unknown' or 'Not specified'
    df_usajobs = df_usajobs[~df_usajobs['contract_time'].isin(['Unknown', 'Not specified'])]
    df_usajobs = df_usajobs[~df_usajobs['contract_type'].isin(['Unknown', 'Not specified'])]
    df_usajobs = df_usajobs.dropna(subset=['title', 'description', 'display_name_from_company'])

    expected_columns = ['salary_is_predicted', 'salary_max', 'created', 'salary_min', 'contract_time', 'description',
                        'title', 'contract_type', 'area_0', 'display_name', 'display_name_from_company', 'label']
    df_usajobs['salary_is_predicted'] = 0

    for col in expected_columns:
        if col not in df_usajobs.columns:
            df_usajobs[col] = None

    df_usajobs = df_usajobs[expected_columns]

    df_usajobs.to_csv('usajobs_jobs.csv', index=False)
    print("USAJOBS job data fetched and saved to usajobs_jobs.csv.")
