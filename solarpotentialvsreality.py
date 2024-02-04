import pandas as pd
import matplotlib.pyplot as plt

# Correct paths to your Excel files
solar_power_tracker_path = '/Users/jt/Documents/Coding/solarpotentialvsreality/data/Global-Solar-Power-Tracker-December-2023.xlsx'
solar_potential_path = '/Users/jt/Documents/Coding/solarpotentialvsreality/data/solargis_pvpotential_countryranking_2020_data.xlsx'

import pandas as pd
import matplotlib.pyplot as plt

# Load the Global Solar Power Tracker dataset
solar_power_tracker_df = pd.read_excel(solar_power_tracker_path, sheet_name='Large Utility-Scale')

# Load the Global Photovoltaic Power Potential dataset from the "Country indicators" sheet
solar_potential_df = pd.read_excel(solar_potential_path, sheet_name='Country indicators', skiprows=1)

# Print the column names to verify correct loading
print(solar_power_tracker_df.columns)
print(solar_potential_df.columns)

# Proceed with filtering solar_power_tracker_df as before
solar_power_tracker_df = solar_power_tracker_df[solar_power_tracker_df['Capacity (MW)'] >= 20]

# Group by country and sum up capacities for operational and under-construction projects
actual_capacity_by_country = solar_power_tracker_df.groupby('Country')['Capacity (MW)'].sum().reset_index()

# Use the correct column for country names in solar_potential_df, and choose an appropriate column for potential values
solar_potential_summary = solar_potential_df[['Country or region', 'Average practical potential \n(PVOUT Level 1, \nkWh/kWp/day), long-term']]

# Rename the columns to simplify them
# Rename the columns to simplify them
solar_potential_df.columns = ['ISO_A3', 'Country or Region', 'Note', 'World Bank Region',
                              'Total Population 2018', 'Total Area 2018', 'Evaluated Area',
                              'Level 1 Area Percentage', 'Human Development Index 2017',
                              'GDP per Capita 2018', 'Average Theoretical Potential GHI',
                              'Average Practical Potential PVOUT', 'Average Economic Potential LCOE 2018',
                              'Average PV Seasonality Index', 'PV Equivalent Area Percentage',
                              'Cumulative Installed PV Capacity MWp 2018', 'Cumulative Installed PV Capacity Wp per Capita 2018',
                              'Access to Electricity Rural 2016', 'Electric Power Consumption per Capita 2014',
                              'Reliability of Supply and Transparency of Tariff Index 2019',
                              'Approximate Electricity Tariffs for SMEs 2019']

# Now you can use the simplified column names
solar_potential_summary = solar_potential_df[['Country or Region', 'Average Practical Potential PVOUT']]

# Merge the two datasets on the country columns using the correct, simplified column names
comparison_df = pd.merge(actual_capacity_by_country, solar_potential_summary, left_on='Country', right_on='Country or Region', how='inner')

# Plotting - adjust column names as necessary. Ensure the column names used here match those in the merged DataFrame
comparison_df.plot(x='Country', y=['Capacity (MW)', 'Average Practical Potential PVOUT'], kind='bar', figsize=(15,7))
plt.title('Comparison of Solar Power Potential vs. Actual Installations by Country')
plt.ylabel('Capacity (MW) / PV Potential (kWh/kWp/day)')
plt.xlabel('Country')
plt.xticks(rotation=90)
plt.legend(['Actual Installed Capacity (MW)', 'PV Potential (kWh/kWp/day)'])
plt.tight_layout()
plt.show()
