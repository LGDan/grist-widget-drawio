import base64
import zlib
import struct
from urllib.parse import unquote
import xml.etree.ElementTree as ET


# Extract the B64 image data from the src value
image_b64 = $Diagram.split(",")[1]
decoded_bytes = bytes(base64.standard_b64decode(image_b64))

# Initialize the pointer and PNG header
ptr = 0
png_header = decoded_bytes[:8]
ptr += 8

loops = 0
drawio_xml = None

while ptr < len(decoded_bytes) and loops <= 12:
    # Read the size in reverse to match endianess
    size = decoded_bytes[ptr: ptr+4][::-1] 
    ptr += 4
    size_as_int = struct.unpack("<I", bytes(size))[0]
    
    # Read the ID
    id_ = decoded_bytes[ptr: ptr + 4].decode('ascii')
    ptr += 4

    # Read the data
    data = decoded_bytes[ptr: ptr + size_as_int]
    ptr += size_as_int

    # Read the CRC
    crc = decoded_bytes[ptr: ptr + 4]
    ptr += 4

    # If ID is 'tEXt', decode and extract the XML content
    if id_ == "tEXt":
        decoded_data = unquote(data.decode('utf-8')[7:])  # Skip the prefix and URL decode
        drawio_xml = ET.fromstring(decoded_data)

    loops += 1

# Return the parsed XML object
return drawio_xml
