
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib

# Simulate only the most essential features
def simulate_features():
    return {
        "volatility": np.random.uniform(0.005, 0.05),
        "spread": np.random.uniform(0.001, 0.01),
        "momentum": np.random.uniform(-0.05, 0.05),
    }

# Simplified rule-based labeling
def label_strategy(features):
    if features["spread"] < 0.003 and features["volatility"] < 0.01:
        return "market_making"
    elif features["volatility"] < 0.015 and abs(features["momentum"]) < 0.01:
        return "mean_reversion"
    else:
        return "none"
# Generate synthetic training data
def generate_training_data(n_samples=1000):
    data = []
    labels = []
    for _ in range(n_samples):
        f = simulate_features()
        label = label_strategy(f)
        data.append(list(f.values()))
        labels.append(label)
    return np.array(data), np.array(labels)

# Train and save model
def train_and_save_model(path="strategy_selector_model.pkl"):
    X, y = generate_training_data()
    clf = RandomForestClassifier()
    clf.fit(X, y)
    joblib.dump(clf, path)
    print(f"Model saved to {path}")


if __name__ == "__main__":
    train_and_save_model("strategy_selector_model.pkl")