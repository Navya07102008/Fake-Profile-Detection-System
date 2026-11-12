from django.contrib import admin
from .models import ProfileAnalysis, UserSettings


@admin.register(ProfileAnalysis)
class ProfileAnalysisAdmin(admin.ModelAdmin):
    list_display = ('username', 'risk_level', 'overall_risk_score', 'final_verdict', 'ml_prediction', 'created_at')
    list_filter = ('risk_level', 'final_verdict', 'is_verified', 'has_profile_pic')
    search_fields = ('username',)
    readonly_fields = ('created_at',)


@admin.register(UserSettings)
class UserSettingsAdmin(admin.ModelAdmin):
    list_display = ('user', 'ml_weight', 'ontology_weight', 'high_risk_threshold', 'medium_risk_threshold')
