# Jobs-Data-Scraper
Data-scraping tool built with Python, takes automated approach to creating an import-ready cleaned CSV file for Neo4j graph database for further analysis.

Running sequence:

main.py                 
-> 	🗎 it_jobs_worldwide.csv 	  	  
clean_data.py           
-> 	🗎 processed_it_jobs.csv
reed_jobs_scraper.py    
-> 	🗎 reed_jobs.csv 			          
usajobs_scraper.py      
->	🗎 usajobs_jobs.csv 			       
process_cleaned_data.py 
->	🗎 processed_it_jobs_cleaned.csv 
merge_data.py          
->	🗎 combined_it_jobs.csv
