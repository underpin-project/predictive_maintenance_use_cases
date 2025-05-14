#!pip install seaborn
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import os
import io
import sys
import glob 
import re
from typing import Tuple, Optional

#import pytz
from datetime import datetime, timedelta, timezone
from ydata_profiling import ProfileReport
from openpyxl import load_workbook


sensor_unit_dict = {
    'Generator RPM Max.': 'RPM',
    'Generator RPM Min.': 'RPM',
    'Generator RPM Avg.': 'RPM',
    'Generator RPM StdDev': 'RPM',
    'Generator Bearing Temp. Avg.': '°C',
    'Generator Phase1 Temp. Avg.': '°C',
    'Generator Phase2 Temp. Avg.': '°C',
    'Generator Phase3 Temp. Avg.': '°C',
    'Generator SlipRing Temp. Avg.': '°C',
    'Generator Bearing2 Temp. Avg.': '°C',
    'Generator CoolingWater Temp. Avg.': '°C',
    'Hydraulic Oil Temp. Avg.': '°C',
    'Gear Oil Temp. Avg.': '°C',
    'Gear Bearing Temp. Avg.': '°C',
    'Gear Oil TemperatureBasis Avg.': '°C',
    'Gear Oil TemperatureLevel1 Avg.': '°C',
    'Gear Oil TemperatureLevel2_3 Avg.': '°C',
    'Gear Bearing TemperatureHSRotorEnd Avg.': '°C',
    'Gear Bearing TemperatureHSGeneratorEnd Avg.': '°C',
    'Gear Bearing TemperatureHSMiddle Avg.': '°C',
    'Gear Bearing TemperatureHollowShaftRotor Avg.': '°C',
    'Gear Bearing TemperatureHollowShaftGenerator Avg.': '°C',
    'Nacelle Temp. Avg.': '°C',
    'Avg. direction': '°',
    'Rotor RPM Max.': 'RPM',
    'Rotor RPM Min.': 'RPM',
    'Rotor RPM Avg.': 'RPM',
    'Rotor RPM StdDev': 'RPM',
    'Ambient WindSpeed Max.': 'm/s',
    'Ambient WindSpeed Min.': 'm/s',
    'Ambient WindSpeed Avg.': 'm/s',
    'Ambient WindSpeed StdDev': 'm/s',
    'Ambient WindDir Relative Avg.': '°',
    'Ambient WindDir Absolute Avg.': '°',
    'Ambient Temp. Avg.': '°C',
    'Ambient WindSpeed Estimated Avg.': 'm/s',
    'Grid InverterPhase1 Temp. Avg.': '°C',
    'Grid RotorInvPhase1 Temp. Avg.': '°C',
    'Grid RotorInvPhase2 Temp. Avg.': '°C',
    'Grid RotorInvPhase3 Temp. Avg.': '°C',
    'Grid Production Power Avg.': 'W',
    'Grid Production CosPhi Avg.': None,
    'Grid Production Frequency Avg.': 'Hz',
    'Grid Production VoltagePhase1 Avg.': 'V',
    'Grid Production VoltagePhase2 Avg.': 'V',
    'Grid Production VoltagePhase3 Avg.': 'V',
    'Grid Production CurrentPhase1 Avg.': 'A',
    'Grid Production CurrentPhase2 Avg.': 'A',
    'Grid Production CurrentPhase3 Avg.': 'A',
    'Grid Production Power Max.': 'W',
    'Grid Production Power Min.': 'W',
    'Grid Busbar Temp. Avg.': '°C',
    'Grid Production Power StdDev': 'W',
    'Grid Production ReactivePower Avg.': 'W',
    'Grid Production ReactivePower Max.': 'W',
    'Grid Production ReactivePower Min.': 'W',
    'Grid Production ReactivePower StdDev': 'W',
    'Grid Production PossiblePower Avg.': 'W',
    'Grid Production PossiblePower Max.': 'W',
    'Grid Production PossiblePower Min.': 'W',
    'Grid Production PossiblePower StdDev': 'W',
    'Grid Production PossibleInductive Avg.': 'var',
    'Grid Production PossibleInductive Max.': 'var',
    'Grid Production PossibleInductive Min.': 'var',
    'Grid Production PossibleInductive StdDev': 'var',
    'Grid Production PossibleCapacitive Avg.': 'var',
    'Grid Production PossibleCapacitive Max.': 'var',
    'Grid Production PossibleCapacitive Min.': 'var',
    'Grid Production PossibleCapacitive StdDev': 'var',
    'Active power limit': 'W',
    'Active power limit source': None,
    'Reactive power set point': 'var',
    'Power factor set point': None,
    'Power factor set point source': None,
    'Controller Ground Temp. Avg.': '°C',
    'Controller Top Temp. Avg.': '°C',
    'Controller Hub Temp. Avg.': '°C',
    'Controller VCP Temp. Avg.': '°C',
    'Controller VCP ChokecoilTemp. Avg.': '°C',
    'Controller VCP WaterTemp. Avg.': '°C',
    'Spinner Temp. Avg.': '°C',
    'Spinner Temp. SlipRing Avg.': '°C',
    'Blades PitchAngle Min.': '°',
    'Blades PitchAngle Max.': '°',
    'Blades PitchAngle Avg.': '°',
    'Blades PitchAngle StdDev': '°',
    'HVTrafo Phase1 Temp. Avg.': '°C',
    'HVTrafo Phase2 Temp. Avg.': '°C',
    'HVTrafo Phase3 Temp. Avg.': '°C',
    'HVTrafo AirOutlet Temp. Avg.': '°C',
    'HourCounters Average Total Avg.': 'h',
    'HourCounters Average GridOn Avg.': 'h',
    'HourCounters Average GridOk Avg.': 'h',
    'HourCounters Average TurbineOk Avg.': 'h',
    'HourCounters Average Run Avg.': 'h',
    'HourCounters Average Gen1 Avg.': 'h',
    'HourCounters Average Gen2 Avg.': 'h',
    'HourCounters Average Yaw Avg.': 'h',
    'HourCounters Average ServiceOn Avg.': 'h',
    'HourCounters Average AmbientOk Avg.': 'h',
    'HourCounters Average WindOk Avg.': 'h',
    'HourCounters Average AlarmActive Avg.': 'h',
    'Total hour counter': 'h',
    'Grid on hours': 'h',
    'Grid ok hours': 'h',
    'Turbine ok hours': 'h',
    'Run hours': 'h',
    'Generator 1 hours': 'h',
    'Generator 2 hours': 'h',
    'Yaw hours': 'h',
    'Service hours': 'h',
    'Ambient ok hours': 'h',
    'Wind ok hours': 'h',
    'Production LatestAverage Active Power Gen 0 Avg.': 'W',
    'Production LatestAverage Active Power Gen 1 Avg.': 'W',
    'Production LatestAverage Active Power Gen 2 Avg.': 'W',
    'Production LatestAverage Total Active Power Avg.': 'W',
    'Production LatestAverage Reactive Power Gen 0 Avg.': 'var',
    'Production LatestAverage Reactive Power Gen 1 Avg.': 'var',
    'Production LatestAverage Reactive Power Gen 2 Avg.': 'var',
    'Production LatestAverage Total Reactive Power Avg.': 'var',
    'Active power generator 0, Total accumulated': 'W',
    'Active power generator 1, Total accumulated': 'W',
    'Active power generator 2, Total accumulated': 'W',
    'Total Active power': 'W',
    'Reactive power generator 0,Total accumulated': 'var',
    'Reactive power generator 1, Total accumulated': 'var',
    'Reactive power generator 2, Total accumulated': 'var',
    'Total reactive power': 'var',
    'System Logs First Active Alarm No': None,
    'First Alarm parameter 1 in 10 min frame': None,
    'First Alarm parameter 2 in 10 min frame': None,
}









