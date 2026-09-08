#!/usr/bin/env python3

"""

Usage:
    Apply this filter to a hex formatted vector containing TLP data in gtkwave.
    In addition some config can be given via environment varialbes all prefixed
    with TLP_HDR_*

    TLP_HDR_PRINT_LEN: Add print of length decoding

License:

Copyright (c)  Tobias Binkowski <tobias.binkowski@missinglinkelectronics.com>

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

import sys

try:
    from cocotbext.pcie.core.tlp import TlpType
    from cocotbext.pcie.intel.ptile.interface import PTilePcieFrame
except ImportError:
    sys.stderr.write("Failed to import cocotbext.pci to decode TLPs, will not decode!\n")


def type_to_name(fmttype: TlpType) -> str:
    names = {
        TlpType.MEM_READ: "MRd3",
        TlpType.MEM_READ_64: "MRd4",
        TlpType.MEM_WRITE: "MWr3",
        TlpType.MEM_WRITE_64: "MWr4",
        TlpType.CFG_READ_0: "CfgRd0",
        TlpType.CFG_WRITE_0: "CfgWr0",
        TlpType.CPL: "Cpl",
        TlpType.CPL_DATA: "CplD",
    }

    if fmttype in names:
        return names[fmttype]
    else:
        return "???"


def tlp_hdr_decode(line: str):
    """ Takes the vector received from gtkwave and decodes it into a TLP

    :param line: The hex vector received from gtkwave (must be hex, 128bit)
    """

    frame = PTilePcieFrame()
    frame.hdr = int(line, base=16)
    tlp = frame.to_tlp()
    return tlp


def tlp_hdr_repr(tlp, line) -> str:
    tlpname = type_to_name(tlp.fmt_type)
    if tlp.fmt_type in [TlpType.CPL, TlpType.CPL_DATA]:
        return f"{tlpname}(len:{tlp.length} laddr:{hex(tlp.lower_address)} tag:{tlp.tag} byte_count:{tlp.byte_count}) {line}\n"
    else:
        return f"{tlpname}(len:{tlp.length} addr:{hex(tlp.address)} tag:{tlp.tag} BE:{tlp.last_be}/{tlp.first_be}) {line}\n"


def main():
    while True:
        line = sys.stdin.readline().rstrip()
        if not line:
            return 0
        if len(line) < 8:
            sys.stderr.write("Vector is too small for a TLP header!\n")
            sys.stdout.write(line)
            sys.stdout.flush()

        sline = ' '.join(line[i:i+8] for i in range(0, len(line), 8))

        try:
            tlp = tlp_hdr_decode(line)
            sys.stdout.write(tlp_hdr_repr(tlp, sline))
            sys.stdout.flush()
        except Exception as e:
            sys.stderr.write(f"Failed to decode HDR into TLP! {e}\n")
            sys.stdout.write(f"{sline}\n")
            sys.stdout.flush()
        continue


if __name__ == '__main__':
    main()
