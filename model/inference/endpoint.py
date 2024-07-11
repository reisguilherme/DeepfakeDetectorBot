from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import torch
import torchaudio
import torch.nn.functional as F
from wav2vec import Wav2VecClassificationModel
from FeatureExtrator import model as feature_extractor_model
from ProcessAudio import process_audio

app = FastAPI()

# Caminho do modelo e mapeamento de rótulos
model_path = 'facebook/wav2vec2-xls-r-300m'
label2id = {'real': 0, 'fake': 1}
id2label = {0: "real", 1: "fake"}

# Carrega o extrator de características e o modelo
extrator, model = feature_extractor_model(model_path, label2id, id2label)
model_w2v = Wav2VecClassificationModel(model=model)
# Carrega os pesos do modelo treinado
model_w2v.load_state_dict(torch.load('/app/weights/checkpoint_epoch_10baseline_w2v-xls-300-dataaug-multistep-lr.pt', map_location=torch.device('cpu')))
model_w2v.eval()

@app.post("/predict/")
async def predict_audio_class(audio_file: UploadFile = File(...)):
    """
    Endpoint para prever a classe de um arquivo de áudio.
    Args:
        audio_file (UploadFile): Arquivo de áudio enviado pelo usuário.
    Returns:
        JSONResponse: Classe prevista (real ou fake) e a confiança.
    """
    audio_path = f"/tmp/{audio_file.filename}"
    with open(audio_path, "wb") as buffer:
        buffer.write(await audio_file.read())
    audio, sr = torchaudio.load(audio_path)
    sample = process_audio(speech_array=audio, sr=sr, target_sample_rate=16000, processor=extrator)
    with torch.no_grad():
        logits = model_w2v(sample.unsqueeze(0))
        probabilities = F.softmax(logits, dim=1).squeeze()
        predicted_class_id = logits.argmax().item()
        predicted_class = id2label[predicted_class_id]
        confidence = probabilities[predicted_class_id].item() * 100
    
    return JSONResponse(content={"predicted_class": predicted_class, "confidence": f"{confidence:.2f}"})

if __name__ == "__main__":
    import uvicorn
    # Inicia o servidor FastAPI na porta 6969
    uvicorn.run(app, host="0.0.0.0", port=6969)
