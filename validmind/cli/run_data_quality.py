from dotenv import load_dotenv
import pandas as pd
import validmind as vm

load_dotenv()

vm.init(project="cl2r3k1ri000009jweny7ba1g")
df = pd.read_csv("notebooks/datasets/bank_customer_churn.csv")

results = vm.run_tests(df)
