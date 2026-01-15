TuboPuffer Implementation Recipes

- This repo contains a collection of tested recipes for common production challenges encountered when building with TurboPuffer

Each recipes includes a standalone Python script designed to demonstrate resiliency, scalability and relevance tuning

Table of Contents

1. Resilient Ingestion: Threading,Batching and Retries
2. Large Content Management: Bypassing attribute limits with non-filterable blobs
3. THe partial Upsert pattern: Using explicit schemas to ensure data integrity
4. Weighted Hybrid Search: Boosting BM25 signals for identity-match relevance
5. Multi-Label Filtering: Advanced set-interaction with ContainsAny

Getting Started

1. Clone the repo
````
git clone https://github.com/username/turbopuffer-recipes.git
````

2. Install dependencies

````
pip install turbopuffer sentence-transformers
````

3.Set your API key

````
 export TURBOPUFFER_API_KEY="api_key"
````
