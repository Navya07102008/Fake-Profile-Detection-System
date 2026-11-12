import csv
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_CSV_PATH = BASE_DIR / 'dataset' / 'raw' / 'profiles.csv'
PROCESSED_CSV_PATH = BASE_DIR / 'dataset' / 'processed' / 'cleaned_profiles.csv'

RAW_CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
PROCESSED_CSV_PATH.parent.mkdir(parents=True, exist_ok=True)

random.seed(42)

AUTHENTIC_ADJECTIVES = ['cyber', 'pixel', 'sunny', 'cosmic', 'urban', 'quiet', 'tech', 'wild', 'blue', 'silver', 'swift', 'golden', 'velvet', 'stellar', 'nordic', 'coastal']
AUTHENTIC_NOUNS = ['coder', 'traveler', 'designer', 'engineer', 'artist', 'nomad', 'reader', 'builder', 'musician', 'photographer', 'scholar', 'baker', 'surfer', 'runner', 'maker']
BOT_PREFIXES = ['bot', 'spam', 'follow', 'crypto', 'airdrop', 'promo', 'boost', 'free', 'gainz', 'fast', 'auto', 'blast']

def generate_profiles(count=2500):
    rows = []
    
    # 50% Authentic, 50% Fake
    for i in range(count):
        is_fake = 1 if i % 2 == 1 else 0
        
        if is_fake == 0:
            # Authentic profile
            profile_type = random.choices(['regular', 'influencer', 'new_organic'], weights=[0.75, 0.15, 0.10])[0]
            
            if profile_type == 'influencer':
                followers = random.randint(15000, 350000)
                following = random.randint(200, 1800)
                posts = random.randint(250, 2500)
                age = random.randint(400, 3650)
                bio_len = random.randint(50, 150)
                has_pic = 1
                is_verified = 1 if random.random() < 0.7 else 0
                avg_likes = round(followers * random.uniform(0.015, 0.08), 1)
                avg_comments = round(avg_likes * random.uniform(0.02, 0.1), 1)
                has_url = 1
                username = f"{random.choice(AUTHENTIC_ADJECTIVES)}_{random.choice(AUTHENTIC_NOUNS)}_official"
            elif profile_type == 'new_organic':
                followers = random.randint(10, 80)
                following = random.randint(15, 120)
                posts = random.randint(1, 15)
                age = random.randint(5, 60)
                bio_len = random.randint(10, 80)
                has_pic = 1 if random.random() < 0.9 else 0
                is_verified = 0
                avg_likes = round(followers * random.uniform(0.1, 0.35), 1)
                avg_comments = round(random.uniform(0.5, 4.0), 1)
                has_url = 0
                username = f"{random.choice(AUTHENTIC_ADJECTIVES)}{random.choice(AUTHENTIC_NOUNS)}{random.randint(1, 99)}"
            else: # regular organic
                followers = random.randint(150, 3500)
                following = random.randint(100, 1500)
                posts = random.randint(20, 600)
                age = random.randint(100, 2500)
                bio_len = random.randint(20, 120)
                has_pic = 1
                is_verified = 0
                avg_likes = round(followers * random.uniform(0.04, 0.18), 1)
                avg_comments = round(avg_likes * random.uniform(0.03, 0.12), 1)
                has_url = 1 if random.random() < 0.3 else 0
                username = f"{random.choice(AUTHENTIC_ADJECTIVES)}.{random.choice(AUTHENTIC_NOUNS)}"
        else:
            # Fake profile
            fake_type = random.choices(['spambot', 'ghost', 'bought_followers', 'fresh_mass_follow'], weights=[0.4, 0.25, 0.2, 0.15])[0]
            
            if fake_type == 'spambot':
                followers = random.randint(0, 50)
                following = random.randint(800, 5000)
                posts = random.randint(0, 4)
                age = random.randint(1, 45)
                bio_len = random.choice([0, random.randint(5, 30)])
                has_pic = 1 if random.random() < 0.2 else 0
                is_verified = 0
                avg_likes = round(random.uniform(0.0, 1.2), 1)
                avg_comments = 0.0
                has_url = 1 if random.random() < 0.6 else 0
                username = f"{random.choice(BOT_PREFIXES)}_{random.randint(10000, 999999)}"
            elif fake_type == 'ghost':
                followers = random.randint(0, 30)
                following = random.randint(50, 800)
                posts = 0
                age = random.randint(100, 1000)
                bio_len = 0
                has_pic = 0
                is_verified = 0
                avg_likes = 0.0
                avg_comments = 0.0
                has_url = 0
                username = f"user_{random.randint(1000000, 9999999)}"
            elif fake_type == 'bought_followers':
                followers = random.randint(20000, 80000)
                following = random.randint(50, 400)
                posts = random.randint(5, 25)
                age = random.randint(20, 150)
                bio_len = random.randint(0, 40)
                has_pic = 1
                is_verified = 0
                # Disproportionately tiny engagement for huge follower count
                avg_likes = round(random.uniform(1.0, 8.0), 1)
                avg_comments = round(random.uniform(0.0, 0.5), 1)
                has_url = 1 if random.random() < 0.5 else 0
                username = f"promoter_{random.choice(BOT_PREFIXES)}{random.randint(100, 999)}"
            else: # fresh_mass_follow
                followers = random.randint(0, 15)
                following = random.randint(400, 3000)
                posts = random.randint(0, 2)
                age = random.randint(1, 10)
                bio_len = random.choice([0, 15])
                has_pic = 0
                is_verified = 0
                avg_likes = 0.0
                avg_comments = 0.0
                has_url = 0
                username = f"{random.choice(BOT_PREFIXES)}{random.randint(1000, 99999)}"

        rows.append({
            'username': username,
            'followers_count': followers,
            'following_count': following,
            'posts_count': posts,
            'account_age_days': age,
            'bio_length': bio_len,
            'has_profile_pic': has_pic,
            'is_verified': is_verified,
            'avg_likes': avg_likes,
            'avg_comments': avg_comments,
            'has_external_url': has_url,
            'is_fake': is_fake,
        })
    return rows

def main():
    profiles = generate_profiles(2500)
    fieldnames = [
        'username', 'followers_count', 'following_count', 'posts_count',
        'account_age_days', 'bio_length', 'has_profile_pic', 'is_verified',
        'avg_likes', 'avg_comments', 'has_external_url', 'is_fake'
    ]

    with open(RAW_CSV_PATH, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(profiles)

    # Processed copy (cleaned, validated, same clean schema)
    with open(PROCESSED_CSV_PATH, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(profiles)

    print(f"Generated {len(profiles)} profile records successfully.")
    print(f"Saved raw dataset to: {RAW_CSV_PATH}")
    print(f"Saved processed dataset to: {PROCESSED_CSV_PATH}")

if __name__ == '__main__':
    main()
