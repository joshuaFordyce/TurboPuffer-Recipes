TurboPuffer Recipe 8: Partial Upserts & Attribute Merging

This recipe demonstrates the Sticke note analogy of database updates. Instea od trditional SQL UPDATE WHERE statements, TurboPuffer uses an ID-based Upsert pattern that allows yout o modify specific attributes of a record while keeping others intact

Problem it solves

- Redundant Data Transfer

- Attribute Loss

- Consistency Management

Features

- Demonstrates changing a status from pending to processed without needing to re-fetch the original doc

- By defining my_schema in every writ call, we'll tell the engine exactly which fields to strack, esnurign that priority remains retrievable even when not included in a specific batch


How it works

1. The columnar Append Strategy
    - When you preform an upsert, the engine doesnt rewrite an old file. It instead appends a new version of that attritbute and when we go to query, th eengine resovles the most recent value for each column

2. The Importance of Schema=
    - If we omit the schema in the scond ns.write, the engine might infer that the record only consists of the status field. BY re-passing the schema, you maintain, the contract that the record still posesses a priority and metadata column

3. Last Write Win

    - In the second step of this script, we explicitly update priority from "high" to "low", This demonstrates that if the same field is provided in a subsequent upsert, the new value overwrites the old one for that specific ID