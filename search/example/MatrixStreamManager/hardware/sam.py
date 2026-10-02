import os
import json
import logging
import time
import boto3
from typing import List, Union, Dict, Any

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Fetch the queue endpoint injected by AWS SAM at startup
QUEUE_URL = os.environ.get("QUEUE_URL")

class LambdaSQSMatrixStreamer:
    """Streams matrix coordinates in chunks directly to SQS with fault-tolerant logging."""
    def __init__(self, queue_url: str):
        self.sqs_client = boto3.client('sqs')
        self.queue_url = queue_url
        self.batch_buffer = []

    def _flush_batch(self) -> None:
        if not self.batch_buffer:
            return
        try:
            response = self.sqs_client.send_message_batch(
                QueueUrl=self.queue_url,
                Entries=self.batch_buffer
            )
            # Check for partial batch delivery failures to alert the infrastructure layer
            if 'Failed' in response and response['Failed']:
                for failure in response['Failed']:
                    logger.error(json.dumps({
                        "event": "sqs_message_failed_isolated_for_dlq",
                        "message_id": failure['Id'],
                        "error_code": failure['Code']
                    }))
        except Exception as e:
            logger.critical(json.dumps({
                "event": "sqs_network_batch_dropped",
                "error": str(e)
            }))
        finally:
            self.batch_buffer.clear()

    def stream_saddleback_to_sqs(self, matrix: List[List[Union[int, float, str]]], target: Union[int, float, str]) -> int:
        if not matrix or not matrix: return 0
        total_streamed = 0
        num_rows = len(matrix)
        row, col = 0, len(matrix) - 1
        
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
                    msg_id = f"msg_{row}_{c}_{time.time_ns()}"
                    self.batch_buffer.append({
                        'Id': msg_id,
                        'MessageBody': json.dumps({"row": row, "col": c})
                    })
                    total_streamed += 1
                    if len(self.batch_buffer) == 10:
                        self._flush_batch()
                row += 1
                col = left_bound
            elif current_val > target:
                col -= 1
            else:
                row += 1
                
        self._flush_batch()
        return total_streamed

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """Production entry point executed by AWS Lambda runtime."""
    try:
        matrix = event.get("matrix")
        target = event.get("target")
        
        if matrix is None or target is None:
            return {"statusCode": 400, "body": json.dumps("Missing parameters 'matrix' or 'target'")}
            
        if not QUEUE_URL:
            return {"statusCode": 500, "body": json.dumps("Infrastructure Error: QUEUE_URL target env variable not set.")}

        streamer = LambdaSQSMatrixStreamer(queue_url=QUEUE_URL)
        count = streamer.stream_saddleback_to_sqs(matrix, target)
        
        return {
            "statusCode": 200,
            "body": json.dumps({"status": "success", "total_messages_streamed": count})
        }
    except Exception as e:
        logger.error(f"Execution failed: {str(e)}")
        return {"statusCode": 500, "body": json.dumps("Internal processing crash.")}
