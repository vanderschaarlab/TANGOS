import numpy as np
import torch
import torch.nn as nn
from functorch import jacrev, vmap


def MSE(output, label):
    return nn.MSELoss()(output.squeeze(), label)


class parameter_schedule:
    def __init__(self, lambda_1, lambda_2, epoch):
        self.lambda_1 = lambda_1
        self.lambda_2 = lambda_2
        self.switch_epoch = epoch

    def get_reg(self, epoch):
        if epoch < self.switch_epoch:
            return 0, 0
        else:
            return self.lambda_1, self.lambda_2


def cosine_similarity(w1, w2):
    return torch.dot(w1, w2).abs() / (torch.norm(w1, 2) * torch.norm(w2, 2))


def weight_correlation(weights, device="cpu"):
    h_dim = weights.shape[0]

    weight_corr = torch.tensor(0.0, requires_grad=True).to(device)
    weights = weights.clone().requires_grad_(True)

    cos = nn.CosineSimilarity(dim=0, eps=1e-6)

    for neuron_i in range(1, h_dim):
        for neuron_j in range(0, neuron_i):
            pairwise_corr = cosine_similarity(
                weights[neuron_i, :],
                weights[neuron_j, :],
            )
            weight_corr = weight_corr + pairwise_corr.norm(p=1)

    return weight_corr / (h_dim * (h_dim - 1) / 2)


def kl_divergence(mu, logvar):
    KLD = -0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp())
    return KLD


def attr_loss(forward_func, data_input, device="cpu", subsample=-1):
    ########## UPDATE functools ############
    batch_size = data_input.shape[0]

    def to_latent(input_):
        _, h_out = forward_func(input_)
        return h_out

    data_input = data_input.clone().requires_grad_(True)
    jacobian = vmap(jacrev(to_latent), randomness="same")(data_input)
    neuron_attr = jacobian.swapaxes(0, 1)
    h_dim = neuron_attr.shape[0]

    if len(neuron_attr.shape) > 3:
        # h_dim x batch_size x features
        neuron_attr = neuron_attr.flatten(start_dim=2)

    sparsity_loss = torch.norm(neuron_attr, p=1) / (
        batch_size * h_dim * neuron_attr.shape[2]
    )

    cos = nn.CosineSimilarity(dim=1, eps=1e-6)
    correlation_loss = torch.tensor(0.0, requires_grad=True).to(device)

    if subsample > 0 and subsample < h_dim * (h_dim - 1) / 2:
        tensor_pairs = [
            list(np.random.choice(h_dim, size=(2), replace=False))
            for i in range(subsample)
        ]
        for tensor_pair in tensor_pairs:
            pairwise_corr = cos(
                neuron_attr[tensor_pair[0], :, :],
                neuron_attr[tensor_pair[1], :, :],
            ).norm(p=1)
            correlation_loss = correlation_loss + pairwise_corr

        correlation_loss = correlation_loss / (batch_size * subsample)

    else:
        for neuron_i in range(1, h_dim):
            for neuron_j in range(0, neuron_i):
                pairwise_corr = cos(
                    neuron_attr[neuron_i, :, :],
                    neuron_attr[neuron_j, :, :],
                ).norm(p=1)
                correlation_loss = correlation_loss + pairwise_corr
        num_pairs = h_dim * (h_dim - 1) / 2
        correlation_loss = correlation_loss / (batch_size * num_pairs)

    return sparsity_loss, correlation_loss
