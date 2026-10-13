# Run after 01_bronze_to_silver.py. Update paths for your Azure account.
from pyspark.sql import functions as F

SILVER_PATH = "abfss://silver@<storage-account>.dfs.core.windows.net/automotive"
GOLD_PATH = "abfss://gold@<storage-account>.dfs.core.windows.net/automotive"

production = spark.read.format("delta").load(f"{SILVER_PATH}/production")
sales = spark.read.format("delta").load(f"{SILVER_PATH}/sales")
quality = spark.read.format("delta").load(f"{SILVER_PATH}/quality")

outputs = {
    "production_overall": production.agg(
        F.sum("units_produced").alias("total_vehicles_produced"),
        F.sum("target_units").alias("total_production_target"),
        F.round(F.sum("units_produced") / F.sum("target_units") * 100, 2).alias("production_achievement_pct")),
    "production_by_plant_model_date": production.groupBy("production_date", "plant", "model").agg(
        F.sum("units_produced").alias("units_produced"), F.sum("target_units").alias("target_units")),
    "sales_overall": sales.agg(
        F.sum("units_sold").alias("total_vehicles_sold"), F.round(F.sum("revenue"), 2).alias("total_revenue")),
    "sales_by_plant_model_date": sales.groupBy("sale_date", "plant", "model").agg(
        F.sum("units_sold").alias("units_sold"), F.round(F.sum("revenue"), 2).alias("revenue")),
    "quality_overall": quality.agg(
        F.sum("inspected_units").alias("total_inspected_units"),
        F.sum("defective_units").alias("total_defective_units"),
        F.round(F.sum("defective_units") / F.sum("inspected_units") * 100, 2).alias("defect_rate_pct")),
    "quality_by_plant_model_date": quality.groupBy("inspection_date", "plant", "model").agg(
        F.sum("inspected_units").alias("inspected_units"), F.sum("defective_units").alias("defective_units")),
}

for name, df in outputs.items():
    df.write.format("delta").mode("overwrite").option("overwriteSchema", "true").save(f"{GOLD_PATH}/{name}")
    print(f"Gold {name}: {df.count()} rows")
