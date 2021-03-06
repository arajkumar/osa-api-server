"""Abstracts data ingestion to graph db"""

from src.graph_traversel import Traversel
from src.ingestion_data import IngestionData
from src.gremlin import execute_query

def _ingest_pcve(pcve):
    g = Traversel() # pylint: disable=invalid-name
    query = str(g.add_unique_node(pcve.dependency)
                .add_unique_node(pcve.version)
                .add_unique_node(pcve.security_event)
                .add_unique_node(pcve.probable_cve)
                .has_version(pcve.dependency, pcve.version)
                .triaged_to(pcve.security_event, pcve.probable_cve)
                .affects(pcve.probable_cve, pcve.version)
                .next())
    return execute_query(query)

def ingest_data_into_graph(data):
    """Ingests given json object to graph"""
    for pcve in data:
        _ingest_pcve(IngestionData(pcve))
    return {'status': 'success'}
