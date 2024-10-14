import requests
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Retrieve the API key and the URL from the .env file
api_key = os.getenv("X_RAPIDAPI_KEY")
request_url = "https://linkedin-data-api.p.rapidapi.com/search-jobs"

# Set up the headers
headers = {
    "X-RapidAPI-Key": api_key,
    "X-RapidAPI-Host": "linkedin-data-api.p.rapidapi.com",
}

def fetch_jobs(keywords, location_id, date_posted="anyTime", sort="mostRecent"):
    # Define the query parameters for the job search
    params = {
        "keywords": keywords,
        "locationId": location_id,
        "datePosted": date_posted,
        "sort": sort,
    }

    # Make the GET request to the API
    response = requests.get(request_url, headers=headers, params=params)

    return response.json() if response.status_code == 200 else None

def display_jobs(jobs_data):
    if jobs_data and 'data' in jobs_data:
        jobs = jobs_data['data']
        for job in jobs:
            print(f"Title: {job.get('title')}")
            print(f"Company: {job.get('company', {}).get('name')}")
            print(f"Location: {job.get('location')}")
            print(f"URL: {job.get('url')}")
            print("---")
    else:
        print("No jobs data available or invalid format.")

# Explicitly export the functions
__all__ = ['fetch_jobs', 'display_jobs']

# Remove this part if you want to use the functions from another file
# if __name__ == "__main__":
#     jobs = fetch_jobs("Software Engineer", "92000000")
#     if jobs:
#         display_jobs(jobs)
#     else:
#         print("Failed to fetch jobs.")