def createTimestamp(_df: pd.DataFrame) -> pd.DataFrame:

  # Identify rows that are missing time (i.e., no ':')
  _df['is_date_only'] = _df['PCTimeStamp'].apply(lambda x: ':' not in x)

  # Forward fill the dates only for the rows missing time
  _df['DateFilled'] = _df['PCTimeStamp'].where(_df['is_date_only'], None).ffill()

  # Define a function to combine forward-filled dates with the time part
  def combine_date_and_time(row):
    if row['is_date_only']:
        return f"{row['DateFilled']} 0:00"  # Append "0:00" to rows that only have a date
    else:
        return row['PCTimeStamp']  # Keep the original timestamp if it contains time

  # Apply the function to create the new Timestamp column
  _df['Timestamp'] = _df.apply(combine_date_and_time, axis=1)
  _df['Timestamp'] = pd.to_datetime(_df['Timestamp'], format='%m/%d/%Y %H:%M', errors='coerce')

    
  # Drop the helper columns
  _df = _df.drop(columns=['is_date_only', 'DateFilled', 'PCTimeStamp'])
  return _df

  return _df




def checkMonotonyTimestamps(_dfSorted: pd.DataFrame):
  # Step 2: Check for duplicates
  duplicates = _dfSorted[_dfSorted.duplicated(subset='Timestamp', keep=False)]
  if not duplicates.empty:
    print("Duplicate values found:", duplicates)

  # Step 3: Check for missing values
  missing_values = _dfSorted[_dfSorted['Timestamp'].isnull()]
  if not missing_values.empty:
    print("Missing values found:", missing_values)

  # Step 4: Verify monotonic increase
  is_monotonic = _dfSorted['Timestamp'].is_monotonic_increasing
  print("Is monotonic:", is_monotonic)
  
  if not is_monotonic:
    print("Monotonicity is violated.")
    # Find where monotonicity is violated
    prev_value = None
    for index, value in _dfSorted['Timestamp'].items():
        if prev_value is not None and value <= prev_value:
            print("Monotonicity violation at row", index)
            print("Previous value:", prev_value)
            print("Current value:", value)
        prev_value = value

    sys.exit('Error - none monotonic')


