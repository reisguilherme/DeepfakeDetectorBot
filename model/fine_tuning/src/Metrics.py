
from torch.utils.tensorboard import SummaryWriter
from sklearn.metrics import (
    f1_score,
    accuracy_score,
    precision_score,
    recall_score, 
    confusion_matrix
)
import torch
import os
import wandb
import matplotlib.pyplot as plt
import pandas as pd


class Metrics():
    def __init__(self, run_name):
        self.metrics_save = {}
        self.best_models_weigths = {}
        self.metrics_names  = ['acuracy','recall','precision','f1-score','eer','loss']
        self.writer = SummaryWriter(log_dir=f'runs/{run_name}')
        wandb.init(project='w2v-deepfake-detection', name=run_name)


    def calc_metrics_complete(self, preds,labels):
        acc = accuracy_score(y_pred=preds, y_true=labels)
        recall = recall_score(y_pred=preds, y_true=labels)
        precision = precision_score(y_pred=preds, y_true=labels)
        f1 = f1_score(y_pred=preds, y_true=labels,average='binary')
        cm = confusion_matrix(
            y_true=labels,
            y_pred=preds
        )
        if cm.shape[1] ==2:
            if (cm[0, 0] + cm[0, 1]) > 0:
                fpr = cm[0, 1] / (cm[0, 0] + cm[0, 1])
            else:
                fpr = 0.0
            if (cm[1, 0] + cm[1, 1]) > 0:
                fnr = cm[1, 0] / (cm[1, 0] + cm[1, 1])
            else:
                fnr = 0.0
            eer = (fpr + fnr) / 2.0
        else:
            eer = 0
        return f1,acc,precision,recall, eer


    def write_metrics(self, t, preds, labels, mode, loss=None, epoch_lr=None):
        f1, acc, precision, recall, eer = self.calc_metrics_complete(preds=preds, labels=labels)
        if loss:
            self.writer.add_scalar(f'Loss/{mode}', loss, t)
            wandb.log({f'Loss/{mode}': loss}, step=t)
        if epoch_lr:
            self.writer.add_scalar(f'Learning rate/{mode}', epoch_lr, t)
            wandb.log({f'Learning rate/{mode}': epoch_lr}, step=t)
        self.writer.add_scalar(f'{mode}/F1-Score/', f1, t)
        self.writer.add_scalar(f'{mode}/Accuracy/', acc, t)
        self.writer.add_scalar(f'{mode}/Precision/', precision, t)
        self.writer.add_scalar(f'{mode}/Recall/', recall, t)
        self.writer.add_scalar(f'{mode}/EER/', eer, t)
        wandb.log({
            f'{mode}/F1-Score': f1,
            f'{mode}/Accuracy': acc,
            f'{mode}/Precision': precision,
            f'{mode}/Recall': recall,
            f'{mode}/EER': eer
        }, step=t)


    def calc_metrics(self,preds,labels,mode,loss, model_weigths=None, show=False):
        f1,acc,precision,recall, eer =  self.calc_metrics_complete(preds=preds,labels=labels)
        metrics_values = [acc,recall,precision,f1,eer,loss]      
        if show:
            print(f"{mode} -  Acuracy: {acc:.5f} - Recall {recall:.5f} - Precision {precision:.5f} - F1-Score {f1:.5f} - EER {eer:.5f} - Loss {loss:.5f}")
        #Metrics
        for metric_name, metric_value in zip(self.metrics_names, metrics_values):
            #Add metrics 
            if f'{mode}_{metric_name}' not in self.metrics_save.keys():
                self.metrics_save[f'{mode}_{metric_name}'] = [metric_value]
            else:
                self.metrics_save[f'{mode}_{metric_name}'].append(metric_value)
            #Save best metrics and respective weigths 
            if mode == 'validation':
                if f'{mode}_best_{metric_name}' not in self.metrics_save.keys():
                    self.metrics_save[f'{mode}_best_{metric_name}'] = metric_value
                    self.best_models_weigths[f'{mode}_best_{metric_name}'] = model_weigths
                elif metric_value > self.metrics_save[f'{mode}_best_{metric_name}'] :
                    self.best_models_weigths[f'{mode}_best_{metric_name}'] = model_weigths


    def get_best_model(self, metric):
        for key in self.best_models_weigths.keys():
            if metric in key:
                return self.best_models_weigths[key]


    def save_best_model(self, all_metrics, metric, name, folder):
        # Cria a pasta se ela não existir
        if not os.path.exists(folder):
            os.makedirs(folder)
        if all_metrics:
            print("Saving all models")
            for key in self.best_models_weigths.keys():
                file_path = os.path.join(folder, f'best_model-{key}-{name}.pt')
                torch.save(self.best_models_weigths[key], file_path)
                print(f"Save model at: {file_path}")
        else:
            print(f"Saving best model for {metric}")
            for key in self.best_models_weigths.keys():
                if metric in key:
                    file_path = os.path.join(folder, f'best_model-{key}-{name}.pt')
                    torch.save(self.best_models_weigths[key], file_path)
                    print(f"Save model at {file_path}")
                    break