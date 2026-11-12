import unittest
from ml_model.feature_extraction import extract_features_from_dict, extract_feature_vector, FEATURE_NAMES


class TestFeatureExtraction(unittest.TestCase):
    """Unit tests for profile feature engineering logic."""

    def test_feature_names_length(self):
        self.assertEqual(len(FEATURE_NAMES), 18)

    def test_division_by_zero_safety(self):
        # Empty zero profile
        profile = {
            'username': 'zero_user',
            'followers_count': 0,
            'following_count': 0,
            'posts_count': 0,
            'account_age_days': 0,
            'bio_length': 0,
            'has_profile_pic': False,
            'is_verified': False,
            'avg_likes': 0.0,
            'avg_comments': 0.0,
        }
        features = extract_features_from_dict(profile)
        self.assertEqual(features['follower_following_ratio'], 0.0)
        self.assertEqual(features['engagement_rate'], 0.0)
        self.assertEqual(features['posts_per_day'], 0.0)

    def test_ratio_calculations(self):
        profile = {
            'username': 'bot_12345',
            'followers_count': 100,
            'following_count': 2000,
            'posts_count': 10,
            'account_age_days': 50,
            'avg_likes': 20.0,
            'avg_comments': 5.0,
        }
        features = extract_features_from_dict(profile)
        # follower_following_ratio = 100 / (2000 + 1)
        expected_ratio = round(100.0 / 2001.0, 4)
        self.assertAlmostEqual(features['follower_following_ratio'], expected_ratio, places=3)
        # digit ratio in username 'bot_12345' (5 digits out of 9 chars)
        self.assertAlmostEqual(features['username_digit_ratio'], round(5.0 / 9.0, 4), places=3)
        self.assertEqual(features['has_numbers_in_username'], 1.0)

    def test_feature_vector_ordering(self):
        profile = {'username': 'test_agent'}
        vector = extract_feature_vector(profile)
        self.assertEqual(len(vector), len(FEATURE_NAMES))
        self.assertTrue(all(isinstance(v, (int, float)) for v in vector))


if __name__ == '__main__':
    unittest.main()