def checkTimestamps(_df: pd.DataFrame, _sampleRate: int):

  # Assuming your DataFrame is called df and has a column "Timestamps"

  # 1. Convert the "Timestamps" column to datetime (if not already in datetime format)
  _df['Timestamp'] = pd.to_datetime(_df['Timestamp'])

  # 2. Sort the DataFrame by the Timestamps column
  _df = _df.sort_values(by='Timestamp')

  # 3. Check for missing 30-second intervals

  # Calculate the difference between consecutive timestamps
  _df['time_diff'] = _df['Timestamp'].diff()

  # Check where the difference is not 30 seconds (timedelta of samplerate seconds is pd.Timedelta(seconds=30))
  missing_intervals = _df[(_df['time_diff'] != pd.Timedelta(seconds=_sampleRate)) & (_df.index != 0)]


  # Get the row numbers where the difference is not 30 seconds
  missing_row_numbers = missing_intervals.index.tolist()
  
  # Print rows where the difference is not 30 seconds
  if not missing_intervals.empty:
    print(f"Timestamps with missing or incorrect intervals (not {_sampleRate}s):")
    print(missing_intervals)
    print("\nRow numbers with missing or incorrect intervals:", missing_row_numbers)  
  else:
    print(f"All consecutive timestamps have {_sampleRate}-second intervals.")

  # 4. Generate a complete range of timestamps between the smallest and largest timestamps
  start_timestamp = _df['Timestamp'].min()
  end_timestamp = _df['Timestamp'].max()
  print(start_timestamp, end_timestamp)

  # Generate a date range with a frequency of 30 seconds
  resample_str = f'{_sampleRate}s'
  complete_timestamps = pd.date_range(start=start_timestamp, end=end_timestamp, freq=resample_str)

  # Check for missing timestamps by comparing the complete range with the actual timestamps
  missing_timestamps = complete_timestamps.difference(_df['Timestamp'])

  # Print missing timestamps
  if not missing_timestamps.empty:
    print(f"Missing timestamps (in {_sampleRate}-second intervals) between {start_timestamp} and {end_timestamp}:")
    print(missing_timestamps)
  else:
    print(f"No missing timestamps. All {_sampleRate}-second intervals are present.")






def checkDF(_df: pd.DataFrame):
 
  # Check if any column contains NaN values
  nan_columns = _df.isnull().any()

  # Check if any column contains infinite values
  inf_columns = _df.apply(lambda x: np.isinf(x).any())

  # Combine both checks
  invalid_columns = nan_columns | inf_columns

  # Print detailed information about NaN and infinite values
  print("Columns containing NaN values:")
  nan_present = nan_columns[nan_columns == True]
  if not nan_present.empty:
    print(nan_present)
  else:
    print("No NaN values found in any column.")

  print("\nColumns containing infinite values:")
  inf_present = inf_columns[inf_columns == True]
  if not inf_present.empty:
    print(inf_present)
  else:
    print("No infinite values found in any column.")

  print("\nColumns containing either NaN or infinite values:")
  invalid_present = invalid_columns[invalid_columns == True]
  if not invalid_present.empty:
    print(invalid_present)
  else:
    print("No invalid (NaN or infinite) values found in any column.")

  duplicate_timestamps = _df.index[_df.index.duplicated()]
  print("\nDuplicate Timestamps:")
  if not duplicate_timestamps.empty:
    print(duplicate_timestamps)
  else:
    print("No duplicate timestamps.")



def prepDF(_df: pd.DataFrame, _filename: str) -> Tuple[pd.DataFrame, Optional[int]]:

  # Use regex to replace the pattern '(1)', '(2)', etc. from the column names
  _df.columns = [re.sub(r'\s*\(\d+\)', '', col) for col in _df.columns]

  _df["missing_data"] = _df.isna().any(axis=1)
  
  # Function to extract and process the WGT code from the external string
  def extract_wgt_from_string(external_str: str):
    # Extract the WGT code using regex
    match = re.search(r'WTG(\d+)', external_str)
    if match:
        # Extract the number and convert it to an integer
        return int(match.group(1))
    return None  # or another default value if needed

  # Extract the WGT code from the external string
  wgt_value = extract_wgt_from_string(_filename)

  # Add the 'WGT' column to the DataFrame with the extracted value
  _df['WGT'] = wgt_value
  #print(wgt_value)

  # Rename columns
  _df.columns = _df.columns.str.replace(r'^WTG.*?_(.*)$', r'\1', regex=True)
  
  
  #_df.columns = [col + f" [{sensor_unit_dict[col]}]" if col in sensor_unit_dict else col for col in _df.columns]
  _df.columns = [
    col + f" [{sensor_unit_dict[col]}]" if sensor_unit_dict.get(col) is not None else col
    for col in _df.columns
  ]

  ##this is only for the paper
  # Define the cutoff date
  cutoff_date = pd.to_datetime('2020-07-01')
  # Filter the DataFrame
  _df = _df[_df['Timestamp'] < cutoff_date]  

  _df = _df.drop('WGT', axis=1)
  # Remove 'Timestamp' column and store it
  timestamp_column = _df.pop('Timestamp')

  # Insert 'Timestamp' at the first position (index 0)
  _df.insert(0, 'Timestamp', timestamp_column)
  
  return _df, wgt_value



def hampel_filter(series, window_size=15, n=3):
    """Returns a boolean series where True indicates an outlier."""
    rolling_median = series.rolling(window=window_size, center=True).median()
    mad = series.rolling(window=window_size, center=True).apply(
        lambda x: np.median(np.abs(x - np.median(x))), raw=True
    )
    threshold = n * 1.4826 * mad  # scale factor for Gaussian-like data
    diff = np.abs(series - rolling_median)
    outliers = diff > threshold

    return outliers.fillna(False)



