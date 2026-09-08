#!/usr/bin/env python3

"""

Usage:
    Apply this filter to a hex formatted vector containing TLP data in gtkwave.
    In addition some config can be given via environment varialbes all prefixed
    with TLP_HDR_*

    TLP_HDR_PRINT_LEN: Add print of length decoding

License:

Copyright (c)  Tobias Binkowski <sessl3r@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

"""

import os
import sys


# TODO: only added most relevant ones for now
tlp_types = {
    0x00: "MRd3",
    0x20: "MRd4",
    0x40: "MWr3",
    0x60: "MWr4",
    0x02: "IORd",
    0x42: "IOWd",
    0x04: "CfgRd0",
    0x44: "CfgWr0",
    0x05: "CfgRd1",
    0x45: "CfgWr1",
    0x0A: "Cpl",
    0x4A: "CplD",
}


def main():
    while True:
        line = sys.stdin.readline().rstrip()
        if not line:
            return 0
        if len(line) < 8:
            sys.stderr.write("Vector is too small for a TLP!\n")
            sys.stdout.write(line)
            sys.stdout.flush()

        sline = ' '.join(line[i:i+8] for i in range(0, len(line), 8))

        try:
            fmttype = int(line[0:2], 16)
            length = int(line[6:8], 16)
        except Exception:
            sys.stdout.write(f"{sline}\n")
            sys.stdout.flush()
            continue

        if fmttype in tlp_types:
            fmttype = tlp_types[fmttype]
        else:
            fmttype = hex(fmttype)

        result = fmttype
        if os.environ.get("TLP_HDR_PRINT_LEN", None):
            result += f"(len:{length})"
        result += f": {sline}\n"

        sys.stdout.write(result)
        sys.stdout.flush()


if __name__ == '__main__':
    main()
