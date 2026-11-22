import shap
import numpy as np

def generate_shap_explanations(model, X_train, X_test):
    """
    Generates SHAP values for the test set.
    """
    # Using TreeExplainer for tree-based models like Random Forest / XGBoost
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_test)
    
    # SHAP values for binary classification in RandomForest might be a 3D array
    # with shape (n_samples, n_features, n_classes) or a list.
    if isinstance(shap_values, list):
        shap_values = shap_values[1]
    elif len(np.shape(shap_values)) == 3:
        shap_values = shap_values[:, :, 1]
        
    return explainer, shap_values

def get_top_features_shap(shap_values, feature_names, instance_idx, top_k=5):
    """
    Extracts top K features for a specific instance based on SHAP values.
    """
    instance_shap = np.abs(shap_values[instance_idx])
    top_indices = np.argsort(instance_shap)[-top_k:][::-1]
    return [feature_names[i] for i in top_indices]
