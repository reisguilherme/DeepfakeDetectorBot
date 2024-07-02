import torch.nn as nn

class Wav2VecClassificationModel(nn.Module):
    def __init__(self, model):
        super(Wav2VecClassificationModel, self).__init__()
        self.model = model

    def forward(self, input_values):
        x = self.model(input_values)['logits']
        x = nn.Softmax()(x)
        return x