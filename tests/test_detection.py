import unittest
from backend.detector.detector import HybridDetectionEngine


class TestDetectionEngine(unittest.TestCase):
    """Unit tests for the Hybrid Detection Engine combining ML and Ontology."""

    def setUp(self):
        self.engine = HybridDetectionEngine(ml_weight=0.55, ontology_weight=0.45)

    def test_spambot_detection(self):
        bot_profile = {
            'username': 'bot_spammer_9921',
            'followers_count': 12,
            'following_count': 2850,
            'posts_count': 0,
            'account_age_days': 7,
            'bio_length': 0,
            'has_profile_pic': False,
            'is_verified': False,
            'avg_likes': 0.0,
            'avg_comments': 0.0,
        }
        result = self.engine.detect(bot_profile)
        self.assertEqual(result['risk_level'], 'High')
        self.assertEqual(result['final_verdict'], 'Fake Profile')
        self.assertGreaterEqual(result['overall_risk_score'], 70.0)
        self.assertTrue(len(result['flagged_reasons']) > 0)

    def test_authentic_profile_detection(self):
        authentic_profile = {
            'username': 'dr_elena_official',
            'followers_count': 94500,
            'following_count': 820,
            'posts_count': 1280,
            'account_age_days': 2400,
            'bio_length': 140,
            'has_profile_pic': True,
            'is_verified': True,
            'avg_likes': 3420.0,
            'avg_comments': 410.0,
        }
        result = self.engine.detect(authentic_profile)
        self.assertEqual(result['risk_level'], 'Low')
        self.assertEqual(result['final_verdict'], 'Authentic Profile')
        self.assertLess(result['overall_risk_score'], 35.0)

    def test_weight_customization(self):
        profile = {
            'username': 'test_account',
            'followers_count': 100,
            'following_count': 100,
            'posts_count': 10,
            'account_age_days': 100,
        }
        res1 = self.engine.detect(profile)
        
        # Change engine weights
        self.engine.set_weights(0.8, 0.2)
        res2 = self.engine.detect(profile)
        self.assertEqual(res2['ml_weight_used'], 0.8)
        self.assertEqual(res2['ontology_weight_used'], 0.2)


if __name__ == '__main__':
    unittest.main()
