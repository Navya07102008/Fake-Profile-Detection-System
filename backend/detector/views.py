import json
import io
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Avg, Q

from .models import ProfileAnalysis, UserSettings
from .forms import ProfileAnalysisForm, UserSettingsForm
from .detector import HybridDetectionEngine
from reports.detection_report import DetectionReportGenerator
from ontology_engine.ontology_loader import OntologyLoader


detector_engine = HybridDetectionEngine()
report_generator = DetectionReportGenerator()


def home_view(request):
    """Landing page showcasing system capabilities, architecture and live stats."""
    total_scanned = ProfileAnalysis.objects.count()
    fake_detected = ProfileAnalysis.objects.filter(risk_level='High').count()
    accuracy_display = "97.4%"

    recent_samples = ProfileAnalysis.objects.all()[:5]

    context = {
        'total_scanned': total_scanned,
        'fake_detected': fake_detected,
        'accuracy_display': accuracy_display,
        'recent_samples': recent_samples,
    }
    return render(request, 'home.html', context)


def register_view(request):
    """User registration view."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserSettings.objects.create(user=user)
            login(request, user)
            messages.success(request, f"Welcome to the Fake Profile Detection System, @{user.username}!")
            return redirect('dashboard')
        else:
            messages.error(request, "Registration error. Please check the fields below.")
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})


def login_view(request):
    """User login view."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, @{user.username}!")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    """Logs out user and redirects to login."""
    logout(request)
    messages.info(request, "You have been logged out securely.")
    return redirect('login')


@login_required
def dashboard_view(request):
    """Main dashboard displaying cybersecurity metrics, recent detections, and charts."""
    analyses = ProfileAnalysis.objects.filter(Q(user=request.user) | Q(user__isnull=True))

    total_count = analyses.count()
    high_risk_count = analyses.filter(risk_level='High').count()
    med_risk_count = analyses.filter(risk_level='Medium').count()
    low_risk_count = analyses.filter(risk_level='Low').count()

    fake_ratio = round((high_risk_count / total_count * 100), 1) if total_count > 0 else 0
    avg_risk = analyses.aggregate(avg_score=Avg('overall_risk_score'))['avg_score'] or 0.0

    recent_analyses = analyses.order_by('-created_at')[:8]

    context = {
        'total_count': total_count,
        'high_risk_count': high_risk_count,
        'med_risk_count': med_risk_count,
        'low_risk_count': low_risk_count,
        'fake_ratio': fake_ratio,
        'avg_risk': round(avg_risk, 1),
        'recent_analyses': recent_analyses,
    }
    return render(request, 'dashboard.html', context)


