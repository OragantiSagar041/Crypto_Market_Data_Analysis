# 🚀 Real-Time Crypto Market Analyzer (Top 100)

## Project Overview

This is an end-to-end Business Intelligence (BI) solution for monitoring and analyzing the performance and volatility of the **Top 100 cryptocurrencies** by market capitalization.
It is real-time which is continuous data 

The system establishes a high-frequency (60-second) data collection pipeline, stores a permanent historical record, and visualizes key market metrics using Power BI for deep analysis.

**Goal:** Provide investors and analysts with a near-real-time view of market health, price trends, and volatility with minimal latency.

---

## 🛠️ Technical Stack

| Tool/Technology | Role in the Project |
| :--- | :--- |
| **Data Source** | CoinGecko Public API (`/coins/markets`) |
| **ETL Pipeline** | Python 3 (`requests`, `pandas`, `sqlite3`) |
| **Data Storage** | SQLite Database (`crypto_top100_data.db`) |
| **BI & Visualization**| Power BI Desktop & Service (Advanced DAX) |

---

## 💻 Getting Started: Setup and Installation

Follow these steps to set up the data collection locally.

### 1. Prerequisites

1.  **Python:** Ensure Python 3.x is installed.
2.  **Libraries:** Install the necessary Python packages:
    ```bash
    pip install requests pandas
    ```

### 2. Data Collection (ETL)

The collector script runs continuously to build your historical database.

**File: `crypto_collector.py`**

* **Action:** Fetches the Top 100 coins and appends the snapshot to the database every 60 seconds.
* **Execution:** Run this script from your terminal and leave it running in the background.
    ```bash
    python crypto_collector.py
    ```

### 3. Power BI Connection

To ingest the constantly updating data, Power BI uses a Python script connector.

**Steps in Power BI Desktop:**

1.  Go to **Get Data** -> **Other** -> **Python script**.
2.  Paste the connector code below, **ensuring you update the `DB_PATH`** to the absolute location of your `crypto_top100_data.db` file.
3.  Load the resulting `dataset` table.

**Code Snippet (`powerbi_connector.py` logic):**
```python
import sqlite3
import pandas as pd
import os 

# --- IMPORTANT: UPDATE THIS PATH ---
DB_PATH = r'/absolute/path/to/your/db/crypto_top100_data.db' 
TABLE_NAME = 'market_data_live'

# Connection and query logic...
conn = sqlite3.connect(DB_PATH)
sql_query = f"SELECT * FROM {TABLE_NAME} ORDER BY Capture_Time ASC;"
dataset = pd.read_sql_query(sql_query, conn)
# Data type transformation applied here (e.g., to Capture_Time)





<img width="788" height="600" alt="image" src="https://github.com/user-attachments/assets/3b42b1c7-7604-47d4-8d2b-6b6cf237f766" />

conn.close()
