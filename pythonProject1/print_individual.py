import sqlite3
import pandas as pd

# Function to get user input for technician name and date range
technician_name = input("Enter the technician's name: ")
start_year = int(input("Enter the start year (YYYY): "))
start_month = int(input("Enter the start month (MM): "))
end_year = int(input("Enter the end year (YYYY): "))
end_month = int(input("Enter the end month (MM): "))

# Connect to the database
conn = sqlite3.connect('technician_metrics.db')
c = conn.cursor()

# SQL query to fetch data for the specific technician and date range
query = """
SELECT Technicians.*, Metrics.*
FROM Technicians
JOIN Metrics ON Technicians.Technician_ID = Metrics.Technician_ID
WHERE Technicians.Technician_Name = ?
AND ((Metrics.Year > ?) 
OR (Metrics.Year = ? AND Metrics.Month >= ?))
AND ((Metrics.Year < ?)
OR (Metrics.Year = ? AND Metrics.Month <= ?))
"""

# Execute the query and load the data into a DataFrame
df = pd.read_sql_query(query, conn, params=(technician_name,
                                            start_year, start_year, start_month,
                                            end_year, end_year, end_month))

# Close the database connection
conn.close()

# Drop the 'Technician_ID' and 'Metric_ID' columns
df.drop(columns=['Technician_ID', 'Metric_ID'], inplace=True)

print(df)
