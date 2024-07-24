import sqlite3
import pandas as pd
import update_Database
import random

# Add a metric to the table
# c.execute(f"ALTER TABLE Metrics ADD COLUMN opportunities INTEGER")
# Plotting
# 1. Figure out which metrics are good to plot against
# 2. Plot everything for individuals
# 3. Ability to choose date ranges to plot, by quarter, year, etc.
# 5. Create wrap up Excel spreadsheets for individual with total metrics


# Read Excel files into dataframes
def read_from_excel_sheets():
    gen_df = pd.read_excel("~/Desktop/Genius.xlsx")
    exp_df = pd.read_excel("~/Desktop/Technical Expert.xlsx")
    special_df = pd.read_excel("~/Desktop/Technical Specialist.xlsx")
    return gen_df, exp_df, special_df


# pre-check
# 1. Look for any technicians to add or remove from database by comparing current employees -- Completed
# 2. Make any changes to roles from promotions Tech specialist -> Tech Expert -> Genius and update -- Completed
# 3. Check if changes from part-time to full-time or vice versa -- Completed
def pre_check(current, data):
    # Lists to hold technicians to be added and removed from database
    list_to_add = []
    list_to_remove = []

    # Connect to the database
    conn = sqlite3.connect('technician_metrics.db')
    c = conn.cursor()

    # Fetch all technician names from SQL table
    c.execute('''SELECT Technician_Name FROM Technicians''')
    sql_table_names = [row[0] for row in c.fetchall()]

    for name1 in sql_table_names:
        if name1 in current:
            continue
        else:
            list_to_remove.append(name1)

    for name2 in current:
        if name2 not in sql_table_names:
            list_to_add.append(name2)

    for remove_name in list_to_remove:
        update_Database.remove_technician(remove_name)
        print("Successfully removed:", remove_name)

    for add_name in list_to_add:
        series_data = data[data['Name'] == add_name].iloc[0]
        s_name = series_data['Name']
        s_role = series_data['Job']
        s_type = series_data['Type']
        update_Database.add_technician(s_name, s_role, s_type)

    for role_change in current:
        series_data = data[data['Name'] == role_change].iloc[0]
        new_job = series_data['Type']
        new_role = series_data['Job']

        # SQL query to fetch the "Job" data based on "Technician_Name"
        query = "SELECT Job FROM Technicians WHERE Technician_Name = ?"
        # Execute the query
        c.execute(query, (role_change,))  # Parameterized query to prevent SQL injection
        # Fetch the current "Job" value
        current_job = c.fetchone()

        # If the record exists, check if "Job" matches the new value
        if current_job is not None:
            if current_job[0] != new_job:  # If they don't match
                # Update the "Job" value in the database
                update_query = "UPDATE Technicians SET Job = ? WHERE Technician_Name = ?"
                c.execute(update_query, (new_job, role_change))
                conn.commit()  # Commit the changes
                print(f"Updated 'Job' for {role_change} to '{new_job}'")
            else:
                continue
        else:
            print(f"Technician with name '{role_change}' not found")

        # SQL query to fetch the "Job" data based on "Technician_Name"
        query = "SELECT Technician_Type FROM Technicians WHERE Technician_Name = ?"
        # Execute the query
        c.execute(query, (role_change,))  # Parameterized query to prevent SQL injection
        # Fetch the current "Job" value
        current_role = c.fetchone()
        # If the record exists, check if "Job" matches the new value
        if current_role is not None:
            if current_role[0] != new_role:  # If they don't match
                # Update the "Job" value in the database
                update_query = "UPDATE Technicians SET Technician_Type = ? WHERE Technician_Name = ?"
                c.execute(update_query, (new_role, role_change))
                conn.commit()  # Commit the changes
                print(f"Updated 'Role' for {role_change} to '{new_role}'")
            else:
                continue
        else:
            print(f"Technician with name '{role_change}' not found")

    # Commit changes and close connection
    conn.commit()
    conn.close()


