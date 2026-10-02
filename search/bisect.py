import bisect

def find_all_coordinates_strict_order(matrix, target):
    """
    Finds ALL matching coordinates of a target (Numbers or Letters).
    Guarantees a strict, ascending coordinate order: (0,0), (0,1), (1,0)...
    Time Complexity: O(M log N + K) where K is number of matches.
    Space Complexity: O(1) auxiliary memory.
    """
    results = []
    
    for row_index, row in enumerate(matrix):
        # Binary search works out-of-the-box for strings/letters too!
        col_index = bisect.bisect_left(row, target)
        
        # Scan left-to-right for duplicates within this row
        while col_index < len(row) and row[col_index] == target:
            # Naturally appends in perfect row-major ascending order
            results.append((row_index, col_index))
            col_index += 1  
            
    return results

# ==========================================
# Verification with Letters (A to Z)
# ==========================================
letter_matrix = [
    ['A', 'B', 'C', 'C'],
    ['B', 'C', 'C', 'D'],
    ['C', 'C', 'D', 'E']
]

target_letter = 'C'
matches = find_all_coordinates_strict_order(letter_matrix, target_letter)
print(f"Coordinates for '{target_letter}': {matches}")
