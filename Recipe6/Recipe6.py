import os
import turbopuffer
from sentence_transformers import SentenceTransformer


os.environ["TOKENIZERS_PARALLELISM"] = "false"
model = SentenceTransformer('all-MiniLM-L6-v2')
tpuf = turbopuffer.Turbopuffer(
    api_key="tpuf_zPDvexzzKn0cfGh3eUNJbw0YgVHQFFg9",
    region="gcp-us-central1"
)

dummy_vector = [0.0] * 384
ns = tpuf.namespace(f'main-py')
ns.write(
    upsert_rows=[
        {
            "id": 1,
            "vector": dummy_vector,
            "title": "Bose QuietComfort Wireless", 
            "description": "Premium noise cancelling headphones with long battery life."
        },
        {
            "id": 2, 
            "vector": dummy_vector,
            "title": "Wireless Audio Pro", 
            "description": "These Bose compatible headphones offer great sound."
        }
    ],
    schema={
        "title": {"type": "string", "full_text_search": True},
        "description": {"type": "string", "full_text_search": True}
    }
)

# 3. Define the Weighted Query
# We give the 'title' field a 3.0x boost relative to the 'description'
query_text = "Bose wireless"

print(f"\nSearching for: '{query_text}' with 3x Title Boost...")
results = ns.query(
    rank_by=['Sum', [
        ['Product', 3.0, ['title', 'BM25', query_text]],
        ['description', 'BM25', query_text]
    ]],
    top_k=2,
    include_attributes=['title', 'description']
)

# 4. Display Results
print(results.rows)

for i, row in enumerate(results.rows):
    score = getattr(row, '$dist')
    print(f"Rank {i+1}: {row.title} (Score: {score})")