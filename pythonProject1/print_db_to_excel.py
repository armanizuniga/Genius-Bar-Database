import sqlite3
import pandas as pd
from openpyxl import load_workbook

"""This program pulls all information from the database and exports to an excel file that can be used for dashboard"""

# Connect to the database
conn = sqlite3.connect('technician_metrics.db')
c = conn.cursor()

# SQL query to join the Technicians and Metrics tables
query = """
SELECT Technicians.*, Metrics.*
FROM Technicians
JOIN Metrics ON Technicians.Technician_ID = Metrics.Technician_ID
"""

# Execute the query and load the data into a DataFrame
df = pd.read_sql_query(query, conn)
# Drop the 'Technician_ID' and 'Metric_ID' columns
df.drop(columns=['Technician_ID', 'Metric_ID'], inplace=True)

# Close the database connection
conn.close()

# Extract first names and add them as a new column
df['First_Name'] = df['Technician_Name'].apply(lambda x: x.split()[0])

# Sort the DataFrame by the 'First_Name' column
df.sort_values(by='First_Name', inplace=True)

# Now, sort the DataFrame by 'Month' and 'Year' while maintaining the order of 'First_Name'
df.sort_values(by=['First_Name', 'Year', 'Month'], inplace=True)

# Drop the 'First_Name' column since it's no longer needed
df.drop(columns=['First_Name'], inplace=True)

# Export the DataFrame to an Excel file
# excel_file_path = '~/Desktop/technician_metrics.xlsx'
# df.to_excel(excel_file_path, index=False)

# Create a dictionary to store DataFrames for each team member
team_members = {name: data for name, data in df.groupby('Technician_Name')}

# Define the path to the Excel file
excel_file_path = '~/Desktop/technician_metrics_individual_sheets.xlsx'

# Create an Excel writer object
with pd.ExcelWriter(excel_file_path, engine='openpyxl') as writer:
    # Iterate through the dictionary and save each DataFrame to a separate sheet
    for name, data in team_members.items():
        # Replace spaces or special characters in sheet names if needed
        sheet_name = name
        data.to_excel(writer, sheet_name=sheet_name, index=False)

print(f"Data has been exported to {excel_file_path}")
