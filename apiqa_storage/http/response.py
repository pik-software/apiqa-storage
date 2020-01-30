from django.http import StreamingHttpResponse, HttpResponse


class PartialHttpResponse(StreamingHttpResponse):
    status_code = 206
    separator = "THIS_STRING_SEPARATES"

    def __init__(self, ranges, contents, *args, **kwargs):
        super(PartialHttpResponse, self).__init__(*args, **kwargs)
        self.ranges = ranges
        self._contents = contents

        if len(self._contents) > 1:
            # We have a multipart/byteranges response.
            self.content_type = self['Content-Type']
            self['Content-Type'] = f"multipart/byteranges; " \
                                   f"boundary={self.separator}"
        else:
            self['Content-Length'] = len(ranges[0])
            self['Content-Range'] = str(ranges[0])

    def __iter__(self):
        for content, byte_range in zip(self._contents, self.ranges):
            data = content.read()
            if len(self._contents) > 1:
                yield self.make_bytes(f"--{self.separator}\r\n")
                headers = {
                    'Content-Type': self.content_type,
                    'Content-Range': str(byte_range)
                }
                yield self.serialize_headers(headers) + b'\r\n\r\n'
                yield self.make_bytes(data) + b'\r\n'
            else:
                yield self.make_bytes(data)
        if len(self._contents) > 1:
            yield self.make_bytes(f"--{self.separator}--")

    def serialize_headers(self, headers=None):
        """HTTP headers as a bytestring."""
        if headers is None:
            headers = self._headers

        def to_bytes(val, encoding):
            return val if isinstance(val, bytes) else val.encode(encoding)

        output = [
            (b': '.join([to_bytes(key, 'ascii'), to_bytes(value, 'latin-1')]))
            for key, value in headers.items()
        ]
        return b'\r\n'.join(output)


class HttpResponseNotSatisfiable(HttpResponse):
    status_code = 416

    def __init__(self, length, *args, **kwargs):
        super(HttpResponseNotSatisfiable, self).__init__(*args, **kwargs)
        self['Content-Range'] = f'bytes */{length}'
