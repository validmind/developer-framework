The following is a list of operations performed on the dataset prior to model training:

# Remove Index Column

The dataset contains an `id` column which is the primary key of every row. This column
does not have any predictive value and is therefore dropped.

# Encoding the `Gender` Column

The `Gender` column has values "Male" and "Gender" and so they have been encoded as numbers
using the following mapping:

- 0: Male
- 1: Female

# Encoding the `Vehicle_Age` Column

The `Vehicle_Age` column has been encoded using one-hot encoding since there are three
unique values for it:

- 1-2 Year
- < 1 Year
- > 2 Years

# Encoding the `Vehicle_Damage` Column

The `Vehicle_Damage` column has values "No" and "Yes" and so they have been encoded as
numbers using the following mapping:

- 0: No
- 1: Yes

# Encoding the `Region_Code` Column

There are 53 unique values for the `Region_Code` column. Since no particular outliers
have been found in the distribution of values, all 53 unique values have been encoded using
one-hot encoding.

# Encoding the `Policy_Sales_Channel` Column

There exist 155 unique values for the `Policy_Sales_Channel` column. After a closer
look at the distribution of values, we have found that there are 134 sales channels
that contain less than 1000 rows (<0.25% of the dataset) each. To simplify the modeling
exercise, the 134 sales channels with low counts have been dropped.

The remaining set of 21 sales channels have been encoded using one-hot encoding.
