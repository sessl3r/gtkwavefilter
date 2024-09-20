#!/usr/bin/env python3

"""

Select this script as Filter Process for a signal and the output will be split
all 8 characters which for hex is 32-bit/1DW.

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

import sys

LENGTH = 8

def main():
    while True:
        line = sys.stdin.readline()
        if not line:
            return 0

        if len(line) > LENGTH:
            line = ' '.join(line[i:i+LENGTH] for i in range(0, len(line), LENGTH))

        sys.stdout.write(line)
        sys.stdout.flush()


if __name__ == '__main__':
    main()
