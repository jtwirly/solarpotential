#  looking not just at solar farms that have a status=operating but also other statuses

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

# Instead of filtering by 'operating' status, let's group by both 'Country' and 'Status'
capacity_by_country_status = solar_power_tracker_df.groupby(['Country', 'Status'])['Capacity (MW)'].sum().reset_index()

# Pivot the data to have statuses as columns and countries as rows
capacity_pivot = capacity_by_country_status.pivot(index='Country', columns='Status', values='Capacity (MW)').fillna(0)

# Add a total capacity by country, regardless of status
capacity_pivot['Total Capacity'] = capacity_pivot.sum(axis=1)

# Now, let's compare the total capacity (regardless of status) with the potential
solar_potential_summary = solar_potential_df[['Country or Region', 'Average Practical Potential PVOUT']].fillna(0)

# Merge the total capacity with the solar potential
comparison_df = pd.merge(capacity_pivot.reset_index(), solar_potential_summary, left_on='Country', right_on='Country or Region', how='inner')

# Scale the capacity and potential data
scaler = MinMaxScaler()
comparison_df[['Total Capacity', 'Average Practical Potential PVOUT']] = scaler.fit_transform(comparison_df[['Total Capacity', 'Average Practical Potential PVOUT']])

# Scatter Plot for Total Capacity
plt.figure(figsize=(10, 6))
plt.scatter(comparison_df['Average Practical Potential PVOUT'], comparison_df['Total Capacity'])
plt.title('Total Installed Capacity vs. PV Potential')
plt.xlabel('Normalized PV Potential (kWh/kWp/day)')
plt.ylabel('Normalized Total Installed Capacity (MW)')
plt.grid(True)
plt.show()

# Reorder comparison_df by 'Total Capacity' for the bar plot
comparison_df_sorted = comparison_df.sort_values(by='Total Capacity', ascending=False)

# Bar Plot for Total Capacity
comparison_df_sorted.plot(
    x='Country', 
    y=['Total Capacity', 'Average Practical Potential PVOUT'],
    kind='bar', 
    figsize=(15, 7)
)
plt.title('Comparison of Solar Power Potential vs. Total Installations by Country')
plt.ylabel('Normalized Values')
plt.xlabel('Country')
plt.xticks(rotation=90)
plt.legend(['Total Installed Capacity (MW)', 'PV Potential (kWh/kWp/day)'])
plt.tight_layout()
plt.show()