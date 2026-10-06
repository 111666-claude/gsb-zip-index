"""读 ZIP 中央目录。"""

import struct

EOCD_SIG = 0x06054B50
CD_SIG = 0x02014B50


class Counter:
    """记录本轮读过的中央目录记录条数。"""

    def __init__(self):
        self.scanned = 0


def read_entries(data, counter):
    eocd = data.rfind(struct.pack("<I", EOCD_SIG))
    if eocd < 0 or eocd + 22 > len(data):
        return []
    total = struct.unpack_from("<H", data, eocd + 10)[0]
    off = struct.unpack_from("<I", data, eocd + 16)[0]
    out = []
    while len(out) < total and off + 46 <= len(data):
        if struct.unpack_from("<I", data, off)[0] != CD_SIG:
            break
        method = struct.unpack_from("<H", data, off + 10)[0]
        crc = struct.unpack_from("<I", data, off + 16)[0]
        csize = struct.unpack_from("<I", data, off + 20)[0]
        usize = struct.unpack_from("<I", data, off + 24)[0]
        nlen = struct.unpack_from("<H", data, off + 28)[0]
        elen = struct.unpack_from("<H", data, off + 30)[0]
        clen = struct.unpack_from("<H", data, off + 32)[0]
        name = data[off + 46:off + 46 + nlen].decode("utf-8", "replace")
        counter.scanned += 1
        out.append({"name": name, "method": method, "crc": crc,
                    "csize": csize, "usize": usize})
        off += 46 + nlen + elen + clen
    return out


def lookup(data, names, counter):
    entries = read_entries(data, counter)
    found = {}
    by_name = {entry["name"]: entry for entry in entries}
    for name in names:
        if name in by_name:
            found[name] = by_name[name]
    return {"entries": found, "scanned": counter.scanned}
