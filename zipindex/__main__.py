"""命令行入口。"""

import argparse
import json

from . import core, samples


def render(entries):
    rows = [("name", "method", "crc", "csize", "usize")]
    for e in entries:
        rows.append((e["name"], str(e["method"]), str(e["crc"]),
                     str(e["csize"]), str(e["usize"])))
    widths = [max(len(row[i]) for row in rows) for i in range(5)]
    return "\n".join("  ".join(cell.ljust(widths[i]) for i, cell in enumerate(row))
                     for row in rows)


def main(argv=None):
    ap = argparse.ArgumentParser(prog="zipindex")
    ap.add_argument("--sample", choices=["prefix", "extra", "count", "work"])
    sub = ap.add_subparsers(dest="cmd")
    dump_parser = sub.add_parser("dump")
    dump_parser.add_argument("--file", required=True)
    args = ap.parse_args(argv)

    if args.sample:
        return samples.run(args.sample)
    if args.cmd is None:
        ap.print_help()
        return 2

    with open(args.file, "rb") as fh:
        data = fh.read()
    entries = core.read_entries(data, core.Counter())
    print(render(entries))
    print(json.dumps({"entries": len(entries)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
