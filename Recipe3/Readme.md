TurboPuffer Recipe 3: High-Throughput Parallel Ingestion.

This recipe demonstrates how to maximize ingestion speed using Python's concurrent.futures. By chunking data into batches and utilizing multiple threads, you can significantly reduce the time to populate a namespace

Problems we solve

- Network Latency
- Rsource Utilization
- Concucurrency Management

Features
- Batching Logic
- Threaded Execution
- Vector Sharding Simulation

How it Works

1. The prepare_batches Generator
    This function creates the data payload in memory. It constructs tuples containing IDs, Vectors, and Attributes. 

2. The upload Worker
    This is the function executed by the threads. It maps your local data structure to the TurboPuffer upsert_rwows format and applies the Explicit Schema to ensure columnar consistency

3. Thread Pool Mapping
    The executor.map funciton handles the distribution of batches across the available workers. It ensures that the main script waits until all threads have completed before reporting the final success count.
