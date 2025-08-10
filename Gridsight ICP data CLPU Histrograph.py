# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 09:32:25 2025

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
start_time_str = '20:00:00'
START_TIME = dt.strptime(start_time_str, '%X').time()
end_time_str1 = '20:30:00'
END_TIME1 = dt.strptime(end_time_str1, '%X').time()
end_time_str2 = '21:00:00'
END_TIME2 = dt.strptime(end_time_str2, '%X').time()
end_time_str3 = '22:00:00'
END_TIME3 = dt.strptime(end_time_str3, '%X').time()
end_time_str4 = '23:00:00'
END_TIME4 = dt.strptime(end_time_str4, '%X').time()

df = pd.read_csv(FILENAME, index_col = False, parse_dates = ['meter_interval_reading_local_timestamp'])

df['Date'] = df['meter_interval_reading_local_timestamp'].dt.date
df['Time'] = df['meter_interval_reading_local_timestamp'].dt.time

df_residential = df[(df['Date'] == DATE) & (df['service_delivery_point_customer_type'] == 'RESIDENTIAL')].reset_index()

# Filter out timestamps of interest first 30min
df_spike_start = df_residential[(df_residential['Time'] == START_TIME)].reset_index()
df_spike_end1 = df_residential[(df_residential['Time'] == END_TIME1)].reset_index()
df_spike1 = df_spike_end1['measured_power_active'] - df_spike_start['measured_power_active']

# Post 1hr
df_spike_end2 = df_residential[(df_residential['Time'] == END_TIME2)].reset_index()
df_spike2 = df_spike_end2['measured_power_active'] - df_spike_start['measured_power_active']

# Post 2hr
df_spike_end3 = df_residential[(df_residential['Time'] == END_TIME3)].reset_index()
df_spike3 = df_spike_end3['measured_power_active'] - df_spike_start['measured_power_active']

# Post 3hr
df_spike_end4 = df_residential[(df_residential['Time'] == END_TIME4)].reset_index()
df_spike4 = df_spike_end4['measured_power_active'] - df_spike_start['measured_power_active']

# Plot histrgrams
plt.figure(figsize=(15, 20))

# First subplot: 30 min post control
plt.subplot(4, 1, 1)  # 3 rows, 1 column, first subplot
plt.hist(df_spike1, bins=40, edgecolor='black', label=f'30 min post control: {start_time_str} to {end_time_str1}')
plt.title('Power Difference (30 min post control)')
plt.xlabel('Power Difference (Watts)')
plt.ylabel('Frequency')
plt.legend()
plt.grid(axis='y', linestyle='-', alpha=0.7)

# Second subplot: 1 hour post control
plt.subplot(4, 1, 2)  # 3 rows, 1 column, second subplot
plt.hist(df_spike2, bins=40, edgecolor='black', label=f'1 hr post control: {start_time_str} to {end_time_str2}')
plt.title('Power Difference (1 hr post control)')
plt.xlabel('Power Difference (Watts)')
plt.ylabel('Frequency')
plt.legend()
plt.grid(axis='y', linestyle='-', alpha=0.7)

# Third subplot: 2 hours post control
plt.subplot(4, 1, 3)  # 3 rows, 1 column, third subplot
plt.hist(df_spike3, bins=40, edgecolor='black', label=f'2 hrs post control: {start_time_str} to {end_time_str3}')
plt.title('Power Difference (2 hrs post control)')
plt.xlabel('Power Difference (Watts)')
plt.ylabel('Frequency')
plt.legend()
plt.grid(axis='y', linestyle='-', alpha=0.7)

# Fourth subplot: 3 hours post control
plt.subplot(4, 1, 4)  # 3 rows, 1 column, third subplot
plt.hist(df_spike4, bins=40, edgecolor='black', label=f'3 hrs post control: {start_time_str} to {end_time_str4}')
plt.title('Power Difference (3 hrs post control)')
plt.xlabel('Power Difference (Watts)')
plt.ylabel('Frequency')
plt.legend()
plt.grid(axis='y', linestyle='-', alpha=0.7)

# Adjust layout
plt.tight_layout()

# Show the plot
plt.show()