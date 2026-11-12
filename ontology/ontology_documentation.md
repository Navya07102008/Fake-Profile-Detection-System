# Fake Profile Detection Ontology (FPO) Documentation

## 1. Overview
The **Fake Profile Detection Ontology (FPO)** is an OWL 2 / RDF-XML knowledge representation schema designed to formalize social media account traits, anomalous indicators, risk classifications, and transparent rule-based inferences.

- **Ontology IRI**: `http://www.semanticweb.org/ontologies/fake_profile_ontology#`
- **Prefix**: `fpo:`
- **Format**: W3C OWL 2 RDF/XML (fully Protégé 5.x compatible)

---

## 2. Class Hierarchy
- `SocialMediaProfile`: Top-level concept representing any account entity.
  - `AuthenticProfile`: Human or legitimate verified accounts.
    - `VerifiedAuthorityProfile`: Public figures, verified organizations.
    - `RegularOrganicUser`: Typical personal/professional human profile.
  - `SuspiciousProfile`: Accounts exhibiting behavioral or structural anomalies.
    - `FakeProfile`: Fraudulent or automated accounts.
      - `BotSpammerProfile`: Automated mass follow and spam scripts.
      - `GhostLurkerProfile`: Dormant empty accounts with zero posts.
      - `EngagementAnomalyProfile`: Accounts with purchased fake followers.
- `RiskCategory`:
  - `LowRisk`: Safe account (Risk Score 0 - 34)
  - `MediumRisk`: Suspicious activity detected (Risk Score 35 - 69)
  - `HighRisk`: Critical fake bot indicators (Risk Score 70 - 100)
- `DetectionRule`: Encapsulates explicit semantic heuristics.

---

## 3. Heuristic Rules & Semantic Axioms

| Rule ID | Name | Trigger Condition | Consequence |
|---|---|---|---|
| `Rule_FollowerAsymmetry` | Following Ratio Asymmetry | `following > 500` AND `followers / (following + 1) < 0.05` | Flagged as Bot Indicator (+25 risk) |
| `Rule_GhostLurker` | Dormant Lurker | `account_age > 180` AND `posts == 0` AND `following > 100` | Flagged as Ghost Profile (+20 risk) |
| `Rule_HyperactiveNewAccount` | Fast Bot Accumulation | `account_age <= 14` AND `following > 400` | Flagged as Rapid Mass Spammer (+30 risk) |
| `Rule_NoAvatarEmptyBio` | Anonymous Account | `has_profile_pic == False` AND `bio_length == 0` AND `posts <= 2` | Flagged as Anonymous Ghost (+20 risk) |
| `Rule_EngagementAnomaly` | Follower Farm | `followers > 10,000` AND `engagement_rate < 0.01%` | Flagged as Purchased Audience (+25 risk) |
| `Rule_MachineGeneratedHandle` | Bot Username Pattern | `digit_count / len(username) > 0.40` | Flagged as Scripted Handle (+15 risk) |
| `Rule_AuthenticityMitigation` | Verified Exemption | `is_verified == True` AND `has_profile_pic == True` | Mitigates risk (-35 risk) |

---

## 4. Protégé Integration Instructions
1. Open **Protégé 5.x**.
2. Select **File -> Open...** and navigate to `ontology/fake_profile_ontology.owl`.
3. Switch to the **Entities** tab to inspect the Class hierarchy, Object Properties, and Data Properties.
4. Switch to **Individuals by class** to view `Individual_Elena_AI`, `Individual_Spammer_9921`, and `Individual_Organic_Sarah`.
5. Run the **HermiT** or **Pellet** reasoner to check consistency and classification.