def flagOutliers(df: pd.DataFrame) ->pd.DataFrame:    
  
  
  dict_limits = {
    "Generator Bearing Temp. Avg.": {"min_value": -20, "max_value": 140},
    "Generator Bearing2 Temp. Avg.": {"min_value": -20, "max_value": 105},
    "Gear Bearing Temp. Avg.": {"min_value": 25, "max_value": 90},
    "Rotor RPM Max.": {"max_value": 134},
    "Gear Oil Temp. Avg.": {"min_value": 5},
  }
  
  
  df_outliers_combined = pd.DataFrame(index=df.index)

  for feature, limits in dict_limits.items():
    if feature in df.columns:
        outlier_mask = pd.Series(False, index=df.index)
        
        if "min_value" in limits:
            outlier_mask |= df[feature] < limits["min_value"]
        
        if "max_value" in limits:
            outlier_mask |= df[feature] > limits["max_value"]
        
        df_outliers_combined[f"{feature}_outlier"] = outlier_mask
  
  outlier_summary = df_outliers_combined.sum()
  print(outlier_summary[outlier_summary > 0])

  param_list = [
    'Generator RPM Max.',
    'Generator RPM Min.',
    'Generator RPM Avg.',
    'Generator RPM StdDev',
    'Generator Bearing Temp. Avg.',
    'Generator Phase1 Temp. Avg.',
    'Generator Phase2 Temp. Avg.',
    'Generator Phase3 Temp. Avg.',
    'Generator SlipRing Temp. Avg.',
    'Generator Bearing2 Temp. Avg.',
    'Generator CoolingWater Temp. Avg.',
    'Hydraulic Oil Temp. Avg.',
    'Gear Oil Temp. Avg.',
    'Gear Bearing Temp. Avg.',
    'Gear Oil TemperatureBasis Avg.',
    'Gear Oil TemperatureLevel1 Avg.',
    'Gear Oil TemperatureLevel2_3 Avg.',
    'Gear Bearing TemperatureHSRotorEnd Avg.',
    'Gear Bearing TemperatureHSGeneratorEnd Avg.',
    'Gear Bearing TemperatureHSMiddle Avg.',
    'Gear Bearing TemperatureHollowShaftRotor Avg.',
    'Gear Bearing TemperatureHollowShaftGenerator Avg.',
    'Nacelle Temp. Avg.',
    'Rotor RPM Max.',
    'Rotor RPM Min.',
    'Rotor RPM Avg.',
    'Rotor RPM StdDev',
    'Ambient WindSpeed Max.',
    'Ambient WindSpeed Min.',
    'Ambient WindSpeed Avg.',
    'Ambient WindSpeed StdDev',
    'Ambient WindDir Relative Avg.',
    'Ambient WindDir Absolute Avg.',
    'Ambient Temp. Avg.',
    'Ambient WindSpeed Estimated Avg.',
    'Grid InverterPhase1 Temp. Avg.',
    'Grid RotorInvPhase1 Temp. Avg.',
    'Grid RotorInvPhase2 Temp. Avg.',
    'Grid RotorInvPhase3 Temp. Avg.',
    'Grid Production Power Avg.',
    'Grid Production CosPhi Avg.',
    'Grid Production Frequency Avg.',
    'Grid Production VoltagePhase1 Avg.',
    'Grid Production VoltagePhase2 Avg.',
    'Grid Production VoltagePhase3 Avg.',
    'Grid Production CurrentPhase1 Avg.',
    'Grid Production CurrentPhase2 Avg.',
    'Grid Production CurrentPhase3 Avg.',
    'Grid Production Power Max.',
    'Grid Production Power Min.',
    'Grid Busbar Temp. Avg.',
    'Grid Production Power StdDev',
    'Grid Production ReactivePower Avg.',
    'Grid Production ReactivePower Max.',
    'Grid Production ReactivePower Min.',
    'Grid Production ReactivePower StdDev',
    'Grid Production PossiblePower Avg.',
    'Grid Production PossiblePower Max.',
    'Grid Production PossiblePower Min.',
    'Grid Production PossiblePower StdDev',
    'Grid Production PossibleInductive Avg.',
    'Grid Production PossibleInductive Max.',
    'Grid Production PossibleInductive Min.',
    'Grid Production PossibleInductive StdDev',
    'Grid Production PossibleCapacitive Avg.',
    'Grid Production PossibleCapacitive Max.',
    'Grid Production PossibleCapacitive Min.',
    'Grid Production PossibleCapacitive StdDev',
    'Active power limit',
    'Active power limit source',
    'Reactive power set point',
    'Power factor set point',
    'Power factor set point source',
    'Controller Ground Temp. Avg.',
    'Controller Top Temp. Avg.',
    'Controller Hub Temp. Avg.',
    'Controller VCP Temp. Avg.',
    'Controller VCP ChokecoilTemp. Avg.',
    'Controller VCP WaterTemp. Avg.',
    'Spinner Temp. Avg.',
    'Spinner Temp. SlipRing Avg.',
    'Blades PitchAngle Min.',
    'Blades PitchAngle Max.',
    'Blades PitchAngle Avg.',
    'Blades PitchAngle StdDev',
    'HVTrafo Phase1 Temp. Avg.',
    'HVTrafo Phase2 Temp. Avg.',
    'HVTrafo Phase3 Temp. Avg.',
    'HVTrafo AirOutlet Temp. Avg.',
    'HourCounters Average Total Avg.',
    'HourCounters Average GridOn Avg.',
    'HourCounters Average GridOk Avg.',
    'HourCounters Average TurbineOk Avg.',
    'HourCounters Average Run Avg.',
    'HourCounters Average Gen1 Avg.',
    'HourCounters Average Gen2 Avg.',
    'HourCounters Average Yaw Avg.',
    'HourCounters Average ServiceOn Avg.',
    'HourCounters Average AmbientOk Avg.',
    'HourCounters Average WindOk Avg.',
    'HourCounters Average AlarmActive Avg.',
    'Total hour counter',
    'Grid on hours',
    'Grid ok hours',
    'Turbine ok hours',
    'Run hours',
    'Generator 1 hours',
    'Generator 2 hours',
    'Yaw hours',
    'Service hours',
    'Ambient ok hours',
    'Wind ok hours',
    'Production LatestAverage Active Power Gen 0 Avg.',
    'Production LatestAverage Active Power Gen 1 Avg.',
    'Production LatestAverage Active Power Gen 2 Avg.',
    'Production LatestAverage Total Active Power Avg.',
    'Production LatestAverage Reactive Power Gen 0 Avg.',
    'Production LatestAverage Reactive Power Gen 1 Avg.',
    'Production LatestAverage Reactive Power Gen 2 Avg.',
    'Production LatestAverage Total Reactive Power Avg.',
    'Active power generator 0, Total accumulated',
    'Active power generator 1, Total accumulated',
    'Active power generator 2, Total accumulated',
    'Total Active power',
    'Reactive power generator 0,Total accumulated',
    'Reactive power generator 1, Total accumulated',
    'Reactive power generator 2, Total accumulated',
    'Total reactive power'
]


  param_list33 = [
    'Generator RPM Max.',
    'Generator RPM Min.',
    'Generator RPM Avg.',
    'Generator Bearing Temp. Avg.',
    'Generator Phase1 Temp. Avg.',
    'Generator Phase2 Temp. Avg.',
    'Generator Phase3 Temp. Avg.',
    'Generator SlipRing Temp. Avg.',
    'Generator Bearing2 Temp. Avg.',
    'Generator CoolingWater Temp. Avg.',
    'Hydraulic Oil Temp. Avg.',
    'Gear Oil Temp. Avg.',
    'Gear Bearing Temp. Avg.',
    'Gear Oil TemperatureBasis Avg.',
    'Gear Oil TemperatureLevel1 Avg.',
    'Gear Oil TemperatureLevel2_3 Avg.',
    'Gear Bearing TemperatureHSRotorEnd Avg.',
    'Gear Bearing TemperatureHSGeneratorEnd Avg.',
    'Gear Bearing TemperatureHSMiddle Avg.',
    'Gear Bearing TemperatureHollowShaftRotor Avg.',
    'Gear Bearing TemperatureHollowShaftGenerator Avg.',
    'Nacelle Temp. Avg.',
    'Rotor RPM Max.',
    'Rotor RPM Min.',
    'Rotor RPM Avg.',
    'Ambient WindSpeed Max.',
    'Ambient WindSpeed Min.',
    'Ambient WindSpeed Avg.',
    'Ambient WindDir Relative Avg.',
    'Ambient WindDir Absolute Avg.',
    'Ambient Temp. Avg.',
    'Ambient WindSpeed Estimated Avg.',
    'Grid InverterPhase1 Temp. Avg.',
    'Grid RotorInvPhase1 Temp. Avg.',
    'Grid RotorInvPhase2 Temp. Avg.',
    'Grid RotorInvPhase3 Temp. Avg.',
    'Grid Production Power Avg.',
    'Grid Production CosPhi Avg.',
    'Grid Production Frequency Avg.',
    'Grid Production VoltagePhase1 Avg.',
    'Grid Production VoltagePhase2 Avg.',
    'Grid Production VoltagePhase3 Avg.',
    'Grid Production CurrentPhase1 Avg.',
    'Grid Production CurrentPhase2 Avg.',
    'Grid Production CurrentPhase3 Avg.',
    'Grid Production Power Max.',
    'Grid Production Power Min.',
    'Grid Busbar Temp. Avg.',
    'Grid Production ReactivePower Avg.',
    'Grid Production ReactivePower Max.',
    'Grid Production ReactivePower Min.',
    'Grid Production PossiblePower Avg.',
    'Grid Production PossiblePower Max.',
    'Grid Production PossiblePower Min.',
    'Grid Production PossibleInductive Avg.',
    'Grid Production PossibleInductive Max.',
    'Grid Production PossibleInductive Min.',
    'Grid Production PossibleCapacitive Avg.',
    'Grid Production PossibleCapacitive Max.',
    'Grid Production PossibleCapacitive Min.',
    'Controller Ground Temp. Avg.',
    'Controller Top Temp. Avg.',
    'Controller Hub Temp. Avg.',
    'Controller VCP Temp. Avg.',
    'Controller VCP ChokecoilTemp. Avg.',
    'Controller VCP WaterTemp. Avg.',
    'Spinner Temp. Avg.',
    'Spinner Temp. SlipRing Avg.',
    'Blades PitchAngle Min.',
    'Blades PitchAngle Max.',
    'Blades PitchAngle Avg.',
    'HVTrafo Phase1 Temp. Avg.',
    'HVTrafo Phase2 Temp. Avg.',
    'HVTrafo Phase3 Temp. Avg.',
    'HVTrafo AirOutlet Temp. Avg.',
    'Production LatestAverage Active Power Gen 0 Avg.',
    'Production LatestAverage Active Power Gen 1 Avg.',
    'Production LatestAverage Active Power Gen 2 Avg.',
    'Production LatestAverage Total Active Power Avg.',
    'Production LatestAverage Reactive Power Gen 0 Avg.',
    'Production LatestAverage Reactive Power Gen 1 Avg.',
    'Production LatestAverage Reactive Power Gen 2 Avg.',
    'Production LatestAverage Total Reactive Power Avg.',
  ]


  param_list2 = [
    'Generator RPM Max.',
    'Generator RPM Min.',
    'Generator RPM Avg.',
    'Generator Bearing Temp. Avg.',
    'Generator Phase1 Temp. Avg.',
  ]


  df_outliers_hampel = pd.DataFrame()#index=df.index)
  df_outliers_hampel['Timestamp'] = df['Timestamp'].copy()

  # Track matched outlier column names
  cols_to_keep = []
  cols_to_keep.append('Timestamp')


  for param in param_list:
    # Find the first matching column that contains the param string
    matched_cols = [col for col in df.columns if param in col]
    
    if matched_cols:
        col_name = matched_cols[0]  # use the first match
        print(f"Matched: {param} → {col_name}")
        outlier_flags = hampel_filter(df[col_name]).astype(int) 
        df_outliers_hampel[f"{col_name}"] = outlier_flags
        outlier_col_name = f"{col_name}"
        cols_to_keep.append(outlier_col_name)
    else:
        print(f"No match found in df for: {param}")

  print(df_outliers_hampel.columns)
  
  #df_outliers_hampel = df_outliers_hampel[cols_to_keep]
  #print(df_outliers_hampel.sum())
  return df_outliers_hampel

  



