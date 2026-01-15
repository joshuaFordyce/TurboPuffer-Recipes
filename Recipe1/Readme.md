TurboPuffer Recipe 1: Large document Handling & Metadata Filtering

This recipe demonstrates the best practices for ingesting large text documents into TurboPuffer while maintaining high-performance metadata filtering and vector search capabilities

Problem It solves
1. Overcoming Attribute Size Limits
2. Schema Enforcement
3. Hybrid Retrieval

Features
- Blob Stoage Strategy
- Vector embeddings using sentence-transformers

How it works
1. Ingesting with Schema
    - When uploading the data, we calculate the vector and the text size. The schema is explicitly defined to ensure TurboPuffer allocates the correct columnar storage

2. The Search Query
    - The Search functino performs two ops in a single request. It first restricts the search space only to documents where doc_cateogyr == 'Legal' and then it ranks those filtered documents by their proximity to the query vector using the ANN operator

3. Attribute Retrieval
   - The query uses include_attributes to pull the large text blob back form storage only from the top 3 results, saving bandwwidth on non-relevant rows.