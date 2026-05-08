import pandas as pd
from sqlalchemy import create_engine
import os
import glob
import csv
from urllib.parse import quote_plus



password = quote_plus("XKdjZEKPncTXOrQycZAL")


user = "uuytmwm0ynbzjvxl"
host = "bl6qrdnbs6fzgn6ogvq2-mysql.services.clever-cloud.com"
database = "bl6qrdnbs6fzgn6ogvq2"

DB_CONNECTION = f"mysql+pymysql://{user}:{password}@{host}:3306/{database}"
engine = create_engine(DB_CONNECTION)


folder_path = './data' 
csv_files = glob.glob(os.path.join(folder_path, "*.csv"))

if not csv_files:
    print("No .csv files found in the /data directory")

for file in csv_files:
    try:
     
        table_name = os.path.basename(file).split('.')[0].lower()
        print(f"Processing file: {file}...")
        
        df = pd.read_csv(
            file, 
            sep=None, 
            engine='python', 
            on_bad_lines='skip',
            encoding='utf-8-sig',
            quoting=csv.QUOTE_MINIMAL
        )
        
      
        df.columns = [col.strip().lower().replace(' ', '_') for col in df.columns]
        df.dropna(how='all', inplace=True)
        df.drop_duplicates(inplace=True)
        
       
        df.to_sql(name=table_name, con=engine, if_exists='replace', index=False)
        print(f"✅ Successfully loaded table '{table_name}' into MySQL.")
        
    except Exception as e:
        print(f"❌ Error when processing file {file}: {e}")

print("\n--- Finished ---")