def profileData2(_df: pd.DataFrame, _path: str, _wgt_value: int):
  
  profile = ProfileReport(_df,
                        title="Predictive Maintenance Windpark Data",
                        dataset={"description": "This profiling report was generated for UNDERPIN",
                                 "copyright_holder": "AIT",
                                 "copyright_year": "2024",
                                },
                        minimal=True,        
                        #explorative=True,
                       )
  ff = 'WTG_profile_' + str(_wgt_value).zfill(2) + '.html'
  f1_out = os.path.join(_path, ff)
  profile.to_file(f1_out)


def profileData(_df: pd.DataFrame, _path: str, _name: str, _wgt_value: int):
  
  profile = ProfileReport(_df,
                        title="Six-Month Monitoring Dataset from a 10-Turbine Onshore Wind Farm in Greece",
                        dataset={"description": "Six-Month Monitoring Dataset from a 10-Turbine Onshore Wind Farm in Greece.",
                                 "url": "https://doi.org/10.5281/zenodo.14546479",
                                 "license": "Creative Commons Attribution 4.0 International",
                                 "publication_date": "2025-05-16"
#                                 "copyright_holder": "Creative Commons Attribution 4.0 International",
                                # "copyright_year": "2025",
                                },
                        explorative=True,
                        #correlations={"pearson": False, "spearman": False, "kendall": False, "phi_k": False, "cramers": False},
                        interactions={"continuous": False},
                        #missing_diagrams={"heatmap": False, "dendrogram": False},
                       )
  ff = _name + str(_wgt_value).zfill(2) + '.html'
  f1_out = os.path.join(_path, ff)
  profile.to_file(f1_out)

  

