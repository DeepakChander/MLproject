import os
import sys
import dill

import numpy as np
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV
from src.exception import CustomException


def save_object(file_path, obj):
    """
    Save an object to a file using dill.
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)
    except Exception as e:
        raise CustomException(e, sys)


def evaluate_models(X_train, y_train, X_test, y_test, models, param):
    """
    Evaluate multiple models with GridSearchCV and return a performance report.
    """
    try:
        report = {}

        for model_name, model in models.items():
            try:
                # Retrieve parameters for the current model
                model_params = param.get(model_name, {})
                
                # Perform GridSearchCV
                gs = GridSearchCV(estimator=model, param_grid=model_params, cv=3)
                gs.fit(X_train, y_train)
                
                # Set best parameters to the model
                model.set_params(**gs.best_params_)
                model.fit(X_train, y_train)

                # Make predictions
                y_train_pred = model.predict(X_train)
                y_test_pred = model.predict(X_test)

                # Calculate R2 scores
                train_model_score = r2_score(y_train, y_train_pred)
                test_model_score = r2_score(y_test, y_test_pred)

                # Save test score in the report
                report[model_name] = test_model_score

            except Exception as e:
                # Handle model-specific errors without stopping the loop
                report[model_name] = f"Error: {str(e)}"

        return report

    except Exception as e:
        raise CustomException(e, sys)
