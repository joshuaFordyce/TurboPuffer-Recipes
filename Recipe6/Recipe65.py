import os
import turbopuffer
from sentence_transformers import SentenceTransformer


os.environ["TOKENIZERS_PARALLELISM"] = "false"
model = SentenceTransformer('all-MiniLM-L6-v2')
tpuf = turbopuffer.Turbopuffer(
    api_key="tpuf_zPDvexzzKn0cfGh3eUNJbw0YgVHQFFg9",
    region="gcp-us-central1"
)
ns = tpuf.namespace(f'main-py')
def run_comparison(query_text):
    print(f"\n--- Comparison for Query: '{query_text}' ---")

    # 1. Standard Query (No Boost)
    # We use Sum but give both fields a 1.0 multiplier (or just list them)
    standard_results = ns.query(
        rank_by=['Sum', [
            ['title', 'BM25', query_text],
            ['description', 'BM25', query_text]
        ]],
        top_k=2,
        include_attributes=['title','description']
    )

    print("\n[STANDARD RESULTS - No Boost]")
    for i, row in enumerate(standard_results.rows):
        print(f"{i+1}. {row.title} (Score: {getattr(row, '$dist'):.4f})")

    # 2. Boosted Query (3x Title Boost)
    boosted_results = ns.query(
        rank_by=['Sum', [
            ['Product', 3.0, ['title', 'BM25', query_text]],
            ['description', 'BM25', query_text]
        ]],
        top_k=2,
        include_attributes=['title','description']
    )

    print("\n[BOOSTED RESULTS - 3x Title Boost]")
    for i, row in enumerate(boosted_results.rows):
        print(f"{i+1}. {row.title} (Score: {getattr(row, '$dist'):.4f})")

if __name__ == "__main__":
    run_comparison("Bose wireless")