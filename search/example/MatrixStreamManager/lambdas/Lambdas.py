import json
import logging
import time
from typing import List, Union, Dict, Any, Generator, Tuple, Optional

# Configure standard AWS Lambda Structured JSON Logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

class LambdaMatrixManager:
    """Optimized for AWS Lambda: High throughput, dynamic resizing, and cloud telemetry."""
    def __init__(self, initial_capacity: int = 1000, growth_factor: float = 2.0):
        self.capacity = initial_capacity
        self.growth_factor = growth_factor
        self.buffer: List[Optional[Tuple[int, int]]] = [None] * self.capacity

    def yield_saddleback(self, matrix: List[List[Union[int, float, str]]], target: Union[int, float, str]) -> Generator[Tuple[int, int], None, None]:
        if not matrix or not matrix[0]: return
        num_rows = len(matrix)
        row, col = 0, len(matrix[0]) - 1
        
        while row < num_rows and col >= 0:
            if matrix[row] is None or len(matrix[row]) <= col:
                row += 1
                continue
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

    def sync_to_buffer(self, matrix: List[List[Union[int, float, str]]], target: Union[int, float, str]) -> int:
        write_index = 0
        start_time = time.perf_counter()
        resize_count = 0
        
        for coordinate in self.yield_saddleback(matrix, target):
            if write_index >= self.capacity:
                # Fast allocation optimization for serverless
                new_capacity = int(self.capacity * self.growth_factor)
                self.buffer.extend([None] * (new_capacity - self.capacity))
                self.capacity = new_capacity
                resize_count += 1
            
            self.buffer[write_index] = coordinate
            write_index += 1
            
        # Clean trailing slots in-place
        for idx in range(write_index, self.capacity):
            self.buffer[idx] = None
            
        duration_ms = (time.perf_counter() - start_time) * 1000
        
        # Telemetry structural log block
        logger.info(json.dumps({
            "event": "matrix_sync_complete",
            "metrics": {
                "elements_found": write_index,
                "execution_time_ms": round(duration_ms, 3),
                "buffer_resizes": resize_count,
                "final_capacity": self.capacity
            }
        }))
        return write_index

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """AWS Lambda entry point function handler."""
    try:
        matrix = event.get("matrix")
        target = event.get("target")
        
        if matrix is None or target is None:
            return {"statusCode": 400, "body": json.dumps("Missing parameters 'matrix' or 'target'")}
            
        manager = LambdaMatrixManager(initial_capacity=10)
        total_found = manager.sync_to_buffer(matrix, target)
        
        # Truncate buffer to only include valid tracked elements for response payload output
        active_coordinates = manager.buffer[:total_found]
        
        return {
            "statusCode": 200,
            "body": json.dumps({
                "status": "success",
                "total_found": total_found,
                "coordinates": active_coordinates
            })
        }
    except Exception as e:
        logger.error(f"Execution failed: {str(e)}")
        return {"statusCode": 500, "body": json.dumps(f"Internal processing crash: {str(e)}")}
