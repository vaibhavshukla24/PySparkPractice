import os
import sys

from pyspark.sql import *
from lib.logger import Log4J

if __name__ == "__main__":
    log4j_path = os.path.abspath("log4j.properties").replace("\\", "/")
    print(f"Using log4j config from: {log4j_path}")

    spark = SparkSession.builder \
        .appName("PySparkFiles") \
        .master("local[3]") \
        .config(
        "spark.driver.extraJavaOptions",
        f'-Dlog4j.configuration="file:{log4j_path}" '
        f'-Dlogfile.name=PySparkFiles '
        f'-Dspark.yarn.app.container.log.dir=app-logs'
    ) \
        .getOrCreate()


    logger = Log4J(spark)

    logger.info("Starting Hello Spark")

    flightTimeCsvDF = spark.read \
                        .format("csv") \
                        .option("header", 'true') \
                        .option("inferSchema", "true") \
                        .load("data/flight-time.csv")

    flightTimeCsvDF.show(5)
    logger.info("CSV Schema:" + flightTimeCsvDF.schema.simpleString())

    flightTimeJsonDF = spark.read \
        .format("json") \
        .option("header", 'true') \
        .load("data/flight-time.json")

    flightTimeJsonDF.show(5)

    logger.info("JSON Schema:" + flightTimeJsonDF.schema.simpleString())

    flightTimeParquetDF = spark.read \
        .format("parquet") \
        .option("header", 'true') \
        .load("data/flight-time.parquet")

    flightTimeParquetDF.show(5)

    logger.info("Parquet Schema:" + flightTimeJsonDF.schema.simpleString())


    flightTimeParquetDF.write \
        .format("json") \
        .mode("overwrite") \
        .option("path", "data/dataSink/json/") \
        .partitionBy("OP_CARRIER", "ORIGIN") \
        .option("maxRecordPerFile","10000") \
        .save()



    logger.info("Finished Hello Spark")
    spark.stop()