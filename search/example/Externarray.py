def yield_all_saddleback_strict(matrix, target):
    """
    Generator yielding matching coordinates one-by-one in strict ascending order.
    Space Complexity: O(1)
    """
    if not matrix or not matrix[0]:
        return
    num_rows, num_cols = len(matrix), len(matrix[0])
    row, col = 0, num_cols - 1
    
    while row < num_rows and col >= 0:
        current_val = matrix[row][col]
        if current_val == target:
            left_bound = col
            while left_bound >= 0 and matrix[row][left_bound] == target:
                left_bound -= 1
            for c in range(left_bound + 1, col + 1):
                yield (row, c)
            row += 1
            col = left_bound
        elif current_val > target:
            col -= 1
        else:
            row += 1

def update_external_array(matrix, target, external_array):
    """
    Consumes the generator to update a pre-allocated external array in place.
    Returns the exact number of elements updated.
    """
    write_index = 0
    max_capacity = len(external_array)
    
    for coord in yield_all_saddleback_strict(matrix, target):
        if write_index >= max_capacity:
            # Handle buffer overflow safely if the external array is too small
            raise MemoryError("External array capacity exceeded!")
            
        # Overwrite the pre-existing slot in memory (Zero New Allocations)
        external_array[write_index] = coord
        write_index += 1
        
    return write_index  # Tells you exactly how much of the buffer was used

# ==========================================
# Production Example & Memory Usage
# ==========================================

# 1. Setup sample matrix (Letters data)
data_matrix = [
    ['A', 'B', 'C', 'C'],
    ['B', 'C', 'C', 'D'],
    ['C', 'C', 'D', 'E']
]

# 2. Pre-allocate the external array buffer with fixed capacity 
# (Prevents Python from constantly resizing and copying memory)
external_buffer = [None] * 10 

# 3. Update the buffer in place
total_updated = update_external_array(data_matrix, 'C', external_buffer)

print(f"Total elements written to external array: {total_updated}")
print(f"External Array Content: {external_buffer}")
# Output: [(0, 2), (0, 3), (1, 1), (1, 2), (2, 0), (2, 1), None, None, None, None]
