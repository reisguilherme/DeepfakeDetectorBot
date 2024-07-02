import torch
import torchaudio

def process_audio(speech_array, sr, target_sample_rate, processor):
    try:
        speech_array = torch.mean(speech_array, dim=0, keepdim=True)
        if sr != target_sample_rate : 
            transform = torchaudio.transforms.Resample(sr, target_sample_rate)
            speech_array = transform(speech_array)
        fixed_length = (
            target_sample_rate * 3
        ) 
        if speech_array.shape[1] < fixed_length:
            speech_array = torch.nn.functional.pad(speech_array, (0, fixed_length - speech_array.shape[1]))
        else:
            speech_array = speech_array[:, :fixed_length]
        speech_array =  processor(speech_array, sampling_rate=target_sample_rate, do_normalize=True, return_tensors="pt").input_values[0]
        speech_array = speech_array.squeeze()
        return speech_array
    except Exception as e:
        print(f"An error occurred: {e}")
        return None