import struct
import machine

class Microcontroller8BitStreamer:
    """Streams matrix coordinates using ultra-compact 8-bit structures for physical pins."""
    def __init__(self, i2c_bus=None, i2c_addr=0x42, spi_bus=None, uart_bus=None):
        self.i2c = i2c_bus
        self.i2c_addr = i2c_addr
        self.spi = spi_bus
        self.uart = uart_bus
        
        # MODIFICATION: Pre-allocate exactly 2 bytes total instead of 4 bytes.
        # 'BB' stands for two unsigned 8-bit integers (0 to 255 maximum limit).
        self.binary_buffer = bytearray(2) 

    def _transmit_live(self, row: int, col: int) -> None:
        """Pipes the coordinates directly into peripheral buses simultaneously."""
        # Safety Check: If indices exceed 8-bit limits, drop or handle gracefully
        if row > 255 or col > 255:
            # Skip or flag integer boundary limitations safely
            return

        # Pack indices cleanly using 8-bit formats (Zero Heap Allocation)
        struct.pack_into('>BB', self.binary_buffer, 0, row, col)
        
        # Send out the 2-byte structure across all provisioned hardware buses
        if self.i2c:
            try:
                self.i2c.writeto(self.i2c_addr, self.binary_buffer)
            except:
                pass
                
        if self.spi:
            try:
                self.spi.write(self.binary_buffer)
            except:
                pass
                
        if self.uart:
            # Keep UART lightweight by transmitting the raw binary bytes instead of heavy ASCII strings
            self.uart.write(self.binary_buffer)

    def process_and_stream(self, matrix, target) -> int:
        """Inline Saddleback processing engine feeding the 8-bit hardware buses."""
        if not matrix or not matrix: return 0
        
        total_transmitted = 0
        num_rows = len(matrix)
        row = 0
        col = len(matrix)[0] - 1 if num_rows > 0 and matrix[0] is not None else -1
        
        while row < num_rows and col >= 0:
            if len(matrix[row]) <= col:
                row += 1
                continue
                
            current_val = matrix[row][col]
            
            if current_val == target:
                left_bound = col
                while left_bound >= 0 and matrix[row][left_bound] == target:
                    left_bound -= 1
                
                for c in range(left_bound + 1, col + 1):
                    self._transmit_live(row, c)
                    total_transmitted += 1
                    
                row += 1
                col = left_bound
            elif current_val > target:
                col -= 1
            else:
                row += 1
                
        return total_transmitted
