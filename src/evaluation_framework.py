import numpy as np
from .xai_generators import generate_shap_explanations, get_top_features_shap
import pandas as pd

def evaluate_stability(model, X_test, feature_names, num_instances=20, noise_level=0.05, top_k=5):
    """
    Evaluates Explanation Stability by adding small Gaussian noise to the input
    and checking if the top K important features remain the same.
    """
    # Note: SHAP can be slow, so we only evaluate a subset of instances
    subset_idx = np.random.choice(len(X_test), min(num_instances, len(X_test)), replace=False)
    X_subset = X_test.iloc[subset_idx].copy()
    
    _, base_shap = generate_shap_explanations(model, X_test, X_subset)
    
    stability_scores = []
    
    for i in range(len(X_subset)):
        base_top_features = get_top_features_shap(base_shap, feature_names, i, top_k)
        
        # Add noise
        noisy_instance = X_subset.iloc[[i]].copy()
        noise = np.random.normal(0, noise_level, noisy_instance.shape)
        noisy_instance += noise
        
        _, noisy_shap = generate_shap_explanations(model, X_test, noisy_instance)
        noisy_top_features = get_top_features_shap(noisy_shap, feature_names, 0, top_k)
        
        # Calculate Jaccard similarity between base and noisy top features
        intersection = len(set(base_top_features).intersection(set(noisy_top_features)))
        union = len(set(base_top_features).union(set(noisy_top_features)))
        stability_scores.append(intersection / union)
        
    return np.mean(stability_scores)


def evaluate_clinician_alignment(model, X_test, feature_names, clinical_knowledge_features, top_k=10):
    """
    Evaluates Clinician Alignment by comparing the model's global top features
    with a predefined list of clinically relevant features.
    """
    _, shap_values = generate_shap_explanations(model, X_test, X_test)
    
    # Global feature importance
    mean_abs_shap = np.mean(np.abs(shap_values), axis=0)
    top_indices = np.argsort(mean_abs_shap)[-top_k:][::-1]
    model_top_features = [feature_names[i] for i in top_indices]
    
    aligned_count = sum([1 for f in model_top_features if f in clinical_knowledge_features])
    alignment_score = aligned_count / len(clinical_knowledge_features)
    
    return alignment_score, model_top_features
