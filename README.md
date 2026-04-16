# Veridion-POC-simulation-challenge
Data cleaning and Entity Resolution POC for a manufacturing procurement digitalization project.

**1. Project Overview**  
This project is part of a digitalization journey for a manufacturing company’s Procurement department. The main objective was to clean, resolve, and analyze a cluttered supplier database to enable a cost-saving strategy and explore supply chain sustainability.

The work involved:

-Entity Resolution: I compared the messy names with the official and verified list to pick the right one

-Data Quality Control (QC): I identified gaps and inconsistencies in the vendor master data.

**2. Entity Resolution**

To resolve the 592 input records, I used a multi-layered validation approach:

Primary Match: Focused on the input_company_name vs company_legal_names and website_url.

Geographical Validation: Cross-referenced input_main_country with the candidate's main_country_code.

Manual Override: Not all automated matches were correct.

Example: For Row Key 0 (24-SEVEN MEDIA NETWORK) the system suggested an Indian entity. Since the input was from Pakistan, I flagged this as an incorrect match to prevent data pollution.

Success Case: For Row Key 1 (2OPERATE A/S) the legal name and Danish domain provided a 100% confidence match.

The automated logic for this resolution can be found in the clean_procurement_data.py script included in this repo.

**3. Data Analysis & Quality Control (QC)**

After resolving the entities, I performed a deep dive into the attribute quality. My key findings include:

The Revenue Gap: Out of the 592 "best matches" 279 records are missing revenue data. This is a major blocker for the leadership's cost-saving strategy, as we cannot accurately prioritize high-volume vendors.

Data Corruption: I identified several #ERROR! strings in the primary_phone column, likely due to a faulty export from the legacy provider's system.

Empty Columns: I noticed there were some empty columns at the end of the sheet Company Data (Digital + Legal) Sample (from column 81 onwards). I decided to remove them because they were just taking up space and making the table harder to read.

**4. Sustainability**

While the department currently lacks the resources to prioritize sustainability, I noticed a significant opportunity for the future during my analysis (even though I didn't perform a technical merge in the script).

By resolving the messy entries and assigning a unique 'veridion_id' to each supplier, I’ve built the bridge to sustainability reporting. I manually cross-checked a few records (like Oracle) and confirmed that the ID in my cleaned list matches perfectly with the entries in the 'Sustainability Sample' file.

This means the mapping is "conceptually ready". When the company is ready, they won't need another expensive data cleaning project. 

**5. Files in this Repository**

main.py: Python script used to process the candidates and flag QC issues.

resolved_presales_data_sample.csv: The final output with the selected matches.

presales_data_sample.csv.csv: The input for my solution.
