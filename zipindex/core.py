"""读 ZIP 中央目录。"""

import struct

EOCD_SIG = 0x06054B50
CD_SIG = 0x02014B50
EOCD_LEN = 22
CD_LEN = 46
MAX_COMMENT = 0xFFFF


class Counter:
    """记录本轮读过的中央目录记录条数。"""

    def __init__(self):
        self.scanned = 0


def _find_eocd(data):
    """从文件末尾向前找 EOCD 记录，返回其偏移，找不到返回 -1。"""
    start = max(0, len(data) - EOCD_LEN - MAX_COMMENT)
    for off in range(len(data) - EOCD_LEN, start - 1, -1):
        if struct.unpack_from("<I", data, off)[0] == EOCD_SIG:
            return off
    return -1


def read_entries(data, counter):
    eocd = _find_eocd(data)
    if eocd < 0:
        return []
    total = struct.unpack_from("<H", data, eocd + 10)[0]
    cd_size = struct.unpack_from("<I", data, eocd + 12)[0]
    cd_off = struct.unpack_from("<I", data, eocd + 16)[0]
    # 允许自解压前缀：EOCD 里的偏移相对归档起点，按实际位置修正。
    prefix = eocd - cd_size - cd_off
    off = cd_off + prefix if prefix > 0 else cd_off
    out = []
    while len(out) < total and off + CD_LEN <= len(data):
        if struct.unpack_from("<I", data, off)[0] != CD_SIG:
            break
        method = struct.unpack_from("<H", data, off + 10)[0]
        crc = struct.unpack_from("<I", data, off + 16)[0]
        csize = struct.unpack_from("<I", data, off + 20)[0]
        usize = struct.unpack_from("<I", data, off + 24)[0]
        nlen = struct.unpack_from("<H", data, off + 28)[0]
        elen = struct.unpack_from("<H", data, off + 30)[0]
        clen = struct.unpack_from("<H", data, off + 32)[0]
        name = data[off + CD_LEN:off + CD_LEN + nlen].decode("utf-8", "replace")
        counter.scanned += 1
        out.append({"name": name, "method": method, "crc": crc,
                    "csize": csize, "usize": usize})
        off += CD_LEN + nlen + elen + clen
    return out


def lookup(data, names, counter):
    entries = read_entries(data, counter)
    by_name = {}
    for entry in entries:
        by_name[entry["name"]] = entry
    found = {}
    for name in names:
        if name in by_name:
            found[name] = by_name[name]
    return {"entries": found, "scanned": counter.scanned}
