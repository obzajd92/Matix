import sys
from typing import List, Tuple, Union, Generator

def yield_saddleback_coordinates(
    matrix: List[List[Union[int, float, str]]], 
    target: Union[int, float, str]
) -> Generator[Tuple[int, int], None, None]:
    """
    Generator that yields matching coordinates one-by-one in strict ascending order.
    
    Time Complexity: O(M + N + K) where M=Rows, N=Cols, K=Duplicates
    Space Complexity: O(1) absolute constant auxiliary space
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
            # Locate the leftmost column boundary of this identical sequence
            left_bound = col
            while left_bound >= 0 and matrix[row][left_bound] == target:
                left_bound -= 1
            
            # Yield coordinates from left to right to guarantee ascending row-major order
            for c in range(left_bound + 1, col + 1):
                yield (row, c)
                
            # Move down to next row and limit column boundary to the left of the match cluster
            row += 1
            col = left_bound
            
        elif current_val > target:
            col -= 1  # Target is smaller; discard current column
        else:
            row += 1  # Target is larger; discard current row


def sync_to_external_array(
    matrix: List[List[Union[int, float, str]]], 
    target: Union[int, float, str], 
    external_array: List[Union[Tuple[int, int], None]],
    truncate_unused: bool = True
) -> int:
    """
    Consumes the coordinate stream and overwrites a pre-allocated external array in-place.
    
    Parameters:
        matrix: Globally sorted 2D grid containing numbers or characters.
        target: The value to search for.
        external_array: Pre-allocated array acting as a static memory buffer.
        truncate_unused: If True, fills remaining unused trailing slots with None.
        
    Returns:
        int: The total count of matching coordinates written to the buffer.
    """
    write_index = 0
    max_capacity = len(external_array)
    
    # Process streamed values directly into pre-allocated memory addresses
    for coordinate in yield_saddleback_coordinates(matrix, target):
        if write_index >= max_capacity:
            raise MemoryError(
                f"Buffer Overflow: Found more target matches than pre-allocated "
                f"external capacity ({max_capacity} slots)."
            )
        
        external_array[write_index] = coordinate
        write_index += 1
        
    # In-place clean slicing for trailing data elements
    if truncate_unused and write_index < max_capacity:
        for idx in range(write_index, max_capacity):
            external_array[idx] = None
            
    return write_index


# =====================================================================
# Execution & Verification (Simulating Cluster-Data and Scattered Lines)
# =====================================================================
if __name__ == "__main__":
    
    # Test Scenario A: Processing Letter-Based Grid containing "Cluster-Data"
    char_matrix = [
        ['A', 'B', 'C', 'C', 'E'],
        ['B', 'C', 'C', 'D', 'F'],
        ['C', 'C', 'D', 'E', 'G'],
        ['D', 'E', 'F', 'G', 'H']
    ]
    
    # Pre-allocate a safe fixed-size external buffer array
    # Size calculation based on constraints (e.g., maximum potential grid perimeter)
    pre_allocated_buffer_char = [None] * 12
    
    print("--- Test A: Character Cluster Processing ---")
    target_char = 'C'
    total_chars_found = sync_to_external_array(
        matrix=char_matrix, 
        target=target_char, 
        external_array=pre_allocated_buffer_char
    )
    
    print(f"Target '{target_char}' Elements Tracked: {total_chars_found}")
    print(f"Buffer Output: {pre_allocated_buffer_char}\n")
    
    
    # Test Scenario B: Processing Numeric Matrix with thin "Scattered Lines"
    numeric_matrix = [
        [10, 20, 30, 42],
        [15, 25, 42, 50],
        [22, 42, 55, 60],
        [42, 48, 59, 70]
    ]
    
    pre_allocated_buffer_num = [None] * 8
    
    print("--- Test B: Numeric Scattered Line Processing ---")
    target_num = 42
    total_nums_found = sync_to_external_array(
        matrix=numeric_matrix, 
        target=target_num, 
        external_array=pre_allocated_buffer_num
    )
    
    print(f"Target '{target_num}' Elements Tracked: {total_nums_found}")
    print(f"Buffer Output: {pre_allocated_buffer_num}")
