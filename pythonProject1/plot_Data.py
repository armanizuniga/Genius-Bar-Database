import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def plot_nps_over_time(name):
    # Connect to the database
    conn = sqlite3.connect('technician_metrics.db')

    # Retrieve data from the database into a Pandas DataFrame
    query = f'''
            SELECT t.Technician_Name, m.Month, m.Year, m.NPS
            FROM Metrics m
            INNER JOIN Technicians t ON m.Technician_ID = t.Technician_ID
            WHERE t.Technician_Name = ?
            '''
    df = pd.read_sql_query(query, conn, params=(name,))

    # Close the database connection
    conn.close()

    # Convert Year and Month columns to datetime format
    df['Date'] = pd.to_datetime(df['Year'].astype(str) + '-' + df['Month'].astype(str))
    # Sort DataFrame by Date column
    df_sorted = df.sort_values(by='Date')
    print(df_sorted)
    # Extract the current year from the sorted DataFrame
    current_year = df_sorted['Year'].iloc[0]

    # Plotting NPS over time
    plt.figure(figsize=(10, 6))
    plt.plot(df_sorted['Date'], df_sorted['NPS'], marker='o', linestyle='-')
    plt.title(f'NPS Over Time for {name} ({current_year})')
    plt.xlabel('Date')
    plt.ylabel('NPS')
    plt.xticks(rotation=45)
    plt.grid(True)

    # Set custom tick labels for the x-axis
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))

    plt.tight_layout()
    plt.show()


def plot_nps_for_genius_technicians():
    # Connect to the database
    conn = sqlite3.connect('technician_metrics.db')

    # Retrieve data from the database into a Pandas DataFrame
    query = '''
            SELECT t.Technician_Name, m.Month, m.Year, m.NPS
            FROM Metrics m
            INNER JOIN Technicians t ON m.Technician_ID = t.Technician_ID
            WHERE t.Technician_Type = 'Genius'
            '''
    df = pd.read_sql_query(query, conn)

    # Close the database connection
    conn.close()

    # Convert Year and Month columns to datetime format
    df['Date'] = pd.to_datetime(df['Year'].astype(str) + '-' + df['Month'].astype(str))
    # Sort DataFrame by Date column
    df_sorted = df.sort_values(by='Date')

    # Plotting NPS over time for each Genius Technician
    plt.figure(figsize=(12, 8))
    for name, group in df_sorted.groupby('Technician_Name'):
        plt.plot(group['Date'], group['NPS'], marker='o', linestyle='-', label=name)

    plt.title('NPS Over Time for Genius Technicians')
    plt.xlabel('Date')
    plt.ylabel('NPS')
    plt.xticks(rotation=45)
    plt.legend(loc='best')
    plt.grid(True)

    # Set custom tick labels for the x-axis
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))

    plt.tight_layout()
    plt.show()


def plot_nps_for_expert_technicians():
    # Connect to the database
    conn = sqlite3.connect('technician_metrics.db')

    # Retrieve data from the database into a Pandas DataFrame
    query = '''
            SELECT t.Technician_Name, m.Month, m.Year, m.NPS
            FROM Metrics m
            INNER JOIN Technicians t ON m.Technician_ID = t.Technician_ID
            WHERE t.Technician_Type = 'Technical Expert'
            '''
    df = pd.read_sql_query(query, conn)

    # Close the database connection
    conn.close()

    # Convert Year and Month columns to datetime format
    df['Date'] = pd.to_datetime(df['Year'].astype(str) + '-' + df['Month'].astype(str))
    # Sort DataFrame by Date column
    df_sorted = df.sort_values(by='Date')

    # Plotting NPS over time for each Genius Technician
    plt.figure(figsize=(12, 8))
    for name, group in df_sorted.groupby('Technician_Name'):
        plt.plot(group['Date'], group['NPS'], marker='o', linestyle='-', label=name)

    plt.title('NPS Over Time for Technical Expert Technicians')
    plt.xlabel('Date')
    plt.ylabel('NPS')
    plt.xticks(rotation=45)
    plt.legend(loc='best')
    plt.grid(True)

    # Set custom tick labels for the x-axis
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))

    plt.tight_layout()
    plt.show()


