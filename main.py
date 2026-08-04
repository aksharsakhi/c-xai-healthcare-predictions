import os
from src.data_preprocessing import load_and_preprocess_data
from src.model_training import train_models
from src.evaluation_framework import evaluate_stability, evaluate_clinician_alignment

def main():
    print("Loading data...")
    X_train, X_test, y_train, y_test, feature_names = load_and_preprocess_data()
    
    print("Training models...")
    results = train_models(X_train, y_train, X_test, y_test)
    
    best_model_name = 'RandomForest'
    best_model = results[best_model_name]['model']
    
    print(f"\nEvaluating XAI for {best_model_name}...")
    
    # Measure Stability
    print("Measuring Explanation Stability (Robustness to noise)...")
    stability_score = evaluate_stability(best_model, X_test, feature_names, num_instances=30, noise_level=0.1)
    print(f"Average Stability Score (Jaccard Index): {stability_score:.4f}")
    
    # Measure Clinician Alignment
    # Simulating Clinical Knowledge: Suppose a doctor says these are key indicators for breast cancer
    clinical_knowledge = ['mean concave points', 'worst concave points', 'worst radius', 'mean perimeter', 'worst area', 'worst perimeter', 'mean radius', 'mean concavity']
    print("\nMeasuring Clinician Alignment...")
    alignment_score, top_global = evaluate_clinician_alignment(best_model, X_test, feature_names, clinical_knowledge)
    print(f"Global Top Features by Model: {top_global}")
    print(f"Clinician Alignment Score: {alignment_score:.4f} ({int(alignment_score*100)}%)")
    
    # Save results to a simple text file
    os.makedirs('paper', exist_ok=True)
    with open('paper/results_summary.txt', 'w') as f:
        f.write("Clinical XAI Evaluation Framework - Results\n")
        f.write("===========================================\n")
        f.write(f"Model: {best_model_name}\n")
        f.write(f"Accuracy: {results[best_model_name]['accuracy']:.4f}\n")
        f.write(f"AUC: {results[best_model_name]['auc']:.4f}\n")
        f.write(f"Explanation Stability Score (Noise robustness): {stability_score:.4f}\n")
        f.write(f"Clinician Alignment Score: {alignment_score:.4f}\n")
        
    print("\nResults saved to paper/results_summary.txt")

if __name__ == "__main__":
    main()
