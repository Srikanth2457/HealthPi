from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ml"))

from pred import status_from_prediction


def test_status_mapping():
    assert status_from_prediction(0) == "Vehicle Status: Normal"
    assert status_from_prediction(1) == "Vehicle Status: Needs Maintenance"
    assert status_from_prediction(2) == "Vehicle Status: Abnormal Condition Detected!"
