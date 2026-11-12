from rdflib import Graph, Namespace, URIRef, Literal, RDF, XSD
from ontology_engine.ontology_loader import FPO


class ProfileMapper:
    """Maps dynamic social media profile dictionaries to RDF triples."""

    def __init__(self, base_graph: Graph = None):
        self.fpo = FPO
        self.base_graph = base_graph

    def map_profile_to_graph(self, profile_data: dict, graph: Graph = None) -> tuple[Graph, URIRef]:
        """
        Creates an RDF representation of a social media profile.
        Returns a tuple of (Graph, profile_uri).
        """
        g = Graph() if graph is None else graph
        g.bind("fpo", self.fpo)

        username = str(profile_data.get("username", "anonymous_user")).strip()
        safe_username = "".join(c if c.isalnum() or c == "_" else "_" for c in username)
        profile_uri = URIRef(self.fpo[f"Profile_{safe_username}"])

        # Base type assertion
        g.add((profile_uri, RDF.type, self.fpo.SocialMediaProfile))

        # Datatype property assertions
        followers = int(profile_data.get("followers_count", 0))
        following = int(profile_data.get("following_count", 0))
        posts = int(profile_data.get("posts_count", 0))
        age = int(profile_data.get("account_age_days", 0))
        bio_len = int(profile_data.get("bio_length", 0))
        has_pic = bool(profile_data.get("has_profile_pic", False))
        is_verified = bool(profile_data.get("is_verified", False))

        # Ratios
        follower_ratio = followers / (following + 1)
        avg_likes = float(profile_data.get("avg_likes", 0.0))
        avg_comments = float(profile_data.get("avg_comments", 0.0))
        engagement = ((avg_likes + avg_comments) / (followers + 1)) * 100

        g.add((profile_uri, self.fpo.hasUsername, Literal(username, datatype=XSD.string)))
        g.add((profile_uri, self.fpo.hasFollowersCount, Literal(followers, datatype=XSD.integer)))
        g.add((profile_uri, self.fpo.hasFollowingCount, Literal(following, datatype=XSD.integer)))
        g.add((profile_uri, self.fpo.hasPostsCount, Literal(posts, datatype=XSD.integer)))
        g.add((profile_uri, self.fpo.hasAccountAgeDays, Literal(age, datatype=XSD.integer)))
        g.add((profile_uri, self.fpo.hasBioLength, Literal(bio_len, datatype=XSD.integer)))
        g.add((profile_uri, self.fpo.hasProfilePicture, Literal(has_pic, datatype=XSD.boolean)))
        g.add((profile_uri, self.fpo.isVerified, Literal(is_verified, datatype=XSD.boolean)))
        g.add((profile_uri, self.fpo.hasFollowerRatio, Literal(round(follower_ratio, 4), datatype=XSD.float)))
        g.add((profile_uri, self.fpo.hasEngagementRate, Literal(round(engagement, 4), datatype=XSD.float)))

        return g, profile_uri
