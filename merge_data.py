import pandas as pd

df_existing = pd.read_csv('processed_it_jobs_cleaned.csv')
df_reed = pd.read_csv('reed_jobs.csv')
df_usajobs = pd.read_csv('usajobs_jobs.csv')

# Remove rows with 'Unknown' or 'Not specified'
df_existing = df_existing[~df_existing['contract_time'].isin(['Unknown', 'Not specified'])]
df_existing = df_existing[~df_existing['contract_type'].isin(['Unknown', 'Not specified'])]

df_combined = pd.concat([df_existing, df_reed, df_usajobs], ignore_index=True)

df_combined.to_csv('combined_it_jobs.csv', index=False)
print("Combined job data saved to combined_it_jobs.csv.")
