import json
import time  # Optional: for rate-limiting requests
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client
client = OpenAI(
    base_url="https://api.studio.nebius.ai/v1/",
    api_key=os.getenv("NEBIUS_API_KEY"),
)


datafile = "jobs.json"


import json
import re

def parse_llm_response(response):
    # Extract content and strip whitespace
    content = response.choices[0].message.content.strip()
    
    # Step 1: Remove leading/trailing triple backticks if present
    if content.startswith("```") and content.endswith("```"):
        content = content[3:-3].strip()
    
    # Step 2: Remove line breaks, backslashes, and extra whitespace
    cleaned_content = re.sub(r'\\n', '', content)  # Remove newline characters
    cleaned_content = re.sub(r'\s+', ' ', cleaned_content)  # Normalize whitespace
    cleaned_content = cleaned_content.replace('\\', '')  # Remove any remaining backslashes
    
    try:
        # Step 3: Attempt JSON deserialization after cleanup
        return json.loads(cleaned_content)
    except json.JSONDecodeError as e:
        print(f"* JSON decoding failed: {e}")
        return cleaned_content  # Return raw content if JSON parsing fails




# Function to extract benefits from a job description
def extract_benefits(job_description):
    response = client.chat.completions.create(
        model="meta-llama/Meta-Llama-3.1-405B-Instruct",
        messages=[
            {"role": "system", "content": """Extract the job benefits from this description and map each benefit to one of the following categories:

- "health insurance": e.g., "medical coverage", "health benefits"
- "retirement plan": e.g., "401k", "pension"
- "paid time off": e.g., "vacation", "sick leave"
- "bonus": e.g., "performance bonus", "annual bonus"
- "wellness programs": e.g., "gym membership", "employee wellness"
- "training": e.g., "professional development", "skills training"
- Use "other" for benefits that do not match these categories.

Standard employer obligations like overtime pay are not benefits and must be excluded from the output. if the benefit does not fit these categories. Return the output as a JSON object where each category has a list of benefits under it. Do not return any other text besides the JSON object. Return an object of empty arrays if there are no benefits. Always return an object containing all of the categories identified as keys. Do not provide commentary or guidance. Do not format the data."""},
            {"role": "user", "content": f"'{job_description}'"}
        ],
        temperature=0.6
    )
    try:
        # Attempt to parse response as JSON
        return parse_llm_response(response)
    except json.JSONDecodeError:
        print("*", end="")
        return response.choices[0].message.content.strip()



# Load your dataset
with open(datafile, "r") as file:
    job_data = json.load(file)
     

# Loop through job postings, append benefits data
print("Extracting job benefits:")
for job in job_data:
    try:
        job_description = job.get("text", "")
        job_benefits = extract_benefits(job_description)
        job["job_benefits"] = job_benefits  # Append extracted benefits

        # Optional: add a delay to avoid rate limits
        #time.sleep(1)
        print(".", end="")
        
    except Exception as e:
        print(f"Error processing job '{job.get('job_title', 'Unknown')}': {e}")

print("\nJob benefits extraction completed.")

# Save updated data with benefits included
with open("jobs_extracted.json", "w") as file:
    json.dump(job_data, file, indent=2)

print("Job benefits extraction completed and saved.")