def prep_scada_data(config: dict):
    
  #sampleRate = 60 #in seconds
  f1 = config["scada_data_path"] 
  fout = config["scada_output_path"]
  print(f1)
  csv_data = sorted(glob.glob(os.path.join(f1, '*data*.csv')))
  print(csv_data)

  # Check if the folder exists
  if not os.path.exists(fout):
    # Create the folder
    os.makedirs(fout)
    print(f"Folder created at: {fout}")
  else:
    print("Folder already exists.")  


  for ii, _f1 in enumerate(csv_data):
    print('FILENAME', _f1)
    #1 step
    print('1 Step: Read data as csv')
    df = pd.read_csv(_f1, sep=',', low_memory=False)
    print('before', df.shape)
     
    #2 step 
    print('2 Step: Remove cols/ rows')
    df = createTimestamp(df)
 
    #3 step:
    print('3 Step: Correct timestamps/ column types')
    df, wgt_value = prepDF(df, _f1)

    print('4 Step: check dataframe\n')
    checkDF(df)

    print('5 Step: checkMonotonyTimestamps\n')
    checkMonotonyTimestamps(df)

    print('6 Step: checkTimestamps\n')
    checkTimestamps(df, int(config["sample_rate"]))
    
        
    print('7 Step: create profile\n')
    profileData(df.copy(), fout, config["scada_profile_name"], wgt_value)
        
    ff = 'WTG_data_' + str(wgt_value).zfill(2) + '.csv'
    f1_out = os.path.join(fout, ff)
    df.to_csv(f1_out, index=False)


    print('8 Step: flag outliers\n')
    df_outliers = flagOutliers(df.copy())    
    
    print('9 Step: create profile of outliers\n')
    profileData(df_outliers.copy(), fout, config["outlier_profile_name"], wgt_value)

    ff = 'WTG_outliers_' + str(wgt_value).zfill(2) + '.csv'
    f1_out = os.path.join(fout, ff)
    df_outliers.to_csv(f1_out, index=False)
    #sys.exit('Ss')



