import torch
import os
from src.Dataset import Data,Wav2vec2CustomDataset
from src.Metrics import Metrics
from src.Learner import Learner
from src.Evaluator import Evaluator
import tqdm

class Trainer:
    def __init__(self, data: Data, learner: Learner, evaluator: Evaluator, metrics: Metrics):
        self.data = data
        self.learner = learner
        self.metrics = metrics
        self.evaluator = evaluator
        self.DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
        seed_value = 42
        torch.manual_seed(seed_value)
        if torch.cuda.is_available():
            torch.cuda.manual_seed(seed_value)
            torch.cuda.manual_seed_all(seed_value)
        g = torch.Generator()
        g.manual_seed(seed_value)


    def one_epoch(self, mode):
        if mode == 'train':
            self.learner.model.train(True)
        else:
            self.learner.model.train(False)
        dataloader = self.data.get_loader(mode)
        preds = []
        labels = []
        epoch_loss = 0
        self.learner.optimizer.zero_grad()
        for (X, y) in tqdm.tqdm(dataloader):
            X, y = X.to(self.DEVICE), y.to(self.DEVICE)
            y_hat = self.learner.predict(X)
            if mode == 'train':
                loss = self.evaluator.get_loss(y, y_hat)
                self.learner.update(loss)
                epoch_loss += loss.item()
            if mode == 'validation':
                loss = self.evaluator.get_loss(y, y_hat)
                epoch_loss += loss.item()
            if len(y.shape) == 2:
                labels.extend(y.argmax(1).int().tolist())
            else:
                labels.extend(y.int().tolist())
            preds.extend((y_hat.argmax(1)).int().tolist())
        epoch_lr = self.learner.optimizer.param_groups[0]["lr"]
        if mode != 'test':
            epoch_loss /= len(dataloader)
        if mode == 'test':
            epoch_loss = 0
        self.metrics.calc_metrics(preds=preds, labels=labels, mode=mode, loss=epoch_loss, model_weigths=self.learner.model.state_dict(), show=True)
        return preds,labels, epoch_loss, epoch_lr


    def run(self, n_epochs: int, frequency_save: int, run_name : str, folder: str):
        if not os.path.exists(folder):
            os.makedirs(folder)
        print("Starting training")
        for t in range(n_epochs):
            if t % frequency_save == 0 and t > 0:
                print("Saving checkpoint")
                torch.save(self.learner.model.state_dict(),f'{folder}/checkpoint_epoch_{t}{run_name}.pt')
            print(f"Epoch {t+1}\n-------------------------------")
            preds,labels, epoch_loss,epoch_lr = self.one_epoch(mode='train')
            self.metrics.write_metrics(t=t,preds=preds,labels=labels,mode='train', loss=epoch_loss, epoch_lr=epoch_lr)  
            with torch.no_grad():
                preds,labels, epoch_loss, epoch_lr = self.one_epoch(mode='validation')
                self.metrics.write_metrics(t=t,preds=preds,labels=labels,mode='validation', loss=epoch_loss)  
            self.learner.scheduler_step()    
        print("Training done")
        print("Save last checkpoint")
        torch.save(self.learner.model.state_dict(),f'{folder}/last_checkpoint_{n_epochs}epochs_{run_name}.pt')
        print("Running test in with best model(F1-Score) ASVSpoof LA data")
        self.learner.model.load_state_dict(self.metrics.get_best_model(metric='f1-score'))
        with torch.no_grad():
            preds,labels, epoch_loss, epoch_lr =self.one_epoch(mode='test')
            self.metrics.write_metrics(t=t,preds=preds,labels=labels,mode='test', loss=None)  
        print('Saving best model')
        self.metrics.save_best_model(all_metrics=False, metric='f1-score', name=run_name, folder=folder)