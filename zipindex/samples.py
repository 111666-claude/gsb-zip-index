"""固定场景，用来复现题面里的锚点。"""

import json

from . import build, core


def _line(obj):
    print(json.dumps(obj, ensure_ascii=False))


def run(name):
    if name == "prefix":
        data = build.archive([build.record("a.txt")], prefix=b"\x00" * 100)
        out = core.read_entries(data, core.Counter())
        _line({"entries": len(out)})
        return 0
    if name == "extra":
        data = build.archive([build.record("a.txt", extra=b"\x01\x00\x04\x00abcd"),
                              build.record("b.txt")])
        out = core.read_entries(data, core.Counter())
        _line({"names": [e["name"] for e in out]})
        return 0
    if name == "count":
        data = build.archive([build.record("a.txt"), build.record("b.txt")], total=1)
        out = core.read_entries(data, core.Counter())
        _line({"entries": len(out)})
        return 0
    if name == "work":
        records = [build.record("f%04d.txt" % i) for i in range(2000)]
        data = build.archive(records)
        names = ["f%04d.txt" % i for i in range(2000)]
        out = core.lookup(data, names, core.Counter())
        _line({"entries": 2000, "scanned": out["scanned"]})
        return 0
    raise SystemExit("未知场景：" + name)
