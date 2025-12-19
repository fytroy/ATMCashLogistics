import pyodbc
import random
from faker import Faker
import time

# --- CONFIGURATION ---
SERVER = r'ROYSHP\FYT' 
DATABASE = 'ATMLogisticsDB'
DRIVER = '{ODBC Driver 17 for SQL Server}'
BASE_LAT = -1.286389
BASE_LON = 36.817223

fake = Faker()

def get_db_connection():
    try:
        return pyodbc.connect(f'DRIVER={DRIVER};SERVER={SERVER};DATABASE={DATABASE};Trusted_Connection=yes;')
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return None

def generate_atm_fleet():
    conn = get_db_connection()
    if not conn: return
    cursor = conn.cursor()
    
    print("\n--- 🔄 Resetting Fleet Data... ---")
    
    # 1. Clear old data 
    # (In a real app, we would UPDATE, but for this demo, recreating is cleaner for the visual)
    try:
        cursor.execute("DELETE FROM Live_Cash_Inventory")
        cursor.execute("DELETE FROM Ref_ATM_Locations")
    except Exception as e:
        print(f"⚠️ Warning cleaning tables: {e}")

    # 2. Generate 50 ATMs with NEW Random Values
    for i in range(1, 51):
        atm_id = 1000 + i
        # We keep the names mostly consistent for realism, or generate new ones
        atm_name = f"Branch {atm_id} - {random.choice(['CBD', 'West', 'East', 'North'])}"
        
        # Jitter the GPS slightly so dots "move" or just stay fixed? 
        # Let's keep GPS fixed relative to base to avoid chaos, but vary cash wildly.
        lat = BASE_LAT + random.uniform(-0.08, 0.08)
        lon = BASE_LON + random.uniform(-0.08, 0.08)
        
        region = random.choice(['North', 'South', 'CBD', 'West'])
        max_cap = 5000000 
        
        cursor.execute(f"""
            INSERT INTO Ref_ATM_Locations (ATMID, ATMName, Region, Latitude, Longitude, MaxCapacity)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (atm_id, atm_name, region, lat, lon, max_cap))
        
        # --- THE IMPORTANT PART: RANDOM CASH LEVELS ---
        # This ensures every loop looks different
        current_bal = random.uniform(50000, 5000000) 
        percentage = (current_bal / max_cap) * 100
        
        status = 'Online'
        if percentage < 20: status = 'Critical'
        elif percentage < 40: status = 'Low Cash'
        
        cursor.execute(f"""
            INSERT INTO Live_Cash_Inventory (ATMID, CurrentBalance, CashLevelPercentage, Status)
            VALUES (?, ?, ?, ?)
        """, (atm_id, current_bal, percentage, status))

    conn.commit()
    conn.close()
    print("--- ✅ Fleet Updated (Waiting 10s...) ---")

# --- MAIN LOOP ---
if __name__ == "__main__":
    print("Starting Live ATM Simulator... (Press Ctrl+C to Stop)")
    try:
        while True:
            generate_atm_fleet()
            time.sleep(300) # Updates every 5 minutes
    except KeyboardInterrupt:
        print("Simulator Stopped.")