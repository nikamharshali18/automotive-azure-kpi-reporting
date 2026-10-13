"""Run local Automotive KPI Reporting calculations on CSV files."""
import argparse
import csv
import json
from pathlib import Path


def read_csv(path):
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def as_int(row, key):
    value = row.get(key, "")
    if value is None or str(value).strip() == "":
        raise ValueError(f"Missing required value: {key}")
    result = int(value)
    if result < 0:
        raise ValueError(f"{key} must be non-negative")
    return result


def as_float(row, key):
    value = row.get(key, "")
    if value is None or str(value).strip() == "":
        raise ValueError(f"Missing required value: {key}")
    result = float(value)
    if result < 0:
        raise ValueError(f"{key} must be non-negative")
    return result


def unique_rows(rows, id_column):
    seen = set()
    output = []
    for row in rows:
        record_id = row.get(id_column, "").strip()
        if not record_id:
            raise ValueError(f"Missing required ID: {id_column}")
        if record_id not in seen:
            seen.add(record_id)
            output.append(row)
    return output


def calculate_kpis(data_dir):
    data_dir = Path(data_dir)
    production = unique_rows(read_csv(data_dir / "production.csv"), "production_id")
    sales = unique_rows(read_csv(data_dir / "sales.csv"), "sale_id")
    quality = unique_rows(read_csv(data_dir / "quality.csv"), "inspection_id")

    total_produced = sum(as_int(r, "units_produced") for r in production)
    total_target = sum(as_int(r, "target_units") for r in production)
    total_sold = sum(as_int(r, "units_sold") for r in sales)
    total_revenue = sum(as_int(r, "units_sold") * as_float(r, "unit_price") for r in sales)
    total_inspected = sum(as_int(r, "inspected_units") for r in quality)
    total_defects = sum(as_int(r, "defective_units") for r in quality)

    if any(as_int(r, "defective_units") > as_int(r, "inspected_units") for r in quality):
        raise ValueError("defective_units cannot exceed inspected_units")

    return {
        "total_vehicles_produced": total_produced,
        "total_production_target": total_target,
        "production_achievement_pct": round(total_produced / total_target * 100, 2) if total_target else None,
        "total_vehicles_sold": total_sold,
        "total_revenue": round(total_revenue, 2),
        "total_inspected_units": total_inspected,
        "total_defective_units": total_defects,
        "defect_rate_pct": round(total_defects / total_inspected * 100, 2) if total_inspected else None,
    }


def main():
    parser = argparse.ArgumentParser(description="Calculate automotive KPIs from sample CSV files.")
    parser.add_argument("--data-dir", default="data/source", help="Folder containing the three CSV files")
    parser.add_argument("--output", help="Optional path to write KPI JSON output")
    args = parser.parse_args()
    results = calculate_kpis(args.data_dir)
    rendered = json.dumps(results, indent=2)
    print(rendered)
    if args.output:
        Path(args.output).write_text(rendered + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
