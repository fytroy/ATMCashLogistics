 🗺️ ATM Logistics Command Center (Geospatial BI)

![Python](https://img.shields.io/badge/Python-Faker-blue) ![SQL Server](https://img.shields.io/badge/SQL-Geospatial-red) ![Power BI](https://img.shields.io/badge/Power%20BI-Maps-yellow)

 Executive Summary
This project simulates a "Last Mile" logistics operation for retail banking. It visualizes the cash inventory of 50 ATMs across a city in real-time, allowing the Cash Management Unit (CMU) to optimize armored truck routes and prevent "Cash-Out" events.

Key Technical Achievement:
Integration of Python scripting for synthetic geospatial data generation with SQL Server logic to categorize inventory health, visualized on an interactive Power BI Map.

---

 🏗️ System Architecture

1.  Data Generation (Python):
     Uses the `Faker` and `random` libraries to deploy a fleet of 50 ATMs.
     Generates realistic GPS coordinates (Latitude/Longitude) clustered around a central business district.
     Simulates cash levels (0% - 100%) to create "Critical" and "Healthy" scenarios for testing.

2.  Logic Layer (SQL Server):
     `Ref_ATM_Locations`: Master data storage for fixed assets (GPS, Max Capacity).
     `Live_Cash_Inventory`: Transactional table for inventory tracking.
     Business Logic View (`v_ATM_Fleet_Status`): Automatically categorizes ATMs for the dashboard:
         `< 20%`: CRITICAL ALERT (Immediate Action - Red)
         `20% - 40%`: Refill Needed (Scheduled - Orange)
         `> 40%`: Healthy (No Action - Green)

3.  Visualization Layer (Power BI):
     Geospatial Mapping: GPS-based visualization of assets.
     Conditional Formatting: Color-coded status bubbles based on the SQL logic view.
     Drill-Down: Ability to filter by Region or Status.

---

 🚀 How to Run This Project

 1. Database Setup
Run the `SQL_Logistics_Setup.sql` script in SSMS to create the schema and views.

 2. Generate Fleet Data
Run the Python script to deploy the virtual fleet and fill the database:
```bash
python atmgenerator.py