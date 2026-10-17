import unittest

import pandas as pd

from validmind.utils import format_records


class TestFormatRecords(unittest.TestCase):
    def test_string_dtype_column_is_left_unchanged(self):
        df = pd.DataFrame(
            {
                "Name": pd.array(["a", "b"], dtype="string"),
                "Value": [0.123456789, 0.5],
            }
        )

        records = format_records(df)

        self.assertEqual([r["Name"] for r in records], ["a", "b"])
        self.assertEqual(records[0]["Value"], 0.1235)

    def test_all_missing_nullable_column_is_left_missing(self):
        df = pd.DataFrame({"Value": pd.array([None, 0.0], dtype="Float64")})

        records = format_records(df)

        self.assertIsNone(records[0]["Value"])
        self.assertEqual(records[1]["Value"], 0.0)

    def test_numeric_rounding_is_unchanged(self):
        df = pd.DataFrame(
            {
                "Small": [0.123456789, 0.5],
                "Big": [12.3456, 20.0],
            }
        )

        records = format_records(df)

        self.assertEqual(records[0]["Small"], 0.1235)
        self.assertEqual(records[0]["Big"], 12.35)
