import sqlite3
import pandas as pd
import requests
import json
from datetime import datetime
import time

# --- Configuration ---
DB_FILE = 'crypto_top100_data.db'
TABLE_NAME = 'market_data_live'

# Changed API Endpoint to fetch Market Data (Top N coins)
API_URL = 'https://api.coingecko.com/api/v3/coins/markets'

# Parameters for the /coins/markets endpoint
PARAMS = {
    'vs_currency': 'usd',
    'order': 'market_cap_desc', # Sort by market cap
    'per_page': 100,            # Fetch top 100 coins in ONE request
    'page': 1,                  # First page of results
    'sparkline': 'false'
}

DELAY_SECONDS = 60 # Fetch data every 60 seconds (1 minute)

# --- 1. Database Initialization ---
def initialize_database():
    conn = sqlite3.connect(DB_FILE)
    # The to_sql function in the collector will create the table structure automatically
    conn.close()
    print(f"Database '{DB_FILE}' initialized successfully for continuous logging.")

# --- 2. Main Live Data Collection Loop ---
def run_live_collector():
    while True:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # --- A. Fetch Data (Single API Call for Top 100 Coins) ---
        try:
            print(f"\n[{timestamp}] Fetching Top 100 coins from API...", end=" ")
            response = requests.get(API_URL, params=PARAMS)
            response.raise_for_status() # Raises an exception for 4xx/5xx errors
            crypto_data_list = response.json()
            
            # Check if data was returned
            if not crypto_data_list:
                print("FAILED. Received empty data list.")
                time.sleep(DELAY_SECONDS)
                continue
            
            print(f"SUCCESS. Found {len(crypto_data_list)} records.")
            
        except requests.exceptions.HTTPError as e:
            print(f"ERROR: HTTP {e.response.status_code} - Rate limit or bad request. Skipping this cycle.")
            time.sleep(DELAY_SECONDS)
            continue
        except Exception as e:
            print(f"GENERAL ERROR: {e}. Skipping this cycle.")
            time.sleep(DELAY_SECONDS)
            continue
        
        # --- B. Prepare Data as DataFrame ---
        records = []
        for coin in crypto_data_list:
            records.append({
                'Coin_ID': coin.get('id'),
                'Coin_Name': coin.get('name'),
                'Symbol': coin.get('symbol').upper(),
                'Current_Price_USD': coin.get('current_price'),
                'Market_Cap_USD': coin.get('market_cap'),
                'Volume_24h_USD': coin.get('total_volume'),
                'Price_Change_24h_PCT': coin.get('price_change_percentage_24h'),
                'Market_Cap_Rank': coin.get('market_cap_rank'),
                'Capture_Time': timestamp
            })
        
        df = pd.DataFrame(records)

        # --- C. Connect to DB and Insert Data ---
        conn = sqlite3.connect(DB_FILE)
        
        # 'append' adds the 100 rows captured in this minute.
        try:
            df.to_sql(TABLE_NAME, conn, if_exists='append', index=False)
            conn.commit()
            print(f"Data successfully appended to '{DB_FILE}' with {len(df)} new rows.")
        except Exception as db_e:
            print(f"Database write error: {db_e}")
        finally:
            conn.close()

        # --- D. Delay for Next Cycle ---
        print(f"Waiting {DELAY_SECONDS} seconds for the next API call...")
        time.sleep(DELAY_SECONDS)

# Execute the functions
if __name__ == "__main__":
    initialize_database()
    run_live_collector()