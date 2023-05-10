"""
Entrypoint to Model Evaluation API
"""
# TODO: rename once we extract metrics to its own function
# def evaluate_model(
#     model,
#     test_set,
#     train_set=None,
#     val_set=None,
#     eval_opts=None,
#     send=True,
#     run_cuid=None,
# ):
#     model_class = model.__class__.__name__

#     if Model.is_supported_model_type(model):
#         raise ValueError(
#             "Model type {} is not supported at the moment.".format(model_class)
#         )

#     if run_cuid is None:
#         run_cuid = start_run()

#     # Only supports xgboost classifiers at the moment
#     if model_class == "XGBClassifier" or model_class == "LogisticRegression":
#         return evaluate_classification_model(
#             model, test_set, train_set, eval_opts, send, run_cuid
#         )
#     elif model_class == "XGBRegressor" or model_class == "LinearRegression":
#         return evaluate_regression_model(
#             model, test_set, train_set, eval_opts, send, run_cuid
#         )
#     elif model_class == "GLMResultsWrapper":
#         # Refitting again, need a big refactor for statsmodels support
#         refitted = model.model.fit()
#         return evaluate_regression_model(
#             refitted, test_set, train_set, eval_opts, send, run_cuid
#         )
