from typing import Optional, List


class Range:
    def __init__(self, start: int, finish: int, size: int):
        self.start = start
        self.finish = finish
        self.size = size

    @property
    def valid(self) -> bool:
        return 0 <= self.start <= self.finish < self.size

    def __len__(self) -> int:
        return self.finish - self.start + 1

    def __str__(self) -> str:
        return f'bytes {self.start}-{self.finish}/{self.size}'

    def __repr__(self) -> str:
        return f'Range({self.start}, {self.finish}, {self.size})'

    def __eq__(self, other) -> bool:
        return self.start == other.start and self.finish == other.finish \
               and self.size == self.size


def parse_http_range(range_header: Optional[str], size: int) -> \
        Optional[List[Range]]:
    """
    Parse a byte range header as specified by HTTP RFC2616 section 14.35.1.
    Takes the byte range header as well as the size of the file requested and
    returns a list of tuples (start, finish) for the byte range specified.
    """
    if range_header is None or '=' not in range_header:
        return None

    _, byte_ranges = range_header.split('=', 1)

    ranges = byte_ranges.split(',')

    results = []
    for byte_range in ranges:
        byte_range = byte_range.strip()

        if '-' not in byte_range:
            return None

        if byte_range.startswith('-'):
            # Get the last x bytes of the file
            try:
                start = size + int(byte_range)
                if start < 0:
                    return None
            except ValueError:
                return None

            finish = size - 1
        else:
            start, finish = byte_range.split('-', 1)
            try:
                start = int(start)
            except ValueError:
                return None

            if finish:
                try:
                    finish = int(finish)
                except ValueError:
                    return None

                if finish > size:
                    finish = size - 1
            else:
                finish = size - 1

            if start > finish:
                return None

        results.append(Range(start, finish, size))

    return results


def http_range_valid(ranges: Optional[List[Range]]) -> bool:
    if not ranges:
        return False

    return all([r.valid for r in ranges])
