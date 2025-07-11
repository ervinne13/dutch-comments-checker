from .load_models import get_spam_detection_model, get_toxicity_detection_model, get_translation_model

def screen_comment(comment):
    spam_detector = get_spam_detection_model()
    toxicity_detector = get_toxicity_detection_model()
    translation = translate_text(comment)

    spam_result = spam_detector(translation)[0]
    toxicity_result = toxicity_detector(translation)[0]

    return {
        "original": comment,
        "translated": translation,
        "spam": {
            "label": spam_result['label'], # we only need either spam or ham, not both
            "score": spam_result['score'],
        },
        "toxicity": toxicity_result # This one we want everything to compare it with perspective API later
    }

def translate_text(str):
    translator = get_translation_model()
    translation = translator(str)[0]['translation_text']
    return translation
