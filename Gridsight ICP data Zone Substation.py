# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 09:24:54 2025

@author: UnaDrayton
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime as dt

FILENAME = r'Load_Control_Extract_ZSS_ICPs_Jan_2025.csv'
SCADA_FILENAME = r'ZSS Load Control Event 20.07.24.csv'
date_string = '2024-07-20'
DATE = dt.strptime(date_string, '%Y-%m-%d').date()
READINGS_PER_DAY = 48 # Reading taken every 30min
HOURS_IN_DAY = 24
POWER_CONVERSION = (11000/(3**(1/2))) / 1000000
# Indexes of control periods
CONTROL_START_INDEX_1 = 15
CONTROL_END_INDEX_1 = 17
CONTROL_START_INDEX_2 = 34
CONTROL_END_INDEX_2 = 41

df = pd.read_csv(FILENAME, index_col = False, parse_dates = ['meter_interval_reading_local_timestamp'])
df_SCADA = pd.read_csv(SCADA_FILENAME, index_col = False, parse_dates = ['DateTime'], dayfirst = True)


df['Date'] = df['meter_interval_reading_local_timestamp'].dt.date
df['Time'] = df['meter_interval_reading_local_timestamp'].dt.time

# Extract date of interest for Residential Smart Meter Data
df_date = df[(df['Date'] == DATE) & (df['service_delivery_point_customer_type'] == 'RESIDENTIAL')].reset_index()

# Group by ICP and average RESIDENTIAL
df_date['TimeBin'] = df_date.index % READINGS_PER_DAY
df_averaged = (df_date.groupby('TimeBin')
               .agg({
                   'measured_power_active': 'mean',
                   'meter_interval_reading_local_timestamp': 'first', # Keeps the first DateTime
                   'service_delivery_point_customer_type': 'first', # Keeps the first customer type                  
                   }))
df_averaged = df_averaged.sort_values(by = 'TimeBin', ascending = False).reset_index() #dates in reverse
df_averaged['measured_power_active'] = df_averaged['measured_power_active'] / 1000

# Group by ICP and average BUSINESS
df_business = df[(df['Date'] == DATE) & (df['service_delivery_point_customer_type']== 'BUSINESS')].reset_index()
df_business['TimeBin'] = df_business.index % READINGS_PER_DAY
df_bus_averaged = (df_business.groupby('TimeBin')
               .agg({
                   'measured_power_active': 'sum',
                   'meter_interval_reading_local_timestamp': 'first', # Keeps the first DateTime
                   'service_delivery_point_customer_type': 'first', # Keeps the first customer type                  
                   }))
df_bus_averaged = df_bus_averaged.sort_values(by = 'TimeBin', ascending = False).reset_index() #dates in reverse
# df_bus_averaged['measured_power_active'] = df_bus_averaged['measured_power_active'] / 1000000


# Process SCADA data
df_SCADA['Total Current'] = (df_SCADA['Current A_x'] + df_SCADA['Current B_x'] + df_SCADA['Current C_x'] + df_SCADA['Current A_y'] + df_SCADA['Current B_y'] + df_SCADA['Current C_y'] + df_SCADA['Current A'] + df_SCADA['Current B'] + df_SCADA['Current C'])
df_SCADA['Total Load'] = df_SCADA['Total Current'] * POWER_CONVERSION
df_SCADA = df_SCADA[['DateTime', 'Total Load']]
df_SCADA = df_SCADA[df_SCADA.index % 2 == 0].reset_index() # This data is every 15min so take every second reading

# Total load
fig, ax1 = plt.subplots(figsize=(10, 6))
line1, = ax1.plot(df_SCADA['Total Load'], 'o-', color='darkorange', label='Total Zone Substation Profile')
ax1.set_ylim(0, 4)
ax1.set_xlim(0, READINGS_PER_DAY)

# Format x-axis
x_ticks = np.arange(HOURS_IN_DAY)  # Tick every hour
x_labels = [f'{str(time).zfill(2)}:00' for time in x_ticks]
plt.xticks(np.arange(0, READINGS_PER_DAY, 2), x_labels, rotation=60)
plt.xlabel('Time (HH:MM)')
plt.grid()


# Residential and business
ax2 = ax1.twinx()
line2, = ax2.plot(df_averaged['measured_power_active'], 'o-', label='Average Residential Profile')
# line3, = ax2.plot(df_bus_averaged['measured_power_active'], 'go-', label='Average Bussiness Profile')
ax2.set_ylim(0, 4)
ax2.set_xlim(0, READINGS_PER_DAY)

# Highlight control periods
plt.axvspan(CONTROL_START_INDEX_1, CONTROL_END_INDEX_1, color='y', alpha=0.5)
plt.axvspan(CONTROL_START_INDEX_2, CONTROL_END_INDEX_2, color='y', alpha=0.5)

# Create a patch for the legend
from matplotlib.patches import Patch
patch = Patch(color='y', alpha=0.5, label='Control Period')


# Combine legends
lines = [line1, line2, patch]  # Add line3 when doing business as well
labels = [line.get_label() for line in lines]
ax1.legend(lines, labels, loc='upper left', bbox_to_anchor=(0, 1), facecolor='white', framealpha=1)

# Labels and title
# plt.title('Zone Substation Ripple Control')
ax1.set_ylabel('Load (MVA) - Total Zone')
ax2.set_ylabel('Load (kW) - Residential')

plt.show()

