import struct

class MicrocontrollerFramedStreamer:
    """Streams matrix coordinates wrapped inside an SOF and Checksum packet protocol."""
    def __init__(self, i2c_bus=None, i2c_addr=0x42, spi_bus=None, uart_bus=None):
        self.i2c = i2c_bus
        self.i2c_addr = i2c_addr
        self.spi = spi_bus
        self.uart = uart_bus
        
        # MODIFICATION: Pre-allocate 4 bytes: [SOF, ROW, COL, CHECKSUM]
        # 'BBBB' means four unsigned 8-bit bytes
        self.packet_buffer = bytearray(4)
        self.sof = 0xAA  # Standard distinctive Start-of-Frame bit pattern

    def _transmit_live(self, row: int, col: int) -> None:
        """Packs and streams data using a safe, verified protocol framing layout."""
        if row > 255 or col > 255:
            return  # Skip values exceeding 8-bit constraints safely

        # Calculate a highly optimized XOR Checksum over the data stream
        checksum = self.sof ^ row ^ col

        # Pack everything into our single static bytearray (Zero Heap Allocation)
        struct.pack_into('>BBBB', self.packet_buffer, 0, self.sof, row, col, checksum)
        
        # Send the framed packet across active hardware lines
        if self.i2c:
            try: self.i2c.writeto(self.i2c_addr, self.packet_buffer)
            except: pass
                
        if self.spi:
            try: self.spi.write(self.packet_buffer)
            except: pass
                
        if self.uart:
            try: self.uart.write(self.packet_buffer)
            except: pass
