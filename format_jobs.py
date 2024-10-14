import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Initialize Gemini API
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables")

genai.configure(api_key=api_key)
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# Define the prompt template for formatting
format_template = """
Format the following job listing into sections. Use only the information provided in the job listing. If any information is not explicitly available, write "Not specified" for that section.

Job Listing:
{job_listing_text}

Format your response as follows:

Company Name: [Company name]
Position Title: [Job title]
Location: [Job location]
Job Type: [Full-time, Part-time, Contract, etc. If not specified, write "Not specified"]
Experience Level: [Entry-level, Mid-level, Senior, etc. If not specified, write "Not specified"]
Job Description: [Provide a brief summary of the job in 2-3 sentences]
Key Responsibilities:
- [List 3-5 main responsibilities, use "Not specified" if no clear responsibilities are provided]
Required Skills:
- [List 3-5 key required skills, use "Not specified" if no clear skills are provided]
Nice-to-have Skills:
- [List 2-3 preferred skills if mentioned, otherwise write "Not specified"]
Application Instructions: [Summarize how to apply or write "Not specified" if not provided]

Ensure all information is derived directly from the provided job listing. Do not invent or assume any details.
"""

# Function to format a single job listing
def format_job_listing(job_listing):
    job_listing_text = f"""
    Title: {job_listing.get('title', 'Not specified')}
    Company: {job_listing.get('company', {}).get('name', 'Not specified')}
    Location: {job_listing.get('location', 'Not specified')}
    Description: {job_listing.get('description', 'Not specified')}
    Apply URL: {job_listing.get('applyUrl', 'Not specified')}
    """
    try:
        response = model.generate_content(format_template.format(job_listing_text=job_listing_text))
        return response.text
    except Exception as e:
        print(f"Error formatting job listing: {e}")
        return None

# Updated comparison template
comparison_template = """
You are an AI career advisor. Your task is to compare a list of job listings with the user's background and expertise, and rank the top 10 matches from best to least match. Address the user directly in your explanations.

User Background:
{user_data}

Job Listings:
{new_jobs}

Please analyze each job listing and compare it to the user's background. Consider factors such as:
1. Required skills vs. your skills
2. Experience level required vs. your experience
3. Job responsibilities vs. your expertise
4. Company industry vs. your industry experience
5. Location preferences (if specified)

Provide a ranked list of the top 10 job matches. For each job, give a brief explanation (1-2 sentences) of why it's ranked in that position, highlighting the main factors that influenced the ranking. Address the user directly in your explanations.

Format your response as follows:

1. [Company Name] - [Position Title]
   Explanation: This role aligns well with your experience in [relevant area]. Your background in [specific skill/experience] makes you a strong candidate for this position.

2. [Company Name] - [Position Title]
   Explanation: [Direct address to the user about job fit]

... (continue for all 10 jobs)

10. [Company Name] - [Position Title]
    Explanation: [Direct address to the user about job fit]

After listing the top 10 matches, provide a "Final Answer" section that includes the top 3 job matches with specific improvement suggestions for each. Format the Final Answer as follows:

Final Answer:
1. [Company Name] - [Position Title]
   Explanation: [Brief recap of why this job is a good match]
   Improvement Suggestion: [Specific skill or area to improve]: [Brief explanation and recommendation for a course, certification, or experience that would enhance their profile for this specific role]

2. [Company Name] - [Position Title]
   Explanation: [Brief recap of why this job is a good match]
   Improvement Suggestion: [Specific skill or area to improve]: [Brief explanation and recommendation]

3. [Company Name] - [Position Title]
   Explanation: [Brief recap of why this job is a good match]
   Improvement Suggestion: [Specific skill or area to improve]: [Brief explanation and recommendation]

Ensure your ranking, explanations, and suggestions are based solely on the information provided in the user background and job listings. Do not invent or assume any additional details. Always address the user directly in your explanations.
"""

def compare_jobs_to_user(user_data, formatted_jobs):
    try:
        new_jobs = "\n\n".join(formatted_jobs)
        response = model.generate_content(comparison_template.format(user_data=user_data, new_jobs=new_jobs))
        return response.text
    except Exception as e:
        print(f"Error comparing jobs to user: {e}")
        return None
