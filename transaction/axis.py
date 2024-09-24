#!/usr/bin/env python3

import argparse
import json
import sys
import vcd
from wave2data.input import VCDWaveInput
from wave2data.wave import Sample
from wave2data.decoder import AXIStream


# Monkey patch _TokenizerState.advance to be able to use streams
def __monkey_advance(self, raise_on_eof: bool = True) -> int:
    if self.pos < self.end:
        self.pos += 1
    else:
        self.buf = self.stream.readline()
        n = len(self.buf)
        if n:
            self.end = n - 1
            self.pos = 0
        elif raise_on_eof:
            raise StopIteration()
        else:
            return 0
    c = self.buf[self.pos]
    if c == 10:
        self.lineno += 1
        self.column = 1
    else:
        self.column += 1
    return self.buf[self.pos]


vcd.reader._TokenizerState.advance = __monkey_advance



def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def main():
    wave = VCDWaveInput(sys.stdin.fileno())
    rx = AXIStream("rx", wave, filter="rx",
                        name_tlast='tlast', name_tkeep='tkeep',
                        name_clk='clk')
    tx = AXIStream("tx", wave, filter="tx",
                        name_tlast='tlast', name_tkeep='tkeep',
                        name_clk='clk')

    while True:
        packets = []
        decoder_errors = 0
        for sample in wave:
            if isinstance(sample, vcd.reader.Token):
                # handle gtkwave's data_end
                if sample.kind == vcd.reader.TokenKind.COMMENT:
                    if "data_end" in sample.data:
                        break
                continue
            if not isinstance(sample, Sample):
                continue
            for decoder in [rx, tx]:
                try:
                    packet = decoder.decode(sample, sample)  # TODO: lastsample
                except Exception as e:
                    eprint(f"ERROR while decoding: {e}")
                    eprint(f"  Decoder: {decoder}")
                    decoder_errors += 1
                    continue
                if packet:
                    eprint(packet)
                    packets.append(packet)

        for decoder in [rx, tx]:
            for traceline in ['Meta', 'Data', 'Keep']:
                print(f"$name {decoder.name} AXIs({traceline})")
                for packet in [p for p in packets if p.name == decoder.name]:
                    if traceline == 'Data':
                        value = packet.data.hex(' ', 4)
                    elif traceline == 'Keep':
                        value = packet.keep.hex()
                    elif traceline == 'Meta':
                        value = f"beats={packet.beats} backpreasure={packet.backpreasure}"
                    print(f"#{int(packet.starttime / wave.timeval)} {value}")
                    # TODO: endtime is posedge of last beat - should be extendedsomehow, no clue how.
                    if packet.endtime:
                        print(f"#{int(packet.endtime / wave.timeval)}")
                print("$next")

        print("$finish")
        sys.stdout.flush()


if __name__ == '__main__':
    main()
