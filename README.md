# Jobs-Data-Scraper
Data-scraping tool built with Python, takes automated approach to creating an import-ready cleaned CSV file for Neo4j graph database for further analysis of jobs in IT.

Running sequence:

1. main.py -> 	🗎 it_jobs_worldwide.csv

2. clean_data.py -> 	🗎 processed_it_jobs.csv

3. reed_jobs_scraper.py  -> 	🗎 reed_jobs.csv

4. usajobs_scraper.py->	🗎 usajobs_jobs.csv

5. process_cleaned_data.py->	🗎 processed_it_jobs_cleaned.csv

6. merge_data.py->	🗎 combined_it_jobs.csv

Please fill out your API keys in `<PLACEHOLDER>` fields.

Add 🗎 combined_it_jobs.csv to your Neo4j Database import folder. It is cleaned, merged and ready to import.

Enjoy!
