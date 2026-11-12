from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from backend.detector.models import ProfileAnalysis, UserSettings


class TestDetectorViews(TestCase):
    """Integration test suite for Django views and endpoints."""

    def setUp(self):
        self.client = Client()
        self.username = "testanalyst"
        self.password = "Secur3P@ssw0rd!"
        self.user = User.objects.create_user(username=self.username, password=self.password)
        UserSettings.objects.create(user=self.user)

        self.analysis = ProfileAnalysis.objects.create(
            user=self.user,
            username="bot_tester_99",
            followers_count=10,
            following_count=2000,
            posts_count=0,
            account_age_days=5,
            bio_length=0,
            has_profile_pic=False,
            is_verified=False,
            avg_likes=0.0,
            avg_comments=0.0,
            overall_risk_score=92.5,
            risk_level="High",
            final_verdict="Fake Profile",
            ml_prediction="Fake",
            ml_fake_probability=0.95,
            ml_confidence=95.0,
            ontology_verdict="High Risk - Fake / Bot Candidate",
            ontology_risk_score=90.0,
            flagged_reasons=["Following asymmetry", "No avatar"],
        )

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Fake Profile Detection System")

    def test_login_logout(self):
        login_res = self.client.post(reverse('login'), {'username': self.username, 'password': self.password})
        self.assertEqual(login_res.status_code, 302)

        logout_res = self.client.get(reverse('logout'))
        self.assertEqual(logout_res.status_code, 302)

    def test_authenticated_dashboard(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Cybersecurity Intelligence Dashboard")

    def test_profile_analysis_post(self):
        self.client.login(username=self.username, password=self.password)
        post_data = {
            'username': 'cyber_newbie_1',
            'followers_count': 50,
            'following_count': 120,
            'posts_count': 5,
            'account_age_days': 20,
            'bio_text': 'Hello world cyber',
            'avg_likes': 8.0,
            'avg_comments': 1.0,
            'has_profile_pic': True,
            'is_verified': False,
            'has_external_url': False,
        }
        response = self.client.post(reverse('profile_check'), post_data)
        self.assertEqual(response.status_code, 302)
        # Verify saved in database
        self.assertTrue(ProfileAnalysis.objects.filter(username='cyber_newbie_1').exists())

    def test_result_and_detail_views(self):
        self.client.login(username=self.username, password=self.password)
        pk = self.analysis.pk

        # Result view
        res = self.client.get(reverse('result', kwargs={'pk': pk}))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "bot_tester_99")

        # Feature Extraction view
        feat_res = self.client.get(reverse('feature_extraction', kwargs={'pk': pk}))
        self.assertEqual(feat_res.status_code, 200)

        # ML & Ontology analysis details view
        details_res = self.client.get(reverse('analysis_details', kwargs={'pk': pk}))
        self.assertEqual(details_res.status_code, 200)

        # Risk assessment view
        risk_res = self.client.get(reverse('risk_assessment', kwargs={'pk': pk}))
        self.assertEqual(risk_res.status_code, 200)

    def test_history_and_analytics_views(self):
        self.client.login(username=self.username, password=self.password)
        
        hist_res = self.client.get(reverse('history'))
        self.assertEqual(hist_res.status_code, 200)
        self.assertContains(hist_res, "bot_tester_99")

        analytics_res = self.client.get(reverse('analytics'))
        self.assertEqual(analytics_res.status_code, 200)

        onto_res = self.client.get(reverse('ontology_visual'))
        self.assertEqual(onto_res.status_code, 200)

        settings_res = self.client.get(reverse('settings'))
        self.assertEqual(settings_res.status_code, 200)

    def test_pdf_report_download(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('download_pdf', kwargs={'pk': self.analysis.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertGreater(len(response.content), 500)
