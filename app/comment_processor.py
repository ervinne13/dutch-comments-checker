from .load_models import get_models

def screen_comment(comment):
    translator, spam_detector, toxicity_detector = get_models()
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
