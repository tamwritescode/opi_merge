Questions: 

After exploring the data to get an idea of contents, potential issues, and limitations, write python code that combines the two datasets into a single dataframe. Edit field names and records so they are more appropriate for a database table. Hint: make sure to explore the data before merging. Based on looking at both datasets, I noticed some potential issues, and limitations:

- Inconsistent field/column names (i.e. some fields are capitalized, others separated by underscores) 

- Many names field/column between the two data info (i.e. 'STR Address' vs. 'FULLADDR')

- Multiple Zero entries for fields [tax base - city tax] from tax_info.csv


How many records are in each source dataset? How many could be joined with high certainty?

- There were 989 records in each dataset, I used .shape to view the dimensions

- print("Original Tax Shape:", tax_df.shape) # (990, 10)
- print("Original Prop Shape:", prop_df.shape) # (990, 11) 

- 9 records could be joined with high certainty

Reasoning via matching on cleaned street_address and owner:
- I am assuming we want records that appear in both datasets (i.e., tax info and property info), so the words "explore tax information about properties" corresponds to SQL inner join, which use intersection of keys from both frames
- Merged Shape: (10, 19)


Imagine that this process of ingesting and merging datasets is set on a schedule so the resultant data is refreshed regularly. What other considerations, checks, and processes should be built into the pipeline to make the process successful?


To make the process more successful, we must consider

- Schema consistency: make sure all columns are expected

- Normalization and data quality: make sure consistent formatting and flag zero entries

- Handling duplicate values, load on the correct keys, and supporting file export

- I think using timestamps and running unit and integration tests on merges would also help monitor and analyze performance


What are three ideas to make the pipeline process run faster or more Efficiently?

- I am a bit familiar with parallel computing in python so perhaps using libraries like dask can speed up functions like .apply() when dealing with large columns.

- I could filter and drop unneeded columns early before an expensive operation like merging.

- I could preprocess things like normalized addresses or owner names once, save them as intermediate files, and skip re-running those steps every time the pipeline runs.


What additional information/data should accompany the dataset? This could be for external data users or fellow teammates.
 
- The data set should provide additional information(usually as a header or README file) on a clear description of each column including both units and formatting to encourage readability for both technical and non-technical users. This is also where I would provided my assumptions and follow up questions (listed below)

- Follow up questions and assumptions for stakeholders:
 
1. What is the expected format for entries like addresses and sale dates? since I observe that some addresses have weird punctuation, sale dates has no MM/DD/YYYY format

2.  Is the information still valid without an official owner name
- in tax_info.csv: 2204 MARYLAND AVE, LLC is under PROP OWNER field
- in prop_info.geojson: "OWNER_1": "726 n carrollton"

3. Mismatched geometry data (i.e. lon and lat vs. list of multiple
coordinates)?