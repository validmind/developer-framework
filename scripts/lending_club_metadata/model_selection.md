This use case was modeled as a supervised classification problem where the model needs to classify existing loans as "Fully Paid" or "Charged Off" based on existing data. To solve this problem, two state of the art techniques for binary classification will be evaluated: Logistic Regression and Decision Tree-Based models.

# Logistic Regression

Logistic regression is commonly used for prediction and classification problems where interpretability is very important. Its simplicity and speed allows for training benchmark models in use cases such as churn prediction and fraud detection. The strength of logistic regression models include:

- Easy to implement, train and interpret
- Provides a probabilistic view of class predictions
- Model coefficients provide a natural interpretation of feature importance
- Good accuracy for simpler datasets

# Tree-Based Models

The use of tree-based models for classification problems with similar dataset size has been established in the industry and literature. The strength of tree-based models include:

- They are intuitive and easy to interpret
- They are a non-parametric method which does not require that the data set follow a
  normal distribution.
- They are tolerant to data quality issues and outliers and work well with both
  categorical and continuous variables. Compared to other tree-based methods such as
  Random Forests, XGBoost offer higher performance with complex data and non-linear
  relationships such as the ones modeled in this use case. They also offer more
  flexibility in hyperparameter tuning options.
