from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, roc_auc_score, classification_report
import warnings
warnings.filterwarnings('ignore')

def train_models(X_train, y_train, X_test, y_test):
    """
    Trains baseline models for predicting the healthcare outcome.
    """
    results = {}
    models = {
        'RandomForest': RandomForestClassifier(n_estimators=100, random_state=42),
    }
    
    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        y_prob = model.predict_proba(X_test)[:, 1]
        
        acc = accuracy_score(y_test, y_pred)
        auc = roc_auc_score(y_test, y_prob)
        print(f"[{name}] Accuracy: {acc:.4f}, AUC: {auc:.4f}")
        
        results[name] = {
            'model': model,
            'accuracy': acc,
            'auc': auc,
            'report': classification_report(y_test, y_pred)
        }
        
    return results
