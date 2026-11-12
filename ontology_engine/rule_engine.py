class SemanticRuleEngine:
    """Executes semantic forensic rules against profile characteristics."""

    def evaluate_rules(self, profile: dict) -> dict:
        """
        Evaluates profile features against defined ontology forensic rules.
        Returns:
            triggered_rules: list of dicts with rule id, name, description, weight, and severity
            risk_score: float (0.0 to 100.0)
            inferred_classes: list of str (ontology class names)
            risk_category: str ('LowRisk', 'MediumRisk', 'HighRisk')
        """
        username = str(profile.get("username", ""))
        followers = int(profile.get("followers_count", 0))
        following = int(profile.get("following_count", 0))
        posts = int(profile.get("posts_count", 0))
        age_days = int(profile.get("account_age_days", 0))
        bio_len = int(profile.get("bio_length", 0))
        has_pic = bool(profile.get("has_profile_pic", False))
        is_verified = bool(profile.get("is_verified", False))
        avg_likes = float(profile.get("avg_likes", 0.0))
        avg_comments = float(profile.get("avg_comments", 0.0))

        follower_ratio = followers / (following + 1)
        engagement = ((avg_likes + avg_comments) / (followers + 1)) * 100
        digit_count = sum(c.isdigit() for c in username)
        digit_ratio = (digit_count / len(username)) if username else 0.0

        triggered_rules = []
        inferred_classes = ["SocialMediaProfile"]
        raw_score = 0.0

        # Rule 1: Extreme Follower-to-Following Asymmetry
        if following > 300 and follower_ratio < 0.05:
            triggered_rules.append({
                "rule_id": "Rule_FollowerAsymmetry",
                "name": "Mass Follower Asymmetry",
                "severity": "HIGH",
                "points": 25,
                "description": f"Following count ({following}) is disproportionately higher than followers ({followers}), ratio: {follower_ratio:.3f}."
            })
            raw_score += 25
            inferred_classes.append("BotSpammerProfile")

        # Rule 2: Dormant Ghost Lurker Profile
        if age_days > 120 and posts == 0 and following > 50:
            triggered_rules.append({
                "rule_id": "Rule_GhostLurker",
                "name": "Dormant Ghost Account",
                "severity": "MEDIUM",
                "points": 20,
                "description": f"Account age is {age_days} days with 0 posts despite actively following {following} accounts."
            })
            raw_score += 20
            inferred_classes.append("GhostLurkerProfile")

        # Rule 3: Hyperactive New Account / Fresh Bot
        if age_days <= 14 and following > 350:
            triggered_rules.append({
                "rule_id": "Rule_HyperactiveNewAccount",
                "name": "Hyperactive Fresh Account",
                "severity": "HIGH",
                "points": 30,
                "description": f"New account created only {age_days} days ago has already accumulated {following} followings."
            })
            raw_score += 30
            inferred_classes.append("BotSpammerProfile")

        # Rule 4: Anonymous Profile (No Avatar, Empty Bio)
        if not has_pic and bio_len == 0 and posts <= 2:
            triggered_rules.append({
                "rule_id": "Rule_NoAvatarEmptyBio",
                "name": "Anonymous Incomplete Profile",
                "severity": "MEDIUM",
                "points": 20,
                "description": "Default avatar, blank bio description, and negligible post history."
            })
            raw_score += 20
            inferred_classes.append("SuspiciousProfile")

        # Rule 5: Engagement Anomaly / Fake Follower Farm
        if followers >= 5000 and posts >= 5 and engagement < 0.02:
            triggered_rules.append({
                "rule_id": "Rule_EngagementAnomaly",
                "name": "Artificially Inflated Audience",
                "severity": "HIGH",
                "points": 25,
                "description": f"High follower volume ({followers}) with near-zero engagement rate ({engagement:.4f}%), indicating purchased followers."
            })
            raw_score += 25
            inferred_classes.append("EngagementAnomalyProfile")

        # Rule 6: Machine-Generated Handle Pattern
        if digit_ratio >= 0.40 and len(username) >= 6:
            triggered_rules.append({
                "rule_id": "Rule_MachineGeneratedHandle",
                "name": "Algorithmic Handle Pattern",
                "severity": "LOW",
                "points": 15,
                "description": f"High concentration of numeric characters in username ({digit_ratio*100:.1f}% digits)."
            })
            raw_score += 15

        # Rule 7: Authenticity Exemption / Mitigating Factors
        if is_verified and has_pic and age_days > 180:
            triggered_rules.append({
                "rule_id": "Rule_AuthenticityMitigation",
                "name": "Verified Identity Trust Anchor",
                "severity": "MITIGATION",
                "points": -35,
                "description": "Identity verified badge and established account history significantly mitigates risk."
            })
            raw_score -= 35
            inferred_classes.append("VerifiedAuthorityProfile")
        elif not triggered_rules and has_pic and age_days > 60:
            inferred_classes.append("RegularOrganicUser")

        # Clamp semantic risk score between 0 and 100
        semantic_risk_score = max(0.0, min(100.0, raw_score))

        # Determine risk classification
        if semantic_risk_score >= 70:
            risk_category = "HighRisk"
            if "FakeProfile" not in inferred_classes:
                inferred_classes.append("FakeProfile")
        elif semantic_risk_score >= 35:
            risk_category = "MediumRisk"
            if "SuspiciousProfile" not in inferred_classes:
                inferred_classes.append("SuspiciousProfile")
        else:
            risk_category = "LowRisk"
            if "AuthenticProfile" not in inferred_classes:
                inferred_classes.append("AuthenticProfile")

        return {
            "triggered_rules": triggered_rules,
            "risk_score": round(semantic_risk_score, 2),
            "inferred_classes": list(dict.fromkeys(inferred_classes)),
            "risk_category": risk_category,
        }
