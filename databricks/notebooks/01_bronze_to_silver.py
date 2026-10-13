# Run as a Databricks notebook/script. Update paths for your Azure account.
from pyspark.sql import functions as F

BRONZE_PATH = "abfss://bronze@<storage-account>.dfs.core.windows.net/automotive"
SILVER_PATH = "abfss://silver@<storage-account>.dfs.core.windows.net/automotive"


def read_csv(name):
    return (spark.read.option("header", True).option("inferSchema", True)
            .option("mode", "FAILFAST").csv(f"{BRONZE_PATH}/{name}"))


production = (read_csv("production.csv")
    .dropDuplicates(["production_id"])
    .withColumn("production_date", F.to_date("production_date", "yyyy-MM-dd"))
    .filter(F.col("production_id").isNotNull())
    .filter(F.col("production_date").isNotNull())
    .filter(F.col("plant").isNotNull() & F.col("model").isNotNull())
    .filter(F.col("units_produced") >= 0)
    .filter(F.col("target_units") >= 0))

sales = (read_csv("sales.csv")
    .dropDuplicates(["sale_id"])
    .withColumn("sale_date", F.to_date("sale_date", "yyyy-MM-dd"))
    .withColumn("revenue", F.round(F.col("units_sold") * F.col("unit_price"), 2))
    .filter(F.col("sale_id").isNotNull())
    .filter(F.col("sale_date").isNotNull())
    .filter(F.col("units_sold") >= 0)
    .filter(F.col("unit_price") >= 0))

quality = (read_csv("quality.csv")
    .dropDuplicates(["inspection_id"])
    .withColumn("inspection_date", F.to_date("inspection_date", "yyyy-MM-dd"))
    .filter(F.col("inspection_id").isNotNull())
    .filter(F.col("inspected_units") >= 0)
    .filter(F.col("defective_units") >= 0)
    .filter(F.col("defective_units") <= F.col("inspected_units")))

for name, df in [("production", production), ("sales", sales), ("quality", quality)]:
    df.write.format("delta").mode("overwrite").option("overwriteSchema", "true").save(f"{SILVER_PATH}/{name}")
    print(f"Silver {name}: {df.count()} rows")
