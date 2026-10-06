"""测试与场景用的小工具：手工拼中央目录。"""

import struct

EOCD_SIG = 0x06054B50
CD_SIG = 0x02014B50


def record(name, method=0, crc=0, csize=0, usize=0, extra=b"", comment=b""):
    raw = name.encode("utf-8")
    head = struct.pack("<IHHHHHHIIIHHHHHII", CD_SIG, 20, 20, 0, method, 0, 0,
                       crc, csize, usize, len(raw), len(extra), len(comment),
                       0, 0, 0, 0)
    return head + raw + extra + comment


def archive(records, total=None, prefix=b""):
    body = b"".join(records)
    count = len(records) if total is None else total
    eocd = struct.pack("<IHHHHIIH", EOCD_SIG, 0, 0, count, count,
                       len(body), len(prefix), 0)
    return prefix + body + eocd
