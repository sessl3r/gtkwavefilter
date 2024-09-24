#!/usr/bin/env python3

import sys
import vcd
from wave2data.input import VCDWaveInput
from wave2data.wave import Sample


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


def main():
    wave = VCDWaveInput(sys.stdin.fileno())
    while True:
        samples = []
        for sample in wave:
            if isinstance(sample, vcd.reader.Token):
                # handle gtkwave's data_end
                if sample.kind == vcd.reader.TokenKind.COMMENT:
                    if "data_end" in sample.data:
                        break
                continue
            if not isinstance(sample, Sample):
                continue
            samples.append(sample)

        for traceline in ['line1', 'line2', 'line3']:
            print(f"$name {traceline}")
            for sample in samples:
                print(f"#{int(sample.timestamp / wave.timeval)} {sample.timestamp}")
            print("$next")

        print("$finish")
        sys.stdout.flush()


if __name__ == '__main__':
    main()
