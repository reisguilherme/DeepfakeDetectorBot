from transformers import AutoFeatureExtractor, Wav2Vec2ForSequenceClassification

def model(model_path, label2id, id2label):
    try:
        feature_extractor = AutoFeatureExtractor.from_pretrained(model_path)
        model = Wav2Vec2ForSequenceClassification.from_pretrained(
            pretrained_model_name_or_path=model_path,
            num_labels=len(label2id),
            label2id=label2id,
            id2label=id2label
        )
        return feature_extractor, model
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None, None
