Why This is Perfectly Optimized for Your Constraints
## 1. Natural Index Progression: 

Because the outer loop marches sequentially from row 0 to row M-1, and the inner while loop moves column-by-column from left to right, your coordinates are packed into memory in exact `row-major` ascending order.
## 2. Zero Overhead: 

Saddleback search hops across rows and columns diagonally, forcing you to pay a performance penalty to sort its output at the end. This `Bisect` method preserves the order instantly.