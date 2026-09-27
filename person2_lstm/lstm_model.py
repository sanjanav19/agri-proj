from tensorflow.keras import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout


def create_lstm_model(input_shape):
    model = Sequential([
        LSTM(64, input_shape=input_shape),

        Dense(128, activation="relu"),
        Dropout(0.2),

        Dense(64, activation="relu"),
        Dropout(0.4),

        Dense(1)
    ])

    model.compile(
        optimizer="adam",
        loss="mse",
        metrics=["mae"]
    )

    return model