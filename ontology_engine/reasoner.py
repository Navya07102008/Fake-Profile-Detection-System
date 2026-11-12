from rdflib import RDF, RDFS, OWL, URIRef, Literal
from ontology_engine.ontology_loader import OntologyLoader, FPO
from ontology_engine.profile_mapper import ProfileMapper
from ontology_engine.rule_engine import SemanticRuleEngine


class OntologyReasoner:
    """Orchestrates ontology loading, profile mapping, and semantic inference."""

    def __init__(self):
        self.loader = OntologyLoader()
        self.mapper = ProfileMapper()
        self.rule_engine = SemanticRuleEngine()

    def reason_profile(self, profile_data: dict) -> dict:
        """
        Executes semantic reasoning on a single profile.
        Returns:
            - ontology_risk_score (0.0 to 100.0)
            - ontology_verdict (str)
            - triggered_rules (list of dicts)
            - inferred_classes (list of strings)
            - semantic_explanation (str)
            - triples_count (int)
        """
        # 1. Evaluate semantic forensic rules
        rule_results = self.rule_engine.evaluate_rules(profile_data)

        # 2. Map profile to dynamic RDF graph
        base_graph = self.loader.get_graph()
        # Create a working copy for this inference to avoid graph pollution
        profile_graph, profile_uri = self.mapper.map_profile_to_graph(profile_data)

        # 3. Add inferred classes and rule violations to profile graph
        for class_name in rule_results["inferred_classes"]:
            profile_graph.add((profile_uri, RDF.type, FPO[class_name]))

        for rule in rule_results["triggered_rules"]:
            rule_uri = FPO[rule["rule_id"]]
            profile_graph.add((profile_uri, FPO.violatesRule, rule_uri))

        profile_graph.add((profile_uri, FPO.hasRiskCategory, FPO[rule_results["risk_category"]]))
        profile_graph.add((profile_uri, FPO.hasSuspicionScore, Literal(rule_results["risk_score"])))

        # Format semantic verdict and explanation
        risk_score = rule_results["risk_score"]
        if risk_score >= 70:
            ontology_verdict = "High Risk - Fake / Bot Candidate"
        elif risk_score >= 35:
            ontology_verdict = "Medium Risk - Suspicious Account"
        else:
            ontology_verdict = "Low Risk - Authentic Account"

        if rule_results["triggered_rules"]:
            rules_summary = "; ".join([f"{r['name']} ({r['severity']})" for r in rule_results["triggered_rules"]])
            semantic_explanation = f"Semantic reasoning triggered {len(rule_results['triggered_rules'])} ontology rules: {rules_summary}."
        else:
            semantic_explanation = "Profile characteristics align with normal organic user activity. No violation rules triggered."

        return {
            "ontology_risk_score": risk_score,
            "ontology_verdict": ontology_verdict,
            "risk_category": rule_results["risk_category"],
            "triggered_rules": rule_results["triggered_rules"],
            "inferred_classes": rule_results["inferred_classes"],
            "semantic_explanation": semantic_explanation,
            "rdf_triples_generated": len(profile_graph),
        }
