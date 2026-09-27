import numpy as np


def fedavg(client_weights, client_sizes):
    """
    Weighted Federated Averaging (McMahan et al., 2017).

    W_global = sum_k (n_k / n) * W_k

    client_weights: list (one per client) of model.get_weights() lists
    client_sizes:   list of local sample counts n_k
    """
    if len(client_weights) != len(client_sizes) or not client_weights:
        raise ValueError("Need one weight list per client size.")

    total = float(sum(client_sizes))
    coefficients = [n_k / total for n_k in client_sizes]

    averaged = []
    for layer_idx in range(len(client_weights[0])):
        layers = [w[layer_idx] for w in client_weights]

        shape = layers[0].shape
        if any(layer.shape != shape for layer in layers):
            raise ValueError(f"Shape mismatch in layer {layer_idx}.")

        layer_avg = sum(c * layer for c, layer in zip(coefficients, layers))
        averaged.append(np.asarray(layer_avg, dtype=layers[0].dtype))

    return averaged
