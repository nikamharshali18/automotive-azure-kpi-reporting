# Power BI dashboard guide

Connect Power BI to registered Gold Delta tables through a Databricks SQL warehouse or another supported reporting connection.

## Suggested cards and charts
- Cards: total produced, total sold, total revenue, production achievement %, defect rate %.
- Charts: produced vs target by date, revenue by model, production by plant, defect rate by plant.
- Slicers: date, plant, model.

## Example DAX measures
```DAX
Total Produced = SUM(silver_production[units_produced])
Total Target = SUM(silver_production[target_units])
Production Achievement % = DIVIDE([Total Produced], [Total Target], 0) * 100
Total Sold = SUM(silver_sales[units_sold])
Total Revenue = SUMX(silver_sales, silver_sales[units_sold] * silver_sales[unit_price])
Total Inspected = SUM(silver_quality[inspected_units])
Total Defects = SUM(silver_quality[defective_units])
Defect Rate % = DIVIDE([Total Defects], [Total Inspected], 0) * 100
```

Keep production, sales, and quality facts separate by their grain. Use shared date/plant/model dimensions rather than joining raw fact tables directly, which may multiply records.
