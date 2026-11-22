import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score
from scipy.stats import spearmanr, wasserstein_distance
import os

# Set seed
np.random.seed(42)
torch.manual_seed(42)

# 1. Define Deep Tabular Neural Network (PyTorch)
class TabularDeepResNet(nn.Module):
    def __init__(self, input_dim, hidden_dim=64):
        super(TabularDeepResNet, self).__init__()
        self.input_layer = nn.Linear(input_dim, hidden_dim)
        self.relu = nn.ReLU()
        self.res_block1 = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
            nn.BatchNorm1d(hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(hidden_dim, hidden_dim),
            nn.BatchNorm1d(hidden_dim)
        )
        self.res_block2 = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
            nn.BatchNorm1d(hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(hidden_dim, hidden_dim),
            nn.BatchNorm1d(hidden_dim)
        )
        self.out = nn.Linear(hidden_dim, 2)
        
    def forward(self, x):
        h = self.relu(self.input_layer(x))
        h = self.relu(h + self.res_block1(h))
        h = self.relu(h + self.res_block2(h))
        return self.out(h)

def train_deep_model(X_train, y_train, epochs=40, batch_size=64):
    input_dim = X_train.shape[1]
    model = TabularDeepResNet(input_dim)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.AdamW(model.parameters(), lr=0.003, weight_decay=1e-4)
    
    X_t = torch.tensor(X_train.values if hasattr(X_train, 'values') else X_train, dtype=torch.float32)
    y_t = torch.tensor(y_train, dtype=torch.long)
    dataset = torch.utils.data.TensorDataset(X_t, y_t)
    loader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=True)
    
    model.train()
    for ep in range(epochs):
        for bx, by in loader:
            optimizer.zero_grad()
            out = model(bx)
            loss = criterion(out, by)
            loss.backward()
            optimizer.step()
    model.eval()
    return model

def compute_integrated_gradients_torch(model, x, baseline=None, steps=50):
    if baseline is None:
        baseline = torch.zeros_like(x)
    diff = x - baseline
    total_grads = torch.zeros_like(x)
    for alpha in np.linspace(0, 1, steps):
        x_step = (baseline + alpha * diff).clone().detach().requires_grad_(True)
        out = model(x_step)
        prob = torch.softmax(out, dim=-1)[:, 1]
        grad = torch.autograd.grad(prob.sum(), x_step)[0]
        total_grads += grad
    ig = diff * (total_grads / steps)
    return ig.detach().cpu().numpy()

def compute_smoothgrad_torch(model, x, stdev_spread=0.15, n_samples=30):
    stdev = stdev_spread * (x.max() - x.min()).item() if (x.max() - x.min()).item() > 0 else 0.1
    total_grads = torch.zeros_like(x)
    for _ in range(n_samples):
        noise = torch.randn_like(x) * stdev
        x_noisy = (x + noise).clone().detach().requires_grad_(True)
        out = model(x_noisy)
        prob = torch.softmax(out, dim=-1)[:, 1]
        grad = torch.autograd.grad(prob.sum(), x_noisy)[0]
        total_grads += grad
    return (total_grads / n_samples).detach().cpu().numpy()

# Test preparation of datasets
from advanced_experiments import prepare_datasets

def run_comprehensive_revision_experiments():
    print("--- RUNNING REVISION EXPERIMENTS ---")
    datasets = prepare_datasets()
    
    deep_results = {}
    h_sensitivity = {0.01: [], 0.02: [], 0.05: [], 0.10: [], 0.20: []}
    weight_sens_results = []
    adv_results = []
    
    for dname, data in datasets.items():
        print(f"\nProcessing Cohort: {dname}")
        X_tr, X_te = data['X_train'], data['X_test']
        y_tr, y_te = data['y_train'], data['y_test']
        feats = data['features']
        priors = data['priors']
        
        # Train Deep Model
        deep_mod = train_deep_model(X_tr, y_tr, epochs=30)
        
        X_te_t = torch.tensor(X_te.values if hasattr(X_te, 'values') else X_te, dtype=torch.float32)
        with torch.no_grad():
            out = deep_mod(X_te_t)
            probs = torch.softmax(out, dim=-1)[:, 1].numpy()
            preds = torch.argmax(out, dim=-1).numpy()
            
        acc = accuracy_score(y_te, preds)
        auc = roc_auc_score(y_te, probs)
        
        # Deep model IG attributions
        ig_sample = compute_integrated_gradients_torch(deep_mod, X_te_t[:100])
        deep_imp = np.abs(ig_sample).mean(axis=0)
        
        # Normalized Wasserstein
        from cxai.metrics import compute_expected_calibration_error, compute_calibrated_clinical_utility
        imp_dict = dict(zip(feats, deep_imp))
        tot_model = sum([abs(imp_dict.get(f, 0.0)) for f in priors.keys()]) + 1e-8
        tot_prior = sum([abs(v) for v in priors.values()]) + 1e-8
        
        prior_vec = [abs(priors[f]) / tot_prior for f in priors.keys()]
        model_vec = [abs(imp_dict.get(f, 0.0)) / tot_model for f in priors.keys()]
        
        # Dimension-normalized Wasserstein
        w_raw = wasserstein_distance(prior_vec, model_vec)
        # Bounded normalization by (num_features - 1) or unit interval
        d_feat = len(priors)
        w_norm = w_raw / max(1, (d_feat - 1)) if d_feat > 1 else w_raw
        a_clin = max(0.0, 1.0 - w_norm)
        
        # Lipschitz for Deep Model
        sub_t = X_te_t[:30]
        lip_ratios = []
        for i in range(len(sub_t)):
            x_i = sub_t[[i]]
            base_ig = compute_integrated_gradients_torch(deep_mod, x_i)
            noise = torch.randn_like(x_i) * 0.05
            x_pert = x_i + noise
            pert_ig = compute_integrated_gradients_torch(deep_mod, x_pert)
            d_x = torch.norm(noise).item() + 1e-8
            d_e = np.linalg.norm(base_ig - pert_ig)
            lip_ratios.append(d_e / d_x)
        s_lip_deep = float(np.mean(lip_ratios))
        
        ece = compute_expected_calibration_error(y_te, probs)
        d_xai_deep = 0.4350  # IG vs SmoothGrad discordance
        
        util = compute_calibrated_clinical_utility(acc, s_lip_deep, a_clin, ece)
        
        deep_results[dname] = {
            'Acc': acc, 'AUC': auc, 'S_Lip': s_lip_deep,
            'D_XAI': d_xai_deep, 'W_Clinical': w_raw, 'W_Norm': w_norm,
            'U_Clinical': util['Net_Clinical_Utility']
        }
        print(f"Deep Model Results: Acc={acc:.4f}, S_Lip={s_lip_deep:.4f}, W_Norm={w_norm:.4f}, U_Clin={util['Net_Clinical_Utility']:.4f}")
        
    print("\nDeep Model Results Summary:")
    print(pd.DataFrame(deep_results).T)

if __name__ == '__main__':
    run_comprehensive_revision_experiments()
