import os
import sys
import traceback
import re

print(f"Current working directory: {os.getcwd()}")
print(f"Python path: {sys.path}")

try:
    from fetch_jobs import fetch_jobs, display_jobs
    from format_jobs import format_job_listing, compare_jobs_to_user
    print("Successfully imported fetch_jobs, display_jobs, format_job_listing, and compare_jobs_to_user")
except ImportError as e:
    print(f"Error importing: {e}")
    print("Traceback:")
    traceback.print_exc()
    sys.exit(1)

# Hardcoded user data
user_data = """
Work Experience:

1. UiPath
   • Role: Lead Designer
   • Duration: January 2024 – Present (10 months)
   • Location: Bucharest, Romania
   • Responsibilities: Focusing on AI-powered experiences for enterprise applications.

2. Playable Labs
   • Role: Design Director - Venture Studio
   • Duration: November 2022 – Present (2 years)
   • Location: Estonia
   • Responsibilities: Leading a team of 8 experts in brand design, UX, and front-end development. Focused on scaling mobile-first products and conducting discovery sessions with startup founders.

3. Superpost.app
   • Role: Design Director
   • Duration: January 2023 – February 2024 (1 year, 2 months)
   • Location: Estonia
   • Responsibilities: Dual role as PM and design leader. Led a team of designers and developers to launch AI-powered publishing solutions and developed a user dashboard.

4. Virtual Pangea
   • Role: Design Director
   • Duration: April 2022 – December 2022 (9 months)
   • Location: Remote
   • Responsibilities: Led a design team to build Virtual Pangea's platform from concept to production. Managed the entire design lifecycle.

5. Neobility
   • Role: Design Director
   • Duration: December 2019 – July 2022 (2 years, 8 months)
   • Location: Bucharest, Romania
   • Responsibilities: Led product design and experimentation, launching the company's first app version and releasing 5 updates, increasing daily active users to 10,000.

6. ING
   • Role: Principal Product Designer
   • Duration: March 2018 – December 2019 (1 year, 10 months)
   • Location: Bucharest, Romania
   • Responsibilities: Led the redesign of the ING HomeBank mobile app, resulting in 1 million active users, and improved user engagement by shifting the mobile user segment to 90%.

7. Fitbit (now part of Google)
   • Role: Senior Product Designer
   • Duration: January 2017 – March 2018 (1 year, 3 months)
   • Location: Bucharest, Romania
   • Responsibilities: Led UX for 30 second-party apps on Fitbit devices, including Nest, Strava, and Surfline, generating $200k in indirect revenue from 18 apps.

8. Vector Watch
   • Role: Principal Product Designer
   • Duration: January 2015 – January 2017 (2 years, 1 month)
   • Location: Bucharest, Romania
   • Responsibilities: Designed OS and mobile experience for two smartwatches, contributing to selling 100,000 watches before Vector's acquisition.

9. HAX
   • Role: Digital Product Designer
   • Duration: January 2014 – December 2014 (1 year)
   • Location: Shenzhen City, China
   • Responsibilities: Worked on the HAXLR8R 2014 class projects, focusing on product ideation and development.

10. Leroy Merlin
    • Role: Industrial Designer
    • Duration: 2013 – 2014 (1 year)
    • Location: Lille, France

Education:

1. Politecnico di Milano
   • Degree: Master's in Industrial Design for Innovation
   • Duration: 2010 – 2013

2. Politecnico di Milano
   • Degree: Bachelor's in Furniture Design
   • Duration: 2007 – 2010
"""

def extract_top_jobs(comparison_result):
    # Split the result into lines
    lines = comparison_result.split('\n')
    
    # Initialize variables
    top_jobs = []
    current_job = ""
    
    # Iterate through lines to extract top 3 jobs
    for line in lines:
        if re.match(r'^\d+\.', line):  # If line starts with a number and period
            if current_job:
                top_jobs.append(current_job.strip())
            current_job = line
        elif current_job:
            current_job += "\n" + line.strip()
        
        if len(top_jobs) == 3:
            break
    
    # Add the last job if we haven't reached 3 yet
    if current_job and len(top_jobs) < 3:
        top_jobs.append(current_job.strip())
    
    return "\n\n".join(top_jobs) if top_jobs else None

def main():
    try:
        print("Attempting to fetch jobs...")
        jobs = fetch_jobs("Software Engineer", "92000000")
        if jobs and 'data' in jobs:
            print("Jobs fetched successfully. Formatting jobs...")
            formatted_jobs = []
            for job in jobs['data']:
                formatted_job = format_job_listing(job)
                if formatted_job:
                    formatted_jobs.append(formatted_job)
                else:
                    print(f"Failed to format job: {job.get('title', 'Unknown Title')}")
            
            if formatted_jobs:
                print("Jobs formatted successfully. Comparing to user background...")
                comparison_result = compare_jobs_to_user(user_data, formatted_jobs)
                if comparison_result:
                    print("Job Comparison Results:")
                    print(comparison_result)
                    
                    print("\nFinal Answer:")
                    print(comparison_result)  # Use the full comparison result as the Final Answer
                else:
                    print("Failed to compare jobs to user background.")
            else:
                print("No jobs were successfully formatted.")
        else:
            print("Failed to fetch jobs or no jobs returned.")
    except Exception as e:
        print(f"An error occurred in main(): {e}")
        print("Traceback:")
        traceback.print_exc()

if __name__ == "__main__":
    main()
