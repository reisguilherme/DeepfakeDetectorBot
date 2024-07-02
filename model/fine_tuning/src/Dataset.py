import pandas as pd
import numpy as np
import librosa
from transformers import (
    Wav2Vec2Processor
)
import torch
import random
import torchaudio
from typing import List, Optional, Union, Dict
from audiomentations import LowPassFilter, AddGaussianNoise,TimeMask
from torch.utils.data import DataLoader

class Wav2vec2CustomDataset(torch.utils.data.Dataset):
    def __init__(
        self,
        processor: Wav2Vec2Processor,
        dataset: pd.DataFrame,
        target_sample_rate: int = 16000,
        apply_augmentation: bool = False,
        apply_mixup: bool = False,
        filepath_column: str = "file_path",
        label_column: str = "label",
        alpha: float = 0.5,
        max_audio_len: int = 3,
        label2id: Dict = None,
        id2label: Dict  = None
    ):
        self.processor = processor
        self.dataset = dataset
        self.target_sample_rate = target_sample_rate
        self.apply_augmentation = apply_augmentation
        self.apply_mixup = apply_mixup
        self.alpha = alpha
        self.filepath_column = filepath_column
        self.label_column = label_column
        self.max_audio_len = max_audio_len
        self.label2id = label2id
        self.id2label = id2label


    def __len__(self):
        return len(self.dataset)


    def process_audio(self, speech_array, sr):
        if sr != self.target_sample_rate : 
            transform = torchaudio.transforms.Resample(sr, self.target_sample_rate)
            speech_array = transform(speech_array)
        fixed_length = (
            self.target_sample_rate * self.max_audio_len
        )  # Adjust this value based on your requirements
        if speech_array.shape[1] < fixed_length:
            speech_array = torch.nn.functional.pad(speech_array, (0, fixed_length - speech_array.shape[1]))
        else:
            speech_array = speech_array[:, :fixed_length]
        speech_array =  self.processor(speech_array, sampling_rate=self.target_sample_rate, do_normalize=True, return_tensors="pt").input_values[0]
        speech_array = speech_array.squeeze()
        return speech_array


    def get_temp_audio(self,label):
        random_index = random.randint(0,len(self.dataset)-1)
        temp_audio = self.dataset.loc[random_index, self.filepath_column]
        temp_audio_label = self.dataset.loc[random_index, self.label_column]
        while temp_audio_label == label:
            random_index = random.randint(0,len(self.dataset)-1)
            temp_audio = self.dataset.loc[random_index, self.filepath_column]
            temp_audio_label = self.dataset.loc[random_index, self.label_column]
        return temp_audio, temp_audio_label


    def apply_augmentations(self, sample):
        if random.random() <= 0.5:
            sample = AddGaussianNoise(p=1)(sample, self.target_sample_rate)
        if random.random() <= 0.5:
            sample = LowPassFilter(p=1)(sample, self.target_sample_rate)
        if random.random() <= 0.5:
            sample = TimeMask(p=1)(sample, self.target_sample_rate)
        return sample


    def __getitem__(self, index) -> Dict[str, torch.Tensor]:
        # Gain Normalization
        filepath = self.dataset.loc[index,self.filepath_column]
        label = self.dataset.loc[index,self.label_column]
        label = self.label2id[label]
        if self.apply_augmentation:
            speech_array, sr = librosa.load(filepath)
            speech_array = self.apply_augmentations(sample=speech_array)
            speech_array = torch.Tensor(speech_array).unsqueeze(0)
        else:
            speech_array, sr = torchaudio.load(filepath)
        if self.apply_mixup:
            speech_2_filepath, label2 = self.get_temp_audio(label)
            speech_array_2, sr2 = torchaudio.load(speech_2_filepath)
            speech_array = self.process_audio(speech_array,sr)
            speech_array_2 = self.process_audio(speech_array_2, sr2)
            mix_lambda = np.random.beta(self.alpha,self.alpha)
            mix_speech_array = mix_lambda * speech_array + ((1 - mix_lambda) * speech_array_2)
            label2 = self.label2id[label2]
            mixup_label = torch.zeros(2)
            mixup_label[label] = mix_lambda
            mixup_label[label2] = (1 - mix_lambda)
            mix_speech_array = torch.Tensor(mix_speech_array)
            return mix_speech_array, mixup_label
        speech_array = self.process_audio(speech_array,sr)
        return filepath,speech_array, label


class Data:
    def __init__(self, batch_size,dataset_train,dataset_test, dataset_val):
        self.seed_value = 42
        torch.manual_seed(self.seed_value)
        if torch.cuda.is_available():
            torch.cuda.manual_seed(self.seed_value)
            torch.cuda.manual_seed_all(self.seed_value)
        self.g = torch.Generator()
        self.g.manual_seed(self.seed_value)
        self.modes = ['train','test','validation']
        self.dataloaders = {}
        self.batch_size = batch_size
        self.dataloaders['train'] = dataset_train
        self.dataloaders['validation'] = dataset_val
        self.dataloaders['test'] = dataset_test


    def seed_worker(self,worker_id):
        worker_seed = self.seed_value + worker_id
        np.random.seed(worker_seed)
        random.seed(worker_seed)


    def get_loader(self, mode):
        num_workers = 24
        if mode != 'test':
            return  DataLoader(self.dataloaders[mode], batch_size=self.batch_size, shuffle=True,worker_init_fn=self.seed_worker, num_workers=num_workers,generator=self.g)
        else:
            return  DataLoader(self.dataloaders[mode], batch_size=self.batch_size, shuffle=False, worker_init_fn=self.seed_worker,num_workers=num_workers, generator=self.g)