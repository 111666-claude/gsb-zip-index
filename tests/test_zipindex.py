import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from zipindex import build, core


class ZipIndexTest(unittest.TestCase):
    def test_single_entry(self):
        data = build.archive([build.record("a.txt", method=0, crc=7, usize=3)])
        out = core.read_entries(data, core.Counter())
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0]["name"], "a.txt")
        self.assertEqual(out[0]["crc"], 7)

    def test_two_entries_same_length_names(self):
        data = build.archive([build.record("a.txt"), build.record("b.txt")])
        out = core.read_entries(data, core.Counter())
        self.assertEqual([e["name"] for e in out], ["a.txt", "b.txt"])

    def test_empty_data(self):
        self.assertEqual(core.read_entries(b"", core.Counter()), [])

    def test_lookup_finds_name(self):
        data = build.archive([build.record("a.txt"), build.record("b.txt")])
        out = core.lookup(data, ["b.txt"], core.Counter())
        self.assertIn("b.txt", out["entries"])

    def test_limit_field_is_read(self):
        data = build.archive([build.record("a.txt", method=8, csize=10, usize=20)])
        out = core.read_entries(data, core.Counter())[0]
        self.assertEqual((out["method"], out["csize"], out["usize"]), (8, 10, 20))


if __name__ == "__main__":
    unittest.main()