def try_parsing_date(x):
    for fmt in ('%m/%d/%Y %I:%M:%S.%f %p', '%m/%d/%Y %I:%M %p', '%m/%d/%Y %H:%M'):
        try:
            return pd.to_datetime(x, format=fmt)
        except (ValueError, TypeError):
            continue
    return pd.NaT



def updateDF(_df: pd.DataFrame) -> Tuple[pd.DataFrame, int]:

  #print(_df.head)
  #print(_df.columns)

  # Renaming the column
  _df.rename(columns={'Unit': 'WTG'}, inplace=True)

  # Deleting rows where WTG is equal to 'Server'
  # Keep rows where "WTG" matches the pattern WTG01 to WTG10
  _df = _df[_df["WTG"].astype(str).str.match(r"^WTG(0[1-9]|10)$")]

  
  # Step 2: Delete rows where all values are NaN
  _df = _df.dropna(how='all') 

  # Step 2: Extract the number from WTG and convert to integer
  _df['WTG'] = _df['WTG'].str.extract(r'(\d+)').astype(int)
  first_wtg_value = _df['WTG'][0]


  # Drop unnecessary columns 'Unnamed: 11', 'Unnamed: 12', 
  columns_to_drop = ['Affected', 'Remark', 'Unnamed: 13', 'Unnamed: 14',
                       'Value changed', 'Old value', 'New value'] 
  _df = _df.drop(columns=[col for col in columns_to_drop if col in _df.columns])

  # Special handling if 'Unnamed: 5' and 'Unnamed: 6' exist
  if {'Detected', 'Unnamed: 5', 'Unnamed: 6'}.issubset(_df.columns):
        # Create the new datetime strings
        combined_datetime = _df['Detected'].astype(str).str.split(' ').str[0] + ' ' + \
                            _df['Unnamed: 5'].astype(str) + ' ' + _df['Unnamed: 6'].astype(str)
        
        # Now parse it using the correct format
        _df['Detected'] = pd.to_datetime(
            combined_datetime, 
            format='%Y-%m-%d %I:%M:%S %p', 
            errors='coerce'
        )

        # Drop the helper columns
        _df = _df.drop(columns=['Unnamed: 5', 'Unnamed: 6'])
  else:

    _df['Detected'] = _df['Detected'].apply(try_parsing_date)


  # Step 2: Drop rows where 'Detected' is NaT (not a time)
  _df = _df.dropna(subset=['Detected'])

  #### ----------- Handling Device + ack. + Unnamed:9 ----------- ####
  if {'Device', 'ack.', 'Unnamed: 9'}.issubset(_df.columns):
        combined_device_datetime = _df['Device'].astype(str).str.split(' ').str[0] + ' ' + \
                                   _df['ack.'].astype(str) + ' ' + _df['Unnamed: 9'].astype(str)
        
        _df['Device ack.'] = pd.to_datetime(
            combined_device_datetime,
            format='%Y-%m-%d %I:%M:%S %p',
            errors='coerce'
        )

        _df = _df.drop(columns=['Device', 'ack.', 'Unnamed: 9'])


  # Handling Reset/Run, Unnamed: 11, Unnamed: 12 columns
  if {'Reset/Run', 'Unnamed: 11', 'Unnamed: 12'}.issubset(_df.columns):
        combined_reset_run = _df['Reset/Run'].astype(str) + ' ' + \
                             _df['Unnamed: 11'].astype(str) + ' ' + _df['Unnamed: 12'].astype(str)
        
        # You can now keep the original 'Reset/Run' column or split it as needed
        _df['Reset/Run'] = combined_reset_run

        # Drop the redundant columns 'Unnamed: 11' and 'Unnamed: 12'
        _df = _df.drop(columns=['Unnamed: 11', 'Unnamed: 12'])

 

  # Convert the "Severity" column to float
  _df['Severity'] = pd.to_numeric(_df['Severity'], errors='coerce')

  # Assuming 'df' is your DataFrame
  new_order = ['WTG', 'Code', 'Description', 'Detected', 'Device ack.', 'Reset/Run', 'Duration', 'Event type', 'Severity']
  _df = _df[new_order]
  

  ##this is only for the paper
  # Define the cutoff date
  cutoff_date = pd.to_datetime('2020-07-01')
  # Filter the DataFrame
  _df = _df[_df['Detected'] < cutoff_date]  


  return _df, first_wtg_value



def prep_log_data(config: dict):
  f1 = config["scada_data_path"] 
  fout = config["scada_output_path"]
  

  print(f1)
  csv_data = sorted(glob.glob(os.path.join(f1, '*Logs*.csv')))
  print(csv_data)

  # Check if the folder exists
  if not os.path.exists(fout):
    # Create the folder
    os.makedirs(fout)
    

  for ii, _f1 in enumerate(csv_data):
    print('FILENAME', _f1)
    #1 step
    print('1 Step: Read data as csv')
    with open(_f1, 'r', encoding='utf-8', errors='replace') as f:
      first_line = f.readline()
      sep = ';' if first_line.count(';') > first_line.count(',') else ','
    df_logs = pd.read_csv(_f1, sep=sep, low_memory=False, encoding='utf-8', on_bad_lines='warn', encoding_errors='replace')

    #df_logs = pd.read_csv(_f1, sep=',', low_memory=False,  encoding='utf-8', on_bad_lines='warn', encoding_errors= "replace")
    print('before', df_logs.columns)
     
    #2 step 
    print('2 Step: Remove cols/ rows')
    df_logs, wgt_value = updateDF(df_logs)
    print('after', len(df_logs.columns), df_logs.columns)
 
    #Replace '�' in the DataFrame with an empty string or something more appropriate
    df_logs = df_logs.replace('�', '', regex=True)
    df_logs = df_logs.drop('WTG', axis=1)
    
    print('3 Step: create profile\n')
    profileData(df_logs, fout, config["logs_profile_name"], wgt_value)
    #profileData2(df, fout, wgt_value)
    #sys.exit('stop')
    
    print('4 Step: Store csv')
    ff = 'WTG_logs_' + str(wgt_value).zfill(2) + '.csv'
    f1_out = os.path.join(fout, ff)
    df_logs.to_csv(f1_out, index=False)
    



