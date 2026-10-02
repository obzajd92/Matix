from typing import List, Tuple, Union, Generator, Optional

class MatrixStreamManager:
    """
    Manages high-performance matrix streaming operations.
    Supports both strict static buffers and dynamic expansion models.
    """
    def __init__(self, initial_capacity: int, dynamic_resize: bool = False, growth_factor: float = 1.5):
        """
        Initializes the manager.
        
        Parameters:
            initial_capacity: Starting number of coordinate slots.
            dynamic_resize: If True, grows the buffer when full. If False, remains strictly fixed.
            growth_factor: Multiplier used to scale the buffer size during dynamic growth.
        """
        if initial_capacity <= 0:
            raise ValueError("Initial capacity must be a positive integer.")
        if growth_factor <= 1.0 and dynamic_resize:
            raise ValueError("Growth factor must be greater than 1.0 for dynamic resizing.")
            
        self.capacity = initial_capacity
        self.dynamic_resize = dynamic_resize
        self.growth_factor = growth_factor
        
        # Initial memory allocation
        self.buffer: List[Optional[Tuple[int, int]]] = [None] * self.capacity

    def _resize_buffer(self) -> None:
        """
        Handles controlled memory expansion when the tracking buffer fills up.
        """
        new_capacity = int(self.capacity * self.growth_factor)
        # Calculate how many extra slots we need to add to the existing block
        additional_slots = new_capacity - self.capacity
        
        # Extend the buffer in-place to minimize structural fragmentation
        self.buffer.extend([None] * additional_slots)
        self.capacity = new_capacity
        print(f"[Memory Alert] Buffer expanded dynamically to {self.capacity} slots.")

    def yield_saddleback_safe(
        self, 
        matrix: Optional[List[List[Union[int, float, str]]]], 
        target: Union[int, float, str]
    ) -> Generator[Tuple[int, int], None, None]:
        """O(1) Auxiliary space matrix coordinate generator."""
        if not matrix or not matrix:
            return

        num_rows = len(matrix)
        row = 0
        col = len(matrix[0]) - 1 if matrix[0] is not None else -1
        
        while row < num_rows and col >= 0:
            current_row = matrix[row]
            if current_row is None or len(current_row) <= col:
                row += 1
                continue
                
            current_val = current_row[col]
            
            if current_val == target:
                left_bound = col
                while left_bound >= 0 and current_row[left_bound] == target:
                    left_bound -= 1
                
                for c in range(left_bound + 1, col + 1):
                    yield (row, c)
                    
                row += 1
                col = left_bound
            elif current_val > target:
                col -= 1
            else:
                row += 1

    def sync_to_buffer(
        self, 
        matrix: Optional[List[List[Union[int, float, str]]]], 
        target: Union[int, float, str],
        truncate_unused: bool = True
    ) -> int:
        """
        Consumes the streamed items and writes them to the tracking buffer.
        Dynamically resizes or throws error based on class configuration.
        """
        write_index = 0
        
        for coordinate in self.yield_saddleback_safe(matrix, target):
            # Check if we are bumping into the top memory limit
            if write_index >= self.capacity:
                if self.dynamic_resize:
                    self._resize_buffer()
                else:
                    raise MemoryError(
                        f"Buffer Overflow: Found more target matches than the strictly fixed "
                        f"capacity limit ({self.capacity} slots) allowed."
                    )
            
            self.buffer[write_index] = coordinate
            write_index += 1
            
        # Truncate remaining trailing elements in-place
        if truncate_unused and write_index < self.capacity:
            for idx in range(write_index, self.capacity):
                self.buffer[idx] = None
                
        return write_index


# =====================================================================
# Execution & Verification
# =====================================================================
if __name__ == "__main__":
    
    # Large target cluster matrix to trigger limits
    cluster_matrix = [
        ['C', 'C', 'C', 'C'],
        ['C', 'C', 'C', 'D'],
        ['C', 'C', 'D', 'E']
    ]
    
    # Scenario A: Strictly Fixed Buffer (Will fail cleanly if overwhelmed)
    print("--- Running Strictly Fixed Capacity Configuration ---")
    fixed_manager = MatrixStreamManager(initial_capacity=5, dynamic_resize=False)
    try:
        fixed_manager.sync_to_buffer(cluster_matrix, target='C')
    except MemoryError as e:
        print(f"Caught Expected Safety Halt: {e}\n")

    # Scenario B: Dynamic Growth Buffer (Will expand to accommodate data automatically)
    print("--- Running Dynamic Resizing Configuration ---")
    dynamic_manager = MatrixStreamManager(initial_capacity=5, dynamic_resize=True, growth_factor=2.0)
    
    total_synced = dynamic_manager.sync_to_buffer(cluster_matrix, target='C')
    print(f"Total elements captured: {total_synced}")
    print(f"Final Buffer Output: {dynamic_manager.buffer}")
