
# Saved from __main__.external_api
# Test ID: my_custom_metrics.ExternalAPI

import requests


def ExternalAPI():
    """This metric calls an external API to get the current BTC price. It then creates
    a table with the relevant data so it can be displayed in the documentation.

    The purpose of this metric is to demonstrate how to call an external API and use the
    data in a metric. A metric like this could even be setup to run in a scheduled
    pipeline to keep your documentation in-sync with an external data source.
    """
    url = "https://api.coindesk.com/v1/bpi/currentprice.json"
    response = requests.get(url)
    data = response.json()

    # extract the time and the current BTC price in USD
    return [
        {
            "Time": data["time"]["updated"],
            "Price (USD)": data["bpi"]["USD"]["rate"],
        }
    ]
