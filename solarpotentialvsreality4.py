#  looking just at solar farms that have a status=operating and not other statuses

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

# Correct paths to your Excel files
solar_power_tracker_path = '/Users/jt/Documents/Coding/solarpotentialvsreality/data/Global-Solar-Power-Tracker-December-2023.xlsx'
solar_potential_path = '/Users/jt/Documents/Coding/solarpotentialvsreality/data/solargis_pvpotential_countryranking_2020_data.xlsx'

# Load the datasets
solar_power_tracker_df = pd.read_excel(solar_power_tracker_path, sheet_name='Large Utility-Scale')
solar_potential_df = pd.read_excel(solar_potential_path, sheet_name='Country indicators', skiprows=1)

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

# Print the column names to verify correct loading
print(solar_power_tracker_df.columns)
print(solar_potential_df.columns)

# Filter projects >= 20 MW and sum capacities by country
# Filter projects >= 20 MW and sum capacities by country
solar_power_tracker_df = solar_power_tracker_df[solar_power_tracker_df['Capacity (MW)'] >= 20]

# Filter for only operating solar farms
operating_solar_farms = solar_power_tracker_df[solar_power_tracker_df['Status'] == 'operating']

# Sum capacities by country for operating solar farms
operating_capacity_by_country = operating_solar_farms.groupby('Country')['Capacity (MW)'].sum().reset_index()

solar_potential_summary = solar_potential_df[['Country or Region', 'Average Practical Potential PVOUT']].fillna(0)

scaler = MinMaxScaler()

# Merge with solar potential data
operating_comparison_df = pd.merge(operating_capacity_by_country, solar_potential_summary, left_on='Country', right_on='Country or Region', how='inner')

# Scale the capacity and potential data for operating solar farms
operating_comparison_df[['Capacity (MW)', 'Average Practical Potential PVOUT']] = scaler.fit_transform(operating_comparison_df[['Capacity (MW)', 'Average Practical Potential PVOUT']])

# Scatter Plot for Operating Capacity
plt.figure(figsize=(10, 6))
plt.scatter(operating_comparison_df['Average Practical Potential PVOUT'], operating_comparison_df['Capacity (MW)'])
plt.title('Operating Installed Capacity vs. PV Potential')
plt.xlabel('Normalized PV Potential (kWh/kWp/day)')
plt.ylabel('Normalized Operating Installed Capacity (MW)')
plt.grid(True)
plt.show()

# Reorder operating_comparison_df by 'Capacity (MW)' for the bar plot
operating_comparison_df_sorted = operating_comparison_df.sort_values(by='Capacity (MW)', ascending=False)

# Bar Plot for Operating Capacity
operating_comparison_df_sorted.plot(
    x='Country', 
    y=['Capacity (MW)', 'Average Practical Potential PVOUT'],
    kind='bar', 
    figsize=(15, 7)
)
plt.title('Comparison of Solar Power Potential vs. Operating Installations by Country')
plt.ylabel('Normalized Values')
plt.xlabel('Country')
plt.xticks(rotation=90)
plt.legend(['Operating Installed Capacity (MW)', 'PV Potential (kWh/kWp/day)'])
plt.tight_layout()
plt.show()
