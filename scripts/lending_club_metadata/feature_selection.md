The following is a list of operations performed on the dataset prior to model training:

# Remove Features without Predictive Power

## Irrelevant Columns

The following columns do not have any predictive value and are therefore dropped:

- id
- url
- issue_year

## Columns Containing Post Loan Application Data

Some columns do not contain any useful information for the model since they track
information for activities performed after the loans have been finalized.

- chargeoff_within_12_mths
- collection_recovery_fee
- funded_amnt
- funded_amnt_inv
- last_credit_pull_d
- last_fico_range_high
- last_fico_range_low
- last_pymnt_amnt
- last_pymnt_d
- next_pymnt_d
- And 22 more columns...

## Columns That Can Introduce Unfair Bias

The following columns can introduce unintended bias to the model:

- zip_code
- addr_state

## Columns with Too Many Categorical Values

Too many categorical values indicates that there are too many unique
or distinct values for a feature. A high amount of distinct values does
not provide any predictive power for a model.

The following categorical features have more than 200 unique values and have been removed:

- emp_title
- title

## Columns with Static Values

Static values do not contain any relationship to the dependent variable. The following
columns have been removed:

- policy_code

# Remove Sparsely Populated Columns

The following features have at least 90% of missing values and have been removed:

- annual_inc_joint
- dti_joint
- verification_status_joint
- revol_bal_joint
- sec_app_fico_range_low
- sec_app_fico_range_high
- sec_app_earliest_cr_line
- sec_app_inq_last_6mths
- sec_app_mort_acc
- sec_app_open_acc
- sec_app_revol_util
- sec_app_open_act_il
- sec_app_num_rev_accts
- sec_app_chargeoff_within_12_mths
- sec_app_collections_12_mths_ex_med
- deferral_term
- hardship_last_payment_amount

# Remove Highly Correlated Columns

The following features have a very high correlation (above 0.9) with other features
in the dataset and have been removed:

- installment
- fico_range_high
- num_rev_tl_bal_gt_0
- num_sats
- tot_hi_cred_lim
- total_il_high_credit_limit

# Encoding the Target Column

The `loan_status` column has values "Charged Off" and "Fully Paid" and so they have been
encoded as binary values using the following mapping:

- 0: Fully Paid
- 1: Charged Off

# Encoding the `earliest_cr_line` Column

The `earliest_cr_line` column is of type `Date` and tracks the month the borrower's
earliest reported credit line was opened. Its value has been transformed and now tracks
the number of years between the earliest creported credit line and the loan issue date.
