# Load API key and secret from environment variables
from dotenv import load_dotenv

load_dotenv()


import pandas as pd
import xgboost as xgb

from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

# Initialize ValidMind SDK
import validmind as vm

print("1. Initializing SDK...")

# For test environment use api_host="https://api.test.vm.validmind.ai/api/v1/tracking"
vm.init(project="cl1jyvh2c000909lg1rk0a0zb")

# Load model_overview.md markdown file and call log_metadata with its text
print("2. Logging model metadata...")
with open("./scripts/lending_club_metadata/model_overview.md", "r") as f:
    # TODO - read metadata from file (check markdown extension)
    vm.log_metadata(content_id="model_overview", text=f.read())

print("3. Loading dataset...")

df = pd.read_pickle("notebooks/datasets/_temp/df_loans_cleaned.pickle")

targets = vm.DatasetTargets(
    target_column="loan_status",
    class_labels={
        "Fully Paid": "Fully Paid",
        "Charged Off": "Charged Off",
    },
)

print("4. Logging dataset metadata and statistics...")

vm.log_dataset(df, "training", analyze=True, targets=targets)


print("5. Running data quality tests...")

results = vm.run_dataset_tests(
    df, target_column="loan_status", dataset_type="training", send=True
)
