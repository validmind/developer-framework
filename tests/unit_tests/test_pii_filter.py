import unittest
from unittest.mock import MagicMock, patch

import pandas as pd

from validmind.vm_models.result import pii_filter
from validmind.vm_models.result.pii_filter import PIIDetectionMode, scan_df


class TestScanDf(unittest.TestCase):
    def _scan(self, df):
        builder = MagicMock()
        builder.generate_analysis.return_value.entity_mapping = {
            "email": "EMAIL_ADDRESS"
        }
        mode = PIIDetectionMode.ALL
        with patch.object(pii_filter, "get_pii_detection_mode", return_value=mode):
            with patch.object(pii_filter, "_get_presidio_df", return_value=builder):
                return scan_df(df)

    def test_object_dtype_column_is_scanned(self):
        df = pd.DataFrame({"email": ["a@b.com"], "value": [1]})

        with self.assertRaisesRegex(ValueError, "email"):
            self._scan(df)

    def test_string_dtype_column_is_scanned(self):
        df = pd.DataFrame(
            {"email": pd.array(["a@b.com"], dtype="string"), "value": [1]}
        )

        with self.assertRaisesRegex(ValueError, "email"):
            self._scan(df)
