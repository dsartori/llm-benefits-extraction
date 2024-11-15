import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

with open("jobs_extracted.json", "r") as file:
    job_data = json.load(file)

# Define benefit categories
categories = ["health insurance", "retirement plan", "paid time off", 
              "bonus", "wellness programs", "training"]

# Extract sector codes and simplified NOC codes
sector_codes = [job.get("sector", "unknown") for job in job_data]
noc_codes = [str(job.get("nocs_2021", "unknown"))[:2] for job in job_data]  # Simplify to first 2 digits


benefit_counts_sector = pd.DataFrame(0, index=pd.Index(sector_codes, name="Sector Code"), columns=categories)
benefit_counts_noc = pd.DataFrame(0, index=pd.Index(noc_codes, name="NOC Code"), columns=categories)

job_counts_sector = pd.Series(0, index=benefit_counts_sector.index)
job_counts_noc = pd.Series(0, index=benefit_counts_noc.index)

for job, sector, noc in zip(job_data, sector_codes, noc_codes):
    benefits = job.get("job_benefits", {})
    if isinstance(benefits, dict): 
        # Increment job counts
        job_counts_sector[sector] += 1
        job_counts_noc[noc] += 1
        # Increment benefit counts
        for category in categories:
            if benefits.get(category):  # Only count benefit if it exists for the job
                benefit_counts_sector.at[sector, category] += 1
                benefit_counts_noc.at[noc, category] += 1

# Aggregate counts for duplicate sector and NOC codes
benefit_counts_sector = benefit_counts_sector.groupby("Sector Code").sum()
benefit_counts_noc = benefit_counts_noc.groupby("NOC Code").sum()
job_counts_sector = job_counts_sector.groupby(job_counts_sector.index).sum()
job_counts_noc = job_counts_noc.groupby(job_counts_noc.index).sum()

# Calculate the percentage of jobs offering each benefit within each sector and NOC code
benefit_percentage_sector = benefit_counts_sector.divide(job_counts_sector, axis=0) * 100
benefit_percentage_noc = benefit_counts_noc.divide(job_counts_noc, axis=0) * 100

# Plot the heatmap for Sector Code
plt.figure(figsize=(12, 8))
sns.heatmap(benefit_percentage_sector, annot=True, fmt=".1f", cmap="YlGnBu", cbar_kws={'label': 'Percentage of Jobs Offering Benefit Type (%)'})
plt.title("Percentage of Jobs Offering Each Benefit Type by Sector Code")
plt.xlabel("Benefit Category")
plt.ylabel("Sector Code")
plt.tight_layout()
plt.savefig("sector_benefit_heatmap.png", format="png")
print("Heatmap saved as 'sector_benefit_heatmap_annotated.png'")

# Plot the heatmap for 2-digit NOC Code
plt.figure(figsize=(12, 8))
sns.heatmap(benefit_percentage_noc, annot=True, fmt=".1f", cmap="YlGnBu", cbar_kws={'label': 'Percentage of Jobs Offering Benefit Type (%)'})
plt.title("Percentage of Jobs Offering Each Benefit Type by 2-Digit NOC Code")
plt.xlabel("Benefit Category")
plt.ylabel("2-Digit NOC Code")
plt.tight_layout()
plt.savefig("noc_benefit_heatmap.png", format="png")
print("Heatmap saved as 'noc_benefit_heatmap_annotated.png'")


# Plot the heatmap for Sector Code, unannotated
plt.figure(figsize=(12, 8))
sns.heatmap(benefit_percentage_sector, annot=False, fmt=".1f", cmap="YlGnBu", cbar_kws={'label': 'Percentage of Jobs Offering Benefit Type (%)'})
plt.title("Percentage of Jobs Offering Each Benefit Ty[e] by Sector Code")
plt.xlabel("Benefit Category")
plt.ylabel("Sector Code")
plt.tight_layout()
plt.savefig("sector_benefit_heatmap.png", format="png")
print("Heatmap saved as 'sector_benefit_heatmap.png'")

# Plot the heatmap for 2-digit NOC Code, unannotated
plt.figure(figsize=(12, 8))
sns.heatmap(benefit_percentage_noc, annot=False, fmt=".1f", cmap="YlGnBu", cbar_kws={'label': 'Percentage of Jobs Offering Benefit Type (%)'})
plt.title("Percentage of Jobs Offering Each Benefit Type by 2-Digit NOC Code")
plt.xlabel("Benefit Category")
plt.ylabel("2-Digit NOC Code")
plt.tight_layout()
plt.savefig("noc_benefit_heatmap.png", format="png")
print("Heatmap saved as 'noc_benefit_heatmap.png'")