def analysisOutliers(config: dict):
  # Folder where your CSV files are stored
  folder_path = config["scada_output_path"]

  # Pattern to match files like: 'something_outliers.csv'
  file_pattern = os.path.join(folder_path, "*outliers*.csv")

  # Find all matching CSV files
  outlier_files = sorted(glob.glob(file_pattern))

  for file in outlier_files:
    print(f"\nProcessing file: {os.path.basename(file)}")

    # Read CSV file
    df = pd.read_csv(file)

    # Drop 'Timestamp' column if it exists
    if "Timestamp" in df.columns:
        df = df.drop(columns=["Timestamp"])

    # Flatten all values into a single array
    values = df.values.flatten()

    # Count total 1s and 0s (skip NaNs)
    total_ones = (values == 1).sum()
    total_zeros = (values == 0).sum()
    total_values = total_ones + total_zeros

    # Calculate percentages
    if total_values > 0:
        perc_ones = (total_ones / total_values) * 100
        perc_zeros = (total_zeros / total_values) * 100
    else:
        perc_ones = perc_zeros = 0

    print(f"  Total 1s (outliers): {total_ones}")
    print(f"  Total 0s (non-outliers): {total_zeros}")
    print(f"  Percentage of 1s: {perc_ones:.2f}%")
    print(f"  Percentage of 0s: {perc_zeros:.2f}%")




def adjustXlsx(f1: str):
    # Load the workbook
    wb = load_workbook(f1)
    
    # Loop through all sheets
    for ws in wb.worksheets:
        # Adjust the column width for each sheet
        for col in ws.columns:
            max_length = 0
            column = col[0].column_letter  # Get column letter
            for cell in col:
                try:
                    if cell.value:  # Skip empty cells
                        max_length = max(max_length, len(str(cell.value)))
                except:
                    pass
            adjusted_width = (max_length + 2)  # Add padding
            ws.column_dimensions[column].width = adjusted_width

    # Save the adjusted file
    wb.save(f1)


def main_export(config: dict):
  fin = config["scada_output_path"]
  filename = config["scada_xlsx_filename"]
  csv_data = sorted(glob.glob(os.path.join(fin, '*data*.csv')))
  print(csv_data)
  csv_outliers = sorted(glob.glob(os.path.join(fin, '*outliers*.csv')))
  print(csv_outliers)  
  csv_logs = sorted(glob.glob(os.path.join(fin, '*logs*.csv')))
  print(csv_logs)

  # Save the DataFrame to an Excel file
  f1 = os.path.join(fin, filename)
  with pd.ExcelWriter(f1) as writer:
    for _f1 in csv_data:
      print(_f1)
      df = pd.read_csv(_f1, sep=',', low_memory=False)
      
      # Extract the numeric part between 'WTG_data_' and '.csv'
      match = re.search(r'WTG_data_(\d+)\.csv', _f1)
      if match:
        number = int(match.group(1))
        print(number)  # ➡️ 1
    
      # Create the new filename
      new_sheetname = f"WTG_{number:02}_data.csv"
      df.to_excel(writer, index=False, sheet_name=new_sheetname)

    for _f1 in csv_outliers:
      print(_f1)
      df = pd.read_csv(_f1, sep=',', low_memory=False)
      
      # Extract the numeric part between 'WTG_data_' and '.csv'
      match = re.search(r'WTG_outliers_(\d+)\.csv', _f1)
      if match:
        number = int(match.group(1))
        print(number)  # ➡️ 1
    
      # Create the new filename
      new_sheetname = f"WTG_{number:02}_outliers.csv"
      df.to_excel(writer, index=False, sheet_name=new_sheetname)

    for _f1 in csv_logs:
      print(_f1)
      df = pd.read_csv(_f1, sep=',', low_memory=False)
      
      # Extract the numeric part between 'WTG_data_' and '.csv'
      # Extract the numeric part between 'WTG_data_' and '.csv'
      match = re.search(r'WTG_logs_(\d+)\.csv', _f1)
      if match:
        number = int(match.group(1))
        print(number)  # ➡️ 1
        
      # Create the new filename
      new_sheetname = f"WTG_{number:02}_logs.csv"      
      df.to_excel(writer, index=False, sheet_name=new_sheetname)

  print('start adjustXlsx - takes ages')
  adjustXlsx(f1)



  
if __name__ == "__main__":
  
  json_file_path = './config.json'
  with open(json_file_path) as f:
    config = json.load(f)

  print(type(config))
  print(config)
  
  
         
  prep_scada_data(config)
  prep_log_data(config)
  main_export(config)
  
  analysisOutliers(config)
  
