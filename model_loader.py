from transformers import pipeline

def load_model(model_name: str = "distilbert-base-uncased-distilled-squad", device: int = -1):
    return pipeline("question-answering", model=model_name, device=device)
