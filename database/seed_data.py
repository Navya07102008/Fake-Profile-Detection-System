import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
import django
django.setup()

from django.contrib.auth.models import User
from backend.detector.models import ProfileAnalysis, UserSettings
from backend.detector.detector import HybridDetectionEngine
from backend.detector.utils import load_sample_profiles


def seed():
    # 1. Create default analyst user if not exists
    user, created = User.objects.get_or_create(username='admin')
    if created:
        user.set_password('admin123')
        user.is_staff = True
        user.is_superuser = True
        user.save()
        print("Created default admin user: 'admin' / 'admin123'")
    else:
        print("Admin user already exists.")

    UserSettings.objects.get_or_create(user=user)

    # 2. Seed benchmark profiles through the Hybrid Detection Engine
    engine = HybridDetectionEngine()
    sample_profiles = load_sample_profiles()
    print(f"Loading {len(sample_profiles)} sample benchmark profiles...")

    for p in sample_profiles:
        username = p.get('username')
        if ProfileAnalysis.objects.filter(username=username).exists():
            continue

        profile_data = {
            'username': username,
            'followers_count': int(p.get('followers_count', 0)),
            'following_count': int(p.get('following_count', 0)),
            'posts_count': int(p.get('posts_count', 0)),
            'account_age_days': int(p.get('account_age_days', 0)),
            'bio_length': int(p.get('bio_length', 0)),
            'has_profile_pic': bool(int(p.get('has_profile_pic', 0))),
            'is_verified': bool(int(p.get('is_verified', 0))),
            'avg_likes': float(p.get('avg_likes', 0.0)),
            'avg_comments': float(p.get('avg_comments', 0.0)),
            'has_external_url': bool(int(p.get('has_external_url', 0))),
            'bio_text': p.get('description', ''),
        }

        result = engine.detect(profile_data)

        ProfileAnalysis.objects.create(
            user=user,
            username=profile_data['username'],
            followers_count=profile_data['followers_count'],
            following_count=profile_data['following_count'],
            posts_count=profile_data['posts_count'],
            account_age_days=profile_data['account_age_days'],
            bio_length=profile_data['bio_length'],
            has_profile_pic=profile_data['has_profile_pic'],
            is_verified=profile_data['is_verified'],
            avg_likes=profile_data['avg_likes'],
            avg_comments=profile_data['avg_comments'],
            has_external_url=profile_data['has_external_url'],
            bio_text=profile_data['bio_text'],

            follower_following_ratio=result['extracted_features'].get('follower_following_ratio', 0.0),
            engagement_rate=result['extracted_features'].get('engagement_rate', 0.0),
            posts_per_day=result['extracted_features'].get('posts_per_day', 0.0),
            username_digit_ratio=result['extracted_features'].get('username_digit_ratio', 0.0),
            extracted_features=result['extracted_features'],

            ml_prediction=result['ml_prediction'],
            ml_fake_probability=result['ml_fake_probability'],
            ml_confidence=result['ml_confidence'],
            ml_feature_importances=result['ml_feature_importances'],

            ontology_verdict=result['ontology_verdict'],
            ontology_risk_score=result['ontology_risk_score'],
            ontology_rules_triggered=result['ontology_rules_triggered'],
            ontology_inferred_classes=result['ontology_inferred_classes'],

            final_verdict=result['final_verdict'],
            risk_level=result['risk_level'],
            overall_risk_score=result['overall_risk_score'],
            explanation_summary=result['explanation_summary'],
            flagged_reasons=result['flagged_reasons'],
        )
        print(f"Seeded analysis for: @{username} -> {result['risk_level']} Risk ({result['overall_risk_score']})")

    print("Database seeding completed.")


if __name__ == '__main__':
    seed()
