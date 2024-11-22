
# Job Benefits Extraction from free text with LLMs


## Procedure

1. **Clone the Repository** and navigate to the project directory:
   ```bash
   git clone https://github.com/dsartori/llm-benefits-extraction.git
   cd llm-benefits-extraction
   ```

2. **Add API Key**: Create a `.env` file in the root directory with your Nebius API key:
   ```plaintext
   NEBIUS_API_KEY=your_nebius_api_key_here
   ```

3. **Build and Run**:
   - Build the Docker image and start a container with an interactive Bash shell:
     ```bash
     docker-compose up --build
     ```

4. **Run Extraction Script**:
   Inside the container, run the extraction script:
   ```bash
   python extract.py
   ```

5. **View Results**:
   The extracted job benefits will be saved in the `app/jobs_extracted.json` file. You can open this file to review the results.

6. **Clustering and Analysis**:
   Run the `analyze.py` script to perform clustering on the `jobs_extracted.json` file. This script will categorize jobs by benefits and generate visualizations:
   ```bash
   python analyze.py
   ```
   The `analyze.py` script generates simple heatmaps to help visualize the distribution of job benefits across different categories.


## Project Structure

- `app/extract.py`: Script to extract job benefits using Nebius AI.
- `app/job_sample.json`: Sample job data.
- `app/jobs_extracted.json`: Output file with extracted benefits.

## Clustering and Analysis

After extraction, apply clustering to `jobs_extracted.json` to categorize jobs by benefits. Use a tool like Jupyter or a script to perform clustering and generate visualizations.
