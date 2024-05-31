import pandas as pd
import json


def safe_json_loads(s):
    try:
        return json.loads(s)
    except json.JSONDecodeError:
        try:
            return json.loads(s.replace("'", '"'))
        except json.JSONDecodeError:
            return {}


def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if isinstance(x, dict):
            for a in x:
                flatten(x[a], name + a + '_')
        elif isinstance(x, list):
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x
    flatten(y)
    return out


df = pd.read_csv('processed_it_jobs.csv')

json_columns = ['location', 'company', 'category']
for col in json_columns:
    df[col] = df[col].apply(lambda x: safe_json_loads(x) if isinstance(x, str) and x.strip().startswith('{') else x)
    df_temp = df[col].apply(flatten_json).apply(pd.Series)
    df_temp = df_temp[df_temp.columns.drop(list(df_temp.filter(regex='__CLASS__')))]
    df = df.drop(columns=[col]).join(df_temp, rsuffix=f'_from_{col}')

df.to_csv('processed_it_jobs_cleaned.csv', index=False)
