"""
OPI Data Engineer – Exercise
Received on May 5th, 2025 @ 10am est
Due on May 7th, 2025 @ 10am est
Tam Nguyen
tamnguyencs25@gmail.com 
"""

# ------ REFERENCES ------
# https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html
# https://geopandas.org/en/stable/docs/user_guide/io.html

# ------ EXPLORING TAX & PROPERTY DATASETS (CSV & GEOJSON) ------
import pandas as pd # type: ignore
import geopandas as gpd # type: ignore
import re

tax_df = pd.read_csv('tax_info.csv')
prop_df = gpd.read_file('prop_info.geojson')
print("Original Tax Shape:", tax_df.shape) 
print("Original Tax Columns:", tax_df.columns)
print("Original Prop Shape:", prop_df.shape) 
print("Original Prop Columns:", prop_df.columns)

# ------ DATA CLEANING AND NORMALIZATION (FIELD NAMES AND RECORDS) ------
# COLUMNS/FIELDS are now all lowercase, with underscores for readability
tax_cleaned_columns = ['street_address', 'owner', 'tax_base', 'curr_land',
                      'curr_impr', 'ar_tax_base', 'state_tax',
                      'city_tax', 'longitude', 'latitude']

prop_cleaned_columns = ['street_address', 'block', 'lot', 'sale_date',
                        'year_build', 'use_group', 'perm_home', 'vacancy_indicator',
                        'exempted_improvement', 'owner', 'geometry']

tax_df.columns = tax_cleaned_columns
prop_df.columns = prop_cleaned_columns

# FILTER out zero entries
non_zero_condition = (
(tax_df['tax_base'] != 0) &
(tax_df['curr_land'] != 0) &
(tax_df['curr_impr'] != 0) &
(tax_df['ar_tax_base'] != 0) &
(tax_df['state_tax'] != 0) &
(tax_df['city_tax'] != 0))

tax_df = tax_df[non_zero_condition]
print("Non-Zero Entries Tax Shape:", tax_df.shape)

# My assumption of the format for addresses and owner records
def normalize_address(address):
  if pd.isnull(address):
    return ''
  address = address.lower() # lowercase
  address = re.sub(r'[^\w\s]','', address) # removes punctuation
  return address

tax_df['street_address'] = tax_df['street_address'].apply(normalize_address)
prop_df['street_address'] = prop_df['street_address'].apply(normalize_address)
tax_df['owner'] = tax_df['owner'].str.lower().str.replace('[.,]', '', regex=True).str.strip()
prop_df['owner'] = prop_df['owner'].str.lower().str.replace('[.,]', '', regex=True).str.strip()

print("Normalized Tax Shape:", tax_df.shape)
print("Normalized Prop Shape:", prop_df.shape)

# ------ COMBINING THE TWO DATASETS INTO A SINGLE 
# I am assuming we want records that appear in both datasets (i.e., tax info and property info)
# "explore tax information about properties" --> inner, use intersection of keys from both frames
merged_df = pd.merge(tax_df, prop_df, on=['street_address', 'owner'], how='inner')
print("Merged Shape:", merged_df.shape)
print("Merged Columns:", merged_df.columns)
print(merged_df)