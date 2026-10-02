# Converting the function into a Python Generator using the yield keyword provides the ultimate memory optimization.
Instead of building and storing a massive list of coordinates in memory, it
 processes elements one at a time as they are found. This drops the auxiliary space complexity to absolute `O(1)`\(\mathcal{O}(1)\) constant memory, regardless of whether you have 10 matches or 10 million matches.

# Why This Protects Your Memory Limits
## 1. Zero Garbage Collection Spikes: 

Because external_buffer is allocated once at startup, Python never has to search for new free blocks of memory or clean up discarded sub-arrays during the search process.

## 2. Predictable Memory Footprint: 

You set the absolute maximum size of your coordinate buffer up front. If a massive Cluster-Data set arrives that exceeds your device's limits, the MemoryError safeguard triggers immediately before the system crashes.

## 3. Data Agnostic: The generator feeds pure tuple structures (row, col) forward, meaning it performs identically whether the underlying matrix cells are processing strings, floats, or large integers.