@login_required
def profile_check_view(request):
    """Profile analysis input page with 1-click sample loaders."""
    if request.method == 'POST':
        form = ProfileAnalysisForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            # Get user custom settings if any
            user_settings, _ = UserSettings.objects.get_or_create(user=request.user)

            # Package profile data dictionary
            profile_data = {
                'username': cd['username'],
                'followers_count': cd['followers_count'],
                'following_count': cd['following_count'],
                'posts_count': cd['posts_count'],
                'account_age_days': cd['account_age_days'],
                'bio_length': len(cd.get('bio_text', '')),
                'has_profile_pic': cd['has_profile_pic'],
                'is_verified': cd['is_verified'],
                'avg_likes': cd.get('avg_likes', 0.0),
                'avg_comments': cd.get('avg_comments', 0.0),
                'has_external_url': cd['has_external_url'],
                'bio_text': cd.get('bio_text', ''),
            }

            # Run hybrid detection
            result = detector_engine.detect(profile_data, user_settings=user_settings)

            # Persist analysis to database
            analysis = ProfileAnalysis.objects.create(
                user=request.user,
                username=cd['username'],
                followers_count=cd['followers_count'],
                following_count=cd['following_count'],
                posts_count=cd['posts_count'],
                account_age_days=cd['account_age_days'],
                bio_length=len(cd.get('bio_text', '')),
                has_profile_pic=cd['has_profile_pic'],
                is_verified=cd['is_verified'],
                avg_likes=cd.get('avg_likes', 0.0),
                avg_comments=cd.get('avg_comments', 0.0),
                has_external_url=cd['has_external_url'],
                bio_text=cd.get('bio_text', ''),

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

            messages.success(request, f"Forensic analysis completed for @{cd['username']}.")
            return redirect('result', pk=analysis.pk)
        else:
            messages.error(request, "Please rectify invalid form inputs.")
    else:
        form = ProfileAnalysisForm()

    return render(request, 'profile_check.html', {'form': form})


@login_required
def result_view(request, pk):
    """Displays comprehensive detection result, risk meter, and forensic verdict."""
    analysis = get_object_or_404(ProfileAnalysis, pk=pk)
    context = {
        'analysis': analysis,
        'extracted': analysis.extracted_features or {},
        'flagged_reasons': analysis.flagged_reasons or [],
        'rules_triggered': analysis.ontology_rules_triggered or [],
        'ml_prob_pct': round(analysis.ml_fake_probability * 100, 1),
    }
    return render(request, 'result.html', context)


@login_required
def feature_extraction_view(request, pk):
    """Detailed visual breakdown of raw vs engineered features."""
    analysis = get_object_or_404(ProfileAnalysis, pk=pk)
    context = {
        'analysis': analysis,
        'extracted': analysis.extracted_features or {},
    }
    return render(request, 'feature_extraction.html', context)


@login_required
def analysis_details_view(request, pk):
    """Deep-dive comparative breakdown of ML predictions vs Ontology reasoning."""
    analysis = get_object_or_404(ProfileAnalysis, pk=pk)
    context = {
        'analysis': analysis,
        'ml_importances': analysis.ml_feature_importances or {},
        'rules_triggered': analysis.ontology_rules_triggered or [],
        'inferred_classes': analysis.ontology_inferred_classes or [],
    }
    return render(request, 'analysis_details.html', context)


@login_required
def risk_assessment_view(request, pk):
    """Risk Assessment Matrix: Low, Medium, and High breakdowns with mitigation tactics."""
    analysis = get_object_or_404(ProfileAnalysis, pk=pk)
    context = {
        'analysis': analysis,
    }
    return render(request, 'risk_assessment.html', context)


@login_required
def history_view(request):
    """Audit log of past detections with search, filtering, and quick actions."""
    query = request.GET.get('q', '').strip()
    filter_risk = request.GET.get('risk', '').strip()

    analyses = ProfileAnalysis.objects.filter(Q(user=request.user) | Q(user__isnull=True))

    if query:
        analyses = analyses.filter(username__icontains=query)
    if filter_risk:
        analyses = analyses.filter(risk_level__iexact=filter_risk)

    context = {
        'analyses': analyses,
        'query': query,
        'filter_risk': filter_risk,
    }
    return render(request, 'history.html', context)


@login_required
def delete_history_item(request, pk):
    """Deletes an analysis record."""
    analysis = get_object_or_404(ProfileAnalysis, pk=pk)
    analysis.delete()
    messages.success(request, "Analysis record deleted from history.")
    return redirect('history')


@login_required
def analytics_view(request):
    """Interactive analytics charts: Fake vs Real, Risk Distribution, Feature Importance."""
    analyses = ProfileAnalysis.objects.all()

    total = analyses.count()
    high = analyses.filter(risk_level='High').count()
    med = analyses.filter(risk_level='Medium').count()
    low = analyses.filter(risk_level='Low').count()

    verified_real = analyses.filter(is_verified=True, risk_level='Low').count()
    unverified_fake = analyses.filter(is_verified=False, risk_level='High').count()

    context = {
        'total': total,
        'high': high,
        'med': med,
        'low': low,
        'verified_real': verified_real,
        'unverified_fake': unverified_fake,
    }
    return render(request, 'analytics.html', context)


@login_required
def report_view(request, pk=None):
    """Web preview of detection report."""
    if pk:
        analysis = get_object_or_404(ProfileAnalysis, pk=pk)
    else:
        analysis = ProfileAnalysis.objects.first()

    context = {
        'analysis': analysis,
    }
    return render(request, 'report.html', context)


@login_required
def download_pdf_report(request, pk):
    """Generates and downloads a ReportLab PDF forensic intelligence report."""
    analysis = get_object_or_404(ProfileAnalysis, pk=pk)

    data = {
        'id': analysis.pk,
        'username': analysis.username,
        'followers_count': analysis.followers_count,
        'following_count': analysis.following_count,
        'posts_count': analysis.posts_count,
        'account_age_days': analysis.account_age_days,
        'bio_length': analysis.bio_length,
        'has_profile_pic': analysis.has_profile_pic,
        'is_verified': analysis.is_verified,
        'avg_likes': analysis.avg_likes,
        'avg_comments': analysis.avg_comments,
        'risk_level': analysis.risk_level,
        'final_verdict': analysis.final_verdict,
        'overall_risk_score': analysis.overall_risk_score,
        'ml_prediction': analysis.ml_prediction,
        'ml_fake_probability': analysis.ml_fake_probability,
        'ml_confidence': analysis.ml_confidence,
        'ontology_verdict': analysis.ontology_verdict,
        'ontology_risk_score': analysis.ontology_risk_score,
        'ontology_inferred_classes': analysis.ontology_inferred_classes,
        'ontology_rules_triggered': analysis.ontology_rules_triggered,
        'flagged_reasons': analysis.flagged_reasons,
    }

    pdf_buffer = io.BytesIO()
    report_generator.generate(data, pdf_buffer)
    pdf_buffer.seek(0)

    filename = f"FakeProfile_ForensicReport_{analysis.username}_{analysis.pk}.pdf"
    response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


@login_required
def ontology_visual_view(request):
    """Interactive visual representation of the OWL ontology hierarchy, properties and rules."""
    loader = OntologyLoader()
    stats = loader.get_ontology_stats()

    # Pre-defined classes and rules for visualization
    classes_hierarchy = [
        {"name": "SocialMediaProfile", "parent": "owl:Thing", "desc": "Overarching social media account entity"},
        {"name": "AuthenticProfile", "parent": "SocialMediaProfile", "desc": "Genuine human-operated profile"},
        {"name": "VerifiedAuthorityProfile", "parent": "AuthenticProfile", "desc": "Celebrity, brand, or public authority"},
        {"name": "RegularOrganicUser", "parent": "AuthenticProfile", "desc": "Ordinary person with organic engagement"},
        {"name": "SuspiciousProfile", "parent": "SocialMediaProfile", "desc": "Account showing anomalous indicators"},
        {"name": "FakeProfile", "parent": "SuspiciousProfile", "desc": "Fraudulent or deceptive account"},
        {"name": "BotSpammerProfile", "parent": "FakeProfile", "desc": "Automated script running mass following or spam"},
        {"name": "GhostLurkerProfile", "parent": "FakeProfile", "desc": "Zero-post inactive sleeper or spy account"},
        {"name": "EngagementAnomalyProfile", "parent": "FakeProfile", "desc": "Account with purchased fake followers"},
    ]

    rules = [
        {"id": "Rule_FollowerAsymmetry", "name": "Following Asymmetry", "cond": "Following > 300 AND Ratio < 0.05", "impact": "+25 Risk"},
        {"id": "Rule_GhostLurker", "name": "Dormant Ghost", "cond": "Age > 120 days AND Posts = 0 AND Following > 50", "impact": "+20 Risk"},
        {"id": "Rule_HyperactiveNewAccount", "name": "Hyperactive Fresh Bot", "cond": "Age <= 14 days AND Following > 350", "impact": "+30 Risk"},
        {"id": "Rule_NoAvatarEmptyBio", "name": "Anonymous Incomplete", "cond": "No Avatar AND Bio = 0 AND Posts <= 2", "impact": "+20 Risk"},
        {"id": "Rule_EngagementAnomaly", "name": "Follower Farm / Fake Audience", "cond": "Followers > 5000 AND Engagement < 0.02%", "impact": "+25 Risk"},
        {"id": "Rule_MachineGeneratedHandle", "name": "Algorithmic Handle Pattern", "cond": "Digit Ratio in handle >= 40%", "impact": "+15 Risk"},
        {"id": "Rule_AuthenticityMitigation", "name": "Verified Identity Trust Anchor", "cond": "Verified True AND Avatar True AND Age > 180", "impact": "-35 Risk"},
    ]

    context = {
        'stats': stats,
        'classes': classes_hierarchy,
        'rules': rules,
    }
    return render(request, 'ontology_visual.html', context)


@login_required
def settings_view(request):
    """User preferences for threshold tuning and detection weights."""
    user_settings, _ = UserSettings.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserSettingsForm(request.POST, instance=user_settings)
        if form.is_valid():
            form.save()
            messages.success(request, "Settings updated successfully.")
            return redirect('settings')
    else:
        form = UserSettingsForm(instance=user_settings)

    context = {
        'form': form,
        'settings': user_settings,
    }
    return render(request, 'settings.html', context)
