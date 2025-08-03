try:
    from typing import TYPE_CHECKING
except ImportError:
    TYPE_CHECKING = False  # pyright:ignore[reportConstantRedefinition]

if TYPE_CHECKING:
    from fakes import framebuf
else:
    import framebuf


def read_pbm_p4(filename: str) -> tuple[framebuf.FrameBuffer, int, int]:
    with open(filename, "rb") as f:
        # Read magic number (P4)
        magic = f.readline().strip()
        if magic != b"P4":
            raise ValueError(f"{filename}: not a PBM P4 file")

        # Skip comments
        while True:
            line = f.readline().strip()
            if not line.startswith(b"#"):
                break

        # Read dimensions
        width, height = [int(val) for val in line.split()]

        # Read binary image data
        data = bytearray(f.read())

    # Create a FrameBuffer object (assuming MONO_HLSB for horizontal scan, MSB first)
    fbuf = framebuf.FrameBuffer(data, width, height, framebuf.MONO_HLSB)
    return fbuf, width, height
