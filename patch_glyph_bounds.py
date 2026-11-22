"""Build a Steam Input glyph bounds fix for the verified unpacked game build."""

import argparse
import hashlib
from pathlib import Path
import struct


BASE_SHA256 = "4cac5967d6619f92190be84f3a25a255613c90ff95122296373cc9bf0ace8e64"
IMAGE_COUNT = 406
TEXT_RVA = 0x1000
TEXT_OFFSET = 0x400
LOOKUP_START = 0xE5E60
LOOKUP_END = 0xE61BE
PADDING_RVA = 0x6D6CAB


def file_offset(rva):
    return TEXT_OFFSET + rva - TEXT_RVA


def build_patch(original):
    if hashlib.sha256(original).hexdigest() != BASE_SHA256:
        raise ValueError("Input does not match the supported unpacked build")

    # All successful lookup branches sign-extend the index into RAX and put
    # the cImage array base in RCX before executing this same leaf return.
    lookup_tail = bytes.fromhex("48 69 c0 f8 20 00 00 48 03 c1 c3")
    # An unsigned comparison rejects both negative indices and indices >= 406.
    # Invalid indices use the lookup's existing no-image return value, NULL.
    bounds_check = b"\x3d" + struct.pack("<I", IMAGE_COUNT)
    checked_tail = bounds_check + b"\x73\x0b" + lookup_tail + b"\x31\xc0\xc3"
    padding = file_offset(PADDING_RVA)
    end = file_offset(LOOKUP_END)
    if original[padding:padding + len(checked_tail)] != b"\xcc" * len(checked_tail):
        raise ValueError("Expected executable padding was not found")

    output = bytearray(original)
    offset = original.find(lookup_tail, file_offset(LOOKUP_START), end)
    patched_exits = 0
    while offset != -1:
        tail_rva = offset - TEXT_OFFSET + TEXT_RVA
        jump = b"\xe9" + struct.pack("<i", PADDING_RVA - (tail_rva + 5))
        output[offset:offset + len(lookup_tail)] = jump.ljust(len(lookup_tail), b"\xcc")
        patched_exits += 1
        offset = original.find(lookup_tail, offset + len(lookup_tail), end)

    if patched_exits != 16:
        raise ValueError(f"Expected 16 lookup exits, found {patched_exits}")
    output[padding:padding + len(checked_tail)] = checked_tail
    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("unpacked", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    patched = build_patch(args.unpacked.read_bytes())
    with args.output.open("xb") as output_file:
        output_file.write(patched)
    print(hashlib.sha256(patched).hexdigest())
