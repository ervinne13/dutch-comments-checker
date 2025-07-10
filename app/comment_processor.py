from transformers import pipeline

# My first iteration was using Ollama and relying only on prompt engineering (You are a spam detector blah blah blah ...).
# This time we'll try using huggingfaces' existing models for translation, spam detection, and toxicity detection.
translator = pipeline("translation", model="Helsinki-NLP/opus-mt-nl-en")
spam_detector = pipeline("text-classification", model="valurank/distilroberta-spam-comments-detection")
toxicity_detector = pipeline("text-classification", model="unitary/toxic-bert")

def process_comment(comment):
    translation = translator(comment)[0]['translation_text']
    spam_result = spam_detector(translation)[0]
    toxicity_result = toxicity_detector(translation)[0]

    return {
        "original": comment,
        "translated": translation,
        "spam": {
            "label": spam_result['label'],
            "score": spam_result['score'],
        },
        "toxicity": {
            "label": toxicity_result['label'],
            "score": toxicity_result['score'],
        }
    }
