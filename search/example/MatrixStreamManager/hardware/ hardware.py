import struct
import machine # MicroPython native hardware access module

class MicrocontrollerHardwareBusStreamer:
    """Streams matrix coordinates instantly across physical hardware lines without heap allocations."""
    def __init__(self, i2c_bus=None, i2c_addr=0x42, spi_bus=None, uart_bus=None):
        self.i2c = i2c_bus
        self.i2c_addr = i2c_addr
        self.spi = spi_bus
        self.uart = uart_bus
        
        # Pre-allocate static byte buffers to prevent garbage collection allocations during hot loops
        # 'HH' represents two unsigned 16-bit integers (4 bytes total: Row, Col)
        self.binary_buffer = bytearray(4) 

    def _transmit_live(self, row: int, col: int) -> None:
        """Pipes the coordinates directly into peripheral buses simultaneously."""
        # 1. Pack indices safely into our static binary buffer layout
        struct.pack_into('>HH', self.binary_buffer, 0, row, col)
        
        # 2. Transmit over I2C if peripheral is provisioned
        if self.i2c:
            try:
                self.i2c.writeto(self.i2c_addr, self.binary_buffer)
            except Exception:
                pass # Fail silently or handle device missing errors in-place
                
        # 3. Transmit over SPI if peripheral is provisioned
        if self.spi:
            try:
                self.spi.write(self.binary_buffer)
            except Exception:
                pass
                
        # 4. Transmit over UART as readable ASCII strings
        if self.uart:
            # Minimizes allocation by sending raw chunks back-to-back
            self.uart.write(b"COORD:")
            self.uart.write(str(row).encode())
            self.uart.write(b",")
            self.uart.write(str(col).encode())
            self.uart.write(b"\n")

    def process_and_stream(self, matrix, target) -> int:
        """Processes matrix rows inline and feeds hardware lines instantly. Auxiliary space is O(1)."""
        if not matrix or not matrix: return 0
        
        total_transmitted = 0
        num_rows = len(matrix)
        row = 0
        col = len(matrix[0]) - 1
        
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
                    # Bypass memory structures: Stream raw coordinate parameters directly to pins
                    self._transmit_live(row, c)
                    total_transmitted += 1
                    
                row += 1
                col = left_bound
            elif current_val > target:
                col -= 1
            else:
                row += 1
                
        return total_transmitted
