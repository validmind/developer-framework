# Copyright © 2023-2024 ValidMind Inc. All rights reserved.
# See the LICENSE file in the root of this repository for details.
# SPDX-License-Identifier: AGPL-3.0 AND ValidMind Commercial

import os
import pandas as pd

current_path = os.path.dirname(os.path.abspath(__file__))
dataset_path = os.path.join(current_path, "datasets/fred")
deposits_file = os.path.join(dataset_path, "DPSACBW027NBOG.csv")
fed_funds_file = os.path.join(dataset_path, "FEDFUNDS.csv")
tb3ms_file = os.path.join(dataset_path, "TB3MS.csv")
gs10_file = os.path.join(dataset_path, "GS10.csv")
gs30_file = os.path.join(dataset_path, "GS30.csv")


def load_data():
    deposits = pd.read_csv(deposits_file, parse_dates=["DATE"], index_col="DATE")
    fed_funds = pd.read_csv(fed_funds_file, parse_dates=["DATE"], index_col="DATE")
    tb3ms = pd.read_csv(tb3ms_file, parse_dates=["DATE"], index_col="DATE")
    gs10 = pd.read_csv(gs10_file, parse_dates=["DATE"], index_col="DATE")
    gs30 = pd.read_csv(gs30_file, parse_dates=["DATE"], index_col="DATE")

    # Merge datasets on the date
    df = deposits.join([fed_funds, tb3ms, gs10, gs30], how="inner")
    df.columns = ["Deposits", "FEDFUNDS", "TB3MS", "GS10", "GS30"]

    return df
