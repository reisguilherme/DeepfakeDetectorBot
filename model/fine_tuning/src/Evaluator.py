import torch.nn as nn

class Evaluator:   
    def __init__(self):
        self.loss_fn = nn.BCELoss()
    def get_loss(self, y, y_hat):
        return self.loss_fn(y_hat, y)