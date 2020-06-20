"""
Source: https://openkore.com/index.php/Field_file_format
struct GATFile {                // Offset
   unsigned char magic[6];     // 0
   uint32 width;               // 6 little-endian
   uint32 height;              // 10 little-endian
   struct GATBlock blocks[];   // 14
};

// Total size: 20 bytes
struct GATBlock {                 // Offset
   float upperLeftHeight;        // 0
   float upperRightHeight;       // 4
   float lowerLeftHeight;        // 8
   float lowerRightHeight;       // 12
   unsigned char type;           // 16
   unsigned char unknown[3];     // 17
};
"""

def read_map(filename : str) -> list:
    """Return a 2d list containing info from a .gat file

    Args:
        filename (str): the filename of the map file (with .gat extension)

    Returns:
        list: 2d list containing info of the map
    """
    with open (filename, 'rb') as f:
        magic = str(f.read(6))
        width = int.from_bytes(f.read(4), "little")
        height = int.from_bytes(f.read(4), "little")
        _cell_block_size = 20
        
        total_bytes = width * height * _cell_block_size
        bytes_left = total_bytes
        i = 0
        x = 0
        y = 0
        
        _map = [[0] * width for _ in range(height)]
        while bytes_left > 20:
            x = i%width
            y = i//width
            
            upper_left_height = f.read(4)
            upper_right_height = f.read(4)
            lower_left_height = f.read(4)
            lower_left_height = f.read(4)
            _type = ord(f.read(1))
            if _type == 0 or _type == 3:
                _type = 0
            else:
                _type = 1
            _unknown = int.from_bytes(f.read(3),"little")
            bytes_left -= 20
            i += 1

            _map[y][x] = _type

        return _map
    return None