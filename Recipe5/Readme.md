TurboPuffer Recipe 5: Multi-Label Filtering iwth ContainsAny

This recipe demonstrates how to handle multi-label metadata and perform efficient queries. This is essential for applications like ecommerce, content management and legal tech

Problems to solve

- Tradition filers often struggle with Or logic. Using Contains Any allows yout o pass a list of target values ina single, high performance operation.

- Demonstrates how to properly define and query attributes that contain multiple values per row

- Shows how to combine specific tag requirements with semantic vector search


Features

- Utilizes the []string type definition, which tells TurboPuffer to treat the attribute as a colleciton of individual tokens rather than a single long string.

- Scans the inverted index to find docs containing at least one of the specified query tags

- Ensures the tags field is marked as filterable: True to enable rapid retrieval during the query phase

How it WOrks

1. Defining the Array Schema

    - In the setup_tag_data function, the schema is defined as: "tags": {"type": "[]string", "filterable": True}. The [] prefix is critical as it signals that each doc can have a list of vals for this attribute. This allows the vector database to index each tag individually

2. The ContainsAny Filter
    - We pass a list of targets to the engine and TurboPuffer's engine performs a "union of intersections" and this finds all docs possessing "urgent' and all docs possesing "reviews". Once this is done, it merges them before ranking by the vector similarility

3. Combining with Vector Search

    - Even though we are filtering by tags, we still want to provide a rank_by vector since this lets us sort how semantically relevant the docs are to our query vector