# Update new metric data by month
# 1. Insert new metric data for each technician -- Completed
def insert_metrics(name_list, data):
    for name in name_list:
        # Connect to the database
        conn = sqlite3.connect('technician_metrics.db')
        c = conn.cursor()

        name_series = data[data['Name'] == name].iloc[0]

        c.execute('''INSERT INTO Metrics (Technician_ID, SPQH, Customers_Helped, Mac_Duration,
                             Mobile_Duration, NPS, TMS, SUR, Business_Intros, Discussed_AppleCare,
                             Offered_Trade_in, Month, Year, survey, full_survey, opportunities, Mac_Sessions_Delivered,
                             Mobile_Sessions_Delivered, Mobile_Support_Hours, Mac_Support_Hours,
                             iPhone_Repair_Hours, Mac_Repair_Hours, Repair_Pickup_Hours, GB_On_Point_Hours,
                             Daily_Download_Hours, Guided_Hours, Connection_Hours, Total_Hours)
                             VALUES ((SELECT Technician_ID FROM Technicians WHERE Technician_Name = ?),
                             ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? , ? , ? , ?, ? , ?, ? ,? ,? ,? )''',
                  (name_series["Name"], name_series["SPQH"], int(name_series["Customers Helped"]),
                   int(name_series["Mac Duration"]), int(name_series["Mobile Duration"]), int(name_series["NPS"]),
                   int(name_series["TMS"]), int(name_series["SUR"]), int(name_series["Business Intros"]),
                   int(name_series["Discussed AppleCare"]), int(name_series["Offered Trade In"]),
                   int(name_series["Month"]), int(name_series["Year"]), int(name_series["Survey Qty"]),
                   int(name_series["Full Survey Qty"]), int(name_series["Opportunities"]),
                   int(name_series["Mac Sessions"]), int(name_series["Mobile Sessions"]),
                   name_series["Mobile Support"], name_series["Mac Support"], name_series["iPhone Repair"],
                   name_series["Mac Repair"], name_series["Repair Pickup"], name_series["GB On Point"],
                   name_series["Daily Download"], name_series["Guided"], name_series["Connection"],
                   name_series["Total Hours"],))

        # Commit changes and close connection
        conn.commit()
        conn.close()


def plot_test(name_list, data):
    # Connect to the database
    conn = sqlite3.connect('technician_metrics.db')
    c = conn.cursor()
    technician_name = "Armani Zuniga"  # The name of the technician to search for

    query = """
    SELECT * FROM Metrics
    WHERE Technician_ID = (
        SELECT Technician_ID FROM Technicians WHERE Technician_Name = ?
    )
    """
    # Use pandas to execute the query and get results into a DataFrame
    df = pd.read_sql(query, conn, params=(technician_name,))

    # Display the DataFrame
    print(df)

    # Commit changes and close connection
    conn.commit()
    conn.close()


if __name__ == "__main__":
    # Read Excel files into dataframes
    genius_df, expert_df, specialist_df = read_from_excel_sheets()
    # Concatenate the DataFrames along the rows (axis=0)
    combined_df = pd.concat([genius_df, expert_df, specialist_df], axis=0)
    # Reset the index if needed (optional, to avoid duplicate indices)
    combined_df.reset_index(drop=True, inplace=True)
    # Get list of all current Genius Bar team members
    current_gb_employees = combined_df['Name'].tolist()
    test_list = current_gb_employees[:-10]
    # Initialize an empty dictionary to store the names and their random percentages
    name_percentage = {}

    # Assign random opportunities and failed opportunities to each name
    for name in test_list:
        opportunities = random.randint(30, 66)  # Between 20 and 50 opportunities
        failed_opportunities = random.randint(0, 2)  # Between 1 and 2 failed opportunities
        # Create a dictionary for each name to hold the metrics
        name_percentage[name] = {
            "Opportunities": opportunities,
            "Failed Opportunities": failed_opportunities
        }

    # Display the resulting dictionary
    print("Name with Opportunities and Failed Opportunities:")
    for name, data in name_percentage.items():
        print(f"{name}: Opportunities = {data['Opportunities']}, Failed Opportunities = {data['Failed Opportunities']}")

    # New dictionary to store the percentage of failed opportunities
    failed_percentage = {}

    # Calculate the percentage of failed opportunities over total opportunities
    for name, data in name_percentage.items():
        opportunities = data["Opportunities"]
        failed_opportunities = data["Failed Opportunities"]
        # Calculate the percentage and multiply by 100 to get a percentage value
        percentage_failed = ((opportunities - failed_opportunities) / opportunities) * 100
        # Store the result in the new dictionary, rounded to two decimal places
        failed_percentage[name] = round(percentage_failed, 2)
        # Calculate repairs needs if below 96 percent
        if failed_percentage[name] < 96:
            if failed_opportunities == 2:
                print(f"{name} needs ", 50 - opportunities, "repairs")
            if failed_opportunities == 1:
                print(f"{name} needs ", 25 - opportunities, "repairs")
            # (37 - 2) -- > ((x - 2) / x) * 100 = 94.59
            # x/2 - x/x * 100 = 96
            # x / 2 - 1 * 100 = 96
            # (x / 2 - 2/2) = 96 / 100
            # (x - 2) = 96 * 2 / 100
            # x = 96 * 2 / 100 + 2

    # Display the dictionary with the percentage of failed opportunities for each name
    print("Percentage of Failed Opportunities:")
    for name, percentage in failed_percentage.items():
        print(f"{name}: {percentage}% ")

    # Calculate the sum of all percentages
    total_sum = sum(failed_percentage.values())
    # Calculate the total number of names
    num_names = len(failed_percentage)
    # Calculate the overall average
    average_percentage = total_sum / num_names
    print("Total average of failed opportunities:", round(average_percentage, 2), "%")

    print(failed_percentage)

    # perform pre-check
    # pre_check(current_gb_employees, combined_df)
    # insert metric data for all employees
    # insert_metrics(current_gb_employees, combined_df)
    # plot_test(current_gb_employees,combined_df)

    print("Database updated successfully.")
    