# Run after Silver tables are written.
from pyspark.sql import functions as F

SILVER_PATH = "abfss://silver@<storage-account>.dfs.core.windows.net/automotive"
production = spark.read.format("delta").load(f"{SILVER_PATH}/production")
sales = spark.read.format("delta").load(f"{SILVER_PATH}/sales")
quality = spark.read.format("delta").load(f"{SILVER_PATH}/quality")

assert production.limit(1).count() > 0, "Production is empty"
assert sales.limit(1).count() > 0, "Sales is empty"
assert quality.limit(1).count() > 0, "Quality is empty"
assert production.count() == production.select("production_id").distinct().count(), "Duplicate production IDs"
assert sales.count() == sales.select("sale_id").distinct().count(), "Duplicate sale IDs"
assert quality.count() == quality.select("inspection_id").distinct().count(), "Duplicate inspection IDs"
assert quality.filter(F.col("defective_units") > F.col("inspected_units")).count() == 0, "Defects exceed inspected units"
print("All data quality checks passed.")
