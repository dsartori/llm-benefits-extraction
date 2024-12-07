import json
import re
import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Configuration
API_KEY = os.getenv("NEBIUS_API_KEY")
BASE_URL = "https://192.168.1.164/api/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

# Data file
datafile = "jobs.json"

# Parse the LLM response
def parse_llm_response(response):
    # Clean up typical LLM response issues
    content = response["choices"][0].get("message", {}).get("content", "").strip()
    # backticks
    if content.startswith("```") and content.endswith("```"):
        content = content[3:-3].strip()
    # line breaks, backslashes, whitespace
    cleaned_content = re.sub(r"\\n", "", content)
    cleaned_content = re.sub(r"\s+", " ", cleaned_content)
    cleaned_content = cleaned_content.replace("\\", "")
    try:
        return json.loads(cleaned_content)
    except json.JSONDecodeError as e:
        print(f"\n* JSON decoding failed: {e}")
        return cleaned_content

# Extract job benefits
def extract_benefits(job_description):
    payload = {
        "model": "llama3.2:latest",  # Replace with the actual model supported by OpenWebUI
        "messages": [
            {"role": "system", "content": """Extract the job benefits from this description and map each benefit to one of the following categories:

- "health insurance": e.g., "medical coverage", "health benefits"
- "retirement plan": e.g., "rrsp", "pension"
- "paid time off": e.g., "vacation", "sick leave"
- "bonus": e.g., "performance bonus", "annual bonus"
- "wellness programs": e.g., "gym membership", "employee wellness"
- "training": e.g., "professional development", "skills training"
- Use "other" for benefits that do not match these categories.

Standard employer obligations like overtime pay are not benefits and must be excluded from the output. 
Return the output as a JSON object where each category has a list of benefits under it. 
Do not return any other text besides the JSON object. 
Return an object of empty arrays if there are no benefits. 
Always return an object containing all of the categories identified as keys. 
Do not provide commentary or guidance. 
Do not format the data."""},
            {"role": "user", "content": f"'{job_description}'"}
        ],
        "temperature": 0.6,
    }

    try:
        response = requests.post(
            BASE_URL,
            headers=HEADERS,
            json=payload,
            verify=False  # Disable SSL verification for self-signed certificates
        )
        print (response.json())
        response.raise_for_status()
        return parse_llm_response(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return {}

# Main script
if __name__ == "__main__":
    with open(datafile, "r") as file:
        job_data = json.load(file)

    # Extract job benefits
    print("Extracting job benefits:")
    for job in job_data:
        try:
            job_description = job.get("text", "")
            job_benefits = extract_benefits(job_description)
            job["job_benefits"] = job_benefits
            print(".", end="", flush=True)

        except Exception as e:
            print(f"\nError processing job '{job.get('job_title', 'Unknown')}': {e}")

    # Save data
    with open("jobs_extracted.json", "w") as file:
        json.dump(job_data, file, indent=2)

    print("\nSaved jobs_extracted.json")
