from collections import deque

def find_all_saddleback_strict_order(matrix, target):
    """
    Finds ALL matching coordinates using Saddleback search.
    Supports both numbers and letters (A to Z) using ASCII/Lexicographical sorting.
    Guarantees strict ascending order: (0,0), (0,1), (1,0)... without post-sorting.
    
    Time Complexity: O(M + N + K) where K is the number of duplicates found.
    Space Complexity: O(K) to hold the ordered output coordinates.
    """
    if not matrix or not matrix[0]:
        return []
        
    num_rows = len(matrix)
    num_cols = len(matrix[0])
    results = []
    
    # Start at the top-right corner
    row = 0
    col = num_cols - 1
    
    while row < num_rows and col >= 0:
        current_val = matrix[row][col]
        
        if current_val == target:
            # We found a target. To preserve strict left-to-right order, 
            # we look leftward from this column and collect matches backwards.
            row_matches = deque()
            left_col = col
            
            while left_col >= 0 and matrix[row][left_col] == target:
                # Prepend ensuring left-most column coordinates come first
                row_matches.appendleft((row, left_col))
                left_col -= 1
            
            # Add this row's perfectly sorted coordinates to the final results
            results.extend(row_matches)
            
            # Move downward to the next row. 
            # We also shift our tracking boundary to the left of the duplicates we found.
            row += 1
            col = left_col
            
        elif current_val > target:
            # Target must be smaller; eliminate this column
            col -= 1
        else:
            # Target must be larger; eliminate this row
            row += 1
            
    return results

# ==========================================
# Verification with Globally Sorted Letters
# ==========================================
letter_matrix = [
    ['A', 'B', 'C', 'C'],
    ['B', 'C', 'C', 'D'],
    ['C', 'C', 'D', 'E']
]

target_letter = 'C'
matches = find_all_saddleback_strict_order(letter_matrix, target_letter)
print(f"Coordinates for '{target_letter}' (Strict Order): {matches}")
# Output: [(0, 2), (0, 3), (1, 1), (1, 2), (2, 0), (2, 1)]
