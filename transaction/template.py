#!/usr/bin/env python3

import sys
from wave2data.input import VCDWaveInput


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
        for sample in wave:
            if not isinstance(sample, vcd.reader.Token):
                continue
            # handle gtkwave's data_end
            if sample.kind == vcd.reader.TokenKind.COMMENT:
                if "data_end" in sample.data:
                    break
            print(sample, file=sys.stderr)  # TODO: debugging, remove in real code

        print("$name Val1")
        print("#0 Val1:Test1?")
        print("#10000 ?darkblue?Val1:Test2")
        print("$next")
        print("$name Val2")
        print("#0 Val2:Test1?")
        print("#20000 Val2:Test2")
        print("$finish")
        sys.stdout.flush()


if __name__ == '__main__':
    main()
