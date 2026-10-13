-- Adapt table names to your catalog/schema after registering Delta tables.
SELECT SUM(units_produced) AS total_produced,
       SUM(target_units) AS total_target,
       ROUND(100.0 * SUM(units_produced) / NULLIF(SUM(target_units), 0), 2) AS achievement_pct
FROM automotive.silver_production;

SELECT plant, SUM(units_produced) AS total_produced
FROM automotive.silver_production
GROUP BY plant
ORDER BY total_produced DESC;

SELECT model, SUM(units_sold) AS total_units_sold,
       SUM(units_sold * unit_price) AS total_revenue
FROM automotive.silver_sales
GROUP BY model
ORDER BY total_revenue DESC;

SELECT plant, SUM(inspected_units) AS inspected,
       SUM(defective_units) AS defects,
       ROUND(100.0 * SUM(defective_units) / NULLIF(SUM(inspected_units), 0), 2) AS defect_rate_pct
FROM automotive.silver_quality
GROUP BY plant;
