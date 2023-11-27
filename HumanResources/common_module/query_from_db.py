import pandas as pd
from sqlalchemy import create_engine
from HumanResources.settings import DATABASES


def create_connection():
    """
    Create a connection to the PostgreSQL database using SQLAlchemy.

    Returns:
    sqlalchemy.engine.base.Engine: A SQLAlchemy Engine object representing the database connection.
    """
    db_creds = DATABASES['default']
    # PostgreSQL database connection details
    db_username = db_creds['USER']
    db_password = db_creds['PASSWORD']
    db_host = db_creds['HOST']
    db_name = db_creds['NAME']

    # Create a connection string for SQLAlchemy
    connection_str = f"postgresql+psycopg2://{db_username}:{db_password}@{db_host}/{db_name}"
    # Create the SQLAlchemy engine
    engine = create_engine(connection_str)
    return engine


def read_data_from_db(conn):
    """
    Read data from the database using the established connection.
    Args:
    param1 (connection object): conn

    Returns:
    Dataframe: Dataframe containing the retrieved data from the database.
    """
    # Query to select all data from the 'employees' table
    query = "SELECT * FROM employees;"

    # Read data into a Pandas DataFrame
    data = pd.read_sql_query(query, conn)
    data = data.fillna(0)
    # Close the database connection
    conn.dispose()
    return data