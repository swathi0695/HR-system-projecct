import json
import pandas as pd
from sqlalchemy import create_engine

# Read the JSON data from the file
with open(r"MOCK_DATA.json", 'r') as f:
    json_data = json.load(f)

# Convert the JSON data to a pandas DataFrame
df = pd.DataFrame(json_data)

# PostgreSQL database connection details
db_username = ''
db_password = ''
db_host = ''  # Change this if your PostgreSQL instance is hosted elsewhere
db_name = ''

# Create a connection string for SQLAlchemy
connection_str = f"postgresql+psycopg2://{db_username}:{db_password}@{db_host}/{db_name}"
# Create the SQLAlchemy engine
engine = create_engine(connection_str)

# Write the DataFrame to a table named 'employees' in the PostgreSQL database
df.to_sql('employees', engine, if_exists='replace', index=False)