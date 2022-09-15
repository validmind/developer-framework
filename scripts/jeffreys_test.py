"""
Using code for the Jeffrey's test as is, without any modification
to integrate with the ValidMind codebase yet
"""

import numpy as np
import pandas as pd
import scipy


def jeffreys_test(p: float, n: int = 0, d: int = 0) -> float:
    """
    Perform a test that the test probability, p, is consistent with the observed number of
    successes, d, from a number of trials, n.

    This uses the Jeffrey's posterior probability, which is the Beta distribution with shape
    parameters a = d + 1/2 and b = n - d + 1/2. The result is the one sided p-value representing the
    probability that the test probability, p, is greater than the true probability.

    :param p: the test probability to be compared to the number of successes given n trials
    :param n: the number of trials
    :param d: the number of successes [optional, default = 0]

    :return p-value: one sided p-value of the test
    """
    return scipy.stats.beta.cdf(p, d + 0.5, n - d + 0.5)


def update_result(s, d, n, dr, p, pval, out="Yet to decide"):
    return {
        "Segment": s,
        "Defaults": d,
        "Observations": n,
        "Default Rate": dr,
        "Calibrated PD": p,
        "P-value": pval,
        "Outcome": out,
    }


def calculate_and_return(
    df=pd.DataFrame, cal_pd={}, pool=None, obs="observed", threshold=0.9
):
    """
    Take the input dataframe, analyse & clean, seprate poolwise.
    Calculate the jeffreys statistic
    """

    result = pd.DataFrame(
        columns=[
            "Segment",
            "Defaults",
            "Observations",
            "Default Rate",
            "Calibrated PD",
            "P-value",
            "Outcome",
        ]
    )

    n = len(df[obs])
    d = np.sum(df[obs])
    dr = np.round(d / n, 2)
    p = cal_pd["Model"]
    pval = np.round(jeffreys_test(p, n, d), 4)
    if pval >= threshold:
        out = "Satisfactory"
    else:
        out = "Not Satisfactory"

    result = result.append(
        update_result("Model", d, n, dr, p, pval, out), ignore_index=True
    )

    if pool != None:
        samples = df.groupby(pool)

        for sample in samples:
            n = len(sample[1][obs])
            d = np.sum(sample[1][obs])
            dr = np.round(d / n, 2)
            p = cal_pd[sample[0]]
            pval = np.round(jeffreys_test(p, n, d), 4)

            if pval >= threshold:
                out = "Satisfactory"
            else:
                out = "Not Satisfactory"

            result = result.append(
                update_result(sample[0], d, n, dr, p, pval, out), ignore_index=True
            )

    return result


def get_calibrated_pds(df, model, segments):
    model_preds = model.predict_proba(df)[:, 1]
    model_class_preds = (model_preds > 0.5).astype(int)

    pds = {"Model": model_class_preds.sum() / len(model_class_preds)}

    for segment in segments:
        for segment in segment["segments"]:
            segment_df = df.query(segment["query"])
            y_pred = model.predict_proba(segment_df)[:, -1]
            class_pred = (y_pred > 0.5).astype(int)
            total_pds = class_pred.sum()
            segment_pd = total_pds / len(class_pred)

            pds[segment["name"]] = segment_pd
    return pds


def process_observations(df, model, segments):
    test_input = pd.DataFrame(columns=["Segment", "Observed"])

    for segment in segments:
        for segment in segment["segments"]:
            segment_df = df.query(segment["query"])
            y_pred = model.predict_proba(segment_df)[:, -1]
            class_pred = (y_pred > 0.5).astype(int)
            # Concat to test_input by adding all rows of class_pred and segment as a single value
            test_input = pd.concat(
                [
                    test_input,
                    pd.DataFrame({"Segment": segment["name"], "Observed": class_pred}),
                ],
                ignore_index=True,
            )

    return test_input
