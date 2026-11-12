import unittest
from ontology_engine.ontology_loader import OntologyLoader
from ontology_engine.profile_mapper import ProfileMapper
from ontology_engine.rule_engine import SemanticRuleEngine
from ontology_engine.reasoner import OntologyReasoner


class TestOntologyEngine(unittest.TestCase):
    """Unit tests for OWL ontology loading, mapping, and semantic reasoning."""

    def setUp(self):
        self.loader = OntologyLoader()
        self.mapper = ProfileMapper()
        self.rule_engine = SemanticRuleEngine()
        self.reasoner = OntologyReasoner()

    def test_ontology_loads_triples(self):
        stats = self.loader.get_ontology_stats()
        self.assertGreater(stats['total_triples'], 0)
        self.assertGreaterEqual(stats['classes_count'], 5)

    def test_spambot_triggers_ontology_rules(self):
        bot_data = {
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
        res = self.rule_engine.evaluate_rules(bot_data)
        self.assertGreaterEqual(res['risk_score'], 70.0)
        self.assertEqual(res['risk_category'], 'HighRisk')
        self.assertIn('BotSpammerProfile', res['inferred_classes'])

        rule_ids = [r['rule_id'] for r in res['triggered_rules']]
        self.assertIn('Rule_FollowerAsymmetry', rule_ids)
        self.assertIn('Rule_HyperactiveNewAccount', rule_ids)

    def test_authentic_profile_low_risk(self):
        authentic_data = {
            'username': 'dr_elena_official',
            'followers_count': 50000,
            'following_count': 600,
            'posts_count': 800,
            'account_age_days': 1500,
            'bio_length': 120,
            'has_profile_pic': True,
            'is_verified': True,
            'avg_likes': 1200.0,
            'avg_comments': 150.0,
        }
        res = self.rule_engine.evaluate_rules(authentic_data)
        self.assertLess(res['risk_score'], 35.0)
        self.assertEqual(res['risk_category'], 'LowRisk')

    def test_reasoner_pipeline(self):
        profile = {
            'username': 'ghost_user',
            'followers_count': 5,
            'following_count': 300,
            'posts_count': 0,
            'account_age_days': 300,
            'bio_length': 0,
            'has_profile_pic': False,
            'is_verified': False,
        }
        out = self.reasoner.reason_profile(profile)
        self.assertIn('ontology_risk_score', out)
        self.assertIn('ontology_verdict', out)
        self.assertIn('inferred_classes', out)


if __name__ == '__main__':
    unittest.main()
