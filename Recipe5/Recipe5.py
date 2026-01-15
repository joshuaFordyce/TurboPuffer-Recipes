import os
import turbopuffer
from sentence_transformers import SentenceTransformer
import numpy as np
#import concurrent.futures

os.environ["TOKENIZERS_PARALLELISM"] = "false"
model = SentenceTransformer('all-MiniLM-L6-v2')
tpuf = turbopuffer.Turbopuffer(
    api_key="tpuf_zPDvexzzKn0cfGh3eUNJbw0YgVHQFFg9",
    region="gcp-us-central1"
)


ns = tpuf.namespace(f'main-py')

def setup_tag_data():
    print("Ingesting tagged data...")
    ns.write(
        upsert_rows=[
            {
                'id': 201,
                'vector': [0.1] * 384,
                'doc_category': 'Legal',
                'tags': ['urgent', 'contract'] # Multiple tags
            },
            {
                'id': 202,
                'vector': [0.2] * 384,
                'doc_category': 'Finance',
                'tags': ['review', 'invoice'] # Multiple tags
            },
            {
                'id': 203,
                'vector': [0.3] * 384,
                'doc_category': 'Legal',
                'tags': ['draft', 'internal'] # None of the target tags
            }
        ],
        schema={
            "tags": {"type": "[]string", "filterable": True} # Note the []string type
        }
    )

def test_contains_any():
    print("\nRunning ContainsAny Query for ['urgent', 'review']...")
    # This should return IDs 201 and 202, but NOT 203
    vector = [0.1] * 384
    results = ns.query(
        
        rank_by=("vector", "ANN",vector),
        filters={
            "tags": ["ContainsAny", ["urgent", "review"]]
        },
        top_k=5,
        include_attributes=["tags", "doc_category"]
    )
    
    for row in results.rows:
        print(f"Found ID: {row.id} | Tags: {row.tags}")

if __name__ == "__main__":
    setup_tag_data()
    test_contains_any()