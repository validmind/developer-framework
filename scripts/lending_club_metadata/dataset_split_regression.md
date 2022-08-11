The dataset was split in three parts:

- Training set: 60% of the data
- Validation set: 20% of the data
- Test set: hold-out set with 20% of the data

With the following approach:

- Use `random_state=42` to ensure reproducibility of any split
- Use `train_test_split` (80%/20%) to randomly split the entire dataset into a training dataset and a hold-out dataset for model evaluation
- Take the new training dataset and split it into training and validation datasets (75%/25%), guaranteeing a 60%/20%/20% split
- The training and validation datasets are used for training the model and the test dataset is used for evaluating the model
