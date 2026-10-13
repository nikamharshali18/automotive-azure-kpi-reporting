from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from automotive_kpi.cli import calculate_kpis


def test_sample_kpis():
    result = calculate_kpis(PROJECT_ROOT / "data" / "source")
    assert result["total_vehicles_produced"] == 2500
    assert result["total_production_target"] == 2650
    assert result["production_achievement_pct"] == 94.34
    assert result["total_vehicles_sold"] == 500
    assert result["total_revenue"] == 699000000
    assert result["total_inspected_units"] == 2500
    assert result["total_defective_units"] == 50
    assert result["defect_rate_pct"] == 2.0
