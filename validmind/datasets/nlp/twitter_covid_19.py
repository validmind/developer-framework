# This software is proprietary and confidential. Unauthorized copying,
# modification, distribution or use of this software is strictly prohibited.
# Please refer to the LICENSE file in the root directory of this repository
# for more information.
#
# Copyright © 2023 ValidMind Inc. All rights reserved.

import os
import pandas as pd

current_path = os.path.dirname(os.path.abspath(__file__))
dataset_path = os.path.join(current_path, "datasets")

drop_columns = ["UserName", "ScreenName", "Location", "TweetAt"]
target_column = "Sentiment"


def load_data(full_dataset=False):

    data_file = os.path.join(dataset_path, "Covid_19.csv")
    df = pd.read_csv(data_file)
    df["OriginalTweet"] = df["OriginalTweet"].astype(str)
    df["Sentiment"] = df["Sentiment"].astype(str)

    # Drop these unnecessary columns when loading since they won't be
    # helpful for showing data quality issues
    if full_dataset is False:
        df.drop(drop_columns, axis=1, inplace=True)

    return df