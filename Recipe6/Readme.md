TurboPuffer Recipe 6: Weighted BM25 & Field Boosting

This recipe demonstates how to implement Relevance Tuning in TurboPuffer. By applying multipliers to specific document fields, we ensure that identity matches rank higher than contextual matches


Problem it solves

- Search Noise
- Lack of Intent Alignment
- Explainability

Features

Explicitly enables full_text_search: True on string attribtues to activate the BM25 inverted index

Utilize the Sum and Product operators to combine scores from multiple fields

Includes a run_comparison function to show the Before and after effect of applying a 3.0x boost to titles


How it works

1. Enabling the Inverted Index
    - For BM25 to work, the schema must be configured to index the strings for text search: "title": {"type": "string", "full_text_search": True}


2. The Boosting Logic
    - The Rank_by parameter uses a nested loist structure to define the math. The BM25 score calculates the base relevance of teh query for each field. THe product Operator multiplies the title BM25 score byy 3.0 and the Sum Operator adds the boosted title score to the raw description score to get the final $dist

3. Accessing the Computed Score
    - Because the $dist is a computed metadata field to retieve and display the relevance score in the results
    