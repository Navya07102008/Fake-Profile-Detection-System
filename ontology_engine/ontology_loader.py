import os
from pathlib import Path
from rdflib import Graph, Namespace, RDF, RDFS, OWL

BASE_DIR = Path(__file__).resolve().parent.parent
ONTOLOGY_PATH = BASE_DIR / 'ontology' / 'fake_profile_ontology.owl'
FPO = Namespace("http://www.semanticweb.org/ontologies/fake_profile_ontology#")


class OntologyLoader:
    """Loads and queries the OWL/RDF Fake Profile Detection Ontology."""

    _instance = None
    _graph = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(OntologyLoader, cls).__new__(cls)
            cls._instance._load_graph()
        return cls._instance

    def _load_graph(self):
        self._graph = Graph()
        if ONTOLOGY_PATH.exists():
            try:
                self._graph.parse(str(ONTOLOGY_PATH), format="xml")
            except Exception as e:
                # If XML parser fails, try turtle or create minimal fallback graph
                pass
        self._graph.bind("fpo", FPO)
        self._graph.bind("owl", OWL)
        self._graph.bind("rdfs", RDFS)

    def get_graph(self) -> Graph:
        """Returns the underlying RDFLib graph."""
        if self._graph is None:
            self._load_graph()
        return self._graph

    def get_ontology_stats(self) -> dict:
        """Returns summary statistics of the loaded ontology."""
        g = self.get_graph()
        classes = list(g.subjects(RDF.type, OWL.Class))
        obj_props = list(g.subjects(RDF.type, OWL.ObjectProperty))
        data_props = list(g.subjects(RDF.type, OWL.DatatypeProperty))
        individuals = list(g.subjects(RDF.type, OWL.NamedIndividual))

        return {
            "total_triples": len(g),
            "classes_count": len(classes),
            "object_properties_count": len(obj_props),
            "datatype_properties_count": len(data_props),
            "named_individuals_count": len(individuals),
            "ontology_uri": str(FPO),
        }

    def execute_sparql(self, query: str):
        """Executes a SPARQL query against the ontology graph."""
        return self.get_graph().query(query)
