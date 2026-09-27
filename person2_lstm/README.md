# Person 2 — Centralized LSTM Crop Yield Prediction

## Objective

Develop and validate a centralized LSTM-based deep learning model for predicting crop yield using the processed agricultural dataset provided by Person 1.

## Dataset

The model uses the already processed dataset from the `processed/` directory.

Dataset split:

* Training samples: 350
* Validation samples: 75
* Testing samples: 75
* Input features: 38
* Target: `yield_kg_per_hectare`

The processed features are tabular agricultural and sensor-related features. The current implementation represents each sample as one LSTM timestep with 38 features.

### Input Shape

```text
(samples, timesteps, features)
(350, 1, 38) — training
(75, 1, 38)  — validation
(75, 1, 38)  — testing
```

## Model Architecture

```text
Input
  ↓
LSTM — 64 units
  ↓
Dense — 128 units, ReLU
  ↓
Dropout — 0.2
  ↓
Dense — 64 units, ReLU
  ↓
Dropout — 0.4
  ↓
Dense — 1
```

Total trainable parameters:

```text
43,009
```

## Training Configuration

| Parameter               | Value                     |
| ----------------------- | ------------------------- |
| Optimizer               | Adam                      |
| Loss                    | Mean Squared Error (MSE)  |
| Metric                  | Mean Absolute Error (MAE) |
| Batch Size              | 32                        |
| Maximum Epochs          | 100                       |
| Early Stopping          | Enabled                   |
| Early Stopping Patience | 10                        |
| Best Model Selection    | Validation Loss           |

## Training

The model is trained using:

```text
person2_lstm/train_lstm.py
```

Early stopping is used to prevent unnecessary training after validation performance stops improving. The best model based on validation loss is saved using ModelCheckpoint.

## Evaluation

The trained model is evaluated using:

```text
person2_lstm/evaluate_lstm.py
```

Evaluation metrics:

* MAE
* MSE
* RMSE
* R²

### Current Test Results

| Metric |        Value |
| ------ | -----------: |
| MAE    |    1176.3268 |
| MSE    | 1774501.5000 |
| RMSE   |    1332.1042 |
| R²     |      -0.2007 |

These results represent the current centralized LSTM baseline on the provided test split.

## Output Files

### Trained model

```text
models/lstm_model.keras
```

### Training history

```text
person2_lstm/results/training_history.csv
```

### Evaluation metrics

```text
person2_lstm/results/metrics.csv
```

### Predictions

```text
person2_lstm/results/predictions.csv
```

## Handoff to Person 3

Person 3 can use the centralized LSTM architecture and training configuration as the reference model for the Federated Learning implementation.

Important model information:

```text
Input shape: (1, 38)

LSTM: 64 units
Dense: 128 ReLU
Dropout: 0.2
Dense: 64 ReLU
Dropout: 0.4
Output: 1

Optimizer: Adam
Loss: MSE
Batch size: 32
Maximum epochs: 100
Early stopping patience: 10
```

Person 3's Federated Learning implementation should preserve the same model architecture when comparing centralized and federated training.

## Important Note

The processed dataset is tabular rather than a multi-timestep time-series dataset. Therefore, the current LSTM implementation uses one timestep containing 38 features. This should be considered when describing the model in the research paper.
