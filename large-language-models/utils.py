import torch

def get_device():
    if torch.cuda.is_available():
        return torch.device('cuda')
    # For M1 Macs
    elif torch.backends.mps.is_available():
        return torch.device('mps')
    else:
        return torch.device('cpu')