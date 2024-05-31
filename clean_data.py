import pandas as pd

df = pd.read_csv('it_jobs_worldwide.csv')
print("Initial dataset shape:", df.shape)

df.drop(columns=['adref', 'id', '__CLASS__', 'redirect_url', 'latitude', 'longitude'], inplace=True)

numeric_cols = ['salary_min', 'salary_max']
categorical_cols = ['location', 'company', 'category', 'contract_time', 'contract_type', 'title', 'description']

df[numeric_cols] = df[numeric_cols].fillna(0)
df[categorical_cols] = df[categorical_cols].replace('', pd.NA).dropna()

# Remove rows with 'Unknown' or 'Not specified' in critical columns
df = df[~df['contract_time'].isin(['Unknown', 'Not specified'])]
df = df[~df['contract_type'].isin(['Unknown', 'Not specified'])]
df = df[~df['title'].isin(['Unknown'])]

# Normalize job titles
df['title'] = df['title'].str.lower().replace(['dev', 'developer', 'development'], 'developer', regex=True)

# Normalize contract_time values
df['contract_time'] = df['contract_time'].str.lower().replace({
    r'.*full[-\s]*time.*': 'full_time',
    r'.*part[-\s]*time.*': 'part_time'
}, regex=True)

print("Processed dataset shape:", df.shape)
print(df.head())

df.to_csv('processed_it_jobs.csv', index=False)
