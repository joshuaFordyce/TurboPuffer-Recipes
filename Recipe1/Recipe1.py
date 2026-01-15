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

def ingest_large_document(doc_id, large_text, category):


    vector = model.encode(large_text).tolist()



    ns.write(



    upsert_rows = [

    {

        'id': int(doc_id),

        'vector': vector,

        'doc_category': category,

        'large_content_blob': large_text,

        'text_size': len(large_text)

    }



    ],

    schema={

    "doc_category": {"type": "string", "filterable": True},

    "large_content_blob": {"type": "string", "filterable": False},

    "text_size": {"type": "int", "filterable": True}

    }

)



def search(query, category_filter):

    query_vector = model.encode(query).tolist()

    return ns.query (

    rank_by=("vector", "ANN", query_vector),

    filters={"doc_category": ["Eq", category_filter]},

    top_k=3,

    include_attributes=["large_content_blob", "doc_category"]

    )





if __name__ == "__main__":



    small_text = "standard legal text"

    print("Testing with small ingestion...")

    ingest_large_document(100, small_text, "Legal")





    fake_large_text = "Important legal clause. " * 500

    print(f"Ingesting large doc with {len(fake_large_text)} characters")



    ingest_large_document(101, fake_large_text, "Legal")



    results = search("legal clause", "Legal")



    print(results)
#for row in results:

# print(f"ID: {[0]}, doc_category: {row.attributes['doc_category']}")

# print(f"Content Preview: { row.attributes['Large_content_blog'][:50]}")


# The 'results' object is a NamespaceQueryResponse

    for row in results.rows:

# row is a NamedTuple, so we use dot notation

        print(f"--- Document ID: {row.id} ---")

        print(f"Category: {row.doc_category}")

# We use .get() or direct access if we're sure it exists

        content = getattr(row, 'large_content_blob', 'No content')

        print(f"Snippet: {content[:100]}...")

        print("\n")

