from django.db import models
from django.contrib.auth.models import User


class ProfileAnalysis(models.Model):
    """Stores all inputs, extracted features, ML outputs, ontology inferences, and verdicts."""

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='analyses')

    # Input attributes
    username = models.CharField(max_length=150)
    followers_count = models.IntegerField(default=0)
    following_count = models.IntegerField(default=0)
    posts_count = models.IntegerField(default=0)
    account_age_days = models.IntegerField(default=0)
    bio_length = models.IntegerField(default=0)
    has_profile_pic = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    avg_likes = models.FloatField(default=0.0)
    avg_comments = models.FloatField(default=0.0)
    has_external_url = models.BooleanField(default=False)
    bio_text = models.TextField(blank=True, default='')

    # Engineered features
    follower_following_ratio = models.FloatField(default=0.0)
    engagement_rate = models.FloatField(default=0.0)
    posts_per_day = models.FloatField(default=0.0)
    username_digit_ratio = models.FloatField(default=0.0)
    extracted_features = models.JSONField(default=dict, blank=True)

    # Machine Learning outputs
    ml_prediction = models.CharField(max_length=30, default='Authentic')
    ml_fake_probability = models.FloatField(default=0.0)
    ml_confidence = models.FloatField(default=0.0)
    ml_feature_importances = models.JSONField(default=dict, blank=True)

    # Ontology reasoning outputs
    ontology_verdict = models.CharField(max_length=100, default='Low Risk - Authentic Account')
    ontology_risk_score = models.FloatField(default=0.0)
    ontology_rules_triggered = models.JSONField(default=list, blank=True)
    ontology_inferred_classes = models.JSONField(default=list, blank=True)

    # Hybrid Final Decision
    final_verdict = models.CharField(max_length=50, default='Authentic Profile')
    risk_level = models.CharField(max_length=20, default='Low')  # Low, Medium, High
    overall_risk_score = models.FloatField(default=0.0)
    explanation_summary = models.TextField(blank=True, default='')
    flagged_reasons = models.JSONField(default=list, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Profile Analyses'

    def __str__(self):
        return f"@{self.username} ({self.risk_level} Risk - {self.overall_risk_score:.1f})"


class UserSettings(models.Model):
    """Custom risk thresholds and scoring weights per user."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='detector_settings')
    ml_weight = models.FloatField(default=0.55)
    ontology_weight = models.FloatField(default=0.45)
    high_risk_threshold = models.FloatField(default=70.0)
    medium_risk_threshold = models.FloatField(default=35.0)
    theme_mode = models.CharField(max_length=20, default='dark')

    def __str__(self):
        return f"Settings for {self.user.username}"