def plot_nps_for_specialist_technicians():
    # Connect to the database
    conn = sqlite3.connect('technician_metrics.db')

    # Retrieve data from the database into a Pandas DataFrame
    query = '''
            SELECT t.Technician_Name, m.Month, m.Year, m.NPS
            FROM Metrics m
            INNER JOIN Technicians t ON m.Technician_ID = t.Technician_ID
            WHERE t.Technician_Type = 'Technical Specialist'
            '''
    df = pd.read_sql_query(query, conn)

    # Close the database connection
    conn.close()

    # Convert Year and Month columns to datetime format
    df['Date'] = pd.to_datetime(df['Year'].astype(str) + '-' + df['Month'].astype(str))
    # Sort DataFrame by Date column
    df_sorted = df.sort_values(by='Date')

    # Plotting NPS over time for each Genius Technician
    plt.figure(figsize=(12, 8))
    for name, group in df_sorted.groupby('Technician_Name'):
        plt.plot(group['Date'], group['NPS'], marker='o', linestyle='-', label=name)

    plt.title('NPS Over Time for Technical Specialist Technicians')
    plt.xlabel('Date')
    plt.ylabel('NPS')
    plt.xticks(rotation=45)
    plt.legend(loc='best')
    plt.grid(True)

    # Set custom tick labels for the x-axis
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))

    plt.tight_layout()
    plt.show()


def plot_nps_for_all_technicians():
    # Connect to the database
    conn = sqlite3.connect('technician_metrics.db')

    # Retrieve data from the database into a Pandas DataFrame
    query = '''
            SELECT t.Technician_Name, m.Month, m.Year, m.NPS
            FROM Metrics m
            INNER JOIN Technicians t ON m.Technician_ID = t.Technician_ID
            '''
    df = pd.read_sql_query(query, conn)

    # Close the database connection
    conn.close()

    # Convert Year and Month columns to datetime format
    df['Date'] = pd.to_datetime(df['Year'].astype(str) + '-' + df['Month'].astype(str))
    # Sort DataFrame by Date column
    df_sorted = df.sort_values(by='Date')

    # Plotting NPS over time for each Technician
    plt.figure(figsize=(12, 8))
    for name, group in df_sorted.groupby('Technician_Name'):
        plt.plot(group['Date'], group['NPS'], marker='o', linestyle='-', label=name)

    plt.title('NPS Over Time for All Technicians')
    plt.xlabel('Date')
    plt.ylabel('NPS')
    plt.xticks(rotation=45)
    plt.legend(loc='best')
    plt.grid(True)

    # Set custom tick labels for the x-axis
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))

    plt.tight_layout()
    plt.show()


def scatter_plot_metric_relationship(metric_x, metric_y):
    # Connect to the database
    conn = sqlite3.connect('technician_metrics.db')

    # Retrieve data from the database into a Pandas DataFrame
    query = f'''
            SELECT {metric_x}, {metric_y}
            FROM Metrics
            '''
    df = pd.read_sql_query(query, conn)
    print(df)
    # Close the database connection
    conn.close()

    # Plotting Scatter Plot
    plt.figure(figsize=(10, 6))
    plt.scatter(df[metric_x], df[metric_y], alpha=0.5)
    plt.title(f'Scatter Plot: {metric_x} vs {metric_y}')
    plt.xlabel(metric_x)
    plt.ylabel(metric_y)
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_average_metric_per_technician(metric):
    # Connect to the database
    conn = sqlite3.connect('technician_metrics.db')

    # Retrieve data from the database into a Pandas DataFrame
    query = f'''
            SELECT Technician_Name, AVG({metric}) AS Average_{metric}
            FROM Metrics m
            INNER JOIN Technicians t ON m.Technician_ID = t.Technician_ID
            GROUP BY Technician_Name
            '''
    df = pd.read_sql_query(query, conn)

    # Close the database connection
    conn.close()

    # Print top 5 technicians with highest average value of the metric
    top_5 = df.nlargest(5, f'Average_{metric}')
    print(f'Top 5 Technicians with Highest Average {metric}:')
    print(top_5)

    # Plotting Bar Chart
    plt.figure(figsize=(10, 6))
    plt.bar(df['Technician_Name'], df[f'Average_{metric}'], color='skyblue')
    plt.title(f'Average {metric} per Technician')
    plt.xlabel('Technician')
    plt.ylabel(f'Average {metric}')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()


