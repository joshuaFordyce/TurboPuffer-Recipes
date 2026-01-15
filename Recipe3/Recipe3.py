import os
import turbopuffer
from sentence_transformers import SentenceTransformer
import numpy as np
import concurrent.futures

os.environ["TOKENIZERS_PARALLELISM"] = "false"
model = SentenceTransformer('all-MiniLM-L6-v2')
tpuf = turbopuffer.Turbopuffer(
    api_key="",
    region="gcp-us-central1"
)


ns = tpuf.namespace(f'main-py')


def upload(batch_data):
    ids, vectors, attributes = batch_data

    rows_to_upsert = []
    for i in range(len(ids)):
        rows_to_upsert.append({
            'id': ids[i],
            'vector': vectors[i],
            'doc_category': attributes['status'][i],
            'large_content_blob': "some text",
            'text_size': 100

        })
    try:
        ns.write(
            upsert_rows=rows_to_upsert,
            schema={
                "doc_category": {"type": "string", "filterable": True},
                "large_content_blob": {"type": "string", "filterable": False},
                "text_size": {"type": "int", "filterable": True}

            }
        )
        return len(ids)
    except Exception as e:
        print(f"Batch failed: {e}")
        return 0
    
        

    
def prepare_batches(total_docs, batch_size):

    batches = []
    for i in range(0, total_docs, batch_size):

        current_size = min(batch_size, total_docs - i)

        batchingIds = list(range(i, i + current_size))

        batch_vectors = np.random.rand(current_size, 384).tolist()

        batch_attributes = {
            "status": ["active"] * current_size,
            "shard_id": [i // batch_size] * current_size
        }
        batches.append((batchingIds, batch_vectors, batch_attributes))
        
    return batches

#RELEVANT DOCS: https://turbopuffer.com/docs/write

if __name__ == "__main__":
    TOTAL_DOCS = 100
    BATCH_SIZE = 25

    print("Preparing {TOTAL_DOCS} documents in batches of {BATCH_SIZE}...")
    work_batches = prepare_batches(TOTAL_DOCS, BATCH_SIZE)

    print("Starting parallel upload...")

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(upload, work_batches))

    total_success = sum(results)
    print(f"Successfully uploaded {total_success}/{TOTAL_DOCS} documents")
