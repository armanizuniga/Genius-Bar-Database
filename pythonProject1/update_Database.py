import sqlite3


# Function to insert a new technician and their role into the SQL Database.
# Example usage:
# add_technician("John Doe", "Genius")G
def add_technician(technician_name, technician_type, job):
    conn = sqlite3.connect('technician_metrics.db')
    c = conn.cursor()

    # Insert technician into Technicians table
    c.execute('''INSERT INTO Technicians (Technician_Name, Technician_Type, Job) VALUES (?,?, ?)''',
              (technician_name, technician_type, job))

    # Commit changes and close connection
    conn.commit()
    conn.close()
    print("Successfully added", technician_name, "to the database.")


# Function to remove a technician and all their metric data from the SQL Database
# Example usage:
# remove_technician("John Doe")
def remove_technician(technician_name):
    conn = sqlite3.connect('technician_metrics.db')
    c = conn.cursor()

    # Remove technician from Technicians table
    c.execute('''DELETE FROM Technicians WHERE Technician_Name = ?''', (technician_name,))

    # Remove technician's metrics from Metrics table
    c.execute('''DELETE FROM Metrics WHERE Technician_ID = 
                 (SELECT Technician_ID FROM Technicians WHERE Technician_Name = ?)''', (technician_name,))

    # Commit changes and close connection
    conn.commit()
    conn.close()


# Function to update the role of a technician
def change_technician_role(technician_name, new_role):
    conn = sqlite3.connect('../technician_metrics.db')
    c = conn.cursor()

    # Update technician's role in Technicians table
    c.execute('''UPDATE Technicians SET Technician_Type = ? WHERE Technician_Name = ?''', (new_role, technician_name))

    # Commit changes and close connection
    conn.commit()
    conn.close()


# Function to get all names of Technicians inside Database
# Example usage:
# genius_names = get_technician_names_by_type("Genius")
# tech_expert_names = get_technician_names_by_type("Technical Expert")
# tech_specialist_names = get_technician_names_by_type("Technical Specialist")
def get_technician_names():
    conn = sqlite3.connect('../technician_metrics.db')
    c = conn.cursor()

    # Fetch all technician names from Technicians table
    c.execute('''SELECT Technician_Name FROM Technicians''')
    technician_names = [row[0] for row in c.fetchall()]

    # Close connection
    conn.close()

    return technician_names


# Function gets a list of Technicians by their role type
def get_technician_names_by_type(technician_type):
    conn = sqlite3.connect('../technician_metrics.db')
    c = conn.cursor()

    # Fetch technician names based on type
    c.execute('''SELECT Technician_Name FROM Technicians WHERE Technician_Type = ?''', (technician_type,))
    technician_names_type = [row[0] for row in c.fetchall()]

    # Close connection
    conn.close()

    return technician_names_type


