from ml_model.predict import ProfilePredictor
from ontology_engine.reasoner import OntologyReasoner


class HybridDetectionEngine:
    """Combines Machine Learning prediction and OWL Ontology reasoning."""

    def __init__(self, ml_weight: float = 0.55, ontology_weight: float = 0.45):
        self.ml_weight = ml_weight
        self.ontology_weight = ontology_weight
        self.predictor = ProfilePredictor()
        self.reasoner = OntologyReasoner()

    def set_weights(self, ml_weight: float, ontology_weight: float):
        total = ml_weight + ontology_weight
        if total > 0:
            self.ml_weight = ml_weight / total
            self.ontology_weight = ontology_weight / total

    def detect(self, profile_data: dict, user_settings=None) -> dict:
        """
        Executes unified hybrid detection on a profile.
        Returns complete analysis payload with scores, verdicts, and explanations.
        """
        # Apply custom settings weights if provided
        ml_w = self.ml_weight
        onto_w = self.ontology_weight
        high_thresh = 70.0
        med_thresh = 35.0

        if user_settings:
            ml_w = getattr(user_settings, 'ml_weight', ml_w)
            onto_w = getattr(user_settings, 'ontology_weight', onto_w)
            high_thresh = getattr(user_settings, 'high_risk_threshold', 70.0)
            med_thresh = getattr(user_settings, 'medium_risk_threshold', 35.0)
            total = ml_w + onto_w
            if total > 0:
                ml_w = ml_w / total
                onto_w = onto_w / total

        # 1. Machine Learning Prediction
        ml_result = self.predictor.predict_profile(profile_data)
        ml_fake_prob = ml_result['fake_probability']  # 0.0 to 1.0
        ml_prob_pct = ml_fake_prob * 100.0

        # 2. Ontology Semantic Reasoning
        onto_result = self.reasoner.reason_profile(profile_data)
        onto_risk_score = onto_result['ontology_risk_score']  # 0.0 to 100.0

        # 3. Hybrid Synthesis
        overall_risk = (ml_w * ml_prob_pct) + (onto_w * onto_risk_score)
        overall_risk = round(max(0.0, min(100.0, overall_risk)), 2)

        # 4. Risk Categorization
        if overall_risk >= high_thresh:
            risk_level = "High"
            final_verdict = "Fake Profile"
        elif overall_risk >= med_thresh:
            risk_level = "Medium"
            final_verdict = "Suspicious Profile"
        else:
            risk_level = "Low"
            final_verdict = "Authentic Profile"

        # 5. Explainable AI (XAI) Synthesis
        flagged_reasons = []

        # From ontology
        for rule in onto_result.get('triggered_rules', []):
            flagged_reasons.append(f"[Ontology] {rule['name']}: {rule['description']}")

        # From ML feature extremes
        extracted = ml_result.get('extracted_features', {})
        if extracted.get('follower_following_ratio', 1.0) < 0.05 and extracted.get('following_count', 0) > 300:
            flagged_reasons.append(f"[ML Model] Critical anomaly: Following-to-follower ratio is extremely skewed ({extracted.get('follower_following_ratio')}).")
        if extracted.get('account_age_days', 999) < 14 and extracted.get('following_count', 0) > 200:
            flagged_reasons.append(f"[ML Model] Fresh account warning: High velocity followings in a {extracted.get('account_age_days')} day old profile.")
        if extracted.get('engagement_rate', 5.0) < 0.01 and extracted.get('followers_count', 0) > 5000:
            flagged_reasons.append(f"[ML Model] Engagement divergence: Near-zero interaction despite large audience size.")
        if extracted.get('has_profile_pic', 1.0) == 0.0 and extracted.get('bio_length', 10) == 0:
            flagged_reasons.append("[ML Model] Incomplete profile footprint: Missing avatar and empty biography.")

        # Deduplicate reasons
        clean_reasons = []
        for r in flagged_reasons:
            if r not in clean_reasons:
                clean_reasons.append(r)

        if not clean_reasons:
            explanation_summary = "Account parameters align with natural, organic usage patterns. No severe behavioral red flags were detected."
            clean_reasons.append("Account metrics adhere to baseline organic behavior.")
        else:
            explanation_summary = f"Hybrid detection detected {len(clean_reasons)} anomalous indicators across ML probabilistic analysis and semantic ontological rules."

        return {
            'final_verdict': final_verdict,
            'risk_level': risk_level,
            'overall_risk_score': overall_risk,
            'ml_prediction': ml_result['prediction'],
            'ml_fake_probability': ml_fake_prob,
            'ml_confidence': ml_result['confidence_percentage'],
            'ml_feature_importances': ml_result['feature_importances'],
            'ontology_verdict': onto_result['ontology_verdict'],
            'ontology_risk_score': onto_risk_score,
            'ontology_rules_triggered': onto_result['triggered_rules'],
            'ontology_inferred_classes': onto_result['inferred_classes'],
            'explanation_summary': explanation_summary,
            'flagged_reasons': clean_reasons,
            'extracted_features': extracted,
            'ml_weight_used': round(ml_w, 2),
            'ontology_weight_used': round(onto_w, 2),
        }
