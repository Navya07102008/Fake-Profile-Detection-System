from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('analyze/', views.profile_check_view, name='profile_check'),
    path('result/<int:pk>/', views.result_view, name='result'),
    path('features/<int:pk>/', views.feature_extraction_view, name='feature_extraction'),
    path('analysis-details/<int:pk>/', views.analysis_details_view, name='analysis_details'),
    path('risk-assessment/<int:pk>/', views.risk_assessment_view, name='risk_assessment'),
    path('history/', views.history_view, name='history'),
    path('history/delete/<int:pk>/', views.delete_history_item, name='delete_history'),
    path('analytics/', views.analytics_view, name='analytics'),
    path('reports/', views.report_view, name='reports'),
    path('reports/<int:pk>/', views.report_view, name='report_detail'),
    path('reports/pdf/<int:pk>/', views.download_pdf_report, name='download_pdf'),
    path('ontology-visual/', views.ontology_visual_view, name='ontology_visual'),
    path('settings/', views.settings_view, name='settings'),
]
