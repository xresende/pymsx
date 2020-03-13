# (C) 2020 by Folkert van Heusden <mail@vanheusden.com>
# released under AGPL v3.0

import sys
from typing import List

class memmap:
    def __init__(self, n_pages:int, debug):
        assert n_pages > 0 and n_pages <= 256

        self.n_pages: int = n_pages
        self.debug = debug

        self.mapper: List[int] = [ 3, 2, 1, 0 ]

        self.ram = [ [ 0 ] * 16384 ] * self.n_pages

    def get_n_pages(self):
        return 4

    def write_mem(self, a:int, v:int) -> None:
        page = self.mapper[a >> 14]

        if page < self.n_pages:
            self.ram[page][a & 0x3fff] = v

    def read_mem(self, a: int) -> int:
        page = self.mapper[a >> 14]

        if page < self.n_pages:
            return self.ram[page][a & 0x3fff]

        return 0xee

    def write_io(self, a: int, v: int) -> None:
        self.debug('memmap write %02x: %d' % (a, v))
        self.mapper[a - 0xfc] = v

    def read_io(self, a: int) -> int:
        self.debug('memmap read %02x' % a)
        return self.mapper[a - 0xfc]

