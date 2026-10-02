def yield_all_saddleback_strict(matrix, target):
    """
    Yields matching coordinates one-by-one in strict ascending order.
    Consumes O(1) auxiliary memory. Perfect for hyper-constrained environments
    processing massive Cluster-Data or Scattered Lines.
    
    Time Complexity: O(M + N + K)
    Space Complexity: O(1) absolute constant space.
    """
    if not matrix or not matrix[0]:
        return
        
    num_rows = len(matrix)
    num_cols = len(matrix[0])
    
    row = 0
    col = num_cols - 1
    
    while row < num_rows and col >= 0:
        current_val = matrix[row][col]
        
        if current_val == target:
            # Find the leftmost boundary of the duplicate streak
            left_bound = col
            while left_bound >= 0 and matrix[row][left_bound] == target:
                left_bound -= 1
            
            # Yield coordinates from left to right to guarantee ascending order
            for c in range(left_bound + 1, col + 1):
                yield (row, c)
                
            # Advance to the next row and adjust the column boundary
            row += 1
            col = left_bound
            
        elif current_val > target:
            col -= 1
        else:
            row += 1