def plot_technician_distribution():
    # Connect to the database
    conn = sqlite3.connect('technician_metrics.db')

    # Retrieve data from the database into a Pandas DataFrame
    query = '''
            SELECT Technician_Type, COUNT(*) AS Technician_Count
            FROM Technicians
            GROUP BY Technician_Type
            '''
    df = pd.read_sql_query(query, conn)

    # Close the database connection
    conn.close()

    # Plotting Pie Chart
    plt.figure(figsize=(8, 8))
    plt.pie(df['Technician_Count'], labels=df['Technician_Type'], autopct='%1.1f%%', startangle=140)
    plt.title('Distribution of Technicians by Role')
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.tight_layout()
    plt.show()


def plot_business_introductions_distribution():
    # Connect to the database
    conn = sqlite3.connect('technician_metrics.db')

    # Retrieve data from the database into a Pandas DataFrame
    query = '''
            SELECT Business_Intros, COUNT(*) AS Technician_Count
            FROM Metrics
            GROUP BY Business_Intros
            '''
    df = pd.read_sql_query(query, conn)

    # Close the database connection
    conn.close()

    # Define your own grouping logic
    def group_intros(intros):
        if intros == 0:
            return 'No Intros'
        elif intros <= 2:
            return '1-2 Intros'
        elif intros >2 and intros <= 5:
            return '3-5 Intros'
        else:
            return 'More than 5 Intros'

    # Apply the grouping logic to create a new column
    df['Grouped_Intros'] = df['Business_Intros'].apply(group_intros)

    # Aggregate counts for the larger categories
    df = df.groupby('Grouped_Intros').sum()

    # Plotting Pie Chart
    plt.figure(figsize=(8, 8))
    plt.pie(df['Technician_Count'], labels=df.index, autopct='%1.1f%%', startangle=140)
    plt.title('Distribution of Technicians by Business Introductions')
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.tight_layout()
    plt.show()


def calculate_total_customers_helped():
    # Connect to the database
    conn = sqlite3.connect('technician_metrics.db')

    # Retrieve data from the database into a Pandas DataFrame
    query = '''
            SELECT t.Technician_Name, SUM(m.Customers_Helped) AS Total_Customers_Helped
            FROM Metrics m
            INNER JOIN Technicians t ON m.Technician_ID = t.Technician_ID
            GROUP BY t.Technician_Name
            '''
    df = pd.read_sql_query(query, conn)

    # Close the database connection
    conn.close()

    # Sort the DataFrame by Total_Customers_Helped in descending order
    df_sorted = df.sort_values(by='Total_Customers_Helped', ascending=False)

    # Print out the top 10 technicians based on Total_Customers_Helped
    print("Top 10 Technicians by Total Customers Helped:")
    print(df_sorted.head(10))


if __name__ == "__main__":
    # Example usage:
    # plot_name = input("Enter Full Name of Technician: ")
    # plot_nps_over_time(plot_name)
    plot_nps_for_genius_technicians()
    # plot_nps_for_expert_technicians()
    # plot_nps_for_specialist_technicians()
    # plot_nps_for_all_technicians()
    # scatter_plot_metric_relationship('SPQH', 'NPS')
    # plot_average_metric_per_technician("Customers_Helped")
    # plot_technician_distribution()
    # plot_business_introductions_distribution()
    # calculate_total_customers_helped()