def insert_technician_metric_data(technician_name, spqh, customers_helped, mac_duration, mobile_duration,
                                  nps, tms, sur, doa, business_intros, discussed_applecare, offered_trade_in,
                                  month, year):
    # Convert user input to None if it represents null value
    if spqh.lower() == "null":
        spqh = None
    if customers_helped.lower() == "null":
        customers_helped = None
    if mac_duration.lower() == "null":
        mac_duration = None
    if mobile_duration.lower() == "null":
        mobile_duration = None
    if nps.lower() == "null":
        nps = None
    if tms.lower() == "null":
        tms = None
    if sur.lower() == "null":
        sur = None
    if doa.lower() == "null":
        doa = None
    if business_intros.lower() == "null":
        business_intros = None
    if discussed_applecare.lower() == "null":
        discussed_applecare = None
    if offered_trade_in.lower() == "null":
        offered_trade_in = None

    conn = sqlite3.connect('../technician_metrics.db')
    c = conn.cursor()

    # Fetch technician type based on technician name
    c.execute('''SELECT Technician_Type FROM Technicians WHERE Technician_Name = ?''', (technician_name,))
    technician_type = c.fetchone()[0]

    # Insert metric data based on technician type
    if technician_type == "Genius":
        c.execute('''INSERT INTO Metrics (Technician_ID, SPQH, Customers_Helped, Mac_Duration,
                     Mobile_Duration, NPS, TMS, SUR, DOA, Business_Intros, Discussed_AppleCare,
                     Offered_Trade_in, Month, Year)
                     VALUES ((SELECT Technician_ID FROM Technicians WHERE Technician_Name = ?),
                     ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                  (technician_name, spqh, customers_helped, mac_duration, mobile_duration,
                   nps, tms, sur, doa, business_intros, discussed_applecare, offered_trade_in,
                   month, year))
    elif technician_type == "Technical Expert":
        c.execute('''INSERT INTO Metrics (Technician_ID, SPQH, Customers_Helped,
                     Mobile_Duration, NPS, TMS, SUR, DOA, Business_Intros, Discussed_AppleCare,
                     Offered_Trade_in, Month, Year)
                     VALUES ((SELECT Technician_ID FROM Technicians WHERE Technician_Name = ?),
                     ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                  (technician_name, spqh, customers_helped, mobile_duration,
                   nps, tms, sur, doa, business_intros, discussed_applecare, offered_trade_in,
                   month, year))
    elif technician_type == "Technical Specialist":
        c.execute('''INSERT INTO Metrics (Technician_ID, SPQH, Customers_Helped,
                     Mobile_Duration, NPS, TMS, Business_Intros, Discussed_AppleCare,
                     Offered_Trade_in, Month, Year)
                     VALUES ((SELECT Technician_ID FROM Technicians WHERE Technician_Name = ?),
                     ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                  (technician_name, spqh, customers_helped, mobile_duration,
                   nps, tms, business_intros, discussed_applecare, offered_trade_in,
                   month, year))
    else:
        print("Invalid technician type")

    # Commit changes and close connection
    conn.commit()
    conn.close()
    print("Updated ", technician_name, "'s metrics successfully.")


# Function that allows user to Manually enter in data for entire month
def get_user_input():
    new_year = input("Enter Year: ")
    new_month = input("Enter Month: ")
    # new_doa = "null"
    employees = get_technician_names_by_type("Genius")
    employees1 = get_technician_names_by_type("Technical Expert")
    employees2 = get_technician_names_by_type("Technical Specialist")

    for name in employees:
        new_spqh = input(name + "'s SPQH: ")
        new_cust = input(name + "'s customers helped: ")
        new_mac = input(name + "'s Mac duration: ")
        new_mobile = input(name + "'s mobile duration: ")
        new_nps = input(name + "'s NPS: ")
        new_tms = input(name + "'s TMS: ")
        new_sur = input(name + "'s SUR: ")
        new_doa = input(name + "'s DOA: ")
        new_busi = input(name + "'s Business intro: ")
        new_apple = input(name + "'s AppleCare: ")
        new_trade = input(name + "'s Offered Trade in: ")
        insert_technician_metric_data(name, new_spqh, new_cust, new_mac,
                                      new_mobile, new_nps, new_tms, new_sur, new_doa, new_busi, new_apple,
                                      new_trade, new_month, new_year)

    new_mac = "null"
    for name1 in employees1:
        new_spqh = input(name1 + "'s SPQH: ")
        new_cust = input(name1 + "'s customers helped: ")
        # new_mac = input(name1 + "'s Mac duration: ")
        new_mobile = input(name1 + "'s mobile duration: ")
        new_nps = input(name1 + "'s NPS: ")
        new_tms = input(name1 + "'s TMS: ")
        new_sur = input(name1 + "'s SUR: ")
        new_doa = input(name1 + "'s DOA: ")
        new_busi = input(name1 + "'s Business intro: ")
        new_apple = input(name1 + "'s AppleCare: ")
        new_trade = input(name1 + "'s Offered Trade in: ")
        insert_technician_metric_data(name1, new_spqh, new_cust, new_mac, new_mobile, new_nps, new_tms,
                                      new_sur, new_doa, new_busi, new_apple, new_trade, new_month, new_year)

    new_sur = "null"
    new_doa = "null"
    for name2 in employees2:
        new_spqh = input(name2 + "'s SPQH: ")
        new_cust = input(name2 + "'s customers helped: ")
        # new_Mac = input(name1 + "'s Mac duration: ")
        new_mobile = input(name2 + "'s mobile duration: ")
        new_nps = input(name2 + "'s NPS: ")
        new_tms = input(name2 + "'s TMS: ")
        # new_sur = input(name2 + "'s SUR: ")
        # new_doa = input(name + "'s DOA: ")
        new_busi = input(name2 + "'s Business intro: ")
        new_apple = input(name2 + "'s AppleCare: ")
        new_trade = input(name2 + "'s Offered Trade in: ")
        insert_technician_metric_data(name2, new_spqh, new_cust, new_mac, new_mobile, new_nps, new_tms,
                                      new_sur, new_doa, new_busi, new_apple, new_trade, new_month, new_year)


# Function to update a specific metric in case of mistake
def update_sur_metric(technician_name, new_sur_value, month, year):
    conn = sqlite3.connect('../technician_metrics.db')
    c = conn.cursor()

    # Update SUR metric for the specified technician at a specific month and year
    c.execute('''UPDATE Metrics
                 SET NPS = ?
                 WHERE Technician_ID = (SELECT Technician_ID FROM Technicians WHERE Technician_Name = ?)
                 AND Month = ? AND Year = ?''',
              (new_sur_value, technician_name, month, year))

    # Commit changes and close connection
    conn.commit()
    conn.close()


# Check if the script is being run directly (not imported as a module)
if __name__ == "__main__":
    print("Hello World")
    # get_user_input()
    # update_sur_metric("Flavio Galindo", 80, 2, 2023)  # Update SUR metric for Armani Zuniga in February 2024 to 90.0
