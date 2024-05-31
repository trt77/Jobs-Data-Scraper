import requests
import pandas as pd
import time

app_id = '#PLACEHOLDER'
app_key = '#PLACEHOLDER'
base_url = 'http://api.adzuna.com/v1/api/jobs'

countries = ['us', 'gb', 'ca', 'au', 'in', 'de', 'fr', 'nl', 'br', 'za']
keywords = ['programming', 'programmer', 'informatics', 'software']
max_pages = 50


def fetch_jobs(keyword_a, country_code, max_pages_a):
    all_jobs_a = []
    for page in range(1, max_pages_a + 1):
        url = (f"{base_url}/{country_code}/search/{page}?app_id={app_id}&app_key="
               f"{app_key}&what={keyword_a}&content-type=application/json")
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if 'results' in data:
                all_jobs_a.extend(data['results'])
                if page >= data.get('count', 0) // 10:
                    break
            else:
                break
        else:
            print(f"Failed to fetch data for keyword '{keyword_a}' in {country_code}: {response.status_code}")
            break
        time.sleep(1)
    return all_jobs_a


all_jobs = []
for country in countries:
    for keyword in keywords:
        print(f"Fetching data for {keyword} in {country}")
        jobs_data = fetch_jobs(keyword, country, max_pages)
        all_jobs.extend(jobs_data)

df = pd.DataFrame(all_jobs)
df.to_csv('it_jobs_worldwide.csv', index=False)
print("Data fetched and saved to it_jobs_worldwide.csv.")
