from typing import List, Tuple, Union, Generator, Optional

class MatrixStreamManager:
    """
    Manages high-performance, memory-safe matrix lookups and streaming operations.
    Enforces a zero-allocation workflow designed for hardware-constrained environments.
    """
    def __init__(self, buffer_capacity: int):
        """
        Initializes the streaming manager with a static, pre-allocated memory buffer.
        """
        if buffer_capacity <= 0:
            raise ValueError("Buffer capacity must be a positive integer.")
        self.capacity = buffer_capacity
        # Allocate static memory footprint once during initialization
        self.buffer: List[Optional[Tuple[int, int]]] = [None] * buffer_capacity

    def yield_saddleback_safe(
        self, 
        matrix: Optional[List[List[Union[int, float, str]]]], 
        target: Union[int, float, str]
    ) -> Generator[Tuple[int, int], None, None]:
        """
        A highly robust Saddleback Search generator.
        Dynamically handles empty matrices and malformed non-rectangular rows
        without allocating any temporary tracking lists.
        
        Time Complexity: O(M + N + K) average case.
        Space Complexity: O(1) absolute constant auxiliary space.
        """
        # Rule 1: Handle completely empty matrices or invalid matrix roots safely
        if not matrix or not matrix[0]:
            return

        num_rows = len(matrix)
        
        row = 0
        # Initialize column pointer based on the first row's width
        col = len(matrix[0]) - 1
        
        while row < num_rows and col >= 0:
            current_row = matrix[row]
            
            # Rule 2: Handle malformed row architectures dynamically
            # If a row is shorter than our active column pointer boundary, we cannot look there.
            if current_row is None or len(current_row) <= col:
                # We skip this malformed row safely by advancing downwards
                row += 1
                continue
                
            current_val = current_row[col]
            
            if current_val == target:
                # Target matched. Slide left to sweep the continuous duplicate sequence.
                left_bound = col
                
                # Check bounds and scan adjacent duplicates inside this current row structure
                while left_bound >= 0 and current_row[left_bound] == target:
                    left_bound -= 1
                
                # Yield matched coordinates left-to-right to maintain strict ascending order
                for c in range(left_bound + 1, col + 1):
                    yield (row, c)
                    
                # Pivot pointers down and adjust left boundary for the next cycle
                row += 1
                col = left_bound
                
            elif current_val > target:
                col -= 1  # Target is smaller; eliminate this column trajectory
            else:
                row += 1  # Target is larger; eliminate this row trajectory

    def sync_to_buffer(
        self, 
        matrix: Optional[List[List[Union[int, float, str]]]], 
        target: Union[int, float, str],
        truncate_unused: bool = True
    ) -> int:
        """
        Consumes the streaming coordinate generator and directly overrides 
        the internal pre-allocated buffer array in-place.
        
        Returns:
            int: The absolute number of targets written to the structural buffer.
        """
        write_index = 0
        
        # Pull items directly out of the pipeline into our fixed memory slots
        for coordinate in self.yield_saddleback_safe(matrix, target):
            if write_index >= self.capacity:
                raise MemoryError(
                    f"Buffer Overflow: Total matched items exceeded pre-allocated "
                    f"capacity bounds ({self.capacity} slots)."
                )
            
            self.buffer[write_index] = coordinate
            write_index += 1
            
        # Clean up any residual data in trailing buffer slots in-place
        if truncate_unused and write_index < self.capacity:
            for idx in range(write_index, self.capacity):
                self.buffer[idx] = None
                
        return write_index


# =====================================================================
# Execution & Verification (Simulating Heavy Structural Chaos)
# =====================================================================
if __name__ == "__main__":
    
    # Instantiate the streaming manager with a fixed memory footprint limit
    manager = MatrixStreamManager(buffer_capacity=10)
    
    print("--- Case 1: Processing a Malformed Non-Rectangular Matrix ---")
    # Row 1 has 5 cols, Row 2 has 2 cols (malformed!), Row 3 has 4 cols.
    malformed_matrix = [
        ['A', 'B', 'C', 'C', 'E'],
        ['B', 'C'],                  # <- Malformed missing column data block
        ['C', 'C', 'D', 'E'],
        ['D', 'E', 'F', 'G']
    ]
    
    found_count = manager.sync_to_buffer(malformed_matrix, target='C')
    print(f"Total elements synced: {found_count}")
    print(f"Buffer State: {manager.buffer}\n")
    
    
    print("--- Case 2: Processing Completely Empty Matrices Safely ---")
    empty_matrix_a = []
    empty_matrix_b = [[]]
    
    count_a = manager.sync_to_buffer(empty_matrix_a, target=42)
    count_b = manager.sync_to_buffer(empty_matrix_b, target='Z')
    
    print(f"Empty Matrix A matches: {count_a} | Buffer: {manager.buffer[:3]}")
    print(f"Empty Matrix B matches: {count_b} | Buffer: {manager.buffer[:3]}")
