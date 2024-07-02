from src.Wav2vecClassificationModel import Wav2VecClassificationModel
import torch.optim.lr_scheduler as lr_scheduler
import torch


class Learner:
    def __init__(self, model):
        DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = Wav2VecClassificationModel(model=model)
        self.model.to(DEVICE)
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=3e-5)
        self.scheduler = lr_scheduler.MultiStepLR(self.optimizer, milestones=[5,10,15,25], gamma=0.5)


    def predict(self, x):
        return self.model(x)


    def scheduler_step(self):
        self.scheduler.step()


    def update(self, loss):
        # Backpropagation
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()


    def update_cumulation(self, loss, back):
        if back:
            self.optimizer.step()
            self.optimizer.zero_grad()