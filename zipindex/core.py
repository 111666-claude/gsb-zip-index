"""读 ZIP 中央目录。"""

import struct

EOCD_SIG = 0x06054B50
CD_SIG = 0x02014B50


class Counter:
    """记录本轮读过的中央目录记录条数。"""

    def __init__(self):
        self.scanned = 0


def read_entries(data, counter):
    off = 0
    out = []
    while off + 46 <= len(data):
        if struct.unpack_from("<I", data, off)[0] != CD_SIG:
            break
        method = struct.unpack_from("<H", data, off + 10)[0]
        crc = struct.unpack_from("<I", data, off + 16)[0]
        csize = struct.unpack_from("<I", data, off + 20)[0]
        usize = struct.unpack_from("<I", data, off + 24)[0]
        nlen = struct.unpack_from("<H", data, off + 28)[0]
        name = data[off + 46:off + 46 + nlen].decode("utf-8", "replace")
        counter.scanned += 1
        out.append({"name": name, "method": method, "crc": crc,
                    "csize": csize, "usize": usize})
        off += 46 + nlen
    return out


def lookup(data, names, counter):
    found = {}
    for name in names:
        for entry in read_entries(data, counter):
            if entry["name"] == name:
                found[name] = entry
    return {"entries": found, "scanned": counter.scanned}
