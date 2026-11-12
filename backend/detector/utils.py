from pathlib import Path
import csv

BASE_DIR = Path(__file__).resolve().parent.parent.parent
SAMPLE_CSV = BASE_DIR / 'dataset' / 'sample' / 'test_profiles.csv'


def load_sample_profiles() -> list[dict]:
    """Loads curated sample benchmark profiles for quick-testing."""
    profiles = []
    if SAMPLE_CSV.exists():
        with open(SAMPLE_CSV, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                profiles.append(row)
    return profiles


def format_risk_badge(level: str) -> dict:
    """Returns CSS class and icon for a risk level."""
    l = level.lower()
    if l == 'high':
        return {'badge_class': 'badge-cyber-danger', 'icon': 'bi-shield-x', 'color': '#EF4444'}
    elif l == 'medium':
        return {'badge_class': 'badge-cyber-warning', 'icon': 'bi-shield-exclamation', 'color': '#F59E0B'}
    return {'badge_class': 'badge-cyber-success', 'icon': 'bi-shield-check', 'color': '#10B981'}
