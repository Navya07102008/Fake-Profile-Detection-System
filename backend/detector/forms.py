from django import forms
from django.contrib.auth.models import User
from .models import ProfileAnalysis, UserSettings


class ProfileAnalysisForm(forms.ModelForm):
    """Form to enter social media profile details for forensic analysis."""

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g. sarah_travels or bot_9921',
            'required': True,
        }),
        label="Account Username"
    )

    followers_count = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': 0,
            'placeholder': '0',
            'required': True,
        }),
        label="Followers Count",
        initial=0
    )

    following_count = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': 0,
            'placeholder': '0',
            'required': True,
        }),
        label="Following Count",
        initial=0
    )

    posts_count = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': 0,
            'placeholder': '0',
            'required': True,
        }),
        label="Total Posts",
        initial=0
    )

    account_age_days = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': 0,
            'placeholder': 'e.g. 180',
            'required': True,
        }),
        label="Account Age (Days)",
        initial=30
    )

    bio_text = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Profile biography / status description...',
        }),
        required=False,
        label="Bio Description"
    )

    avg_likes = forms.FloatField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': 0,
            'step': '0.1',
            'placeholder': '0.0',
        }),
        label="Avg Likes per Post",
        initial=0.0,
        required=False
    )

    avg_comments = forms.FloatField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': 0,
            'step': '0.1',
            'placeholder': '0.0',
        }),
        label="Avg Comments per Post",
        initial=0.0,
        required=False
    )

    has_profile_pic = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
        }),
        required=False,
        label="Has Profile Picture (Avatar)",
        initial=True
    )

    is_verified = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
        }),
        required=False,
        label="Verified Badge Present",
        initial=False
    )

    has_external_url = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
        }),
        required=False,
        label="Bio Contains External Link",
        initial=False
    )

    class Meta:
        model = ProfileAnalysis
        fields = [
            'username', 'followers_count', 'following_count', 'posts_count',
            'account_age_days', 'bio_text', 'avg_likes', 'avg_comments',
            'has_profile_pic', 'is_verified', 'has_external_url'
        ]

    def clean_followers_count(self):
        val = self.cleaned_data.get('followers_count', 0)
        if val < 0:
            raise forms.ValidationError("Followers count cannot be negative.")
        return val

    def clean_following_count(self):
        val = self.cleaned_data.get('following_count', 0)
        if val < 0:
            raise forms.ValidationError("Following count cannot be negative.")
        return val


class UserSettingsForm(forms.ModelForm):
    """Form to tune weights and risk thresholds."""

    class Meta:
        model = UserSettings
        fields = ['ml_weight', 'ontology_weight', 'high_risk_threshold', 'medium_risk_threshold', 'theme_mode']
        widgets = {
            'ml_weight': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.05', 'min': '0.1', 'max': '0.9'}),
            'ontology_weight': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.05', 'min': '0.1', 'max': '0.9'}),
            'high_risk_threshold': forms.NumberInput(attrs={'class': 'form-control', 'step': '1', 'min': '50', 'max': '90'}),
            'medium_risk_threshold': forms.NumberInput(attrs={'class': 'form-control', 'step': '1', 'min': '20', 'max': '60'}),
            'theme_mode': forms.Select(attrs={'class': 'form-select'}, choices=[('dark', 'Cyber Dark Navy'), ('midnight', 'Midnight Purple')]),
        }
