'''
import os
from pyspark.sql import *
from lib.logger import Log4J


if __name__ == "__main__":
    log4j_path = os.path.abspath("log4j.properties").replace("\\", "/")
    print(f"Using log4j config from: {log4j_path}")

    spark = SparkSession .builder .appName("Hello Spark") .master("local[3]") .config("spark.driver.extraJavaOptions", f"-Dlog4j.configuration=file:{log4j_path}") .getOrCreate()

    logger = Log4J(spark)

    logger.info("Starting Hello Spark")

    logger.info("Finished Hello Spark")

    spark.stop()


import os
from pyspark.sql import SparkSession
from lib.logger import Log4J

if __name__ == "__main__":
    log4j_path = os.path.abspath("log4j.properties").replace("\\", "/")
    print(f"Using log4j config from: {log4j_path}")

    spark = SparkSession.builder \
        .appName("HelloSpark") \
        .master("local[3]") \
        .config("spark.driver.extraJavaOptions", f"-Dlog4j.configuration=file:{log4j_path}") \
        .getOrCreate()

    logger = Log4J(spark)
    logger.info("Starting Hello Spark")
    logger.info("Finished Hello Spark")

    spark.stop()
'''

import os
import sys

from pyspark.sql import SparkSession
from lib.logger import Log4J
from lib.utils import load_survey_df

if __name__ == "__main__":
    log4j_path = os.path.abspath("log4j.properties").replace("\\", "/")
    print(f"Using log4j config from: {log4j_path}")

    spark = SparkSession.builder \
        .appName("HelloSpark") \
        .master("local[3]") \
        .config(
            "spark.driver.extraJavaOptions",
            f'-Dlog4j.configuration="file:{log4j_path}" '
            f'-Dlogfile.name=hello-spark '
            f'-Dspark.yarn.app.container.log.dir=app-logs'
        ) \
        .getOrCreate()

    logger = Log4J(spark)

    if len(sys.argv) != 2:
        logger.error("Usage: HelloSpark <filename>")
        sys.exit(-1)

    logger.info("Starting Hello Spark")


    survey_df = load_survey_df(spark, sys.argv[1])

    new_survey_df = survey_df.where("Age < 40") \
        .select("Age", "Gender", "Country", "state") \

    new_survey_df.show()

    logger.info("Finished Hello Spark")
    spark.stop()
