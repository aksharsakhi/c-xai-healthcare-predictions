import unittest
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import cxai

class TestCXAIBenchmark(unittest.TestCase):

    def setUp(self):
        np.random.seed(42)
        self.X = pd.DataFrame({
            'Age': np.random.normal(60, 10, 100),
            'Systolic_BP': np.random.normal(120, 15, 100),
            'Cholesterol': np.random.normal(200, 25, 100)
        })
        self.y = np.random.binomial(1, 0.4, 100)
        self.clinical_priors = {'Age': 4.0, 'Systolic_BP': 3.0, 'Cholesterol': 1.0}
        self.model = RandomForestClassifier(n_estimators=10, random_state=42).fit(self.X, self.y)

    def test_lipschitz_stability(self):
        s_lip, s_std = cxai.compute_empirical_lipschitz_stability(self.model, self.X.iloc[:20], noise_level=0.05)
        self.assertGreaterEqual(s_lip, 0.0)
        self.assertIsInstance(s_lip, float)

    def test_cross_explainer_discordance(self):
        imp1 = np.array([0.5, 0.3, 0.2])
        imp2 = np.array([0.5, 0.3, 0.2])
        d_xai_zero = cxai.compute_cross_explainer_discordance(imp1, imp2)
        self.assertAlmostEqual(d_xai_zero, 0.0, places=4)
        
        imp3 = np.array([0.2, 0.3, 0.5])
        d_xai_inv = cxai.compute_cross_explainer_discordance(imp1, imp3)
        self.assertGreater(d_xai_inv, 1.0)

    def test_clinical_wasserstein_distance(self):
        model_imp = [0.4, 0.3, 0.3]
        features = ['Age', 'Systolic_BP', 'Cholesterol']
        w_dist, a_score = cxai.compute_clinical_wasserstein_distance(model_imp, features, self.clinical_priors)
        self.assertGreaterEqual(w_dist, 0.0)
        self.assertTrue(0.0 <= a_score <= 1.0)

    def test_expected_calibration_error(self):
        y_true = np.array([1, 0, 1, 0, 1, 1, 0, 0])
        y_prob = np.array([0.9, 0.1, 0.8, 0.2, 0.95, 0.7, 0.3, 0.05])
        ece = cxai.compute_expected_calibration_error(y_true, y_prob)
        self.assertTrue(0.0 <= ece <= 1.0)

    def test_brier_score(self):
        y_true = np.array([1, 0, 1, 0])
        y_prob = np.array([0.9, 0.1, 0.8, 0.2])
        bs = cxai.metrics.compute_brier_score(y_true, y_prob)
        self.assertGreaterEqual(bs, 0.0)
        self.assertLessEqual(bs, 1.0)

    def test_calibrated_utility(self):
        util = cxai.compute_calibrated_clinical_utility(acc=0.95, s_lip=0.05, a_clinical=0.90, ece=0.02)
        self.assertIn('Net_Clinical_Utility', util)
        self.assertGreaterEqual(util['Net_Clinical_Utility'], 0.0)

    def test_cxai_api_evaluate(self):
        res = cxai.evaluate(self.model, self.X, self.y, list(self.X.columns), self.clinical_priors)
        self.assertIn('Accuracy', res)
        self.assertIn('U_Clinical', res)

    def test_cxai_api_benchmark(self):
        models = {'RF': self.model}
        df_lead = cxai.benchmark(models, self.X, self.y, list(self.X.columns), self.clinical_priors)
        self.assertIsInstance(df_lead, pd.DataFrame)
        self.assertEqual(len(df_lead), 1)

    def test_fgsm_attribution_attack(self):
        base_imp = self.model.feature_importances_
        X_adv, d_adv = cxai.fgsm_attribution_attack(self.model, self.X.iloc[:5], base_imp, eps_adv=0.02)
        self.assertEqual(X_adv.shape, self.X.iloc[:5].shape)
        self.assertGreaterEqual(d_adv, 0.0)

    def test_demographic_fairness(self):
        res = cxai.evaluate_demographic_fairness(self.model, self.X, self.y, age_column='Age')
        self.assertIn('Instability_Disparity', res)

    def test_metric_ablation(self):
        res = cxai.run_metric_ablation_study(acc=0.95, s_lip=0.05, a_clinical=0.90, ece=0.02)
        self.assertIn('Full_Trust_Factor', res)
        self.assertIn('Stability_Importance_Pct', res)

if __name__ == '__main__':
    unittest.main()
