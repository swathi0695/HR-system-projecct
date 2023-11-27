import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import current_date, datediff
from HumanResources.settings import PYSPARK_CREDS, DATABASES

os.environ['HADOOP_HOME'] = PYSPARK_CREDS['HADOOP_HOME']

def read_table_data_using_spark():
    """
    Read and return data from a specified table using PySpark.

    Returns:
    tuple: A tuple containing the DataFrame read from the table using PySpark and the SparkSession object.
    """
    spark = SparkSession \
        .builder \
        .appName(PYSPARK_CREDS['SPARK_APP_NAME']) \
        .config("spark.jars",  PYSPARK_CREDS['SPARK_JDBC_DRIVER_JAR']) \
        .getOrCreate()

    df_spark = spark.read.format(PYSPARK_CREDS['SPARK_FORMAT']) \
    .option("url", PYSPARK_CREDS['SPARK_JDBC_URL']) \
    .option("driver", PYSPARK_CREDS['SPARK_DRIVER']) \
    .option("user", DATABASES['default']['USER']) \
    .option("password", DATABASES['default']['PASSWORD']) \
    .option("dbtable", PYSPARK_CREDS['DB_TABLE']) \
    .load()

    return df_spark, spark


def calculate_age(date_of_birth):
    return datediff(current_date(), date_of_birth) / 365