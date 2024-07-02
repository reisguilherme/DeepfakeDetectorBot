from src.Trainer import Trainer
from src.Dataset import Data,Wav2vec2CustomDataset
from src.Metrics import Metrics
from src.Learner import Learner
from src.Evaluator import Evaluator
import argparse
import torch
import json  
import torch.nn as nn  
import argparse
import pandas as pd
from transformers import AutoFeatureExtractor, Wav2Vec2ForSequenceClassification  

def read_config(path):
    with open(path, "r") as arquivo:
        # Carrega os dados do arquivo JSON em um dicionário
        dados = json.load(arquivo)
    return dados

def main():
    seed_value = 42
    torch.manual_seed(seed_value)
    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed_value)
        torch.cuda.manual_seed_all(seed_value)
    g = torch.Generator()
    g.manual_seed(seed_value)
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-n',
        '--run_name',
        type=str
    )
    args = parser.parse_args()
    run_name = args.run_name
    model_path = 'facebook/wav2vec2-xls-r-300m'
    feature_extractor = AutoFeatureExtractor.from_pretrained(model_path)
    label2id = {'real':0, 'fake':1} # from the model 
    id2label = {0:"real", 1:"fake"} # from the model
    model = Wav2Vec2ForSequenceClassification.from_pretrained(
        pretrained_model_name_or_path=model_path,
        num_labels=len(label2id),
        label2id=label2id,
        id2label=id2label
    )
    df_train = pd.read_csv("../ASVPOOF_2019/LA/LA/train_metadata.csv")
    df_test = pd.read_csv("../ASVPOOF_2019/LA/LA/eval_metadata.csv")
    df_val = pd.read_csv("../ASVPOOF_2019/LA/LA/dev_metadata.csv")
    train_dataset = Wav2vec2CustomDataset(dataset=df_train, processor=feature_extractor, apply_mixup=False, apply_augmentation=False, id2label=id2label,label2id=label2id)
    val_dataset = Wav2vec2CustomDataset(dataset=df_val, processor=feature_extractor,apply_mixup=False, id2label=id2label,label2id=label2id)
    test_dataset = Wav2vec2CustomDataset(dataset=df_test, processor=feature_extractor,apply_mixup=False, id2label=id2label,label2id=label2id)
    data = Data(batch_size=48,dataset_train=train_dataset,dataset_val=val_dataset,dataset_test=test_dataset)
    learner = Learner(model=model)
    evaluator = Evaluator()
    metrics = Metrics(run_name=run_name)
    trainer = Trainer(data=data, evaluator=evaluator, learner=learner, metrics=metrics)
    frequency_save = 15
    trainer.run(n_epochs=30, frequency_save=frequency_save, run_name=run_name, folder=f'models/{run_name}')

if __name__ == "__main__":
    main()