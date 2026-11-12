import numpy as np


FEATURE_NAMES = [
    'followers_count',
    'following_count',
    'posts_count',
    'account_age_days',
    'bio_length',
    'has_profile_pic',
    'is_verified',
    'avg_likes',
    'avg_comments',
    'has_external_url',
    'follower_following_ratio',
    'following_follower_ratio',
    'engagement_rate',
    'posts_per_day',
    'username_length',
    'username_digit_count',
    'username_digit_ratio',
    'has_numbers_in_username',
]


def extract_features_from_dict(profile: dict) -> dict:
    """
    Extracts raw and engineered features from a profile dictionary.
    Returns a dictionary of feature names and values.
    """
    username = str(profile.get('username', '')).strip()
    followers = float(profile.get('followers_count', 0))
    following = float(profile.get('following_count', 0))
    posts = float(profile.get('posts_count', 0))
    age = float(profile.get('account_age_days', 0))
    bio_length = float(profile.get('bio_length', len(str(profile.get('bio_text', '')))))
    has_pic = 1.0 if bool(profile.get('has_profile_pic', False)) else 0.0
    verified = 1.0 if bool(profile.get('is_verified', False)) else 0.0
    likes = float(profile.get('avg_likes', 0.0))
    comments = float(profile.get('avg_comments', 0.0))
    has_url = 1.0 if bool(profile.get('has_external_url', False)) else 0.0

    # Engineered ratios and rates
    follower_ratio = followers / (following + 1.0)
    following_ratio = following / (followers + 1.0)
    engagement = ((likes + comments) / (followers + 1.0)) * 100.0
    posts_per_day = posts / (age + 1.0)

    u_len = float(len(username))
    digit_count = float(sum(c.isdigit() for c in username))
    digit_ratio = (digit_count / max(u_len, 1.0))
    has_numbers = 1.0 if digit_count > 0 else 0.0

    return {
        'followers_count': followers,
        'following_count': following,
        'posts_count': posts,
        'account_age_days': age,
        'bio_length': bio_length,
        'has_profile_pic': has_pic,
        'is_verified': verified,
        'avg_likes': likes,
        'avg_comments': comments,
        'has_external_url': has_url,
        'follower_following_ratio': round(follower_ratio, 4),
        'following_follower_ratio': round(following_ratio, 4),
        'engagement_rate': round(engagement, 4),
        'posts_per_day': round(posts_per_day, 4),
        'username_length': u_len,
        'username_digit_count': digit_count,
        'username_digit_ratio': round(digit_ratio, 4),
        'has_numbers_in_username': has_numbers,
    }


def extract_feature_vector(profile: dict) -> list[float]:
    """
    Extracts ordered numerical feature vector matching FEATURE_NAMES.
    """
    feat_dict = extract_features_from_dict(profile)
    return [feat_dict[k] for k in FEATURE_NAMES]
