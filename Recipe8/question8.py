import os
import turbopuffer
from sentence_transformers import SentenceTransformer
import time

os.environ["TOKENIZERS_PARALLELISM"] = "false"
model = SentenceTransformer('all-MiniLM-L6-v2')
tpuf = turbopuffer.Turbopuffer(
    api_key="",
    region="gcp-us-central1"
)

dummy_vector = [0.0] * 384
ns = tpuf.namespace(f'main-py')

def test_partial_update():
    # Define the schema ONCE so we can reuse it
    my_schema = {
        "status": {"type": "string", "filterable": True},
        "priority": {"type": "string", "filterable": True},
        "metadata": {"type": "string", "filterable": False}
    }

    print("Step 1: Creating initial record...")
    ns.write(
        upsert_rows=[{
            "id": 500,
            "vector": [0.1] * 384,
            "status": "pending",
            "priority": "high",
            "metadata": "initial_data"
        }],
        schema=my_schema # Established here
    )

    print("\nStep 2: Performing partial upsert (No priority sent)...")
    ns.write(
        upsert_rows=[{
            "id": 500,
            "vector": [0.1] * 384,
            "status": "processed",
            "priority":"low" 
        }],
        schema=my_schema # Re-confirmed here
    )

    # No sleep needed! Explicit schemas allow for faster resolution
    res_updated = ns.query(
        filters=["id", "Eq", 500],
        top_k=1,
        include_attributes=["status", "priority"]
    )
    
    row = res_updated.rows[0]
    # Use getattr just in case, but with the schema fixed, it should be there!
    print(f"Verified Intact: Priority is '{getattr(row, 'priority', 'Not Found')}'")
    print(f"Updated State: {row.status}")

if __name__ == "__main__":
    test_partial_update()
