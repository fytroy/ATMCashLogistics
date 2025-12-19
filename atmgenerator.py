import pyodbc
import random
from faker import Faker
import time

# --- CONFIGURATION ---
SERVER = r'ROYSHP\FYT'
DATABASE = 'ATMLogisticsDB'
DRIVER = '{ODBC Driver 17 for SQL Server}'

# Center Point (Nairobi, Kenya) - Change this if you want another city
BASE_LAT = -1.286389
BASE_LON = 36.817223

fake = Faker()

def get_db_connection():
    return pyodbc.connect(f'DRIVER={DRIVER};SERVER={SERVER};DATABASE={DATABASE};Trusted_Connection=yes;')

def generate_atm_fleet():
    print("--- 🏧 Generating ATM Fleet Data ---")
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Clear old data to start fresh
    cursor.execute("DELETE FROM Live_Cash_Inventory")
    cursor.execute("DELETE FROM Ref_ATM_Locations")
    
    # Generate 50 ATMs
    for i in range(1, 51):
        atm_id = 1000 + i
        # Create a name like "Westlands Mall Branch" or "Mombasa Rd Drive-Thru"
        atm_name = f"{fake.street_name()} {random.choice(['Branch', 'Mall', 'Drive-Thru', 'Lobby'])}"
        
        # Generate random GPS nearby (Spread out by ~0.1 degrees)
        lat = BASE_LAT + random.uniform(-0.1, 0.1)
        lon = BASE_LON + random.uniform(-0.1, 0.1)
        
        region = random.choice(['North District', 'South District', 'CBD', 'Westlands'])
        max_cap = 5000000 # 5 Million currency units
        
        # Insert Master Data
        cursor.execute(f"""
            INSERT INTO Ref_ATM_Locations (ATMID, ATMName, Region, Latitude, Longitude, MaxCapacity)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (atm_id, atm_name, region, lat, lon, max_cap))
        
        # Generate Initial Cash Balance (Random)
        current_bal = random.uniform(200000, 5000000) # Between 200k and 5M
        percentage = (current_bal / max_cap) * 100
        
        status = 'Online'
        if percentage < 10: status = 'Critical'
        elif percentage < 30: status = 'Low Cash'
        
        # Insert Live Inventory
        cursor.execute(f"""
            INSERT INTO Live_Cash_Inventory (ATMID, CurrentBalance, CashLevelPercentage, Status)
            VALUES (?, ?, ?, ?)
        """, (atm_id, current_bal, percentage, status))
        
        print(f"📍 Installed ATM {atm_id}: {atm_name} at [{lat:.4f}, {lon:.4f}]")

    conn.commit()
    conn.close()
    print("--- ✅ Fleet Deployment Complete ---")

if __name__ == "__main__":
    generate_atm_fleet()